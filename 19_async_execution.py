"""
19_async_execution.py - Async and Concurrent Execution

This tutorial demonstrates how to use async/await patterns in LangGraph
for better performance and concurrency. Async execution is essential for
I/O-bound operations, API calls, and handling multiple requests.

Key Concepts:
- Async nodes: Nodes that use async/await
- Concurrent execution: Running multiple operations simultaneously
- Async state updates: Non-blocking state modifications
- Performance optimization: When and how to use async
- Async streaming: Streaming with async patterns
"""

import os
import asyncio
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State for async execution
class AsyncState(TypedDict):
    """State for async workflow"""
    input_data: str
    async_results: list[str]
    processing_times: dict[str, float]
    concurrent_tasks: int
    completed_tasks: int


# ========== ASYNC HELPER FUNCTIONS ==========

async def simulate_api_call(name: str, delay: float) -> str:
    """
    Simulate an async API call.
    
    In production, this would be an actual HTTP request or database query.
    """
    await asyncio.sleep(delay)  # Simulate network latency
    return f"{name}: API call completed in {delay}s"


async def simulate_database_query(query: str, delay: float) -> str:
    """
    Simulate an async database query.
    """
    await asyncio.sleep(delay)
    return f"Database query '{query}' completed in {delay}s"


async def simulate_file_operation(filename: str, delay: float) -> str:
    """
    Simulate an async file operation.
    """
    await asyncio.sleep(delay)
    return f"File operation '{filename}' completed in {delay}s"


# ========== ASYNC NODES ==========

async def async_node_a(state: AsyncState) -> AsyncState:
    """
    Async node that performs I/O operations.
    
    This node demonstrates async/await for non-blocking operations.
    """
    print("[Async Node A] Starting async operation...")
    
    input_data = state.get("input_data", "")
    async_results = state.get("async_results", [])
    processing_times = state.get("processing_times", {})
    
    import time
    start_time = time.time()
    
    # Perform async API call
    result = await simulate_api_call("NodeA", 0.5)
    
    elapsed = time.time() - start_time
    processing_times["node_a"] = elapsed
    
    async_results.append(result)
    
    print(f"[Async Node A] Completed in {elapsed:.2f}s")
    
    return {
        "async_results": async_results,
        "processing_times": processing_times,
    }


async def async_node_b(state: AsyncState) -> AsyncState:
    """
    Another async node.
    """
    print("[Async Node B] Starting async operation...")
    
    async_results = state.get("async_results", [])
    processing_times = state.get("processing_times", {})
    
    import time
    start_time = time.time()
    
    # Perform async database query
    result = await simulate_database_query("SELECT * FROM users", 0.3)
    
    elapsed = time.time() - start_time
    processing_times["node_b"] = elapsed
    
    async_results.append(result)
    
    print(f"[Async Node B] Completed in {elapsed:.2f}s")
    
    return {
        "async_results": async_results,
        "processing_times": processing_times,
    }


async def async_node_c(state: AsyncState) -> AsyncState:
    """
    Another async node.
    """
    print("[Async Node C] Starting async operation...")
    
    async_results = state.get("async_results", [])
    processing_times = state.get("processing_times", {})
    
    import time
    start_time = time.time()
    
    # Perform async file operation
    result = await simulate_file_operation("data.txt", 0.2)
    
    elapsed = time.time() - start_time
    processing_times["node_c"] = elapsed
    
    async_results.append(result)
    
    print(f"[Async Node C] Completed in {elapsed:.2f}s")
    
    return {
        "async_results": async_results,
        "processing_times": processing_times,
    }


async def concurrent_operations_node(state: AsyncState) -> AsyncState:
    """
    Node that runs multiple async operations concurrently.
    
    This demonstrates how to run multiple async operations in parallel.
    """
    print("[Concurrent Node] Starting concurrent operations...")
    
    async_results = state.get("async_results", [])
    processing_times = state.get("processing_times", {})
    
    import time
    start_time = time.time()
    
    # Run multiple async operations concurrently
    # asyncio.gather() runs them in parallel and waits for all to complete
    results = await asyncio.gather(
        simulate_api_call("Concurrent-1", 0.4),
        simulate_database_query("SELECT * FROM orders", 0.3),
        simulate_file_operation("output.txt", 0.2),
    )
    
    elapsed = time.time() - start_time
    processing_times["concurrent_operations"] = elapsed
    
    async_results.extend(results)
    
    print(f"[Concurrent Node] All operations completed in {elapsed:.2f}s (would be ~0.9s sequentially)")
    
    return {
        "async_results": async_results,
        "processing_times": processing_times,
        "completed_tasks": state.get("completed_tasks", 0) + len(results),
    }


def main():
    """
    Demonstrate async execution patterns.
    """
    # Note: LangGraph supports async nodes, but the graph execution
    # might need to be wrapped in async context
    
    # For this example, we'll demonstrate the concepts
    # In production, use astream() or ainvoke() for async execution
    
    print("\n=== Async Execution Example ===\n")
    
    # Demonstrate async operations
    async def run_async_example():
        """Run async operations"""
        state = {
            "input_data": "Test data",
            "async_results": [],
            "processing_times": {},
            "concurrent_tasks": 0,
            "completed_tasks": 0,
        }
        
        print("--- Running Async Nodes Sequentially ---\n")
        state = await async_node_a(state)
        state = await async_node_b(state)
        state = await async_node_c(state)
        
        print("\n--- Running Concurrent Operations ---\n")
        state = await concurrent_operations_node(state)
        
        print("\n=== Results ===")
        print(f"Total Results: {len(state['async_results'])}")
        print(f"Processing Times: {state['processing_times']}")
        print(f"Total Time: {sum(state['processing_times'].values()):.2f}s")
        print("\nResults:")
        for i, result in enumerate(state['async_results'], 1):
            print(f"  {i}. {result}")
        
        return state
    
    # Run the async example
    final_state = asyncio.run(run_async_example())
    
    print("\n=== Key Points ===")
    print("1. Async nodes use async/await for non-blocking I/O")
    print("2. asyncio.gather() runs operations concurrently")
    print("3. Concurrent execution is faster than sequential")
    print("4. Use async for API calls, database queries, file I/O")
    print("5. LangGraph supports async with astream() and ainvoke()")
    print("6. Async is essential for handling multiple requests efficiently")
    
    print("\n=== Performance Comparison ===")
    sequential_time = sum([
        final_state['processing_times'].get('node_a', 0),
        final_state['processing_times'].get('node_b', 0),
        final_state['processing_times'].get('node_c', 0),
    ])
    concurrent_time = final_state['processing_times'].get('concurrent_operations', 0)
    
    print(f"Sequential execution: ~{sequential_time:.2f}s")
    print(f"Concurrent execution: {concurrent_time:.2f}s")
    print(f"Speedup: {sequential_time/concurrent_time:.2f}x faster")
    
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

