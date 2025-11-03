"""
18_branching_merging.py - Complex Branching and Merging Patterns

This tutorial demonstrates advanced branching and merging patterns in LangGraph.
These patterns are essential for workflows that need to split into multiple
paths, process them independently, and then merge results back together.

Key Concepts:
- Dynamic branching: Creating branches based on runtime conditions
- Merge strategies: Different ways to combine branch results
- Conditional merges: Merging only specific branches
- Result aggregation: Combining outputs from multiple paths
- Synchronization points: Waiting for all branches before continuing
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


# State for branching and merging
class BranchingState(TypedDict):
    """State for branching workflow"""
    input_data: str
    branch_paths: list[str]
    branch_results: dict[str, str]
    merged_result: str
    merge_strategy: str


# ========== BRANCH NODES ==========

def branch_a_processor(state: BranchingState) -> BranchingState:
    """
    Process data in branch A.
    """
    print("[Branch A] Processing...")
    
    input_data = state.get("input_data", "")
    branch_results = state.get("branch_results", {})
    
    # Process in branch A style (uppercase)
    result = f"BranchA: {input_data.upper()}"
    branch_results["branch_a"] = result
    
    return {
        "branch_results": branch_results,
    }


def branch_b_processor(state: BranchingState) -> BranchingState:
    """
    Process data in branch B.
    """
    print("[Branch B] Processing...")
    
    input_data = state.get("input_data", "")
    branch_results = state.get("branch_results", {})
    
    # Process in branch B style (lowercase)
    result = f"BranchB: {input_data.lower()}"
    branch_results["branch_b"] = result
    
    return {
        "branch_results": branch_results,
    }


def branch_c_processor(state: BranchingState) -> BranchingState:
    """
    Process data in branch C.
    """
    print("[Branch B] Processing...")
    
    input_data = state.get("input_data", "")
    branch_results = state.get("branch_results", {})
    
    # Process in branch C style (reverse)
    result = f"BranchC: {input_data[::-1]}"
    branch_results["branch_c"] = result
    
    return {
        "branch_results": branch_results,
    }


# ========== BRANCHING LOGIC ==========

def determine_branches(state: BranchingState) -> list[str]:
    """
    Dynamically determine which branches to execute.
    
    This function decides which branches to create based on the input data.
    """
    input_data = state.get("input_data", "")
    branch_paths = state.get("branch_paths", [])
    
    # Simple logic: determine branches based on input length
    branches_to_execute = []
    
    if len(input_data) > 5:
        branches_to_execute.append("branch_a_processor")
    if len(input_data) > 10:
        branches_to_execute.append("branch_b_processor")
    if len(input_data) > 15:
        branches_to_execute.append("branch_c_processor")
    
    # Default: at least one branch
    if not branches_to_execute:
        branches_to_execute.append("branch_a_processor")
    
    print(f"[Branching] Creating {len(branches_to_execute)} branches: {branches_to_execute}")
    
    return branches_to_execute


# ========== MERGING STRATEGIES ==========

def merge_all_strategy(state: BranchingState) -> BranchingState:
    """
    Merge strategy: Combine all branch results.
    """
    print("[Merging] Using 'merge_all' strategy...")
    
    branch_results = state.get("branch_results", {})
    
    # Combine all results
    all_results = []
    for branch_name, result in branch_results.items():
        all_results.append(result)
    
    merged_result = " | ".join(all_results)
    
    return {
        "merged_result": merged_result,
        "merge_strategy": "merge_all",
    }


def merge_selective_strategy(state: BranchingState) -> BranchingState:
    """
    Merge strategy: Selectively merge only specific branches.
    """
    print("[Merging] Using 'merge_selective' strategy...")
    
    branch_results = state.get("branch_results", {})
    
    # Only merge branch_a and branch_b, skip branch_c
    selected_results = []
    for branch_name in ["branch_a", "branch_b"]:
        if branch_name in branch_results:
            selected_results.append(branch_results[branch_name])
    
    merged_result = " + ".join(selected_results) if selected_results else "No results"
    
    return {
        "merged_result": merged_result,
        "merge_strategy": "merge_selective",
    }


def merge_priority_strategy(state: BranchingState) -> BranchingState:
    """
    Merge strategy: Use priority order (first available wins).
    """
    print("[Merging] Using 'merge_priority' strategy...")
    
    branch_results = state.get("branch_results", {})
    
    # Priority order: branch_a > branch_b > branch_c
    priority_order = ["branch_a", "branch_b", "branch_c"]
    
    for branch_name in priority_order:
        if branch_name in branch_results:
            merged_result = branch_results[branch_name]
            return {
                "merged_result": merged_result,
                "merge_strategy": "merge_priority",
            }
    
    return {
        "merged_result": "No results available",
        "merge_strategy": "merge_priority",
    }


def route_to_merge_strategy(state: BranchingState) -> str:
    """
    Route to appropriate merge strategy based on conditions.
    """
    input_data = state.get("input_data", "")
    branch_results = state.get("branch_results", {})
    
    # Determine merge strategy based on number of branches completed
    num_branches = len(branch_results)
    
    if num_branches >= 3:
        return "merge_all_strategy"
    elif num_branches == 2:
        return "merge_selective_strategy"
    else:
        return "merge_priority_strategy"


def main():
    """
    Demonstrate branching and merging patterns.
    """
    # Create the graph
    workflow = StateGraph(BranchingState)
    
    # Add branch nodes
    workflow.add_node("branch_a_processor", branch_a_processor)
    workflow.add_node("branch_b_processor", branch_b_processor)
    workflow.add_node("branch_c_processor", branch_c_processor)
    
    # Add merge strategy nodes
    workflow.add_node("merge_all_strategy", merge_all_strategy)
    workflow.add_node("merge_selective_strategy", merge_selective_strategy)
    workflow.add_node("merge_priority_strategy", merge_priority_strategy)
    
    # Set entry point (we'll start with branching)
    workflow.set_entry_point("branch_a_processor")
    
    # Dynamic branching: route to multiple branches
    # Note: In LangGraph, we use conditional edges that return lists
    # For this example, we'll manually add edges but in practice,
    # you'd use a routing function that returns a list
    
    # For demonstration, we'll use a simpler approach:
    # Route all branches in parallel, then merge
    
    def route_to_all_branches(state: BranchingState) -> list[str]:
        return determine_branches(state)
    
    # Add conditional edge for dynamic branching
    workflow.add_conditional_edges(
        "branch_a_processor",
        lambda state: ["branch_b_processor", "branch_c_processor"] if len(state.get("input_data", "")) > 10 else [END],
        {
            "branch_b_processor": "branch_b_processor",
            "branch_c_processor": "branch_c_processor",
        }
    )
    
    # All branches converge to merge
    workflow.add_edge("branch_b_processor", "merge_all_strategy")
    workflow.add_edge("branch_c_processor", "merge_all_strategy")
    
    # After merge, route based on strategy
    workflow.add_conditional_edges(
        "merge_all_strategy",
        route_to_merge_strategy,
        {
            "merge_all_strategy": END,
            "merge_selective_strategy": "merge_selective_strategy",
            "merge_priority_strategy": "merge_priority_strategy",
        }
    )
    
    workflow.add_edge("merge_selective_strategy", END)
    workflow.add_edge("merge_priority_strategy", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Test with different inputs
    test_cases = [
        "Short",  # Single branch
        "Medium length input",  # Multiple branches
        "This is a very long input string",  # All branches
    ]
    
    print("\n=== Branching and Merging Example ===\n")
    
    for test_input in test_cases:
        print(f"\n--- Test Case: '{test_input}' ---")
        
        initial_state = {
            "input_data": test_input,
            "branch_paths": [],
            "branch_results": {},
            "merged_result": "",
            "merge_strategy": "",
        }
        
        result = app.invoke(initial_state)
        
        print(f"Branches executed: {list(result['branch_results'].keys())}")
        print(f"Merged result: {result['merged_result']}")
        print(f"Strategy used: {result['merge_strategy']}")
    
    print("\n=== Key Points ===")
    print("1. Dynamic branching creates paths based on runtime conditions")
    print("2. All branches execute independently (potentially in parallel)")
    print("3. Merge strategies determine how to combine branch results")
    print("4. Synchronization points wait for all branches before merging")
    print("5. Conditional merges allow selective result combination")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

