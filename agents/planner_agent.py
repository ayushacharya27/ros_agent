from AgentState.AgentState import AgentState
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from dotenv import load_dotenv
from pydantic import BaseModel # Coz LLM Returns in Markdown Format





class PlannerOutput(BaseModel):

    plan: list[str]



load_dotenv()


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.2
)

'''llm = ChatOllama(

    model="qwen3:8b",
    keep_alive="5m",

    temperature=0
)'''

PLANNER_PROMPT = """
You are a ROS2 software planning agent.

Your responsibilities:
- Break user goals into HIGH-LEVEL structured tasks
- Identify required files
- Determine important file dependencies
- Plan the architecture flow only

IMPORTANT RULES:

1. Do NOT create overly detailed plans
Bad Example:
- write import statements
- create class
- define callback

Good Example:
- Create Directory

- Create ROS2 node
- Implement LiDAR processing


2. If workspace_summary is empty:
Start by planning:
- workspace creation
- ROS2 package creation
- sourcing/setup steps
- directory structure

Then Only Go to Code Files Creation and Running Scripts, like overwrite(OR MAYBE Remove Plans which are done) the Plans if you see the workspace_summary is enough to start Coding.



3. Use Python for all implementations.



4. Return concise and practical plans.

5. Do NOT generate implementation/code.
Only planning.




Return ONLY valid JSON.

Format:

{
    "plan": [
        "task1",
        "task2"
    ]
}


"""

def planner_node(state: AgentState) -> AgentState:
    """ This Node is to Plan Out the Before the Actual Implementation Begins.
    It Subdivides the Goal into Multiple 
    """

    
    user_goal = state["user_goal"]
    work_space_summary = state["workspace_summary"]

    structured_llm = llm.with_structured_output(PlannerOutput)


    parsed = structured_llm.invoke(
        [
            HumanMessage(
                content = f"""
                {PLANNER_PROMPT}

                USER GOAL:
                {user_goal}

                WORK_SPACE SUMMARY:
                {work_space_summary}
            """
            )
        ]
    )

    
    return {

    "plan": parsed.plan,

    "current_task":
        parsed.plan[0],

    "current_task_completed":
        False,

    "current_agent":
        "planner"
}