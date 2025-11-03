"""
01_hello_world.py - Basic LangGraph Introduction

This is the simplest LangGraph example. We'll create a basic graph with two nodes
that pass messages to each other, demonstrating the fundamental concepts of
LangGraph: nodes, edges, and state flow.

Key Concepts:
- StateGraph: The main graph class for creating workflows
- Nodes: Functions that process state
- Edges: Connections between nodes
- State: Data passed between nodes
"""

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI LLM
llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# Define the state structure
# TypedDict allows us to define a clear schema for our graph state
class GraphState(TypedDict):
    """State schema for our simple graph"""
    message: str  # The message being passed through nodes


def node_a(state: GraphState) -> GraphState:
    """
    First node in the graph.
    
    This function receives the current state, processes it, and returns
    an updated state. In LangGraph, nodes must always accept and return state.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with modified message
    """
    print("Node A is processing...")
    # Access and modify state
    current_message = state.get("message", "")
    new_message = f"Node A says: {current_message}"
    
    # Return updated state (state is immutable, so we return a new dict)
    return {"message": new_message}


def node_b(state: GraphState) -> GraphState:
    """
    Second node in the graph.
    
    This node receives state from node_a and processes it further.
    """
    print("Node B is processing...")
    current_message = state.get("message", "")
    new_message = f"{current_message} -> Node B processed it!"
    
    return {"message": new_message}


def main():
    """
    Main function to create and run the graph.
    """
    # Create a StateGraph instance
    # StateGraph manages the flow of state through nodes
    workflow = StateGraph(GraphState)
    
    # Add nodes to the graph
    # Nodes are functions that process state
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    
    # Define the entry point
    # This is where execution starts
    workflow.set_entry_point("node_a")
    
    # Add edges to define the flow
    # This creates a path: node_a -> node_b -> END
    workflow.add_edge("node_a", "node_b")
    workflow.add_edge("node_b", END)
    
    # Compile the graph
    # This validates the graph structure and makes it executable
    app = workflow.compile()
    
    # Run the graph with initial state
    # The state dictionary matches our GraphState TypedDict
    initial_state = {"message": "Hello, LangGraph!"}
    
    print("\n=== Running Hello World Graph ===")
    print(f"Initial message: {initial_state['message']}\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print(f"\nFinal result: {result['message']}")
    print("\n=== Graph Execution Complete ===")


if __name__ == "__main__":
    main()

