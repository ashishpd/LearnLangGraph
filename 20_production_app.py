"""
20_production_app.py - Complete Production Application

This tutorial demonstrates a complete, production-ready LangGraph application
that combines all the concepts learned in previous tutorials. This includes
error handling, logging, monitoring, checkpoints, async execution, and
best practices.

Key Concepts:
- Production architecture: How to structure a production app
- Error handling: Comprehensive error management
- Logging: Structured logging for monitoring
- Monitoring: Tracking workflow execution
- Best practices: Production-ready patterns
"""

import os
import logging
from typing import TypedDict, Annotated
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)

# ========== LOGGING SETUP ==========

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workflow.log'),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)


# ========== STATE SCHEMA ==========

class ProductionState(TypedDict):
    """
    Production-ready state schema with comprehensive tracking.
    """
    # Core data
    request_id: str
    user_input: str
    processed_data: str
    
    # Execution tracking
    start_time: str
    end_time: str | None
    execution_time: float
    
    # Status tracking
    status: str  # "pending", "processing", "completed", "failed"
    current_step: str
    
    # Error handling
    errors: list[str]
    warnings: list[str]
    
    # Monitoring
    nodes_executed: list[str]
    node_durations: dict[str, float]
    
    # Messages (with reducer)
    messages: Annotated[list[str], add_messages]
    
    # Metadata
    metadata: dict[str, str]


# ========== PRODUCTION NODES ==========

def input_validation_node(state: ProductionState) -> ProductionState:
    """
    Validate input with comprehensive error handling.
    """
    logger.info(f"[{state.get('request_id')}] Input validation started")
    
    user_input = state.get("user_input", "")
    errors = state.get("errors", [])
    warnings = state.get("warnings", [])
    nodes_executed = state.get("nodes_executed", [])
    messages = state.get("messages", [])
    
    import time
    start_time = time.time()
    
    try:
        # Validate input
        if not user_input:
            errors.append("Input is empty")
            logger.error(f"[{state.get('request_id')}] Validation failed: empty input")
            return {
                "status": "failed",
                "errors": errors,
                "messages": messages + ["Validation failed: empty input"],
            }
        
        if len(user_input) < 3:
            warnings.append("Input is very short")
            logger.warning(f"[{state.get('request_id')}] Input warning: too short")
        
        # Validation passed
        duration = time.time() - start_time
        nodes_executed.append("input_validation")
        
        logger.info(f"[{state.get('request_id')}] Input validation completed in {duration:.3f}s")
        
        return {
            "status": "processing",
            "errors": errors,
            "warnings": warnings,
            "nodes_executed": nodes_executed,
            "node_durations": state.get("node_durations", {}) | {"input_validation": duration},
            "current_step": "validated",
            "messages": messages + ["Input validated successfully"],
        }
    
    except Exception as e:
        error_msg = f"Validation error: {str(e)}"
        logger.exception(f"[{state.get('request_id')}] {error_msg}")
        errors.append(error_msg)
        return {
            "status": "failed",
            "errors": errors,
            "messages": messages + [error_msg],
        }


def processing_node(state: ProductionState) -> ProductionState:
    """
    Main processing node with error handling and monitoring.
    """
    request_id = state.get("request_id", "unknown")
    logger.info(f"[{request_id}] Processing started")
    
    user_input = state.get("user_input", "")
    nodes_executed = state.get("nodes_executed", [])
    messages = state.get("messages", [])
    
    import time
    start_time = time.time()
    
    try:
        # Simulate processing (in production, call LLM or perform operations)
        processed_data = f"Processed: {user_input.upper()}"
        
        duration = time.time() - start_time
        nodes_executed.append("processing")
        
        logger.info(f"[{request_id}] Processing completed in {duration:.3f}s")
        
        return {
            "processed_data": processed_data,
            "nodes_executed": nodes_executed,
            "node_durations": state.get("node_durations", {}) | {"processing": duration},
            "current_step": "processed",
            "messages": messages + ["Processing completed"],
        }
    
    except Exception as e:
        error_msg = f"Processing error: {str(e)}"
        logger.exception(f"[{request_id}] {error_msg}")
        return {
            "status": "failed",
            "errors": state.get("errors", []) + [error_msg],
            "messages": messages + [error_msg],
        }


def output_node(state: ProductionState) -> ProductionState:
    """
    Output node that finalizes the workflow.
    """
    request_id = state.get("request_id", "unknown")
    logger.info(f"[{request_id}] Output generation started")
    
    processed_data = state.get("processed_data", "")
    start_time_str = state.get("start_time", "")
    nodes_executed = state.get("nodes_executed", [])
    messages = state.get("messages", [])
    
    import time
    node_start = time.time()
    
    try:
        # Calculate total execution time
        if start_time_str:
            start_dt = datetime.fromisoformat(start_time_str)
            end_dt = datetime.now()
            execution_time = (end_dt - start_dt).total_seconds()
        else:
            execution_time = 0.0
        
        duration = time.time() - node_start
        nodes_executed.append("output")
        
        logger.info(f"[{request_id}] Output generation completed in {duration:.3f}s")
        
        return {
            "status": "completed",
            "end_time": datetime.now().isoformat(),
            "execution_time": execution_time,
            "nodes_executed": nodes_executed,
            "node_durations": state.get("node_durations", {}) | {"output": duration},
            "current_step": "completed",
            "messages": messages + ["Workflow completed successfully"],
        }
    
    except Exception as e:
        error_msg = f"Output error: {str(e)}"
        logger.exception(f"[{request_id}] {error_msg}")
        return {
            "status": "failed",
            "errors": state.get("errors", []) + [error_msg],
            "messages": messages + [error_msg],
        }


def error_handler_node(state: ProductionState) -> ProductionState:
    """
    Centralized error handling node.
    """
    request_id = state.get("request_id", "unknown")
    errors = state.get("errors", [])
    
    logger.error(f"[{request_id}] Error handler invoked with {len(errors)} errors")
    
    # Log all errors
    for error in errors:
        logger.error(f"[{request_id}] Error: {error}")
    
    # Prepare error summary
    error_summary = "; ".join(errors)
    
    return {
        "status": "failed",
        "end_time": datetime.now().isoformat(),
        "messages": state.get("messages", []) + [f"Workflow failed: {error_summary}"],
    }


def route_after_validation(state: ProductionState) -> str:
    """Route based on validation result"""
    status = state.get("status", "")
    errors = state.get("errors", [])
    
    if status == "failed" or errors:
        return "error_handler"
    return "processing_node"


def route_after_processing(state: ProductionState) -> str:
    """Route after processing"""
    status = state.get("status", "")
    errors = state.get("errors", [])
    
    if status == "failed" or errors:
        return "error_handler"
    return "output_node"


def main():
    """
    Create and run a production-ready workflow.
    """
    logger.info("=== Starting Production Application ===")
    
    # Create checkpointer for state persistence
    checkpointer = MemorySaver()
    
    # Create the graph
    workflow = StateGraph(ProductionState)
    
    # Add nodes
    workflow.add_node("input_validation", input_validation_node)
    workflow.add_node("processing_node", processing_node)
    workflow.add_node("output_node", output_node)
    workflow.add_node("error_handler", error_handler_node)
    
    # Set entry point
    workflow.set_entry_point("input_validation")
    
    # Define flow with error handling
    workflow.add_conditional_edges(
        "input_validation",
        route_after_validation,
        {
            "processing_node": "processing_node",
            "error_handler": "error_handler",
        }
    )
    
    workflow.add_conditional_edges(
        "processing_node",
        route_after_processing,
        {
            "output_node": "output_node",
            "error_handler": "error_handler",
        }
    )
    
    workflow.add_edge("output_node", END)
    workflow.add_edge("error_handler", END)
    
    # Compile with checkpointer
    app = workflow.compile(checkpointer=checkpointer)
    
    # Test cases
    test_cases = [
        {"input": "Hello World", "should_succeed": True},
        {"input": "", "should_succeed": False},  # Empty input should fail
        {"input": "Production Test", "should_succeed": True},
    ]
    
    print("\n=== Production Application Example ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}: '{test_case['input']}'")
        print(f"{'='*60}\n")
        
        # Create initial state
        request_id = f"REQ-{i:03d}"
        initial_state = {
            "request_id": request_id,
            "user_input": test_case["input"],
            "processed_data": "",
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "execution_time": 0.0,
            "status": "pending",
            "current_step": "start",
            "errors": [],
            "warnings": [],
            "nodes_executed": [],
            "node_durations": {},
            "messages": [],
            "metadata": {"test_case": str(i)},
        }
        
        # Execute workflow
        config = {"configurable": {"thread_id": request_id}}
        result = app.invoke(initial_state, config=config)
        
        # Display results
        print(f"Status: {result['status']}")
        print(f"Execution Time: {result['execution_time']:.3f}s")
        print(f"Nodes Executed: {result['nodes_executed']}")
        print(f"Node Durations: {result['node_durations']}")
        
        if result.get("processed_data"):
            print(f"Processed Data: {result['processed_data']}")
        
        if result.get("errors"):
            print(f"Errors: {result['errors']}")
        
        if result.get("warnings"):
            print(f"Warnings: {result['warnings']}")
        
        print(f"Messages: {result['messages']}")
    
    print("\n" + "="*60)
    print("=== Production Best Practices Summary ===")
    print("="*60)
    print("\n1. ERROR HANDLING:")
    print("   - Validate inputs early")
    print("   - Use try-except blocks in nodes")
    print("   - Centralized error handling")
    print("   - Comprehensive error logging")
    
    print("\n2. LOGGING:")
    print("   - Use structured logging")
    print("   - Log at appropriate levels (INFO, WARNING, ERROR)")
    print("   - Include request IDs for tracing")
    print("   - Log execution times and metrics")
    
    print("\n3. MONITORING:")
    print("   - Track node execution times")
    print("   - Monitor workflow status")
    print("   - Track errors and warnings")
    print("   - Measure end-to-end execution time")
    
    print("\n4. STATE MANAGEMENT:")
    print("   - Use TypedDict for type safety")
    print("   - Track execution progress")
    print("   - Include metadata for debugging")
    print("   - Use checkpoints for persistence")
    
    print("\n5. RELIABILITY:")
    print("   - Implement retry logic for transient failures")
    print("   - Use timeouts for long-running operations")
    print("   - Provide fallback paths")
    print("   - Handle edge cases gracefully")
    
    print("\n6. ARCHITECTURE:")
    print("   - Separate validation, processing, and output")
    print("   - Use conditional routing for error handling")
    print("   - Support resumable workflows with checkpoints")
    print("   - Design for scalability")
    
    print("\n=== Application Complete ===")
    logger.info("=== Production Application Complete ===")


if __name__ == "__main__":
    main()

