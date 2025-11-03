"""
14_graph_comparison.py - Comparing Different Graph Patterns

This tutorial demonstrates different graph patterns and when to use each.
We'll compare sequential, parallel, conditional, and hybrid approaches,
showing their strengths and use cases.

Key Concepts:
- Sequential graphs: Linear execution paths
- Parallel graphs: Simultaneous execution
- Conditional graphs: Dynamic routing
- Hybrid patterns: Combining multiple approaches
- Performance considerations: When to use which pattern
"""

import os
import time
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)


# State for comparison
class GraphState(TypedDict):
    """State for graph patterns"""
    input_data: str
    results: list[str]
    execution_time: float
    pattern_used: str


# ========== NODES ==========

def node_a(state: GraphState) -> GraphState:
    """Node A that processes data"""
    time.sleep(0.1)  # Simulate processing
    data = state.get("input_data", "")
    results = state.get("results", [])
    results.append(f"NodeA: {data}")
    return {"results": results}


def node_b(state: GraphState) -> GraphState:
    """Node B that processes data"""
    time.sleep(0.1)
    data = state.get("input_data", "")
    results = state.get("results", [])
    results.append(f"NodeB: {data}")
    return {"results": results}


def node_c(state: GraphState) -> GraphState:
    """Node C that processes data"""
    time.sleep(0.1)
    data = state.get("input_data", "")
    results = state.get("results", [])
    results.append(f"NodeC: {data}")
    return {"results": results}


# ========== PATTERN 1: SEQUENTIAL ==========

def create_sequential_graph() -> StateGraph:
    """
    Create a sequential graph: A -> B -> C
    
    Best for: Operations that depend on previous results
    """
    workflow = StateGraph(GraphState)
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    workflow.add_node("node_c", node_c)
    workflow.set_entry_point("node_a")
    workflow.add_edge("node_a", "node_b")
    workflow.add_edge("node_b", "node_c")
    workflow.add_edge("node_c", END)
    return workflow.compile()


# ========== PATTERN 2: PARALLEL ==========

def create_parallel_graph() -> StateGraph:
    """
    Create a parallel graph: A -> [B, C] (parallel)
    
    Best for: Independent operations that can run simultaneously
    """
    workflow = StateGraph(GraphState)
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    workflow.add_node("node_c", node_c)
    workflow.set_entry_point("node_a")
    
    # Route to both B and C in parallel
    def route_to_parallel(state: GraphState) -> list[str]:
        return ["node_b", "node_c"]
    
    workflow.add_conditional_edges(
        "node_a",
        route_to_parallel,
        {
            "node_b": "node_b",
            "node_c": "node_c",
        }
    )
    
    workflow.add_edge("node_b", END)
    workflow.add_edge("node_c", END)
    
    return workflow.compile()


# ========== PATTERN 3: CONDITIONAL ==========

def create_conditional_graph() -> StateGraph:
    """
    Create a conditional graph: A -> (condition) -> B or C
    
    Best for: Different paths based on data or decisions
    """
    workflow = StateGraph(GraphState)
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    workflow.add_node("node_c", node_c)
    workflow.set_entry_point("node_a")
    
    def route_conditionally(state: GraphState) -> str:
        # Simple condition: route based on input data length
        input_data = state.get("input_data", "")
        if len(input_data) % 2 == 0:
            return "node_b"
        else:
            return "node_c"
    
    workflow.add_conditional_edges(
        "node_a",
        route_conditionally,
        {
            "node_b": "node_b",
            "node_c": "node_c",
        }
    )
    
    workflow.add_edge("node_b", END)
    workflow.add_edge("node_c", END)
    
    return workflow.compile()


# ========== PATTERN 4: HYBRID ==========

def create_hybrid_graph() -> StateGraph:
    """
    Create a hybrid graph: A -> B -> (condition) -> C or D
    
    Best for: Complex workflows with both sequential and conditional elements
    """
    def node_d(state: GraphState) -> GraphState:
        time.sleep(0.1)
        data = state.get("input_data", "")
        results = state.get("results", [])
        results.append(f"NodeD: {data}")
        return {"results": results}
    
    workflow = StateGraph(GraphState)
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    workflow.add_node("node_c", node_c)
    workflow.add_node("node_d", node_d)
    
    workflow.set_entry_point("node_a")
    workflow.add_edge("node_a", "node_b")
    
    def route_after_b(state: GraphState) -> str:
        results = state.get("results", [])
        if len(results) >= 2:
            return "node_c"
        else:
            return "node_d"
    
    workflow.add_conditional_edges(
        "node_b",
        route_after_b,
        {
            "node_c": "node_c",
            "node_d": "node_d",
        }
    )
    
    workflow.add_edge("node_c", END)
    workflow.add_edge("node_d", END)
    
    return workflow.compile()


def run_graph_pattern(pattern_name: str, graph: StateGraph, input_data: str) -> dict:
    """
    Run a graph pattern and measure execution time.
    """
    initial_state = {
        "input_data": input_data,
        "results": [],
        "execution_time": 0.0,
        "pattern_used": pattern_name,
    }
    
    start_time = time.time()
    result = graph.invoke(initial_state)
    execution_time = time.time() - start_time
    
    result["execution_time"] = execution_time
    result["pattern_used"] = pattern_name
    
    return result


def main():
    """
    Compare different graph patterns.
    """
    print("\n=== Graph Pattern Comparison ===\n")
    
    # Test input
    test_input = "Test Data"
    
    # Create all graphs
    sequential_graph = create_sequential_graph()
    parallel_graph = create_parallel_graph()
    conditional_graph = create_conditional_graph()
    hybrid_graph = create_hybrid_graph()
    
    # Run and compare
    patterns = [
        ("Sequential", sequential_graph),
        ("Parallel", parallel_graph),
        ("Conditional", conditional_graph),
        ("Hybrid", hybrid_graph),
    ]
    
    results = {}
    
    for pattern_name, graph in patterns:
        print(f"--- Running {pattern_name} Pattern ---")
        result = run_graph_pattern(pattern_name, graph, test_input)
        results[pattern_name] = result
        print(f"Execution Time: {result['execution_time']:.3f}s")
        print(f"Results: {result['results']}\n")
    
    # Comparison summary
    print("\n=== Pattern Comparison Summary ===")
    print("\n1. SEQUENTIAL PATTERN:")
    print("   - Pros: Simple, predictable, dependencies handled naturally")
    print("   - Cons: Slower for independent operations")
    print("   - Use When: Operations depend on previous results")
    print(f"   - Performance: {results['Sequential']['execution_time']:.3f}s")
    
    print("\n2. PARALLEL PATTERN:")
    print("   - Pros: Faster for independent operations, efficient resource use")
    print("   - Cons: More complex, requires synchronization")
    print("   - Use When: Operations are independent and can run simultaneously")
    print(f"   - Performance: {results['Parallel']['execution_time']:.3f}s")
    
    print("\n3. CONDITIONAL PATTERN:")
    print("   - Pros: Flexible, only runs necessary paths")
    print("   - Cons: Can be harder to debug, path selection logic needed")
    print("   - Use When: Different processing needed based on data/conditions")
    print(f"   - Performance: {results['Conditional']['execution_time']:.3f}s")
    
    print("\n4. HYBRID PATTERN:")
    print("   - Pros: Best of multiple approaches, handles complex workflows")
    print("   - Cons: Most complex, harder to understand")
    print("   - Use When: Workflow requires both sequential and conditional logic")
    print(f"   - Performance: {results['Hybrid']['execution_time']:.3f}s")
    
    print("\n=== Key Takeaways ===")
    print("1. Choose pattern based on operation dependencies")
    print("2. Parallel patterns are faster but require independent operations")
    print("3. Sequential patterns are simpler but may be slower")
    print("4. Conditional patterns optimize for specific use cases")
    print("5. Hybrid patterns handle complex real-world scenarios")
    print("\n=== Comparison Complete ===")


if __name__ == "__main__":
    main()

