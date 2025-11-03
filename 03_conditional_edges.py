"""
03_conditional_edges.py - Routing and Decision Making

This tutorial demonstrates conditional edges in LangGraph. Conditional edges
allow you to route to different nodes based on the current state, enabling
decision-making and dynamic workflows.

Key Concepts:
- Conditional edges: Routes based on state evaluation
- Routing functions: Functions that return the next node name
- Multiple paths: Different execution paths based on conditions
- END node: Special node that terminates graph execution
"""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# Define state with a decision field
class GraphState(dict):
    """State that includes a number and routing decision"""
    number: int
    path: str  # Which path was taken
    processed: bool


def start_node(state: GraphState) -> GraphState:
    """
    Initial node that processes a number.
    
    Returns updated state with the number.
    """
    print("Start node: Processing number...")
    number = state.get("number", 0)
    
    return {
        "number": number,
        "path": "started",
        "processed": False,
    }


def even_handler(state: GraphState) -> GraphState:
    """
    Handler for even numbers.
    
    This node processes numbers that are even.
    """
    print("Even handler: Processing even number...")
    number = state.get("number", 0)
    
    return {
        "number": number,
        "path": "even",
        "processed": True,
    }


def odd_handler(state: GraphState) -> GraphState:
    """
    Handler for odd numbers.
    
    This node processes numbers that are odd.
    """
    print("Odd handler: Processing odd number...")
    number = state.get("number", 0)
    
    return {
        "number": number,
        "path": "odd",
        "processed": True,
    }


def route_by_number(state: GraphState) -> Literal["even_handler", "odd_handler"]:
    """
    Conditional routing function.
    
    This function examines the state and returns the name of the next node
    to execute. The return type must match one of the node names or END.
    
    Args:
        state: Current graph state
        
    Returns:
        Name of the next node to execute
    """
    number = state.get("number", 0)
    
    # Make routing decision based on state
    if number % 2 == 0:
        print(f"Routing: {number} is even -> even_handler")
        return "even_handler"
    else:
        print(f"Routing: {number} is odd -> odd_handler")
        return "odd_handler"


def main():
    """
    Create a graph with conditional routing.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("start", start_node)
    workflow.add_node("even_handler", even_handler)
    workflow.add_node("odd_handler", odd_handler)
    
    # Set entry point
    workflow.set_entry_point("start")
    
    # Add conditional edge
    # The routing function determines which node to go to next
    workflow.add_conditional_edges(
        "start",
        route_by_number,  # Function that returns the next node name
        {
            "even_handler": "even_handler",  # Map return value to node
            "odd_handler": "odd_handler",
        }
    )
    
    # After handling, both paths end
    workflow.add_edge("even_handler", END)
    workflow.add_edge("odd_handler", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Test with different numbers
    test_cases = [
        {"number": 4, "path": "", "processed": False},  # Even
        {"number": 7, "path": "", "processed": False},  # Odd
        {"number": 0, "path": "", "processed": False},  # Even (edge case)
    ]
    
    print("\n=== Conditional Edges Example ===\n")
    
    for i, initial_state in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: number = {initial_state['number']} ---")
        result = app.invoke(initial_state)
        print(f"Result: Path taken = {result['path']}, Processed = {result['processed']}")
    
    print("\n=== All Tests Complete ===")


if __name__ == "__main__":
    main()

