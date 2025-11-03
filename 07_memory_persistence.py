"""
07_memory_persistence.py - State Persistence and Checkpoints

This tutorial demonstrates how to persist state in LangGraph workflows.
State persistence allows you to save and resume workflows, which is crucial
for long-running processes and human-in-the-loop applications.

Key Concepts:
- MemorySaver: In-memory checkpoint storage
- Checkpointing: Saving state at specific points
- Thread IDs: Unique identifiers for workflow instances
- Resuming: Continuing from a saved checkpoint
- State recovery: Loading previous state
"""

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State that tracks progress through multiple steps
class GraphState(TypedDict):
    """State with checkpoint tracking"""
    step_number: int
    data: str
    processed_steps: list[str]
    completed: bool


def step_one(state: GraphState) -> GraphState:
    """
    First step in the workflow.
    
    This demonstrates a node that saves its state for later resumption.
    """
    print("Step 1: Processing...")
    data = state.get("data", "")
    
    processed_steps = state.get("processed_steps", [])
    processed_steps.append("step_one")
    
    return {
        "step_number": 1,
        "data": f"{data} -> Step1",
        "processed_steps": processed_steps,
    }


def step_two(state: GraphState) -> GraphState:
    """
    Second step in the workflow.
    """
    print("Step 2: Processing...")
    data = state.get("data", "")
    
    processed_steps = state.get("processed_steps", [])
    processed_steps.append("step_two")
    
    return {
        "step_number": 2,
        "data": f"{data} -> Step2",
        "processed_steps": processed_steps,
    }


def step_three(state: GraphState) -> GraphState:
    """
    Third and final step.
    """
    print("Step 3: Processing...")
    data = state.get("data", "")
    
    processed_steps = state.get("processed_steps", [])
    processed_steps.append("step_three")
    
    return {
        "step_number": 3,
        "data": f"{data} -> Step3",
        "processed_steps": processed_steps,
        "completed": True,
    }


def main():
    """
    Demonstrate state persistence with checkpoints.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("step_one", step_one)
    workflow.add_node("step_two", step_two)
    workflow.add_node("step_three", step_three)
    
    # Set entry point
    workflow.set_entry_point("step_one")
    
    # Define flow
    workflow.add_edge("step_one", "step_two")
    workflow.add_edge("step_two", "step_three")
    workflow.add_edge("step_three", END)
    
    # Create a MemorySaver for checkpointing
    # In production, use SQLiteSaver or similar for persistent storage
    memory = MemorySaver()
    
    # Compile with checkpointer
    # This enables saving and loading state
    app = workflow.compile(checkpointer=memory)
    
    # Create a unique thread ID for this workflow instance
    # Thread IDs allow multiple workflows to run independently
    thread_id = "workflow-001"
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial state
    initial_state = {
        "step_number": 0,
        "data": "Initial",
        "processed_steps": [],
        "completed": False,
    }
    
    print("\n=== Memory Persistence Example ===")
    print(f"Thread ID: {thread_id}\n")
    
    # Run first step - state is automatically checkpointed
    print("--- Executing Step 1 ---")
    state_after_step1 = app.invoke(initial_state, config=config)
    print(f"State after step 1: {state_after_step1}\n")
    
    # Simulate workflow interruption
    # In a real scenario, this might be a system crash, user pause, etc.
    print("--- Simulating Workflow Interruption ---")
    print("(In production, workflow might pause here for hours/days)\n")
    
    # Later, resume from checkpoint
    # The checkpointer has saved our state, so we can continue
    print("--- Resuming from Checkpoint ---")
    print("(Loading saved state and continuing...)\n")
    
    # Get the current state from checkpoint
    # In practice, you'd get this from the saved checkpoint
    current_checkpoint = memory.get({"configurable": {"thread_id": thread_id}})
    if current_checkpoint:
        print(f"Found checkpoint with {len(current_checkpoint.get('channel_values', {}).get('processed_steps', []))} completed steps")
    
    # Continue execution from where we left off
    print("--- Continuing Execution ---")
    final_state = app.invoke(None, config=config)  # None means use checkpoint state
    
    print("\n=== Final Result ===")
    print(f"Completed: {final_state.get('completed')}")
    print(f"Final Data: {final_state.get('data')}")
    print(f"Processed Steps: {final_state.get('processed_steps')}")
    
    print("\n=== Key Points ===")
    print("1. Checkpoints save state after each node execution")
    print("2. Thread IDs allow multiple independent workflow instances")
    print("3. You can resume workflows from any checkpoint")
    print("4. Use SQLiteSaver for production (persists across restarts)")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

