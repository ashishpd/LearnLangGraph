"""
11_agent_patterns.py - Agent Workflows and Patterns

This tutorial demonstrates how to build agent workflows using LangGraph.
Agents are systems that can make decisions, use tools, and interact with
users through multiple iterations.

Key Concepts:
- ReAct pattern: Reasoning and Acting loop
- Agent loops: Iterative decision-making
- Tool use: Agents selecting and using tools
- State management: Tracking agent thoughts and actions
- Termination conditions: When to stop the agent loop
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


# State for agent workflow
class AgentState(TypedDict):
    """State for the agent workflow"""
    user_query: str
    agent_thoughts: list[str]
    agent_actions: list[str]
    tool_results: list[str]
    final_answer: str
    iteration_count: int
    max_iterations: int
    should_continue: bool


# ========== TOOLS FOR AGENT ==========

@tool
def search_web(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: Search query
        
    Returns:
        Search results (simulated)
    """
    return f"Web search results for '{query}': Found relevant information about the topic."


@tool
def calculate_math(expression: str) -> str:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: Mathematical expression
        
    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return f"Calculation result: {result}"
    except:
        return "Error: Invalid expression"


available_tools = {
    "search_web": search_web,
    "calculate_math": calculate_math,
}


# ========== AGENT NODES ==========

def agent_think(state: AgentState) -> AgentState:
    """
    Agent thinking node.
    
    In a ReAct agent, this node would use an LLM to:
    1. Analyze the current situation
    2. Decide what action to take
    3. Select a tool if needed
    """
    print("[Agent] Thinking...")
    
    user_query = state.get("user_query", "")
    iteration_count = state.get("iteration_count", 0)
    agent_thoughts = state.get("agent_thoughts", [])
    
    # Simulate agent reasoning (in production, use LLM here)
    if iteration_count == 0:
        thought = f"Initial thought: I need to answer the query '{user_query}'. Let me search for information."
        action = "search_web"
    elif iteration_count == 1:
        thought = f"Thought: I found some information. Let me process it and provide an answer."
        action = "finalize"
    else:
        thought = "Thought: I have enough information. I should provide the final answer."
        action = "finalize"
    
    agent_thoughts.append(thought)
    
    print(f"  {thought}")
    
    return {
        "agent_thoughts": agent_thoughts,
        "agent_actions": state.get("agent_actions", []) + [action],
        "iteration_count": iteration_count + 1,
    }


def agent_act(state: AgentState) -> AgentState:
    """
    Agent action node.
    
    This node executes the action decided by the think node.
    It can use tools or perform other actions.
    """
    print("[Agent] Acting...")
    
    agent_actions = state.get("agent_actions", [])
    if not agent_actions:
        return state
    
    last_action = agent_actions[-1]
    user_query = state.get("user_query", "")
    tool_results = state.get("tool_results", [])
    
    if last_action == "search_web":
        # Execute tool
        print(f"  Executing tool: {last_action}")
        tool_func = available_tools.get("search_web")
        result = tool_func.invoke({"query": user_query})
        tool_results.append(result)
        print(f"  Tool result: {result}")
    
    elif last_action == "finalize":
        # Prepare final answer
        print("  Preparing final answer...")
        tool_results.append("Finalizing answer based on collected information")
    
    return {
        "tool_results": tool_results,
    }


def agent_respond(state: AgentState) -> AgentState:
    """
    Agent response node.
    
    This node generates the final response based on all thoughts and actions.
    In production, this would use an LLM to synthesize the information.
    """
    print("[Agent] Generating response...")
    
    user_query = state.get("user_query", "")
    agent_thoughts = state.get("agent_thoughts", [])
    tool_results = state.get("tool_results", [])
    
    # Synthesize final answer (in production, use LLM)
    final_answer = f"Based on my analysis:\n"
    final_answer += f"Query: {user_query}\n"
    final_answer += f"Thoughts: {'; '.join(agent_thoughts)}\n"
    final_answer += f"Findings: {'; '.join(tool_results)}\n"
    final_answer += "Final Answer: I've gathered the necessary information to address your query."
    
    print("  Response generated")
    
    return {
        "final_answer": final_answer,
    }


def should_continue(state: AgentState) -> str:
    """
    Determine if the agent should continue or finish.
    
    This implements the termination condition for the agent loop.
    """
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    agent_actions = state.get("agent_actions", [])
    
    # Check if max iterations reached
    if iteration_count >= max_iterations:
        print("[Agent] Max iterations reached. Stopping.")
        return "respond"
    
    # Check if agent decided to finalize
    if agent_actions and agent_actions[-1] == "finalize":
        print("[Agent] Agent decided to finalize. Stopping.")
        return "respond"
    
    # Continue the loop
    print("[Agent] Continuing agent loop...")
    return "think"


def main():
    """
    Create an agent workflow with ReAct pattern.
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes for the agent loop
    workflow.add_node("think", agent_think)
    workflow.add_node("act", agent_act)
    workflow.add_node("respond", agent_respond)
    
    # Set entry point
    workflow.set_entry_point("think")
    
    # Define the ReAct loop:
    # think -> act -> decide (continue or respond)
    workflow.add_edge("think", "act")
    
    workflow.add_conditional_edges(
        "act",
        should_continue,
        {
            "think": "think",  # Continue loop
            "respond": "respond",  # End loop
        }
    )
    
    workflow.add_edge("respond", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Test the agent
    initial_state = {
        "user_query": "What is LangGraph and how does it work?",
        "agent_thoughts": [],
        "agent_actions": [],
        "tool_results": [],
        "final_answer": "",
        "iteration_count": 0,
        "max_iterations": 3,
        "should_continue": True,
    }
    
    print("\n=== Agent Patterns Example ===")
    print(f"User Query: {initial_state['user_query']}\n")
    
    # Execute the agent
    result = app.invoke(initial_state)
    
    print("\n=== Agent Results ===")
    print(f"Iterations: {result['iteration_count']}")
    print(f"Thoughts: {len(result['agent_thoughts'])}")
    print(f"Actions: {result['agent_actions']}")
    print(f"\nFinal Answer:\n{result['final_answer']}")
    
    print("\n=== Key Points ===")
    print("1. ReAct pattern: Think -> Act -> Observe -> Think...")
    print("2. Agent loops continue until termination condition")
    print("3. Agents can use tools to gather information")
    print("4. State tracks thoughts, actions, and results")
    print("5. Termination conditions prevent infinite loops")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

