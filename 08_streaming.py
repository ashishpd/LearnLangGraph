"""
08_streaming.py - Streaming Responses and Real-time Updates

This tutorial demonstrates how to stream responses from LangGraph workflows.
Streaming is essential for providing real-time feedback to users, especially
for long-running operations or LLM-based workflows.

Key Concepts:
- Stream events: Real-time updates from graph execution
- Async streaming: Using async/await for streaming
- Event types: Different types of events (node start, node end, etc.)
- Consumer patterns: How to consume and process streamed events
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


# State for streaming example
class GraphState(TypedDict):
    """State that gets updated during streaming"""
    input_message: str
    processed_message: str
    steps_completed: list[str]
    final_result: str


def node_a(state: GraphState) -> GraphState:
    """
    First processing node.
    
    This node processes the input and updates state.
    The execution of this node will be streamed.
    """
    print("[Node A] Starting processing...")
    input_message = state.get("input_message", "")
    
    import time
    time.sleep(0.5)  # Simulate processing time
    
    processed = f"NodeA processed: {input_message.upper()}"
    steps = state.get("steps_completed", [])
    steps.append("node_a")
    
    print("[Node A] Completed")
    return {
        "processed_message": processed,
        "steps_completed": steps,
    }


def node_b(state: GraphState) -> GraphState:
    """
    Second processing node.
    """
    print("[Node B] Starting processing...")
    processed_message = state.get("processed_message", "")
    
    import time
    time.sleep(0.5)  # Simulate processing time
    
    result = f"{processed_message} -> NodeB enhanced"
    steps = state.get("steps_completed", [])
    steps.append("node_b")
    
    print("[Node B] Completed")
    return {
        "processed_message": result,
        "steps_completed": steps,
    }


def node_c(state: GraphState) -> GraphState:
    """
    Final processing node.
    """
    print("[Node C] Starting processing...")
    processed_message = state.get("processed_message", "")
    
    import time
    time.sleep(0.5)  # Simulate processing time
    
    final = f"{processed_message} -> NodeC finalized"
    steps = state.get("steps_completed", [])
    steps.append("node_c")
    
    print("[Node C] Completed")
    return {
        "final_result": final,
        "steps_completed": steps,
    }


def main():
    """
    Demonstrate streaming from a LangGraph workflow.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    workflow.add_node("node_c", node_c)
    
    # Set entry point
    workflow.set_entry_point("node_a")
    
    # Define flow
    workflow.add_edge("node_a", "node_b")
    workflow.add_edge("node_b", "node_c")
    workflow.add_edge("node_c", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Initial state
    initial_state = {
        "input_message": "Hello Streaming",
        "processed_message": "",
        "steps_completed": [],
        "final_result": "",
    }
    
    print("\n=== Streaming Example ===")
    print(f"Input: {initial_state['input_message']}\n")
    
    # Stream the execution
    # The stream() method yields events as they occur
    print("--- Streaming Events ---\n")
    
    for event in app.stream(initial_state):
        # Each event is a tuple: (node_name, event_data)
        for node_name, event_data in event.items():
            event_type = event_data.get("event") if isinstance(event_data, dict) else "unknown"
            
            if event_type == "on_chain_start":
                print(f"→ Event: Node '{node_name}' started")
            elif event_type == "on_chain_end":
                print(f"✓ Event: Node '{node_name}' completed")
                
                # Access the state if available
                if isinstance(event_data, dict) and "data" in event_data:
                    state_update = event_data["data"]
                    if "steps_completed" in state_update:
                        print(f"  Steps completed so far: {state_update['steps_completed']}")
    
    print("\n--- Final Invocation ---")
    # Get the final state
    final_result = app.invoke(initial_state)
    
    print("\n=== Final Result ===")
    print(f"Final Result: {final_result['final_result']}")
    print(f"All Steps: {final_result['steps_completed']}")
    
    print("\n=== Async Streaming Example ===")
    print("(Demonstrating async streaming pattern)\n")
    
    async def async_stream_example():
        """
        Example of async streaming for better performance.
        """
        async for event in app.astream(initial_state):
            for node_name, event_data in event.items():
                print(f"Async Event: {node_name} - {type(event_data).__name__}")
    
    # Uncomment to run async example:
    # asyncio.run(async_stream_example())
    
    print("\n=== Key Points ===")
    print("1. stream() yields events in real-time as nodes execute")
    print("2. Events include node starts, ends, and state updates")
    print("3. Use astream() for async streaming (better for web apps)")
    print("4. Streaming enables progress bars, real-time UI updates, etc.")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

