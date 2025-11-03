"""
04_multiple_paths.py - Parallel Execution Paths

This tutorial demonstrates how to create multiple execution paths in LangGraph.
We'll see how one node can route to multiple nodes, and how to handle
parallel or branching workflows.

Key Concepts:
- Multiple edges from one node
- Parallel execution paths
- Collecting results from multiple paths
- Different routing strategies
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


# State that collects results from multiple paths
class GraphState(TypedDict):
    """State that tracks multiple processing paths"""
    input_data: str
    path_a_result: str
    path_b_result: str
    path_c_result: str
    all_results: list[str]
    processing_complete: bool


def start_node(state: GraphState) -> GraphState:
    """
    Starting node that prepares data.
    
    Returns state ready for multiple processing paths.
    """
    print("Start node: Preparing data for parallel processing...")
    input_data = state.get("input_data", "")
    
    return {
        "input_data": input_data,
    }


def path_a_processor(state: GraphState) -> GraphState:
    """
    First parallel path: Uppercase processing.
    
    This node processes the input in one way (uppercase).
    """
    print("Path A: Processing (uppercase)...")
    input_data = state.get("input_data", "")
    
    result = f"PATH_A: {input_data.upper()}"
    
    return {
        "path_a_result": result,
    }


def path_b_processor(state: GraphState) -> GraphState:
    """
    Second parallel path: Lowercase processing.
    
    This node processes the input differently (lowercase).
    """
    print("Path B: Processing (lowercase)...")
    input_data = state.get("input_data", "")
    
    result = f"PATH_B: {input_data.lower()}"
    
    return {
        "path_b_result": result,
    }


def path_c_processor(state: GraphState) -> GraphState:
    """
    Third parallel path: Reverse processing.
    
    This node processes the input by reversing it.
    """
    print("Path C: Processing (reverse)...")
    input_data = state.get("input_data", "")
    
    result = f"PATH_C: {input_data[::-1]}"
    
    return {
        "path_c_result": result,
    }


def collect_results(state: GraphState) -> GraphState:
    """
    Collection node that gathers results from all paths.
    
    This node runs after all parallel paths complete and combines their results.
    """
    print("Collect node: Gathering results from all paths...")
    
    # Collect results from all paths
    results = []
    
    if path_a := state.get("path_a_result"):
        results.append(path_a)
    if path_b := state.get("path_b_result"):
        results.append(path_b)
    if path_c := state.get("path_c_result"):
        results.append(path_c)
    
    return {
        "all_results": results,
        "processing_complete": True,
    }


def route_to_all_paths(state: GraphState) -> list[str]:
    """
    Routing function that sends execution to multiple nodes.
    
    This demonstrates parallel execution - all returned nodes will execute.
    The order may vary, but all will complete before moving to the next step.
    
    Returns:
        List of node names to execute in parallel
    """
    # Route to all three processing paths
    return ["path_a_processor", "path_b_processor", "path_c_processor"]


def main():
    """
    Create a graph with multiple parallel paths.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("start", start_node)
    workflow.add_node("path_a_processor", path_a_processor)
    workflow.add_node("path_b_processor", path_b_processor)
    workflow.add_node("path_c_processor", path_c_processor)
    workflow.add_node("collect", collect_results)
    
    # Set entry point
    workflow.set_entry_point("start")
    
    # Add conditional edge that routes to multiple nodes
    # When a routing function returns a list, all nodes execute in parallel
    workflow.add_conditional_edges(
        "start",
        route_to_all_paths,
        {
            "path_a_processor": "path_a_processor",
            "path_b_processor": "path_b_processor",
            "path_c_processor": "path_c_processor",
        }
    )
    
    # All parallel paths converge to the collection node
    workflow.add_edge("path_a_processor", "collect")
    workflow.add_edge("path_b_processor", "collect")
    workflow.add_edge("path_c_processor", "collect")
    
    # Collection node leads to END
    workflow.add_edge("collect", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Test the graph
    initial_state = {
        "input_data": "Hello LangGraph",
        "path_a_result": "",
        "path_b_result": "",
        "path_c_result": "",
        "all_results": [],
        "processing_complete": False,
    }
    
    print("\n=== Multiple Paths Example ===")
    print(f"Input: {initial_state['input_data']}\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print("\n=== Results ===")
    print(f"Path A Result: {result['path_a_result']}")
    print(f"Path B Result: {result['path_b_result']}")
    print(f"Path C Result: {result['path_c_result']}")
    print(f"\nAll Results: {result['all_results']}")
    print(f"Processing Complete: {result['processing_complete']}")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

