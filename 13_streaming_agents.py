"""
13_streaming_agents.py - Streaming Agent Responses

This tutorial demonstrates how to stream agent responses in real-time.
This provides a better user experience by showing agent thoughts and
actions as they happen, rather than waiting for the final result.

Key Concepts:
- Streaming agent thoughts: Real-time thought process updates
- Streaming tool execution: Showing tools as they're executed
- Progressive response building: Building the response incrementally
- Event handling: Processing different types of stream events
"""

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State for streaming agent
class AgentState(TypedDict):
    """State for streaming agent"""
    user_query: str
    agent_thought: str
    tool_name: str
    tool_input: str
    tool_output: str
    partial_response: str
    final_response: str
    iteration: int
    max_iterations: int


# ========== TOOLS ==========

@tool
def get_user_info(user_id: str) -> str:
    """Get user information by ID"""
    return f"User {user_id}: John Doe, email: john@example.com"


@tool
def get_order_info(order_id: str) -> str:
    """Get order information by ID"""
    return f"Order {order_id}: Status: Shipped, Total: $99.99"


available_tools = {
    "get_user_info": get_user_info,
    "get_order_info": get_order_info,
}


# ========== STREAMING AGENT NODES ==========

def agent_think_streaming(state: AgentState) -> AgentState:
    """
    Agent thinking node that updates state progressively.
    
    In a streaming scenario, this would emit thought chunks as they're generated.
    """
    print("\n[Agent Thinking...]", end="", flush=True)
    
    user_query = state.get("user_query", "")
    iteration = state.get("iteration", 0)
    
    # Simulate progressive thinking (in production, stream from LLM)
    thoughts = [
        f"Analyzing query: {user_query}",
        "Determining required information",
        "Selecting appropriate tools",
    ]
    
    if iteration < len(thoughts):
        thought = thoughts[iteration]
        print(f" {thought}", end="", flush=True)
    else:
        thought = "Ready to take action"
        print(f" {thought}", end="", flush=True)
    
    return {
        "agent_thought": thought,
        "iteration": iteration + 1,
    }


def agent_act_streaming(state: AgentState) -> AgentState:
    """
    Agent action node that executes tools and streams updates.
    """
    agent_thought = state.get("agent_thought", "")
    user_query = state.get("user_query", "").lower()
    
    # Determine which tool to use (simplified)
    if "user" in agent_thought.lower() or "user_id" in user_query:
        tool_name = "get_user_info"
        tool_input = {"user_id": "12345"}
    elif "order" in agent_thought.lower() or "order_id" in user_query:
        tool_name = "get_order_info"
        tool_input = {"order_id": "ORD-001"}
    else:
        tool_name = "get_user_info"
        tool_input = {"user_id": "12345"}
    
    print(f"\n[Agent Acting] Using tool: {tool_name}")
    print(f"  Tool input: {tool_input}", end="", flush=True)
    
    # Execute tool
    tool_func = available_tools.get(tool_name)
    tool_output = tool_func.invoke(tool_input)
    
    print(f"\n  Tool output: {tool_output}")
    
    return {
        "tool_name": tool_name,
        "tool_input": str(tool_input),
        "tool_output": tool_output,
    }


def agent_respond_streaming(state: AgentState) -> AgentState:
    """
    Agent response node that builds response progressively.
    """
    print("\n[Agent Responding]", end="", flush=True)
    
    user_query = state.get("user_query", "")
    agent_thought = state.get("agent_thought", "")
    tool_name = state.get("tool_name", "")
    tool_output = state.get("tool_output", "")
    partial_response = state.get("partial_response", "")
    
    # Build response incrementally
    response_chunks = [
        f"Based on my analysis of '{user_query}',",
        f" I used the {tool_name} tool",
        f" and found: {tool_output}",
        " This answers your question.",
    ]
    
    # In production, this would stream from LLM
    new_chunk = response_chunks[len(partial_response.split(" ")) // 3] if partial_response else response_chunks[0]
    new_partial = partial_response + " " + new_chunk if partial_response else new_chunk
    
    print(f" {new_chunk}", end="", flush=True)
    
    # Check if response is complete
    is_complete = len(partial_response.split(" ")) >= len(" ".join(response_chunks).split(" ")) - 2
    
    if is_complete:
        final_response = " ".join(response_chunks)
        print("\n[Response Complete]")
    else:
        final_response = ""
    
    return {
        "partial_response": new_partial,
        "final_response": final_response if is_complete else "",
    }


def should_continue_streaming(state: AgentState) -> str:
    """
    Determine if agent should continue or finish.
    """
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 3)
    final_response = state.get("final_response", "")
    
    if final_response:
        return "end"
    
    if iteration >= max_iterations:
        return "respond"
    
    return "think"


def main():
    """
    Create a streaming agent workflow.
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("think", agent_think_streaming)
    workflow.add_node("act", agent_act_streaming)
    workflow.add_node("respond", agent_respond_streaming)
    
    # Set entry point
    workflow.set_entry_point("think")
    
    # Define flow
    workflow.add_edge("think", "act")
    
    workflow.add_conditional_edges(
        "act",
        should_continue_streaming,
        {
            "think": "think",
            "respond": "respond",
        }
    )
    
    workflow.add_conditional_edges(
        "respond",
        should_continue_streaming,
        {
            "think": "think",
            "end": END,
        }
    )
    
    # Compile the graph
    app = workflow.compile()
    
    # Test with streaming
    initial_state = {
        "user_query": "What is the status of order ORD-001?",
        "agent_thought": "",
        "tool_name": "",
        "tool_input": "",
        "tool_output": "",
        "partial_response": "",
        "final_response": "",
        "iteration": 0,
        "max_iterations": 3,
    }
    
    print("\n=== Streaming Agent Example ===")
    print(f"User Query: {initial_state['user_query']}\n")
    
    # Stream the execution
    print("--- Streaming Agent Execution ---\n")
    
    for event in app.stream(initial_state):
        for node_name, event_data in event.items():
            # Process different event types
            if node_name == "think":
                print("✓ Thought completed")
            elif node_name == "act":
                print("✓ Action completed")
            elif node_name == "respond":
                print("✓ Response chunk completed")
    
    print("\n--- Getting Final State ---")
    final_result = app.invoke(initial_state)
    
    print("\n=== Final Result ===")
    print(f"Final Response: {final_result.get('final_response', final_result.get('partial_response', ''))}")
    
    print("\n=== Key Points ===")
    print("1. Stream events provide real-time updates during execution")
    print("2. Users see agent thoughts and actions as they happen")
    print("3. Progressive response building improves UX")
    print("4. Streaming is essential for long-running agent operations")
    print("5. Use astream() for async streaming in web applications")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

