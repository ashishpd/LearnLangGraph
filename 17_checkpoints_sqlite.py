"""
17_checkpoints_sqlite.py - SQLite Checkpoints for Persistence

This tutorial demonstrates how to use SQLite for persistent checkpoints
in LangGraph. SQLite checkpoints allow workflows to survive restarts,
support multi-user scenarios, and enable resuming from any point.

Key Concepts:
- SQLiteSaver: Persistent checkpoint storage
- Checkpoint management: Saving and loading state
- Thread management: Multiple independent workflow instances
- Resume workflows: Continuing from saved checkpoints
- Multi-user support: Concurrent workflow execution
"""

import os
import tempfile
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State for checkpointed workflow
class CheckpointedState(TypedDict):
    """State that will be checkpointed"""
    user_id: str
    task_description: str
    current_step: int
    total_steps: int
    results: list[str]
    completed: bool


def step_one(state: CheckpointedState) -> CheckpointedState:
    """
    First step in the workflow.
    
    This step will be checkpointed automatically.
    """
    print(f"[Step 1] Processing for user {state.get('user_id')}...")
    
    task_description = state.get("task_description", "")
    results = state.get("results", [])
    results.append(f"Step 1: Started processing '{task_description}'")
    
    return {
        "current_step": 1,
        "results": results,
    }


def step_two(state: CheckpointedState) -> CheckpointedState:
    """
    Second step in the workflow.
    """
    print(f"[Step 2] Processing...")
    
    results = state.get("results", [])
    task_description = state.get("task_description", "")
    results.append(f"Step 2: Analyzed '{task_description}'")
    
    return {
        "current_step": 2,
        "results": results,
    }


def step_three(state: CheckpointedState) -> CheckpointedState:
    """
    Final step in the workflow.
    """
    print(f"[Step 3] Finalizing...")
    
    results = state.get("results", [])
    task_description = state.get("task_description", "")
    results.append(f"Step 3: Completed '{task_description}'")
    
    return {
        "current_step": 3,
        "results": results,
        "completed": True,
    }


def main():
    """
    Demonstrate SQLite checkpoints.
    """
    # Create a temporary SQLite database for this example
    # In production, use a real database file path
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = db_file.name
    db_file.close()
    
    print(f"\n=== SQLite Checkpoints Example ===")
    print(f"Database: {db_path}\n")
    
    # Create SQLiteSaver for persistent checkpoints
    # This saves all state transitions to the database
    checkpointer = SqliteSaver.from_conn_string(db_path)
    
    # Create the graph
    workflow = StateGraph(CheckpointedState)
    
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
    
    # Compile with SQLite checkpointer
    # This enables persistent checkpointing
    app = workflow.compile(checkpointer=checkpointer)
    
    # Create thread IDs for different users/workflows
    user1_thread = "user-001"
    user2_thread = "user-002"
    
    # ========== USER 1 WORKFLOW ==========
    print("--- User 1 Workflow ---")
    config_user1 = {"configurable": {"thread_id": user1_thread}}
    
    initial_state_user1 = {
        "user_id": "user-001",
        "task_description": "Process user 1's request",
        "current_step": 0,
        "total_steps": 3,
        "results": [],
        "completed": False,
    }
    
    # Execute first step - checkpoint is automatically saved
    print("\n[User 1] Executing step 1...")
    state_after_step1 = app.invoke(initial_state_user1, config=config_user1)
    print(f"Checkpoint saved after step 1")
    
    # Simulate workflow interruption (system restart, user pause, etc.)
    print("\n--- Simulating System Restart ---")
    print("(In production, this could be hours or days later)\n")
    
    # Later: Resume from checkpoint
    # The checkpointer automatically loads the saved state
    print("--- Resuming User 1 Workflow ---")
    print("(Loading from SQLite checkpoint...)\n")
    
    # Continue from checkpoint (None means use saved state)
    final_state_user1 = app.invoke(None, config=config_user1)
    
    print(f"\n[User 1] Final Results:")
    print(f"  Completed: {final_state_user1.get('completed')}")
    print(f"  Steps: {final_state_user1.get('current_step')}/{final_state_user1.get('total_steps')}")
    print(f"  Results: {final_state_user1.get('results')}")
    
    # ========== USER 2 WORKFLOW (CONCURRENT) ==========
    print("\n--- User 2 Workflow (Concurrent) ---")
    config_user2 = {"configurable": {"thread_id": user2_thread}}
    
    initial_state_user2 = {
        "user_id": "user-002",
        "task_description": "Process user 2's request",
        "current_step": 0,
        "total_steps": 3,
        "results": [],
        "completed": False,
    }
    
    # User 2's workflow runs independently
    print("\n[User 2] Executing all steps...")
    final_state_user2 = app.invoke(initial_state_user2, config=config_user2)
    
    print(f"\n[User 2] Final Results:")
    print(f"  Completed: {final_state_user2.get('completed')}")
    print(f"  Steps: {final_state_user2.get('current_step')}/{final_state_user2.get('total_steps')}")
    print(f"  Results: {final_state_user2.get('results')}")
    
    # ========== CHECKPOINT QUERY ==========
    print("\n--- Querying Checkpoints ---")
    
    # Get checkpoint for user 1
    checkpoint_user1 = checkpointer.get({"configurable": {"thread_id": user1_thread}})
    if checkpoint_user1:
        print(f"User 1 checkpoint exists: {checkpoint_user1 is not None}")
        if hasattr(checkpoint_user1, 'channel_values'):
            print(f"  Step: {checkpoint_user1.channel_values.get('current_step')}")
    
    # List all thread IDs (all workflows)
    # In production, use checkpointer.list() to get all threads
    print(f"Multiple workflows supported via different thread IDs")
    
    print("\n=== Key Points ===")
    print("1. SQLiteSaver provides persistent checkpoint storage")
    print("2. Checkpoints survive system restarts")
    print("3. Thread IDs enable multiple independent workflows")
    print("4. State is automatically saved after each node")
    print("5. Workflows can resume from any checkpoint")
    print("6. Supports concurrent multi-user scenarios")
    print(f"\nDatabase file: {db_path}")
    print("(In production, use a proper database location)")
    
    # Cleanup
    try:
        os.unlink(db_path)
        print("\nTemporary database cleaned up")
    except:
        pass
    
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

