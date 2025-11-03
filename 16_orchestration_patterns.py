"""
16_orchestration_patterns.py - Workflow Orchestration Patterns

This tutorial demonstrates advanced orchestration patterns for coordinating
multiple workflows, tasks, and resources. Orchestration is crucial for
complex systems that need to manage dependencies, scheduling, and resource
coordination.

Key Concepts:
- Workflow orchestration: Coordinating multiple workflows
- Task scheduling: Managing execution order and dependencies
- Dependency management: Handling task dependencies
- Resource coordination: Managing shared resources
- Workflow coordination: Multiple graphs working together
"""

import os
from typing import TypedDict
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State for orchestration
class OrchestrationState(TypedDict):
    """State for workflow orchestration"""
    workflow_id: str
    tasks: list[dict]
    completed_tasks: list[str]
    failed_tasks: list[str]
    task_dependencies: dict[str, list[str]]
    resources: dict[str, bool]  # Resource availability
    execution_order: list[str]
    orchestration_status: str


# ========== TASK DEFINITIONS ==========

def task_a(state: OrchestrationState) -> OrchestrationState:
    """Task A that requires resource_1"""
    print("[Orchestrator] Executing Task A...")
    workflow_id = state.get("workflow_id", "")
    completed_tasks = state.get("completed_tasks", [])
    resources = state.get("resources", {})
    
    # Acquire resource
    if resources.get("resource_1", False):
        print("  Resource 1 acquired")
        resources["resource_1"] = False  # Mark as in use
    else:
        print("  Waiting for resource_1...")
        return state
    
    # Execute task
    completed_tasks.append("task_a")
    
    # Release resource
    resources["resource_1"] = True
    
    return {
        "completed_tasks": completed_tasks,
        "resources": resources,
    }


def task_b(state: OrchestrationState) -> OrchestrationState:
    """Task B that depends on task_a"""
    print("[Orchestrator] Executing Task B...")
    completed_tasks = state.get("completed_tasks", [])
    
    # Check dependency
    if "task_a" not in completed_tasks:
        print("  Waiting for task_a to complete...")
        return state
    
    # Execute task
    completed_tasks.append("task_b")
    print("  Task B completed")
    
    return {
        "completed_tasks": completed_tasks,
    }


def task_c(state: OrchestrationState) -> OrchestrationState:
    """Task C that can run in parallel with task_b"""
    print("[Orchestrator] Executing Task C...")
    completed_tasks = state.get("completed_tasks", [])
    
    # No dependencies
    completed_tasks.append("task_c")
    print("  Task C completed")
    
    return {
        "completed_tasks": completed_tasks,
    }


def dependency_resolver(state: OrchestrationState) -> OrchestrationState:
    """
    Resolve task dependencies and determine execution order.
    
    This node analyzes dependencies and creates an execution plan.
    """
    print("[Orchestrator] Resolving dependencies...")
    
    tasks = state.get("tasks", [])
    task_dependencies = state.get("task_dependencies", {})
    execution_order = state.get("execution_order", [])
    
    # Topological sort for dependency resolution
    # Simple implementation for demonstration
    all_tasks = set()
    for task in tasks:
        all_tasks.add(task["name"])
        all_tasks.update(task_dependencies.get(task["name"], []))
    
    # Build execution order (simplified topological sort)
    completed = set(state.get("completed_tasks", []))
    remaining = all_tasks - completed
    
    new_order = []
    for task_name in remaining:
        deps = task_dependencies.get(task_name, [])
        if all(dep in completed for dep in deps):
            new_order.append(task_name)
    
    execution_order.extend(new_order)
    
    print(f"  Execution order: {execution_order}")
    
    return {
        "execution_order": execution_order,
    }


def resource_manager(state: OrchestrationState) -> OrchestrationState:
    """
    Manage resource allocation and availability.
    """
    print("[Orchestrator] Managing resources...")
    
    resources = state.get("resources", {})
    execution_order = state.get("execution_order", [])
    completed_tasks = state.get("completed_tasks", [])
    
    # Initialize resources if needed
    if not resources:
        resources = {
            "resource_1": True,
            "resource_2": True,
        }
    
    # Check resource availability for next tasks
    next_tasks = [t for t in execution_order if t not in completed_tasks]
    
    print(f"  Available resources: {[k for k, v in resources.items() if v]}")
    print(f"  Next tasks: {next_tasks}")
    
    return {
        "resources": resources,
    }


def orchestrator_node(state: OrchestrationState) -> OrchestrationState:
    """
    Main orchestrator node that coordinates task execution.
    """
    print("[Orchestrator] Coordinating workflow...")
    
    execution_order = state.get("execution_order", [])
    completed_tasks = state.get("completed_tasks", [])
    orchestration_status = state.get("orchestration_status", "running")
    
    # Check if all tasks are complete
    remaining_tasks = [t for t in execution_order if t not in completed_tasks]
    
    if not remaining_tasks:
        orchestration_status = "completed"
        print("  All tasks completed!")
    
    return {
        "orchestration_status": orchestration_status,
    }


def route_orchestration(state: OrchestrationState) -> str:
    """Route based on orchestration status"""
    orchestration_status = state.get("orchestration_status", "running")
    execution_order = state.get("execution_order", [])
    completed_tasks = state.get("completed_tasks", [])
    
    if orchestration_status == "completed":
        return "end"
    
    # Determine next task to execute
    remaining_tasks = [t for t in execution_order if t not in completed_tasks]
    if remaining_tasks:
        next_task = remaining_tasks[0]
        
        # Route to appropriate task node
        if next_task == "task_a":
            return "task_a"
        elif next_task == "task_b":
            return "task_b"
        elif next_task == "task_c":
            return "task_c"
    
    return "end"


def main():
    """
    Demonstrate workflow orchestration patterns.
    """
    # Create the orchestration graph
    workflow = StateGraph(OrchestrationState)
    
    # Add nodes
    workflow.add_node("dependency_resolver", dependency_resolver)
    workflow.add_node("resource_manager", resource_manager)
    workflow.add_node("task_a", task_a)
    workflow.add_node("task_b", task_b)
    workflow.add_node("task_c", task_c)
    workflow.add_node("orchestrator", orchestrator_node)
    
    # Set entry point
    workflow.set_entry_point("dependency_resolver")
    
    # Define orchestration flow
    workflow.add_edge("dependency_resolver", "resource_manager")
    workflow.add_edge("resource_manager", "orchestrator")
    
    workflow.add_conditional_edges(
        "orchestrator",
        route_orchestration,
        {
            "task_a": "task_a",
            "task_b": "task_b",
            "task_c": "task_c",
            "end": END,
        }
    )
    
    # Tasks loop back to orchestrator
    workflow.add_edge("task_a", "orchestrator")
    workflow.add_edge("task_b", "orchestrator")
    workflow.add_edge("task_c", "orchestrator")
    
    # Compile the graph
    app = workflow.compile()
    
    # Initial state with tasks and dependencies
    initial_state = {
        "workflow_id": "WORKFLOW-001",
        "tasks": [
            {"name": "task_a", "description": "Initial task"},
            {"name": "task_b", "description": "Depends on task_a"},
            {"name": "task_c", "description": "Independent task"},
        ],
        "completed_tasks": [],
        "failed_tasks": [],
        "task_dependencies": {
            "task_b": ["task_a"],  # task_b depends on task_a
        },
        "resources": {},
        "execution_order": [],
        "orchestration_status": "pending",
    }
    
    print("\n=== Orchestration Patterns Example ===")
    print(f"Workflow ID: {initial_state['workflow_id']}")
    print(f"Tasks: {[t['name'] for t in initial_state['tasks']]}")
    print(f"Dependencies: {initial_state['task_dependencies']}\n")
    
    # Execute the orchestration
    result = app.invoke(initial_state)
    
    print("\n=== Orchestration Results ===")
    print(f"Status: {result['orchestration_status']}")
    print(f"Completed Tasks: {result['completed_tasks']}")
    print(f"Execution Order: {result['execution_order']}")
    print(f"Resources: {result['resources']}")
    
    print("\n=== Key Points ===")
    print("1. Orchestration manages task execution order")
    print("2. Dependency resolution ensures correct execution sequence")
    print("3. Resource management prevents conflicts")
    print("4. Orchestrator coordinates overall workflow")
    print("5. Tasks can execute in parallel when dependencies allow")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

