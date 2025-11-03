"""
06_error_handling.py - Error Handling and Recovery

This tutorial demonstrates how to handle errors in LangGraph workflows.
Error handling is crucial for production applications to ensure robustness
and provide graceful degradation.

Key Concepts:
- Try-except blocks in nodes
- Error state tracking
- Fallback paths
- Recovery mechanisms
- Retry logic
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


# State that tracks errors and retry attempts
class GraphState(TypedDict):
    """State with error tracking"""
    input_data: str
    result: str
    error: str | None
    retry_count: int
    max_retries: int
    success: bool


def risky_operation(state: GraphState) -> GraphState:
    """
    A node that might fail.
    
    This simulates an operation that can fail (like API calls, file operations, etc.)
    """
    input_data = state.get("input_data", "")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    
    print(f"Risky operation: Attempt {retry_count + 1}/{max_retries + 1}")
    
    # Simulate failure on first attempt, success on retry
    if retry_count == 0:
        raise ValueError(f"Simulated error processing: {input_data}")
    
    # Success on retry
    return {
        "result": f"Successfully processed: {input_data}",
        "success": True,
        "error": None,
    }


def error_handler(state: GraphState) -> GraphState:
    """
    Node that handles errors and prepares for retry.
    
    This node is called when an error occurs. It can log the error,
    update state, and prepare for retry or fallback.
    """
    error = state.get("error", "Unknown error")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    
    print(f"\nError Handler: {error}")
    print(f"Retry count: {retry_count}/{max_retries}")
    
    # Check if we should retry
    if retry_count < max_retries:
        print("Preparing for retry...")
        return {
            "retry_count": retry_count + 1,
            "error": None,  # Clear error for retry
        }
    else:
        print("Max retries reached. Moving to fallback.")
        return {
            "error": f"Failed after {max_retries} retries: {error}",
        }


def fallback_handler(state: GraphState) -> GraphState:
    """
    Fallback handler when all retries fail.
    
    This provides a graceful degradation path when primary operations fail.
    """
    input_data = state.get("input_data", "")
    error = state.get("error", "Unknown error")
    
    print(f"\nFallback Handler: Using fallback processing")
    print(f"Original error: {error}")
    
    # Provide a fallback result
    return {
        "result": f"Fallback result for: {input_data} (Original operation failed)",
        "success": True,  # Still mark as success since we have a result
    }


def safe_operation_node(state: GraphState) -> GraphState:
    """
    A wrapper that catches errors from risky operations.
    
    This demonstrates error handling at the node level.
    """
    input_data = state.get("input_data", "")
    retry_count = state.get("retry_count", 0)
    
    try:
        # Attempt the risky operation
        result = risky_operation(state)
        return result
    
    except Exception as e:
        # Catch and handle the error
        error_message = str(e)
        print(f"\nCaught error in safe_operation_node: {error_message}")
        
        return {
            "error": error_message,
            "retry_count": retry_count,
        }


def route_after_error_handling(state: GraphState) -> str:
    """
    Route based on error state.
    
    If there's an error and retries exhausted, go to fallback.
    Otherwise, retry the operation.
    """
    error = state.get("error")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    
    if error and retry_count >= max_retries:
        return "fallback_handler"
    elif error:
        return "safe_operation_node"  # Retry
    else:
        return END  # Success


def main():
    """
    Create a graph with error handling.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("safe_operation", safe_operation_node)
    workflow.add_node("error_handler", error_handler)
    workflow.add_node("fallback_handler", fallback_handler)
    
    # Set entry point
    workflow.set_entry_point("safe_operation")
    
    # After safe operation, route based on success/failure
    workflow.add_conditional_edges(
        "safe_operation",
        lambda state: "error_handler" if state.get("error") else END,
        {
            "error_handler": "error_handler",
            END: END,
        }
    )
    
    # After error handling, decide on retry or fallback
    workflow.add_conditional_edges(
        "error_handler",
        route_after_error_handling,
        {
            "safe_operation": "safe_operation",
            "fallback_handler": "fallback_handler",
            END: END,
        }
    )
    
    # Fallback leads to END
    workflow.add_edge("fallback_handler", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Test with initial failure
    initial_state = {
        "input_data": "Test data",
        "result": "",
        "error": None,
        "retry_count": 0,
        "max_retries": 3,
        "success": False,
    }
    
    print("\n=== Error Handling Example ===")
    print(f"Input: {initial_state['input_data']}")
    print(f"Max Retries: {initial_state['max_retries']}\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print("\n=== Final Result ===")
    print(f"Success: {result['success']}")
    print(f"Result: {result['result']}")
    print(f"Final Retry Count: {result['retry_count']}")
    if result.get("error"):
        print(f"Final Error: {result['error']}")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

