# LangGraph Interview Questions - 150 Multiple Choice Questions

This document contains 150 multiple-choice interview questions covering LangGraph concepts from basics to advanced topics. Each question includes explanations for why the correct answer is right and why other options are incorrect.

---

## Section 1: Fundamentals (Questions 1-30)

### Question 1
**What is the primary purpose of StateGraph in LangGraph?**

A) To manage database connections  
B) To create and manage stateful workflows with nodes and edges  
C) To handle HTTP requests  
D) To manage environment variables  

**Correct Answer: B**

**Explanation:** StateGraph is the core class in LangGraph for creating stateful, multi-actor applications. It manages the flow of state through nodes connected by edges. Option A is incorrect as StateGraph doesn't handle database connections. Option C is wrong - LangGraph doesn't directly handle HTTP requests. Option D is incorrect - environment variables are managed separately.

---

### Question 2
**In LangGraph, what must a node function always accept and return?**

A) HTTP request and response objects  
B) State dictionary and updated state dictionary  
C) Database connection and query results  
D) File paths and file contents  

**Correct Answer: B**

**Explanation:** Nodes in LangGraph are functions that accept the current state (as a dictionary) and return an updated state dictionary. This is fundamental to how state flows through the graph. Options A, C, and D are incorrect as they don't represent the LangGraph node contract.

---

### Question 3
**What is the purpose of the END node in LangGraph?**

A) To restart the graph execution  
B) To terminate graph execution  
C) To pause execution temporarily  
D) To skip the current node  

**Correct Answer: B**

**Explanation:** END is a special node in LangGraph that signals the termination of graph execution. When a node has an edge to END, execution stops after that node completes. Options A, C, and D are incorrect - END doesn't restart, pause, or skip nodes.

---

### Question 4
**Which Python construct is recommended for defining state schemas in LangGraph?**

A) Regular dictionaries  
B) TypedDict from typing module  
C) Classes with __init__ methods  
D) JSON files  

**Correct Answer: B**

**Explanation:** TypedDict provides type safety and clear documentation for state schemas. It allows IDEs and type checkers to validate state structure. While regular dictionaries (A) work, TypedDict is recommended. Classes (C) are not the standard approach. JSON files (D) are for data storage, not schema definition.

---

### Question 5
**What happens if you modify the state dictionary directly inside a node function?**

A) The changes are automatically saved  
B) The changes are ignored  
C) It violates LangGraph's immutability principle and may cause issues  
D) It works perfectly fine  

**Correct Answer: C**

**Explanation:** LangGraph follows an immutability principle. Nodes should return new state dictionaries rather than modifying the input state in place. Direct modification can cause unexpected behavior. Options A, B, and D are incorrect.

---

### Question 6
**What method is used to add a node to a StateGraph?**

A) add_node()  
B) insert_node()  
C) create_node()  
D) register_node()  

**Correct Answer: A**

**Explanation:** The `add_node()` method is used to add nodes to a StateGraph. It takes a node name and a function. Options B, C, and D are not valid StateGraph methods.

---

### Question 7
**What method sets the entry point of a graph?**

A) set_start()  
B) set_entry_point()  
C) set_begin()  
D) set_initial()  

**Correct Answer: B**

**Explanation:** `set_entry_point()` is the method used to specify which node execution should start from. Options A, C, and D are not valid StateGraph methods.

---

### Question 8
**What is required before you can execute a StateGraph?**

A) Saving it to a file  
B) Compiling it using compile()  
C) Converting it to JSON  
D) Registering it with a server  

**Correct Answer: B**

**Explanation:** A StateGraph must be compiled using the `compile()` method before it can be executed. This validates the graph structure and creates an executable application. Options A, C, and D are not required for execution.

---

### Question 9
**How do you execute a compiled LangGraph application?**

A) Using run() method  
B) Using invoke() method  
C) Using execute() method  
D) Using start() method  

**Correct Answer: B**

**Explanation:** The `invoke()` method is used to execute a compiled graph with an initial state. Options A, C, and D are not valid methods for executing LangGraph applications.

---

### Question 10
**What is the purpose of edges in a LangGraph?**

A) To store data  
B) To define the flow of execution between nodes  
C) To handle errors  
D) To manage memory  

**Correct Answer: B**

**Explanation:** Edges define the connections between nodes, determining the order and flow of execution. They don't store data (A), handle errors (C), or manage memory (D).

---

### Question 11
**In LangGraph, what does a node function return?**

A) The next node name  
B) An updated state dictionary  
C) A boolean value  
D) Nothing (void)  

**Correct Answer: B**

**Explanation:** Node functions must return an updated state dictionary (or a partial state dictionary that will be merged). They don't return node names (A), booleans (C), or nothing (D).

---

### Question 12
**What happens when a node returns an empty dictionary {}?**

A) The graph execution stops  
B) The state remains unchanged  
C) An error is raised  
D) The graph restarts  

**Correct Answer: B**

**Explanation:** When a node returns an empty dictionary, LangGraph merges it with the current state, resulting in no changes. Execution continues normally. Options A, C, and D are incorrect.

---

### Question 13
**Which of the following is a valid way to access state in a node function?**

A) state['key']  
B) state.get('key', default_value)  
C) Both A and B  
D) state.key (dot notation)  

**Correct Answer: C**

**Explanation:** Both dictionary access (A) and the `.get()` method (B) are valid. The `.get()` method is safer as it allows default values. Dot notation (D) doesn't work with TypedDict/dict objects.

---

### Question 14
**What is the relationship between nodes and edges in LangGraph?**

A) Nodes are optional, edges are required  
B) Edges are optional, nodes are required  
C) Both are required for a valid graph  
D) Neither is required  

**Correct Answer: C**

**Explanation:** A valid LangGraph requires both nodes (to process state) and edges (to define flow). Without nodes, there's nothing to execute. Without edges, nodes aren't connected. Option D is incorrect.

---

### Question 15
**What does it mean when we say LangGraph state is "immutable"?**

A) State cannot be read  
B) State cannot be modified in place; nodes return new state  
C) State is stored in read-only memory  
D) State is encrypted  

**Correct Answer: B**

**Explanation:** Immutability means nodes shouldn't modify the input state directly. Instead, they return new state dictionaries. Options A, C, and D are incorrect interpretations.

---

### Question 16
**How do you add a simple edge from one node to another?**

A) add_edge(from_node, to_node)  
B) connect(from_node, to_node)  
C) link(from_node, to_node)  
D) route(from_node, to_node)  

**Correct Answer: A**

**Explanation:** `add_edge()` is the method to add a simple, unconditional edge between nodes. Options B, C, and D are not valid StateGraph methods.

---

### Question 17
**What is the initial state passed to a graph?**

A) Always an empty dictionary  
B) The state returned by the entry point node  
C) The state provided to invoke() method  
D) A randomly generated state  

**Correct Answer: C**

**Explanation:** The initial state is explicitly provided when calling `invoke(initial_state)`. It's not empty (A), not from the entry point (B), and not random (D).

---

### Question 18
**Can a node have multiple outgoing edges?**

A) Yes, always  
B) No, never  
C) Yes, but only with conditional edges  
D) Only if using special routing nodes  

**Correct Answer: C**

**Explanation:** A node can have multiple outgoing edges, but this requires conditional edges (using `add_conditional_edges()`). Simple edges (using `add_edge()`) only allow one outgoing edge. Options A, B, and D are incorrect.

---

### Question 19
**What happens if you don't set an entry point for a graph?**

A) The graph uses the first added node  
B) The graph cannot be compiled  
C) The graph starts from a random node  
D) The graph doesn't need an entry point  

**Correct Answer: B**

**Explanation:** An entry point is required. If not set, the graph compilation will fail or execution will error. Options A, C, and D are incorrect.

---

### Question 20
**In a TypedDict state schema, what happens if you return a state field that wasn't defined in the TypedDict?**

A) It's automatically added  
B) It's ignored  
C) A type error may occur, but runtime execution continues  
D) The graph execution fails immediately  

**Correct Answer: C**

**Explanation:** TypedDict provides type hints, but Python's runtime doesn't enforce them strictly. Type checkers will warn, but execution may continue. Options A, B, and D are not accurate.

---

### Question 21
**What is the purpose of state reducers in LangGraph?**

A) To reduce memory usage  
B) To merge partial state updates with existing state  
C) To compress state data  
D) To validate state structure  

**Correct Answer: B**

**Explanation:** State reducers define how partial state updates (returned by nodes) are merged with the existing state. They're not for memory reduction (A), compression (C), or validation (D).

---

### Question 22
**Can a graph have multiple entry points?**

A) Yes, you can call set_entry_point() multiple times  
B) No, only one entry point is allowed  
C) Yes, but only for subgraphs  
D) Yes, using special configuration  

**Correct Answer: B**

**Explanation:** A StateGraph can have only one entry point. Calling `set_entry_point()` multiple times will overwrite the previous entry point. Options A, C, and D are incorrect.

---

### Question 23
**What is the return type of workflow.compile()?**

A) StateGraph  
B) A compiled application object  
C) A dictionary  
D) None  

**Correct Answer: B**

**Explanation:** `compile()` returns a compiled application object that can be executed with `invoke()`. It doesn't return the StateGraph (A), a dictionary (C), or None (D).

---

### Question 24
**How are state updates from nodes merged with existing state?**

A) By completely replacing the state  
B) By deep merging dictionaries  
C) By appending to lists and updating dictionaries  
D) Using state reducers (default or custom)  

**Correct Answer: D**

**Explanation:** LangGraph uses state reducers to merge updates. By default, it does a shallow merge, but custom reducers can define specific merge behavior. Options A, B, and C describe specific behaviors but don't capture the reducer mechanism.

---

### Question 25
**What happens if a node returns a state key that already exists?**

A) An error is raised  
B) The new value overwrites the old value  
C) The values are merged automatically  
D) Both values are kept in a list  

**Correct Answer: B**

**Explanation:** By default, returned state values overwrite existing values. Custom reducers can change this behavior. Options A, C, and D don't describe the default behavior.

---

### Question 26
**Can you add the same node function to a graph multiple times with different names?**

A) No, each function can only be added once  
B) Yes, the same function can be added with different names  
C) Yes, but only if the function is modified  
D) No, this causes a compilation error  

**Correct Answer: B**

**Explanation:** The same function can be added multiple times with different node names, allowing reuse of logic in different parts of the graph. Options A, C, and D are incorrect.

---

### Question 27
**What is the order of execution when a node has multiple incoming edges?**

A) All incoming nodes execute in parallel  
B) The node executes once after all incoming nodes complete  
C) The node executes multiple times, once for each incoming edge  
D) Only the first incoming edge triggers execution  

**Correct Answer: B**

**Explanation:** When multiple nodes have edges to the same target node, that target node executes once after all source nodes complete. Options A, C, and D are incorrect.

---

### Question 28
**In LangGraph, what is a "channel" in the context of state?**

A) A communication channel between nodes  
B) A state field that can be updated  
C) A network connection  
D) A file stream  

**Correct Answer: B**

**Explanation:** In LangGraph terminology, a "channel" refers to a state field. Each field in the state schema is a channel. Options A, C, and D are incorrect interpretations.

---

### Question 29
**What happens if you try to compile a graph with no nodes?**

A) Compilation succeeds but execution fails  
B) Compilation fails with an error  
C) Compilation succeeds and creates an empty graph  
D) A warning is issued but compilation continues  

**Correct Answer: B**

**Explanation:** A graph without nodes is invalid and compilation will fail. Options A, C, and D are incorrect.

---

### Question 30
**Can a node have an edge that points back to itself?**

A) No, this creates an infinite loop  
B) Yes, but only with conditional edges  
C) Yes, this is always allowed  
D) Yes, but only if a termination condition exists  

**Correct Answer: D**

**Explanation:** A node can have an edge back to itself, but this requires a termination condition (like a counter or conditional edge) to prevent infinite loops. Options A, B, and C are partially correct but D is most accurate.

---

## Section 2: Conditional Edges and Routing (Questions 31-50)

### Question 31
**What is the purpose of conditional edges in LangGraph?**

A) To handle errors  
B) To route execution to different nodes based on state  
C) To pause execution  
D) To validate state  

**Correct Answer: B**

**Explanation:** Conditional edges allow dynamic routing based on the current state, enabling decision-making in workflows. They're not for error handling (A), pausing (C), or validation (D).

---

### Question 32
**What method is used to add conditional edges?**

A) add_edge()  
B) add_conditional_edge()  
C) add_conditional_edges()  
D) add_routing_edge()  

**Correct Answer: C**

**Explanation:** `add_conditional_edges()` is the method for adding conditional routing. Options A, B, and D are not valid methods (though B is close, the correct method name uses plural "edges").

---

### Question 33
**What must a conditional routing function return?**

A) A boolean value  
B) A state dictionary  
C) A node name (string) that exists in the graph  
D) An integer  

**Correct Answer: C**

**Explanation:** Conditional routing functions must return a string matching a node name (or END) to route execution. They don't return booleans (A), state (B), or integers (D).

---

### Question 34
**In add_conditional_edges(), what is the purpose of the mapping dictionary?**

A) To define state transformations  
B) To map routing function return values to node names  
C) To define error handlers  
D) To configure timeouts  

**Correct Answer: B**

**Explanation:** The mapping dictionary maps the return values of the routing function to actual node names in the graph. Options A, C, and D are incorrect.

---

### Question 35
**What happens if a routing function returns a value not in the mapping dictionary?**

A) Execution stops with an error  
B) The graph uses a default route  
C) Execution continues to the next node  
D) The graph restarts  

**Correct Answer: A**

**Explanation:** If the routing function returns a value not in the mapping dictionary, LangGraph raises an error. Options B, C, and D are incorrect.

---

### Question 36
**Can a conditional routing function access the current state?**

A) No, it only receives the node name  
B) Yes, it receives the current state as a parameter  
C) Yes, but only through global variables  
D) No, routing is stateless  

**Correct Answer: B**

**Explanation:** Conditional routing functions receive the current state as their parameter, allowing them to make decisions based on state values. Options A, C, and D are incorrect.

---

### Question 37
**What is the recommended return type annotation for a routing function that returns specific node names?**

A) str  
B) Literal["node1", "node2"]  
C) Any  
D) None  

**Correct Answer: B**

**Explanation:** Using `Literal` with specific node names provides type safety and makes the routing contract explicit. While `str` (A) works, `Literal` is more precise. Options C and D are incorrect.

---

### Question 38
**Can a node have both regular edges and conditional edges?**

A) No, you must choose one type  
B) Yes, but conditional edges take precedence  
C) Yes, but regular edges take precedence  
D) No, this causes a compilation error  

**Correct Answer: D**

**Explanation:** A node cannot have both regular and conditional edges - this will cause a compilation error. You must use either `add_edge()` or `add_conditional_edges()`, not both. Options A, B, and C are incorrect.

---

### Question 39
**What happens if all conditional routes point to the same node?**

A) An error is raised  
B) The conditional edge behaves like a regular edge  
C) Execution stops  
D) A warning is issued  

**Correct Answer: B**

**Explanation:** If all routes point to the same node, it effectively behaves like a regular edge, though using `add_edge()` would be simpler. Options A, C, and D are incorrect.

---

### Question 40
**In a routing function, can you return END directly?**

A) No, END must be in the mapping dictionary  
B) Yes, END is a special constant that works directly  
C) Yes, but only if imported from langgraph.graph  
D) Both B and C  

**Correct Answer: D**

**Explanation:** END is a special constant from `langgraph.graph` that can be returned directly from routing functions and doesn't need to be in the mapping dictionary. Both B and C are correct, so D is the best answer.

---

### Question 41
**What is a common use case for conditional edges?**

A) Error handling  
B) Implementing if-else logic in workflows  
C) Parallel execution  
D) State validation  

**Correct Answer: B**

**Explanation:** Conditional edges are primarily used to implement decision-making logic (if-else, switch-like behavior) in workflows. While they can be used for error handling (A), that's not their primary purpose. Options C and D are not typical use cases.

---

### Question 42
**Can a routing function modify the state?**

A) Yes, and changes are persisted  
B) No, routing functions should only read state  
C) Yes, but only through side effects  
D) No, routing functions don't receive state  

**Correct Answer: B**

**Explanation:** Routing functions should be pure functions that only read state to make routing decisions. State modifications should happen in nodes, not routing functions. Options A, C, and D are incorrect.

---

### Question 43
**What is the maximum number of different nodes a conditional edge can route to?**

A) 2  
B) 4  
C) 8  
D) Unlimited  

**Correct Answer: D**

**Explanation:** There's no hard limit on the number of routes a conditional edge can have. The mapping dictionary can contain as many node mappings as needed. Options A, B, and C are incorrect.

---

### Question 44
**If a routing function returns "node_x" but "node_x" doesn't exist in the graph, what happens?**

A) Execution continues to the next available node  
B) An error is raised during execution  
C) The graph compilation fails  
D) Execution stops silently  

**Correct Answer: B**

**Explanation:** If a routing function returns a non-existent node name, an error is raised during execution (not compilation, as the routing function is called at runtime). Options A, C, and D are incorrect.

---

### Question 45
**Can you nest conditional edges (route to a node that itself has conditional edges)?**

A) No, conditional edges cannot be nested  
B) Yes, this is a common pattern  
C) Yes, but only up to 2 levels deep  
D) Yes, but only with special configuration  

**Correct Answer: B**

**Explanation:** Conditional edges can be nested - a node reached via conditional routing can itself have conditional edges. This is a common pattern for complex decision trees. Options A, C, and D are incorrect.

---

### Question 46
**What is the difference between add_edge() and add_conditional_edges()?**

A) add_edge() is faster  
B) add_conditional_edges() allows dynamic routing based on state  
C) add_edge() supports multiple targets  
D) There is no difference  

**Correct Answer: B**

**Explanation:** `add_edge()` creates a fixed, unconditional connection, while `add_conditional_edges()` enables dynamic routing based on state evaluation. Options A, C, and D are incorrect.

---

### Question 47
**In a routing function, what should you do if the state doesn't contain expected values?**

A) Return a random node name  
B) Return END to stop execution  
C) Handle the missing values gracefully (e.g., use defaults)  
D) Raise an exception  

**Correct Answer: C**

**Explanation:** Routing functions should handle missing or unexpected state values gracefully, using defaults or fallback logic. Options A, B, and D are not best practices.

---

### Question 48
**Can a conditional edge route to the same node it originates from?**

A) No, this creates an infinite loop  
B) Yes, but only with a termination condition  
C) Yes, this is always safe  
D) No, this causes a compilation error  

**Correct Answer: B**

**Explanation:** A conditional edge can route back to the same node, but this requires a termination condition (like a counter) to prevent infinite loops. Options A, C, and D are incorrect.

---

### Question 49
**What is the execution order when a node has multiple conditional edges defined?**

A) All routes are taken in parallel  
B) Only one route is taken based on the routing function  
C) Routes are taken sequentially  
D) This is not allowed  

**Correct Answer: B**

**Explanation:** A node can only have one set of conditional edges, and the routing function determines which single route is taken. Options A, C, and D are incorrect.

---

### Question 50
**How do you implement a "default" route in conditional edges?**

A) Use a special "default" key in the mapping  
B) Handle it in the routing function logic  
C) Add a regular edge as fallback  
D) LangGraph doesn't support default routes  

**Correct Answer: B**

**Explanation:** Default routes are implemented by having the routing function return a default node name when no specific conditions match. There's no special "default" key (A), and you can't mix regular and conditional edges (C). Option D is incorrect.

---

## Section 3: State Management (Questions 51-70)

### Question 51
**What is the default behavior when a node returns a partial state update?**

A) Only the returned fields are kept, others are deleted  
B) Returned fields are merged with existing state  
C) An error is raised  
D) The state is completely replaced  

**Correct Answer: B**

**Explanation:** By default, LangGraph merges partial state updates with existing state. Only the returned fields are updated; other fields remain unchanged. Options A, C, and D are incorrect.

---

### Question 52
**What is a state reducer in LangGraph?**

A) A function that reduces memory usage  
B) A function that defines how state updates are merged  
C) A function that validates state  
D) A function that compresses state  

**Correct Answer: B**

**Explanation:** State reducers define how partial state updates are merged with existing state, especially for complex types like lists. Options A, C, and D are incorrect.

---

### Question 53
**When would you need a custom state reducer?**

A) Always, reducers are required  
B) When you need custom merge logic (e.g., appending to lists)  
C) Never, default behavior is always sufficient  
D) Only for validation  

**Correct Answer: B**

**Explanation:** Custom reducers are needed when default merge behavior isn't sufficient, such as appending to lists instead of replacing them. Options A, C, and D are incorrect.

---

### Question 54
**What happens to list fields in state when a node returns a new list value?**

A) The new list replaces the old list  
B) The lists are concatenated  
C) Lists are merged element by element  
D) An error is raised  

**Correct Answer: A**

**Explanation:** By default, list fields are replaced entirely. To append, you need a custom reducer. Options B, C, and D are incorrect.

---

### Question 55
**Can state fields have different types in different nodes?**

A) Yes, Python is dynamically typed  
B) No, state schema must be consistent  
C) Yes, but only for optional fields  
D) No, this causes runtime errors  

**Correct Answer: B**

**Explanation:** While Python allows dynamic typing, LangGraph expects consistent state schemas. Changing field types can cause issues. Options A, C, and D are not accurate.

---

### Question 56
**What is the purpose of using TypedDict for state schemas?**

A) Runtime type enforcement  
B) Type hints for IDEs and type checkers  
C) Automatic validation  
D) Performance optimization  

**Correct Answer: B**

**Explanation:** TypedDict provides type hints for static analysis tools and IDEs, but Python's runtime doesn't enforce them. Options A, C, and D are not accurate - TypedDict doesn't provide runtime enforcement, automatic validation, or performance benefits.

---

### Question 57
**How do you access nested state values?**

A) state['key']['nested_key']  
B) state.get('key', {}).get('nested_key')  
C) Both A and B  
D) state.key.nested_key (dot notation)  

**Correct Answer: C**

**Explanation:** Both dictionary access and chained `.get()` calls work for nested values. The `.get()` method is safer for missing keys. Dot notation (D) doesn't work with dictionaries.

---

### Question 58
**What happens if a node returns a state key that doesn't exist in the TypedDict schema?**

A) It's automatically added to the schema  
B) It's ignored  
C) Type checkers warn, but execution may continue  
D) Execution fails immediately  

**Correct Answer: C**

**Explanation:** TypedDict is for type hints, not runtime enforcement. Type checkers will warn, but Python execution may continue. Options A, B, and D are not accurate.

---

### Question 59
**Can state contain functions or callable objects?**

A) Yes, always  
B) No, never  
C) Yes, but they won't be serialized for checkpoints  
D) Only if using special serializers  

**Correct Answer: C**

**Explanation:** State can contain functions, but they won't be serialized when using checkpoints/persistence. This can cause issues if you need to resume from checkpoints. Options A, B, and D are not fully accurate.

---

### Question 60
**What is the recommended way to initialize optional state fields?**

A) Always provide them in initial state  
B) Use None as default  
C) Use empty values (empty string, empty list, etc.)  
D) All of the above, depending on the use case  

**Correct Answer: D**

**Explanation:** The approach depends on the use case. Some fields should always be provided (A), some can use None (B), and some can use empty values (C). The best practice depends on the specific field's purpose.

---

### Question 61
**How do state reducers handle dictionary merging?**

A) Deep merge by default  
B) Shallow merge by default  
C) Complete replacement by default  
D) No merging, dictionaries are replaced  

**Correct Answer: B**

**Explanation:** Default state reducers perform shallow merging for dictionaries. Nested dictionaries are replaced, not merged. Options A, C, and D are incorrect.

---

### Question 62
**What is the purpose of the "reducer" parameter in state field definitions?**

A) To reduce memory usage  
B) To define custom merge logic for that field  
C) To validate field values  
D) To encrypt field data  

**Correct Answer: B**

**Explanation:** The reducer parameter allows defining custom merge logic for specific state fields. Options A, C, and D are incorrect.

---

### Question 63
**Can you have state fields with the same name but different types in a TypedDict?**

A) Yes, Python allows this  
B) No, TypedDict doesn't allow duplicate keys  
C) Yes, but only with Union types  
D) No, this causes a syntax error  

**Correct Answer: B**

**Explanation:** TypedDict doesn't allow duplicate keys. Each field name must be unique. Options A, C, and D are incorrect.

---

### Question 64
**What happens when a node returns state with a None value for a field?**

A) The field is deleted from state  
B) The field is set to None  
C) The field remains unchanged  
D) An error is raised  

**Correct Answer: B**

**Explanation:** Returning None sets the field to None; it doesn't delete the field or leave it unchanged. Option D is incorrect - None is a valid value.

---

### Question 65
**How do you implement a state field that accumulates values (like a log)?**

A) Use a list and return the entire list each time  
B) Use a list with a custom reducer that appends  
C) Use a string and concatenate  
D) All of the above can work  

**Correct Answer: B**

**Explanation:** For accumulating values, a custom reducer that appends to a list is the most efficient approach. Option A works but is inefficient. Option C works for strings. Option D is technically true, but B is the best practice.

---

### Question 66
**What is the difference between state.get('key') and state['key']?**

A) No difference  
B) .get() returns None if key missing, [] raises KeyError  
C) .get() is faster  
D) [] is more type-safe  

**Correct Answer: B**

**Explanation:** `.get()` returns None (or a default) if the key is missing, while `[]` raises a KeyError. Options A, C, and D are incorrect.

---

### Question 67
**Can state contain circular references?**

A) Yes, always  
B) No, never  
C) Yes, but they cause issues with serialization  
D) Only in specific configurations  

**Correct Answer: C**

**Explanation:** State can contain circular references, but they will cause problems with checkpoint serialization. Options A, B, and D are not accurate.

---

### Question 68
**What is the maximum size for state in LangGraph?**

A) 1 MB  
B) 10 MB  
C) 100 MB  
D) No hard limit, but practical limits apply  

**Correct Answer: D**

**Explanation:** There's no hard-coded limit, but very large states can cause performance issues and serialization problems with checkpoints. Options A, B, and C are arbitrary limits.

---

### Question 69
**How do you clear a state field (remove it from state)?**

A) Return it with value None  
B) Return it with an empty value  
C) State fields cannot be removed once set  
D) Use a special "delete" marker  

**Correct Answer: C**

**Explanation:** Once a state field is set, it cannot be removed. You can set it to None or empty, but the field remains in the state. Options A, B, and D are incorrect.

---

### Question 70
**What is the recommended approach for state fields that represent flags or status?**

A) Always use booleans  
B) Use strings like "active", "inactive"  
C) Use integers (0, 1)  
D) Use booleans for simple flags, enums for status  

**Correct Answer: D**

**Explanation:** Booleans are best for simple true/false flags, while enums or string literals are better for status fields with multiple values. Options A, B, and C are too restrictive.

---

## Section 4: Error Handling and Reliability (Questions 71-85)

### Question 71
**What happens if a node function raises an exception?**

A) The exception is automatically caught and logged  
B) Execution stops and the exception propagates  
C) The graph automatically retries  
D) Execution continues to the next node  

**Correct Answer: B**

**Explanation:** By default, exceptions in nodes propagate and stop execution. You need to implement error handling yourself. Options A, C, and D are incorrect - LangGraph doesn't automatically handle exceptions.

---

### Question 72
**What is a common pattern for error handling in LangGraph nodes?**

A) Using try-except blocks inside nodes  
B) Creating error handler nodes  
C) Using conditional edges to route errors  
D) All of the above  

**Correct Answer: D**

**Explanation:** All approaches can be used: try-except in nodes (A), dedicated error handler nodes (B), and conditional routing for error cases (C). The best approach depends on the use case.

---

### Question 73
**How do you implement retry logic in LangGraph?**

A) LangGraph has built-in retry support  
B) Implement it manually in nodes or use external libraries  
C) Retries are automatic  
D) Retries are not possible  

**Correct Answer: B**

**Explanation:** LangGraph doesn't have built-in retry logic. You need to implement it manually in nodes or use libraries like tenacity. Options A, C, and D are incorrect.

---

### Question 74
**What is a circuit breaker pattern in the context of LangGraph?**

A) A node that stops execution  
B) A pattern to prevent cascading failures by stopping calls to failing services  
C) A type of conditional edge  
D) A state validation mechanism  

**Correct Answer: B**

**Explanation:** A circuit breaker stops calling a failing service after a threshold of failures, preventing cascading failures. Options A, C, and D are incorrect.

---

### Question 75
**How can you handle timeouts in LangGraph nodes?**

A) LangGraph has built-in timeout support  
B) Use Python's signal module or asyncio timeouts  
C) Timeouts are not possible  
D) Use special timeout nodes  

**Correct Answer: B**

**Explanation:** LangGraph doesn't have built-in timeout support. You need to implement timeouts using Python's signal module (synchronous) or asyncio (asynchronous). Options A, C, and D are incorrect.

---

### Question 76
**What is the purpose of fallback nodes in error handling?**

A) To catch all exceptions automatically  
B) To provide alternative execution paths when errors occur  
C) To log errors  
D) To restart the graph  

**Correct Answer: B**

**Explanation:** Fallback nodes provide alternative execution paths when errors occur, allowing the workflow to continue or gracefully degrade. Options A, C, and D are incorrect.

---

### Question 77
**Can you have multiple error handler nodes for different error types?**

A) No, only one error handler is allowed  
B) Yes, using conditional edges based on error type  
C) Yes, but they must be in sequence  
D) No, errors are handled automatically  

**Correct Answer: B**

**Explanation:** You can route to different error handlers based on error type using conditional edges. Options A, C, and D are incorrect.

---

### Question 78
**What is the recommended way to handle validation errors in state?**

A) Raise exceptions immediately  
B) Store errors in state and route to error handler  
C) Ignore validation errors  
D) Always use external validation  

**Correct Answer: B**

**Explanation:** Storing validation errors in state and routing to error handlers provides better control and allows the workflow to decide how to handle errors. Options A, C, and D are less flexible.

---

### Question 79
**How do you implement exponential backoff for retries?**

A) Use LangGraph's built-in backoff  
B) Implement it manually or use libraries like tenacity  
C) Backoff is automatic  
D) Backoff is not possible  

**Correct Answer: B**

**Explanation:** Exponential backoff must be implemented manually or using libraries. LangGraph doesn't provide this. Options A, C, and D are incorrect.

---

### Question 80
**What happens if a node takes too long to execute?**

A) LangGraph automatically times it out  
B) Execution continues indefinitely  
C) You need to implement timeout handling  
D) The graph automatically skips slow nodes  

**Correct Answer: C**

**Explanation:** LangGraph doesn't automatically timeout nodes. You need to implement timeout handling using signals, asyncio, or external monitoring. Options A, B, and D are incorrect.

---

### Question 81
**What is a health check node used for?**

A) To check system health  
B) To validate state health  
C) To monitor node execution  
D) All of the above  

**Correct Answer: D**

**Explanation:** Health check nodes can be used for system health (A), state validation (B), and execution monitoring (C). The specific use depends on implementation.

---

### Question 82
**How do you handle partial failures in a graph with multiple paths?**

A) Stop the entire graph  
B) Continue with successful paths, handle failures separately  
C) Retry all paths  
D) Ignore failures  

**Correct Answer: B**

**Explanation:** In graphs with multiple paths, you can continue with successful paths while handling failures in error handler nodes. Options A, C, and D are not ideal strategies.

---

### Question 83
**What is the purpose of error state fields?**

A) To store error information in state  
B) To trigger error handlers  
C) To log errors  
D) All of the above  

**Correct Answer: D**

**Explanation:** Error state fields can store error info (A), be used in conditional routing to trigger handlers (B), and for logging (C). All uses are valid.

---

### Question 84
**Can you recover from errors and continue execution?**

A) No, errors always stop execution  
B) Yes, by catching exceptions and routing to recovery nodes  
C) Yes, but only for specific error types  
D) No, recovery is not possible  

**Correct Answer: B**

**Explanation:** By catching exceptions in nodes and using conditional routing to recovery nodes, you can implement error recovery. Options A, C, and D are incorrect.

---

### Question 85
**What is the difference between transient and permanent errors?**

A) Transient errors can be retried, permanent errors cannot  
B) There is no difference  
C) Permanent errors are more severe  
D) Transient errors always cause graph failure  

**Correct Answer: A**

**Explanation:** Transient errors (network issues, temporary unavailability) can often be retried, while permanent errors (invalid input, authentication failure) should not be retried. Options B, C, and D are incorrect.

---

## Section 5: Persistence and Checkpoints (Questions 86-100)

### Question 86
**What is the purpose of checkpoints in LangGraph?**

A) To save memory  
B) To enable resuming workflows from saved state  
C) To validate state  
D) To optimize performance  

**Correct Answer: B**

**Explanation:** Checkpoints save workflow state, allowing workflows to be resumed after interruptions (restarts, crashes, pauses). Options A, C, and D are not the primary purpose.

---

### Question 87
**What is SQLiteSaver used for?**

A) To save SQL queries  
B) To persist checkpoints in a SQLite database  
C) To manage database connections  
D) To execute SQL in nodes  

**Correct Answer: B**

**Explanation:** SQLiteSaver is a checkpoint saver that stores workflow state in a SQLite database for persistence. Options A, C, and D are incorrect.

---

### Question 88
**How do you enable checkpointing in a compiled graph?**

A) Checkpointing is always enabled  
B) Pass a checkpointer to compile()  
C) Set an environment variable  
D) Use a special node  

**Correct Answer: B**

**Explanation:** Checkpointing is enabled by passing a checkpointer (like SQLiteSaver) to the `compile()` method. Options A, C, and D are incorrect.

---

### Question 89
**What is a thread_id used for in checkpointing?**

A) To identify Python threads  
B) To identify independent workflow instances  
C) To manage concurrency  
D) To track execution time  

**Correct Answer: B**

**Explanation:** thread_id identifies independent workflow instances, allowing multiple workflows to run concurrently with separate checkpointed states. Options A, C, and D are incorrect.

---

### Question 90
**How do you resume a workflow from a checkpoint?**

A) Call invoke() with the saved state  
B) Call invoke() with None and the thread_id config  
C) Use a special resume() method  
D) Checkpoints cannot be resumed  

**Correct Answer: B**

**Explanation:** To resume, call `invoke(None, config={"configurable": {"thread_id": "..."}})` - the checkpointer loads the saved state automatically. Options A, C, and D are incorrect.

---

### Question 91
**What happens to checkpoints when a workflow completes successfully?**

A) They are automatically deleted  
B) They are kept for a configurable retention period  
C) They are always kept forever  
D) They are moved to archive storage  

**Correct Answer: B**

**Explanation:** Checkpoint retention depends on the checkpointer configuration. Most allow configurable retention. Options A, C, and D are not universally true.

---

### Question 92
**Can multiple workflows share the same checkpoint storage?**

A) No, each workflow needs its own storage  
B) Yes, using different thread_ids  
C) Yes, but only if they have the same state schema  
D) No, this causes conflicts  

**Correct Answer: B**

**Explanation:** Multiple workflows can share checkpoint storage by using different thread_ids to identify separate workflow instances. Options A, C, and D are incorrect.

---

### Question 93
**What data is stored in a checkpoint?**

A) Only the final state  
B) The current state and execution history  
C) Only node outputs  
D) Only state changes  

**Correct Answer: B**

**Explanation:** Checkpoints typically store the current state and execution history, allowing full workflow resumption. Options A, C, and D are incomplete.

---

### Question 94
**What is the difference between MemorySaver and SQLiteSaver?**

A) MemorySaver is faster  
B) SQLiteSaver persists to disk, MemorySaver is in-memory only  
C) MemorySaver doesn't support resumption  
D) Both B and C  

**Correct Answer: D**

**Explanation:** SQLiteSaver persists to disk (B), while MemorySaver is in-memory only and doesn't survive restarts (C). Option A is not necessarily true, and B and C together make D the best answer.

---

### Question 95
**When are checkpoints created?**

A) Manually by calling a save method  
B) Automatically after each node execution  
C) Only at the end of execution  
D) Only on errors  

**Correct Answer: B**

**Explanation:** With checkpointing enabled, checkpoints are automatically created after each node execution. Options A, C, and D are incorrect.

---

### Question 96
**Can you access checkpoint history (all previous checkpoints)?**

A) No, only the latest checkpoint is available  
B) Yes, through the checkpointer API  
C) Yes, but only for SQLiteSaver  
D) No, history is not stored  

**Correct Answer: B**

**Explanation:** Most checkpointer implementations provide APIs to access checkpoint history. Options A, C, and D are incorrect.

---

### Question 97
**What happens if you try to resume a non-existent thread_id?**

A) A new workflow starts  
B) An error is raised  
C) Execution continues with empty state  
D) The graph restarts from the beginning  

**Correct Answer: A**

**Explanation:** If a thread_id doesn't exist, invoking with that thread_id starts a new workflow. Options B, C, and D are incorrect.

---

### Question 98
**Can checkpoints be used for debugging?**

A) No, they're only for resumption  
B) Yes, to inspect state at any point  
C) Yes, but only with special tools  
D) No, checkpoints are encrypted  

**Correct Answer: B**

**Explanation:** Checkpoints can be inspected to see state at any execution point, making them useful for debugging. Options A, C, and D are incorrect.

---

### Question 99
**What is required for state to be checkpointable?**

A) State must be JSON serializable  
B) State must be small (< 1MB)  
C) State must contain only primitives  
D) No special requirements  

**Correct Answer: A**

**Explanation:** State must be serializable (typically JSON) to be checkpointed. Complex objects like functions won't serialize. Options B, C, and D are incorrect.

---

### Question 100
**How do you clear/delete a checkpoint?**

A) Delete the database file  
B) Use checkpointer.delete() if available  
C) Overwrite with a new checkpoint  
D) All of the above, depending on the checkpointer  

**Correct Answer: D**

**Explanation:** The method depends on the checkpointer implementation. Some provide delete methods, others require file/database manipulation. Option D is most accurate.

---

## Section 6: Streaming and Real-time Updates (Questions 101-110)

### Question 101
**What is streaming in LangGraph?**

A) Processing data in chunks  
B) Sending node outputs in real-time as they're produced  
C) Reading from files  
D) Network communication  

**Correct Answer: B**

**Explanation:** Streaming in LangGraph refers to sending node outputs incrementally as they're produced, rather than waiting for completion. Options A, C, and D are not the LangGraph-specific meaning.

---

### Question 102
**What method is used to stream graph execution?**

A) stream()  
B) invoke_stream()  
C) Both A and B (different versions)  
D) stream_nodes()  

**Correct Answer: C**

**Explanation:** Both `stream()` and `invoke_stream()` can be used for streaming, depending on the LangGraph version. Options A, B alone, and D are incomplete.

---

### Question 103
**What do you receive when streaming a graph?**

A) Complete final state  
B) Incremental state updates as nodes execute  
C) Only error messages  
D) Node execution logs  

**Correct Answer: B**

**Explanation:** Streaming provides incremental updates (state changes, node outputs) as execution progresses. Options A, C, and D are incorrect.

---

### Question 104
**What is the primary use case for streaming?**

A) Performance optimization  
B) Providing real-time feedback to users  
C) Reducing memory usage  
D) Error handling  

**Correct Answer: B**

**Explanation:** Streaming is primarily used to provide real-time feedback to users as the workflow progresses. Options A, C, and D are secondary benefits.

---

### Question 105
**Can you stream specific nodes only?**

A) No, streaming is all-or-nothing  
B) Yes, by configuring which nodes to stream  
C) Yes, by using special stream nodes  
D) No, but you can filter the stream  

**Correct Answer: D**

**Explanation:** You receive updates for all nodes, but you can filter the stream to process only specific node outputs. Options A, B, and C are not accurate.

---

### Question 106
**What format do streamed updates come in?**

A) Raw strings  
B) State dictionaries  
C) Event objects with node names and state  
D) JSON strings  

**Correct Answer: C**

**Explanation:** Streamed updates are typically event objects containing node names and state updates. Options A, B, and D are incomplete.

---

### Question 107
**How do you handle streaming in async contexts?**

A) Use stream_async()  
B) Use async for with stream()  
C) Streaming doesn't work in async  
D) Use special async nodes  

**Correct Answer: B**

**Explanation:** You can use `async for` with streaming methods in async contexts. Options A, C, and D are incorrect.

---

### Question 108
**What is the difference between streaming and regular execution?**

A) Streaming is faster  
B) Streaming provides incremental updates, regular execution waits for completion  
C) Streaming uses less memory  
D) There is no difference  

**Correct Answer: B**

**Explanation:** The key difference is that streaming provides incremental updates during execution, while regular execution returns only the final result. Options A, C, and D are not the primary difference.

---

### Question 109
**Can you combine streaming with checkpoints?**

A) No, they are mutually exclusive  
B) Yes, streaming works with checkpointed graphs  
C) Yes, but only with MemorySaver  
D) Yes, but checkpoints are disabled during streaming  

**Correct Answer: B**

**Explanation:** Streaming and checkpointing can be used together - you can stream execution of checkpointed graphs. Options A, C, and D are incorrect.

---

### Question 110
**What happens if a node fails during streaming?**

A) Streaming stops and an error is raised  
B) Streaming continues with error events  
C) The failed node is skipped  
D) Streaming restarts from the beginning  

**Correct Answer: A**

**Explanation:** If a node fails, streaming stops and the exception propagates. Options B, C, and D are incorrect.

---

## Section 7: Tools and Integration (Questions 111-120)

### Question 111
**What are tools in the context of LangGraph agents?**

A) Development utilities  
B) Functions that agents can call to perform actions  
C) Graph visualization tools  
D) Debugging instruments  

**Correct Answer: B**

**Explanation:** Tools are callable functions that agents can invoke to perform actions (web search, calculations, API calls, etc.). Options A, C, and D are incorrect.

---

### Question 112
**How do you make a function available as a tool to an agent?**

A) Use the @tool decorator from langchain  
B) Register it with a special registry  
C) Add it to a tools list  
D) All of the above can work  

**Correct Answer: D**

**Explanation:** All approaches can work: @tool decorator (A), tool registries (B), and tools lists (C). The @tool decorator is the most common approach.

---

### Question 113
**What information does a tool need to provide to an LLM?**

A) Only the function name  
B) Name, description, and parameters schema  
C) Source code  
D) Execution results  

**Correct Answer: B**

**Explanation:** Tools need to provide name, description, and parameter schemas so the LLM can understand when and how to use them. Options A, C, and D are incomplete.

---

### Question 114
**How do agents decide which tool to use?**

A) Random selection  
B) The LLM decides based on tool descriptions  
C) Sequential trial of all tools  
D) Based on a predefined priority list  

**Correct Answer: B**

**Explanation:** The LLM (language model) analyzes the situation and tool descriptions to decide which tool to use. Options A, C, and D are incorrect.

---

### Question 115
**What happens after an agent calls a tool?**

A) Execution stops  
B) The tool result is added to state and execution continues  
C) The agent restarts  
D) The graph ends  

**Correct Answer: B**

**Explanation:** Tool results are added to state, and the agent loop continues (typically to think about the result and decide next action). Options A, C, and D are incorrect.

---

### Question 116
**Can tools call other tools?**

A) No, tools are independent  
B) Yes, tools can call other tools directly  
C) Yes, but only through the agent  
D) No, this creates circular dependencies  

**Correct Answer: B**

**Explanation:** Tools are regular Python functions and can call other tools or functions. Options A, C, and D are incorrect.

---

### Question 117
**What is tool error handling best practice?**

A) Tools should never raise exceptions  
B) Tools should raise exceptions and let the agent handle them  
C) Tools should return error messages in their return value  
D) Both B and C can be valid approaches  

**Correct Answer: D**

**Explanation:** Both approaches can work: raising exceptions for the agent to handle (B) or returning error information in results (C). The choice depends on the use case. Option A is too restrictive.

---

### Question 118
**How do you limit which tools an agent can use?**

A) Don't provide unwanted tools in the tools list  
B) Use tool filtering nodes  
C) Configure tool permissions  
D) All of the above  

**Correct Answer: A**

**Explanation:** The simplest approach is to only provide the desired tools to the agent. Options B, C, and D are more complex and not standard approaches.

---

### Question 119
**What is the ReAct pattern in agent workflows?**

A) A reactive programming pattern  
B) Reasoning and Acting - think, act, observe, repeat  
C) A state management pattern  
D) An error handling pattern  

**Correct Answer: B**

**Explanation:** ReAct stands for Reasoning and Acting - agents think, decide on an action (often tool use), observe results, and repeat. Options A, C, and D are incorrect.

---

### Question 120
**How do you implement tool execution in a LangGraph agent?**

A) Create a node that calls the selected tool  
B) Tools are automatically executed  
C) Use special tool nodes  
D) Tools execute outside the graph  

**Correct Answer: A**

**Explanation:** You create nodes that execute tools based on agent decisions. Tools aren't automatically executed (B), there are no special tool nodes (C), and tools execute within the graph (D).

---

## Section 8: Agent Patterns (Questions 121-135)

### Question 121
**What is an agent loop in LangGraph?**

A) A circular graph structure  
B) An iterative process where an agent thinks, acts, and observes  
C) A debugging technique  
D) A performance optimization  

**Correct Answer: B**

**Explanation:** An agent loop is the iterative cycle of reasoning, acting (using tools), and observing results. Options A, C, and D are incorrect.

---

### Question 122
**How do you prevent infinite agent loops?**

A) Set a maximum iteration count  
B) Implement termination conditions  
C) Use timeouts  
D) All of the above  

**Correct Answer: D**

**Explanation:** All approaches are valid: max iterations (A), termination conditions like "task complete" (B), and timeouts (C). Using multiple safeguards is best practice.

---

### Question 123
**What state fields are typically needed for an agent workflow?**

A) Only the user query  
B) Query, thoughts, actions, tool results, and iteration count  
C) Only tool results  
D) Query and final answer  

**Correct Answer: B**

**Explanation:** Agent workflows typically track query, thoughts (reasoning), actions (tool selections), tool results, and iteration count. Options A, C, and D are incomplete.

---

### Question 124
**What is the purpose of a "should_continue" function in agent patterns?**

A) To validate state  
B) To determine if the agent loop should continue or terminate  
C) To check system health  
D) To validate tool results  

**Correct Answer: B**

**Explanation:** "should_continue" functions implement termination logic for agent loops, deciding whether to continue or finish. Options A, C, and D are incorrect.

---

### Question 125
**Can you have multiple agents in a single graph?**

A) No, only one agent per graph  
B) Yes, as separate agent loops  
C) Yes, but they must share state  
D) No, this causes conflicts  

**Correct Answer: B**

**Explanation:** Multiple agents can exist in a graph as separate agent loops, potentially coordinating through shared state. Options A, C, and D are incorrect.

---

### Question 126
**What is agent coordination?**

A) Multiple agents working together on a task  
B) A single agent using multiple tools  
C) Agents sharing the same tools  
D) Agents executing in parallel  

**Correct Answer: A**

**Explanation:** Agent coordination refers to multiple agents collaborating, often through shared state or communication. Options B, C, and D describe different concepts.

---

### Question 127
**How do agents communicate with each other in LangGraph?**

A) Through shared state  
B) Through direct function calls  
C) Through message queues  
D) All of the above can work  

**Correct Answer: D**

**Explanation:** Agents can communicate through shared state (A), direct calls (B), or external systems like message queues (C). Shared state is the most common LangGraph approach.

---

### Question 128
**What is the difference between a single-agent and multi-agent system?**

A) Number of tools available  
B) Number of independent agent loops  
C) Complexity of state  
D) Number of nodes  

**Correct Answer: B**

**Explanation:** The key difference is the number of independent agent loops. Options A, C, and D are not the defining characteristic.

---

### Question 129
**What is a supervisor agent pattern?**

A) An agent that manages other agents  
B) An agent with elevated permissions  
C) An agent that validates results  
D) An agent that handles errors  

**Correct Answer: A**

**Explanation:** A supervisor agent coordinates and manages other agents, routing tasks and aggregating results. Options B, C, and D are not the supervisor pattern.

---

### Question 130
**How do you implement agent memory (remembering previous interactions)?**

A) Store conversation history in state  
B) Use external databases  
C) Use checkpoints  
D) All of the above  

**Correct Answer: D**

**Explanation:** All approaches work: state storage (A), external databases (B), and checkpoints (C). Often a combination is used.

---

### Question 131
**What is the purpose of agent thoughts in state?**

A) To debug agent reasoning  
B) To provide transparency into agent decision-making  
C) To store intermediate reasoning  
D) All of the above  

**Correct Answer: D**

**Explanation:** Agent thoughts serve all purposes: debugging (A), transparency (B), and storing reasoning (C). They're valuable for understanding agent behavior.

---

### Question 132
**Can agents use the output of other agents as input?**

A) No, agents are independent  
B) Yes, through state or node connections  
C) Yes, but only through files  
D) No, this creates dependencies  

**Correct Answer: B**

**Explanation:** Agents can use other agents' outputs through shared state or by connecting agent nodes in the graph. Options A, C, and D are incorrect.

---

### Question 133
**What is the typical flow of a ReAct agent?**

A) Think -> Act -> Observe -> Think...  
B) Act -> Think -> Observe  
C) Observe -> Think -> Act  
D) Think -> Observe -> Act  

**Correct Answer: A**

**Explanation:** ReAct follows: Think (reason), Act (use tool), Observe (get result), then repeat. Options B, C, and D are incorrect orders.

---

### Question 134
**How do you handle agent failures (when an agent gets stuck)?**

A) Let it run indefinitely  
B) Implement timeouts and max iterations  
C) Use a supervisor to intervene  
D) Both B and C  

**Correct Answer: D**

**Explanation:** Both timeouts/iterations (B) and supervisor intervention (C) are valid approaches. Option A is not recommended.

---

### Question 135
**What is the difference between agent actions and tool execution?**

A) Actions are decisions, tool execution is the actual call  
B) There is no difference  
C) Actions are synchronous, tools are async  
D) Actions are for planning, tools are for execution  

**Correct Answer: A**

**Explanation:** Actions are the agent's decisions (which tool to use), while tool execution is the actual function call. Options B, C, and D are incorrect.

---

## Section 9: Advanced Topics (Questions 136-150)

### Question 136
**What are subgraphs in LangGraph?**

A) Smaller versions of graphs  
B) Graphs that can be composed into larger graphs  
C) Graph templates  
D) Graph backups  

**Correct Answer: B**

**Explanation:** Subgraphs are reusable graph components that can be composed into larger graphs, promoting modularity. Options A, C, and D are incorrect.

---

### Question 137
**How do you create a subgraph?**

A) Use a special SubGraph class  
B) Create a regular graph and use it as a node  
C) Use graph composition methods  
D) Both B and C  

**Correct Answer: D**

**Explanation:** Subgraphs are created as regular graphs and then used as nodes (B) or composed using composition methods (C). Option A is not accurate.

---

### Question 138
**What is the benefit of using subgraphs?**

A) Performance improvement  
B) Code reusability and modularity  
C) Automatic error handling  
D) Built-in caching  

**Correct Answer: B**

**Explanation:** Subgraphs provide reusability and modularity, allowing you to build complex graphs from simpler components. Options A, C, and D are not primary benefits.

---

### Question 139
**Can subgraphs have their own state schemas?**

A) No, they must use the parent graph's schema  
B) Yes, but they must be compatible  
C) Yes, completely independent  
D) No, state is always shared  

**Correct Answer: B**

**Explanation:** Subgraphs can have their own schemas, but they must be compatible with the parent graph's state for composition to work. Options A, C, and D are incorrect.

---

### Question 140
**What is async execution in LangGraph?**

A) Using async/await in node functions  
B) Executing nodes concurrently  
C) Non-blocking execution  
D) All of the above  

**Correct Answer: D**

**Explanation:** Async execution involves async/await syntax (A), concurrent node execution (B), and non-blocking behavior (C). All are aspects of async execution.

---

### Question 141
**How do you make a node async?**

A) Define it as an async def function  
B) Use a special decorator  
C) Configure it in add_node()  
D) Nodes cannot be async  

**Correct Answer: A**

**Explanation:** Nodes are made async by defining them as `async def` functions. Options B, C, and D are incorrect.

---

### Question 142
**What is the benefit of async nodes?**

A) They're always faster  
B) They allow concurrent I/O operations  
C) They use less memory  
D) They're simpler to write  

**Correct Answer: B**

**Explanation:** Async nodes allow concurrent I/O operations (API calls, database queries) without blocking. They're not always faster (A), don't necessarily use less memory (C), and can be more complex (D).

---

### Question 143
**What is graph orchestration?**

A) Coordinating multiple graphs  
B) Managing graph execution and dependencies  
C) Visualizing graphs  
D) Optimizing graph performance  

**Correct Answer: B**

**Explanation:** Orchestration involves managing execution, dependencies, scheduling, and coordination of graph workflows. Options A, C, and D are aspects but not the full definition.

---

### Question 144
**What is branching and merging in graphs?**

A) Creating multiple execution paths and combining results  
B) Error handling patterns  
C) State management techniques  
D) Performance optimizations  

**Correct Answer: A**

**Explanation:** Branching creates multiple parallel paths, and merging combines their results. Options B, C, and D are different concepts.

---

### Question 145
**How do you implement parallel node execution?**

A) Use async nodes  
B) Create multiple edges from one node  
C) Use conditional edges  
D) LangGraph doesn't support parallelism  

**Correct Answer: B**

**Explanation:** Multiple edges from one node (using conditional edges that return multiple targets or using add_conditional_edges with multiple routes) enable parallel execution. Async (A) helps but isn't required. Option D is incorrect.

---

### Question 146
**What is a merge strategy?**

A) How to combine results from parallel paths  
B) How to merge state updates  
C) How to combine graphs  
D) How to merge checkpoints  

**Correct Answer: A**

**Explanation:** Merge strategies define how to combine results when multiple parallel execution paths converge. Options B, C, and D are different concepts.

---

### Question 147
**What is the difference between sequential and parallel execution?**

A) Sequential is faster  
B) Parallel executes multiple nodes simultaneously  
C) Sequential is more reliable  
D) There is no difference  

**Correct Answer: B**

**Explanation:** Parallel execution runs multiple nodes simultaneously, while sequential runs them one after another. Options A, C, and D are incorrect.

---

### Question 148
**What is state transformation?**

A) Converting state to JSON  
B) Modifying state structure between nodes  
C) Validating state  
D) Encrypting state  

**Correct Answer: B**

**Explanation:** State transformation involves changing state structure or format as it flows through the graph. Options A, C, and D are different operations.

---

### Question 149
**What are production best practices for LangGraph applications?**

A) Error handling, logging, monitoring, and checkpointing  
B) Only error handling  
C) Only logging  
D) No special practices needed  

**Correct Answer: A**

**Explanation:** Production applications should include error handling, logging, monitoring, and checkpointing for reliability. Options B, C, and D are incomplete.

---

### Question 150
**What is the recommended approach for deploying LangGraph applications?**

A) Run as standalone scripts  
B) Wrap in web frameworks (FastAPI, Flask) or use LangServe  
C) Deploy as microservices only  
D) Only use serverless functions  

**Correct Answer: B**

**Explanation:** LangGraph applications are typically wrapped in web frameworks or use LangServe for API endpoints. Options A, C, and D are too restrictive - B is the most flexible and recommended approach.

---

## Summary

This document contains 150 multiple-choice questions covering:

- **Fundamentals (1-30)**: Basic concepts, nodes, edges, state, compilation
- **Conditional Edges (31-50)**: Routing, decision-making, dynamic workflows  
- **State Management (51-70)**: TypedDict, reducers, merging, immutability
- **Error Handling (71-85)**: Exceptions, retries, timeouts, circuit breakers
- **Persistence (86-100)**: Checkpoints, SQLiteSaver, resumption, thread_ids
- **Streaming (101-110)**: Real-time updates, incremental outputs
- **Tools (111-120)**: Tool integration, agent tool use, ReAct pattern
- **Agent Patterns (121-135)**: Agent loops, multi-agent systems, coordination
- **Advanced (136-150)**: Subgraphs, async, orchestration, branching, production

Each question includes:
- Clear question text
- Four answer options (A, B, C, D)
- Correct answer identification
- Detailed explanation of why the correct answer is right
- Brief notes on why other options are incorrect

These questions are designed to test understanding from basic concepts to advanced production patterns in LangGraph.

