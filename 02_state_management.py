"""
02_state_management.py - Understanding State and Annotations

This tutorial demonstrates how to manage state in LangGraph. We'll see how
to define state schemas, pass data between nodes, and understand state
immutability.

Key Concepts:
- TypedDict for state schemas
- State immutability (nodes return new state, don't modify in place)
- Accessing nested state properties
- State reducers (for merging state)
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


# Define a more complex state structure
# Using TypedDict provides type safety and clear documentation
class GraphState(TypedDict):
    """
    State schema for our graph.
    
    In LangGraph, state is passed between nodes as a dictionary-like object.
    TypedDict helps define the structure and enables type checking.
    """
    # Simple fields
    counter: int  # A counter that will be incremented
    messages: list[str]  # A list of messages
    user_input: str  # User input string
    processed: bool  # Flag to track processing status


def input_node(state: GraphState) -> GraphState:
    """
    First node: Collect and initialize state.
    
    This node demonstrates initializing state fields.
    Note: We return a dictionary that represents the NEW state.
    The state parameter contains the current state, which we merge with our updates.
    """
    print("Input node: Initializing state...")
    
    # Access current state (with defaults)
    counter = state.get("counter", 0)
    messages = state.get("messages", [])
    user_input = state.get("user_input", "")
    
    # Create new state (don't modify the input state!)
    # LangGraph uses state reducers to merge returned state with current state
    return {
        "counter": counter,
        "messages": messages + [f"Input: Received '{user_input}'"],
        "user_input": user_input,
        "processed": False,
    }


def process_node(state: GraphState) -> GraphState:
    """
    Second node: Process the input and increment counter.
    
    This node shows how to read from state, process data, and return updates.
    """
    print("Process node: Processing state...")
    
    # Read current state
    counter = state.get("counter", 0)
    messages = state.get("messages", [])
    user_input = state.get("user_input", "")
    
    # Process: increment counter and add message
    new_counter = counter + 1
    new_messages = messages + [f"Processed: '{user_input.upper()}' (step {new_counter})"]
    
    # Return updated state
    # Only include fields you want to update
    return {
        "counter": new_counter,
        "messages": new_messages,
        "processed": False,  # Still not fully processed
    }


def output_node(state: GraphState) -> GraphState:
    """
    Third node: Finalize processing.
    
    This node completes the processing and marks state as processed.
    """
    print("Output node: Finalizing...")
    
    # Read state
    counter = state.get("counter", 0)
    messages = state.get("messages", [])
    
    # Add final message and mark as processed
    final_messages = messages + [f"Output: Completed in {counter} steps"]
    
    return {
        "messages": final_messages,
        "processed": True,  # Mark as complete
    }


def main():
    """
    Create and run a graph that demonstrates state management.
    """
    # Create the graph with our state schema
    workflow = StateGraph(GraphState)
    
    # Add all nodes
    workflow.add_node("input", input_node)
    workflow.add_node("process", process_node)
    workflow.add_node("output", output_node)
    
    # Set the entry point
    workflow.set_entry_point("input")
    
    # Define the flow: input -> process -> output -> END
    workflow.add_edge("input", "process")
    workflow.add_edge("process", "output")
    workflow.add_edge("output", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Create initial state
    # All fields from GraphState should be provided
    initial_state = {
        "counter": 0,
        "messages": [],
        "user_input": "Hello from LangGraph",
        "processed": False,
    }
    
    print("\n=== State Management Example ===")
    print(f"Initial state: {initial_state}\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print("\n=== Final State ===")
    print(f"Counter: {result['counter']}")
    print(f"Processed: {result['processed']}")
    print(f"Messages:")
    for msg in result['messages']:
        print(f"  - {msg}")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

