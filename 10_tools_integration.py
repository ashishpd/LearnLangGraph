"""
10_tools_integration.py - Tools and Function Calling

This tutorial demonstrates how to integrate LangChain tools into LangGraph
workflows. Tools enable your graphs to interact with external systems, APIs,
databases, and perform various operations beyond LLM calls.

Key Concepts:
- LangChain tools: Reusable tools for various operations
- Tool execution nodes: Nodes that call tools
- Tool selection: Choosing which tool to use
- Tool results: Handling tool outputs in graph state
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


# State that includes tool usage
class GraphState(TypedDict):
    """State with tool integration"""
    user_query: str
    selected_tool: str
    tool_result: str
    final_answer: str
    tools_used: list[str]


# ========== DEFINE TOOLS ==========

@tool
def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2+2", "10*5")
        
    Returns:
        The result of the calculation
    """
    try:
        # Simple and safe evaluation (in production, use a proper math parser)
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {e}"


@tool
def get_weather(city: str) -> str:
    """
    Get weather information for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Weather information (simulated)
    """
    # Simulated weather data
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Cloudy, 15°C",
        "Tokyo": "Rainy, 18°C",
    }
    return weather_data.get(city, f"Weather data not available for {city}")


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search a knowledge base for information.
    
    Args:
        query: Search query
        
    Returns:
        Search results (simulated)
    """
    # Simulated search results
    return f"Knowledge base results for '{query}': Found 3 relevant documents."


# Create a list of available tools
available_tools = [calculate, get_weather, search_knowledge_base]


# ========== GRAPH NODES ==========

def analyze_query(state: GraphState) -> GraphState:
    """
    Analyze the user query to determine which tool to use.
    
    In a real application, you might use an LLM to analyze the query
    and select the appropriate tool.
    """
    print("Analyzing query to select tool...")
    user_query = state.get("user_query", "").lower()
    
    # Simple rule-based tool selection (in production, use LLM)
    if any(word in user_query for word in ["calculate", "math", "compute", "+", "*", "-", "/"]):
        selected_tool = "calculate"
    elif any(word in user_query for word in ["weather", "temperature", "forecast"]):
        selected_tool = "get_weather"
    elif any(word in user_query for word in ["search", "find", "information", "knowledge"]):
        selected_tool = "search_knowledge_base"
    else:
        selected_tool = "search_knowledge_base"  # Default
    
    print(f"Selected tool: {selected_tool}")
    
    return {
        "selected_tool": selected_tool,
    }


def execute_tool(state: GraphState) -> GraphState:
    """
    Execute the selected tool.
    
    This node calls the appropriate tool based on the selection.
    """
    selected_tool = state.get("selected_tool", "")
    user_query = state.get("user_query", "")
    tools_used = state.get("tools_used", [])
    
    print(f"Executing tool: {selected_tool}")
    
    # Find and execute the tool
    tool_result = ""
    for tool_func in available_tools:
        if tool_func.name == selected_tool:
            # Extract parameters from query (simplified)
            # In production, use LLM to extract parameters properly
            if selected_tool == "calculate":
                # Extract math expression (simplified)
                import re
                numbers = re.findall(r'\d+', user_query)
                if len(numbers) >= 2:
                    expression = f"{numbers[0]}+{numbers[1]}"
                else:
                    expression = "2+2"  # Default
                tool_result = tool_func.invoke({"expression": expression})
            
            elif selected_tool == "get_weather":
                # Extract city name (simplified)
                cities = ["New York", "London", "Tokyo"]
                city = next((c for c in cities if c.lower() in user_query.lower()), "New York")
                tool_result = tool_func.invoke({"city": city})
            
            elif selected_tool == "search_knowledge_base":
                tool_result = tool_func.invoke({"query": user_query})
            
            break
    
    tools_used.append(selected_tool)
    
    return {
        "tool_result": tool_result,
        "tools_used": tools_used,
    }


def generate_final_answer(state: GraphState) -> GraphState:
    """
    Generate the final answer using the tool result.
    
    In a real application, you'd use an LLM here to format the tool result
    into a natural language response.
    """
    print("Generating final answer...")
    user_query = state.get("user_query", "")
    tool_result = state.get("tool_result", "")
    
    # In production, use LLM to generate natural language response
    final_answer = f"Based on your query '{user_query}', here's what I found: {tool_result}"
    
    return {
        "final_answer": final_answer,
    }


def route_by_tool_selection(state: GraphState) -> str:
    """
    Route to appropriate tool execution node.
    
    This could be extended to route to different tool execution nodes
    for different tool types.
    """
    return "execute_tool"


def main():
    """
    Create a graph with tool integration.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("analyze_query", analyze_query)
    workflow.add_node("execute_tool", execute_tool)
    workflow.add_node("generate_answer", generate_final_answer)
    
    # Set entry point
    workflow.set_entry_point("analyze_query")
    
    # Flow: analyze -> route to tool -> execute -> generate answer
    workflow.add_conditional_edges(
        "analyze_query",
        route_by_tool_selection,
        {
            "execute_tool": "execute_tool",
        }
    )
    
    workflow.add_edge("execute_tool", "generate_answer")
    workflow.add_edge("generate_answer", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Test with different queries
    test_queries = [
        "What is 5 plus 3?",
        "What's the weather in London?",
        "Search for information about LangGraph",
    ]
    
    print("\n=== Tools Integration Example ===\n")
    
    for query in test_queries:
        print(f"\n--- Query: {query} ---")
        initial_state = {
            "user_query": query,
            "selected_tool": "",
            "tool_result": "",
            "final_answer": "",
            "tools_used": [],
        }
        
        result = app.invoke(initial_state)
        print(f"Tool Used: {result['selected_tool']}")
        print(f"Final Answer: {result['final_answer']}")
    
    print("\n=== Key Points ===")
    print("1. Tools are LangChain-compatible functions")
    print("2. Tools can be called from graph nodes")
    print("3. Use LLM to select appropriate tools (tool selection)")
    print("4. Tools enable graphs to interact with external systems")
    print("5. Tool results can be used in subsequent nodes")
    print("\n=== Execution Complete ===")


if __name__ == "__main__":
    main()

