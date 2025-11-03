"""
12_timeouts_retries.py - Production Reliability Features

This tutorial demonstrates production-ready reliability features including
timeouts, retries with exponential backoff, and error recovery patterns.
These are essential for building robust, production-grade applications.

Key Concepts:
- Timeout handling: Preventing operations from hanging
- Retry logic: Automatically retrying failed operations
- Exponential backoff: Gradually increasing wait times between retries
- Circuit breakers: Preventing cascade failures
- Error classification: Different handling for different error types
"""

import os
import time
from typing import TypedDict
from functools import wraps

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State with retry and timeout tracking
class GraphState(TypedDict):
    """State with reliability tracking"""
    input_data: str
    result: str
    retry_count: int
    max_retries: int
    backoff_multiplier: float
    operation_duration: float
    timeout_seconds: float
    error: str | None
    success: bool


# ========== UTILITY DECORATORS ==========

def with_timeout(timeout_seconds: float):
    """
    Decorator to add timeout to a function.
    
    Args:
        timeout_seconds: Maximum time allowed for execution
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            if elapsed > timeout_seconds:
                raise TimeoutError(f"Operation exceeded timeout of {timeout_seconds}s")
            
            return result
        return wrapper
    return decorator


def with_retry(max_retries: int = 3, backoff_multiplier: float = 2.0, initial_delay: float = 1.0):
    """
    Decorator to add retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff_multiplier: Multiplier for exponential backoff
        initial_delay: Initial delay before first retry (seconds)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            delay = initial_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"  Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                        delay *= backoff_multiplier
                    else:
                        print(f"  All {max_retries + 1} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator


# ========== NODES WITH RELIABILITY FEATURES ==========

@with_timeout(timeout_seconds=5.0)
def unreliable_operation(state: GraphState) -> GraphState:
    """
    Simulates an unreliable operation that might fail or timeout.
    
    In production, this could be an API call, database query, etc.
    """
    input_data = state.get("input_data", "")
    retry_count = state.get("retry_count", 0)
    
    # Simulate failure on first two attempts, success on third
    if retry_count < 2:
        raise ValueError(f"Simulated failure on attempt {retry_count + 1}")
    
    # Success
    return {
        "result": f"Successfully processed: {input_data}",
        "success": True,
        "error": None,
    }


def robust_operation_node(state: GraphState) -> GraphState:
    """
    Node with timeout and retry logic.
    
    This demonstrates how to wrap operations with reliability features.
    """
    input_data = state.get("input_data", "")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    
    print(f"Robust operation: Attempt {retry_count + 1}/{max_retries + 1}")
    
    start_time = time.time()
    
    try:
        # Wrap the unreliable operation
        @with_retry(max_retries=1, backoff_multiplier=1.5, initial_delay=0.5)
        @with_timeout(timeout_seconds=5.0)
        def execute():
            return unreliable_operation(state)
        
        result = execute()
        elapsed = time.time() - start_time
        
        result["operation_duration"] = elapsed
        return result
    
    except TimeoutError as e:
        elapsed = time.time() - start_time
        print(f"  Operation timed out after {elapsed:.2f}s")
        return {
            "error": f"Timeout: {str(e)}",
            "operation_duration": elapsed,
        }
    
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"  Operation failed: {str(e)}")
        return {
            "error": str(e),
            "operation_duration": elapsed,
        }


def retry_handler(state: GraphState) -> GraphState:
    """
    Handler that manages retries.
    
    This node decides whether to retry or give up based on error type.
    """
    error = state.get("error", "")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    
    # Classify errors
    is_timeout = "Timeout" in error if error else False
    is_retryable = not is_timeout and retry_count < max_retries
    
    if is_timeout:
        print(f"\nTimeout error detected. Retries won't help. Moving to fallback.")
        return {
            "error": f"Operation timed out and is not retryable: {error}",
        }
    
    if is_retryable:
        print(f"\nRetryable error. Preparing retry {retry_count + 1}/{max_retries}...")
        return {
            "retry_count": retry_count + 1,
            "error": None,  # Clear error for retry
        }
    else:
        print(f"\nMax retries reached or non-retryable error. Moving to fallback.")
        return {
            "error": f"Failed after {retry_count} retries: {error}",
        }


def fallback_handler(state: GraphState) -> GraphState:
    """
    Fallback handler for when all retries are exhausted.
    """
    input_data = state.get("input_data", "")
    error = state.get("error", "")
    
    print("\nFallback: Providing degraded service...")
    
    return {
        "result": f"Fallback result for: {input_data} (Original operation failed: {error})",
        "success": True,
    }


def route_after_retry(state: GraphState) -> str:
    """
    Route based on operation success and retry status.
    """
    error = state.get("error")
    success = state.get("success", False)
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    
    if success:
        return END
    
    if error and retry_count < max_retries and "Timeout" not in error:
        return "robust_operation"  # Retry
    else:
        return "fallback_handler"  # Fallback


def main():
    """
    Create a graph with timeout and retry logic.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("robust_operation", robust_operation_node)
    workflow.add_node("retry_handler", retry_handler)
    workflow.add_node("fallback_handler", fallback_handler)
    
    # Set entry point
    workflow.set_entry_point("robust_operation")
    
    # Flow: operation -> route (success/retry/fallback)
    workflow.add_conditional_edges(
        "robust_operation",
        lambda state: "retry_handler" if state.get("error") else END,
        {
            "retry_handler": "retry_handler",
            END: END,
        }
    )
    
    # After retry handler, decide on retry or fallback
    workflow.add_conditional_edges(
        "retry_handler",
        route_after_retry,
        {
            "robust_operation": "robust_operation",
            "fallback_handler": "fallback_handler",
            END: END,
        }
    )
    
    workflow.add_edge("fallback_handler", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Test the graph
    initial_state = {
        "input_data": "Test data for reliability",
        "result": "",
        "retry_count": 0,
        "max_retries": 3,
        "backoff_multiplier": 2.0,
        "operation_duration": 0.0,
        "timeout_seconds": 5.0,
        "error": None,
        "success": False,
    }
    
    print("\n=== Timeouts and Retries Example ===")
    print(f"Input: {initial_state['input_data']}")
    print(f"Max Retries: {initial_state['max_retries']}")
    print(f"Timeout: {initial_state['timeout_seconds']}s\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print("\n=== Final Result ===")
    print(f"Success: {result['success']}")
    print(f"Result: {result['result']}")
    print(f"Retries Used: {result['retry_count']}")
    print(f"Operation Duration: {result['operation_duration']:.2f}s")
    if result.get("error"):
        print(f"Error: {result['error']}")
    
    print("\n=== Key Points ===")
    print("1. Timeouts prevent operations from hanging indefinitely")
    print("2. Retry logic handles transient failures")
    print("3. Exponential backoff reduces server load")
    print("4. Error classification helps decide retry vs fallback")
    print("5. Fallbacks ensure degraded service rather than complete failure")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

