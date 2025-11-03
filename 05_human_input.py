"""
05_human_input.py - Human-in-the-Loop Workflows

This tutorial demonstrates how to add human input/intervention points in
LangGraph workflows. Human-in-the-loop is crucial for workflows that need
approval, feedback, or decision-making from users.

Key Concepts:
- Human nodes: Special nodes that pause execution for user input
- Interrupts: Points where the graph pauses and waits
- Resuming: Continuing execution after receiving input
- Async execution: Human input nodes typically work better with async
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


# State that includes human input
class GraphState(TypedDict):
    """State that includes human feedback"""
    user_query: str
    ai_response: str
    human_feedback: str
    approved: bool
    iterations: int


def process_query(state: GraphState) -> GraphState:
    """
    Process the initial user query.
    
    In a real application, this might call an LLM or process the query.
    """
    print("Processing user query...")
    user_query = state.get("user_query", "")
    
    # Simulate AI processing (in real app, call LLM here)
    ai_response = f"AI Response to: {user_query}"
    
    return {
        "user_query": user_query,
        "ai_response": ai_response,
        "iterations": 1,
    }


def get_human_feedback(state: GraphState) -> GraphState:
    """
    Get human feedback on the AI response.
    
    This function simulates getting human input. In a real application,
    this would pause and wait for actual user input.
    
    Note: This is a simulation. In production, you'd use:
    - Streamlit/Web interface
    - API endpoints that wait for POST requests
    - Message queues
    """
    print("\n--- HUMAN INPUT REQUIRED ---")
    print(f"AI Response: {state.get('ai_response', '')}")
    
    # Simulate human input (in real app, wait for actual input)
    # For demo purposes, we'll simulate different scenarios
    simulated_feedback = "needs_revision"  # Could be "approved" or "needs_revision"
    
    print(f"Simulated Human Feedback: {simulated_feedback}")
    print("--- INPUT RECEIVED ---\n")
    
    return {
        "human_feedback": simulated_feedback,
        "approved": simulated_feedback == "approved",
    }


def revise_response(state: GraphState) -> GraphState:
    """
    Revise the response based on human feedback.
    
    This node runs when human feedback indicates revision is needed.
    """
    print("Revising response based on feedback...")
    
    user_query = state.get("user_query", "")
    human_feedback = state.get("human_feedback", "")
    iterations = state.get("iterations", 0)
    
    # Simulate revised response
    new_response = f"Revised Response (iteration {iterations + 1}): {user_query} [Incorporating: {human_feedback}]"
    
    return {
        "ai_response": new_response,
        "iterations": iterations + 1,
    }


def route_after_feedback(state: GraphState) -> str:
    """
    Route based on human feedback.
    
    If approved, end the workflow. Otherwise, continue to revision.
    """
    approved = state.get("approved", False)
    
    if approved:
        print("Feedback: Approved -> Ending workflow")
        return END
    else:
        print("Feedback: Needs revision -> Revising")
        return "revise_response"


def main():
    """
    Create a graph with human input points.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("process_query", process_query)
    workflow.add_node("get_feedback", get_human_feedback)
    workflow.add_node("revise_response", revise_response)
    
    # Set entry point
    workflow.set_entry_point("process_query")
    
    # Flow: process -> get feedback -> route
    workflow.add_edge("process_query", "get_feedback")
    
    # Conditional routing based on feedback
    workflow.add_conditional_edges(
        "get_feedback",
        route_after_feedback,
        {
            "revise_response": "revise_response",
            END: END,
        }
    )
    
    # If revision is needed, loop back to get feedback again
    workflow.add_edge("revise_response", "get_feedback")
    
    # Use MemorySaver for checkpoints (enables resuming after interrupts)
    # In production, use persistent storage like SQLite
    memory = MemorySaver()
    
    # Compile with checkpointer for human input support
    app = workflow.compile(checkpointer=memory)
    
    # Create initial state
    initial_state = {
        "user_query": "What is LangGraph?",
        "ai_response": "",
        "human_feedback": "",
        "approved": False,
        "iterations": 0,
    }
    
    print("\n=== Human-in-the-Loop Example ===")
    print(f"User Query: {initial_state['user_query']}\n")
    
    # Note: In a real application, human input would pause execution
    # Here we simulate with multiple invocations
    config = {"configurable": {"thread_id": "demo-thread-1"}}
    
    # First iteration: process and get feedback
    print("=== Iteration 1 ===")
    state1 = app.invoke(initial_state, config=config)
    print(f"State after feedback: Approved={state1.get('approved')}\n")
    
    # If not approved, simulate another iteration
    # In real app, this would wait for human input before continuing
    if not state1.get("approved"):
        print("=== Iteration 2 (Simulated) ===")
        # Update feedback to approved for demo
        state_with_approval = app.update_state(
            config=config,
            values={"human_feedback": "approved", "approved": True}
        )
        print("Human approved the response")
    
    print("\n=== Workflow Complete ===")
    print("\nNote: In production, human input nodes would:")
    print("  1. Pause execution at the human input node")
    print("  2. Wait for actual user input (via API, UI, etc.)")
    print("  3. Resume execution when input is received")
    print("  4. Use persistent checkpoints to save/restore state")


if __name__ == "__main__":
    main()

