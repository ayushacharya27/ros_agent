from langgraph.graph import StateGraph, START, END
from AgentState.AgentState import AgentState
from agents.reasoner_agent import reasoner_node
from agents.planner_agent import planner_node
from agents.builder_agent import builder_node


# For Conditional Routing
def route_next_agent(state: AgentState) -> AgentState:

    return state["next_agent"]

graph = StateGraph(AgentState)

graph.add_node("reasoner", reasoner_node)
graph.add_node("planner", planner_node)
graph.add_node("builder", builder_node)
graph.set_entry_point("reasoner")

graph.add_conditional_edges(
    "reasoner",
    route_next_agent,
    {
        "planner":"planner",
        "builder": "builder",
        "finish": END
    }
)

graph.add_edge(
    "planner",
    "reasoner"
)
graph.add_edge(
    "builder",
    "reasoner"
)

workflow = graph.compile()


