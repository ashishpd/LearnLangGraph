"""
15_advanced_state.py - Advanced State Management

This tutorial demonstrates advanced state management patterns including
complex state schemas, state reducers, validation, and transformations.
These patterns are essential for managing complex workflows.

Key Concepts:
- Complex state schemas: Nested and structured state
- State reducers: Custom logic for merging state updates
- State validation: Ensuring state integrity
- State transformations: Converting between state formats
- Immutable state patterns: Proper state update patterns
"""

import os
from typing import TypedDict, Annotated
from typing_extensions import Literal

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# ========== COMPLEX STATE SCHEMA ==========

class UserProfile(TypedDict):
    """Nested user profile structure"""
    user_id: str
    name: str
    email: str
    preferences: dict[str, str]


class ProcessingMetadata(TypedDict):
    """Metadata about processing"""
    start_time: str
    nodes_executed: list[str]
    errors: list[str]
    warnings: list[str]


class AdvancedGraphState(TypedDict):
    """
    Complex state schema with nested structures and lists.
    
    This demonstrates how to define rich state structures for complex workflows.
    """
    # Simple fields
    task_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    
    # Nested structures
    user: UserProfile
    
    # Lists
    steps: list[str]
    results: list[dict[str, str]]
    
    # Metadata
    metadata: ProcessingMetadata
    
    # Annotated fields (for reducers)
    messages: Annotated[list[str], add_messages]


# ========== STATE VALIDATION ==========

def validate_state(state: dict) -> tuple[bool, str]:
    """
    Validate state integrity.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    if "task_id" not in state:
        return False, "Missing required field: task_id"
    
    if "user" not in state:
        return False, "Missing required field: user"
    
    # Validate nested structure
    user = state.get("user", {})
    if "user_id" not in user:
        return False, "User profile missing user_id"
    
    # Validate status
    valid_statuses = ["pending", "processing", "completed", "failed"]
    if state.get("status") not in valid_statuses:
        return False, f"Invalid status. Must be one of: {valid_statuses}"
    
    return True, ""


# ========== STATE TRANSFORMATION ==========

def transform_state_for_node(state: AdvancedGraphState) -> dict:
    """
    Transform state to a format suitable for a specific node.
    
    This is useful when nodes need state in different formats.
    """
    return {
        "task_id": state.get("task_id", ""),
        "user_name": state.get("user", {}).get("name", ""),
        "status": state.get("status", "pending"),
    }


# ========== GRAPH NODES ==========

def initialize_node(state: AdvancedGraphState) -> AdvancedGraphState:
    """
    Initialize node that sets up complex state.
    """
    print("Initializing state...")
    
    task_id = state.get("task_id", "TASK-001")
    
    # Build nested user profile
    user_profile = {
        "user_id": "USER-123",
        "name": "John Doe",
        "email": "john@example.com",
        "preferences": {"theme": "dark", "language": "en"},
    }
    
    # Initialize metadata
    import datetime
    metadata = {
        "start_time": datetime.datetime.now().isoformat(),
        "nodes_executed": [],
        "errors": [],
        "warnings": [],
    }
    
    return {
        "task_id": task_id,
        "status": "processing",
        "user": user_profile,
        "steps": [],
        "results": [],
        "metadata": metadata,
        "messages": ["State initialized"],
    }


def process_node(state: AdvancedGraphState) -> AdvancedGraphState:
    """
    Process node that updates complex state.
    """
    print("Processing node: Updating state...")
    
    # Get current state
    steps = state.get("steps", [])
    results = state.get("results", [])
    metadata = state.get("metadata", {})
    nodes_executed = metadata.get("nodes_executed", [])
    messages = state.get("messages", [])
    
    # Add step
    new_step = f"Processing step {len(steps) + 1}"
    steps.append(new_step)
    
    # Add result
    new_result = {
        "step": new_step,
        "output": f"Processed for task {state.get('task_id')}",
        "timestamp": str(len(results)),
    }
    results.append(new_result)
    
    # Update metadata
    nodes_executed.append("process_node")
    
    # Add message
    messages.append(f"Executed {new_step}")
    
    # Return updated state (only fields that changed)
    return {
        "steps": steps,
        "results": results,
        "metadata": {
            **metadata,
            "nodes_executed": nodes_executed,
        },
        "messages": messages,
    }


def validate_node(state: AdvancedGraphState) -> AdvancedGraphState:
    """
    Validation node that checks state integrity.
    """
    print("Validating state...")
    
    # Validate state
    is_valid, error_message = validate_state(state)
    
    metadata = state.get("metadata", {})
    errors = metadata.get("errors", [])
    warnings = metadata.get("warnings", [])
    messages = state.get("messages", [])
    
    if not is_valid:
        errors.append(error_message)
        messages.append(f"Validation failed: {error_message}")
        status = "failed"
    else:
        messages.append("Validation passed")
        status = "completed"
    
    return {
        "status": status,
        "metadata": {
            **metadata,
            "errors": errors,
            "warnings": warnings,
        },
        "messages": messages,
    }


def main():
    """
    Demonstrate advanced state management.
    """
    # Create the graph
    workflow = StateGraph(AdvancedGraphState)
    
    # Add nodes
    workflow.add_node("initialize", initialize_node)
    workflow.add_node("process", process_node)
    workflow.add_node("validate", validate_node)
    
    # Set entry point
    workflow.set_entry_point("initialize")
    
    # Define flow
    workflow.add_edge("initialize", "process")
    workflow.add_edge("process", "validate")
    workflow.add_edge("validate", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Initial state (minimal - will be enhanced by initialize node)
    initial_state = {
        "task_id": "TASK-001",
        "status": "pending",
        "user": {},  # Will be populated by initialize
        "steps": [],
        "results": [],
        "metadata": {},
        "messages": [],
    }
    
    print("\n=== Advanced State Management Example ===")
    print(f"Initial Task ID: {initial_state['task_id']}\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print("\n=== Final State ===")
    print(f"Task ID: {result['task_id']}")
    print(f"Status: {result['status']}")
    print(f"User: {result['user'].get('name')} ({result['user'].get('email')})")
    print(f"Steps Completed: {len(result['steps'])}")
    print(f"Results: {len(result['results'])}")
    print(f"Nodes Executed: {result['metadata']['nodes_executed']}")
    print(f"Messages: {result['messages']}")
    
    if result['metadata']['errors']:
        print(f"Errors: {result['metadata']['errors']}")
    
    print("\n=== Key Points ===")
    print("1. TypedDict provides type safety and documentation")
    print("2. Nested structures allow complex data modeling")
    print("3. State validation ensures data integrity")
    print("4. State transformations adapt data for different nodes")
    print("5. Reducers (like add_messages) handle list merging correctly")
    print("6. Return only changed fields - LangGraph merges automatically")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

