"""
09_subgraphs.py - Modular Graphs and Composition

This tutorial demonstrates how to create and compose subgraphs in LangGraph.
Subgraphs allow you to build reusable, modular workflow components that can
be composed into larger, more complex graphs.

Key Concepts:
- Subgraphs: Graphs that can be used as nodes in other graphs
- Graph composition: Combining multiple graphs together
- Modular design: Reusable workflow components
- Nested execution: Graphs executing within graphs
"""

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State for the subgraph
class SubgraphState(TypedDict):
    """State for the reusable subgraph"""
    value: int
    subgraph_result: str


# State for the main graph
class MainGraphState(TypedDict):
    """State for the main graph that uses subgraphs"""
    input_data: str
    processed_data: str
    subgraph_outputs: list[str]
    final_result: str


# ========== SUBGRAPH DEFINITION ==========
def create_preprocessing_subgraph() -> StateGraph:
    """
    Create a reusable preprocessing subgraph.
    
    This subgraph performs preprocessing operations that can be reused
    in multiple places or graphs.
    """
    # Define the subgraph
    subgraph = StateGraph(SubgraphState)
    
    def preprocess_step1(state: SubgraphState) -> SubgraphState:
        """First preprocessing step"""
        print("  [Subgraph] Step 1: Preprocessing...")
        value = state.get("value", 0)
        return {
            "value": value * 2,
            "subgraph_result": f"Preprocessed (step 1): {value * 2}",
        }
    
    def preprocess_step2(state: SubgraphState) -> SubgraphState:
        """Second preprocessing step"""
        print("  [Subgraph] Step 2: Preprocessing...")
        value = state.get("value", 0)
        return {
            "value": value + 10,
            "subgraph_result": f"Preprocessed (step 2): {value + 10}",
        }
    
    # Build the subgraph
    subgraph.add_node("step1", preprocess_step1)
    subgraph.add_node("step2", preprocess_step2)
    subgraph.set_entry_point("step1")
    subgraph.add_edge("step1", "step2")
    subgraph.add_edge("step2", END)
    
    return subgraph.compile()


# ========== MAIN GRAPH DEFINITION ==========
def main_graph_node(state: MainGraphState) -> MainGraphState:
    """
    Main graph node that doesn't use subgraphs.
    """
    print("[Main Graph] Processing main data...")
    input_data = state.get("input_data", "")
    
    return {
        "processed_data": f"Main processed: {input_data}",
    }


def node_with_subgraph(state: MainGraphState) -> MainGraphState:
    """
    Node that uses the preprocessing subgraph.
    
    This demonstrates how to call a subgraph from within a node.
    """
    print("[Main Graph] Node using subgraph...")
    
    # Get the preprocessing subgraph
    preprocessing_graph = create_preprocessing_subgraph()
    
    # Prepare state for subgraph
    subgraph_state = {
        "value": 5,  # Example value to preprocess
        "subgraph_result": "",
    }
    
    # Execute the subgraph
    subgraph_result = preprocessing_graph.invoke(subgraph_state)
    
    # Get the current main graph state
    processed_data = state.get("processed_data", "")
    subgraph_outputs = state.get("subgraph_outputs", [])
    
    # Add subgraph result to main state
    subgraph_outputs.append(subgraph_result["subgraph_result"])
    
    return {
        "processed_data": f"{processed_data} -> Used subgraph",
        "subgraph_outputs": subgraph_outputs,
    }


def final_node(state: MainGraphState) -> MainGraphState:
    """
    Final node that combines all results.
    """
    print("[Main Graph] Finalizing...")
    processed_data = state.get("processed_data", "")
    subgraph_outputs = state.get("subgraph_outputs", [])
    
    all_outputs = ", ".join(subgraph_outputs)
    final_result = f"{processed_data} | Subgraphs: [{all_outputs}]"
    
    return {
        "final_result": final_result,
    }


def main():
    """
    Demonstrate using subgraphs in a main graph.
    """
    # Create the main graph
    workflow = StateGraph(MainGraphState)
    
    # Add nodes
    workflow.add_node("main_node", main_graph_node)
    workflow.add_node("subgraph_node", node_with_subgraph)
    workflow.add_node("final_node", final_node)
    
    # Set entry point
    workflow.set_entry_point("main_node")
    
    # Define flow
    workflow.add_edge("main_node", "subgraph_node")
    workflow.add_edge("subgraph_node", "final_node")
    workflow.add_edge("final_node", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Initial state
    initial_state = {
        "input_data": "Initial Data",
        "processed_data": "",
        "subgraph_outputs": [],
        "final_result": "",
    }
    
    print("\n=== Subgraphs Example ===")
    print(f"Input: {initial_state['input_data']}\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print("\n=== Final Result ===")
    print(f"Final Result: {result['final_result']}")
    print(f"Subgraph Outputs: {result['subgraph_outputs']}")
    
    print("\n=== Key Points ===")
    print("1. Subgraphs are reusable workflow components")
    print("2. Subgraphs can be called from within nodes")
    print("3. Subgraphs can have their own state schemas")
    print("4. Composition allows building complex workflows from simple parts")
    print("5. In LangGraph, you can also use add_node() with compiled graphs")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

