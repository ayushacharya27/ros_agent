import os
from AgentState.AgentState import AgentState
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel # Coz LLM Returns in Markdown Format





class PlannerOutput(BaseModel):

    plan: list[str]

    pending_files: list[str]

    file_dependencies: dict[str, list[str]]


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

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
- Create ROS2 node
- Implement LiDAR processing


2. If workspace_summary is empty:
Start by planning:
- workspace creation
- ROS2 package creation
- sourcing/setup steps
- directory structure

3. Do NOT include package.xml in pending_files.
Assume dependencies will mostly be handled using:
- colcon build
- setup.py

4. Use Python for all implementations.

5. Generate only meaningful architectural files.

6. Return concise and practical plans.

7. Do NOT generate implementation/code.
Only planning.


Return ONLY valid JSON.

Format:

{
    "plan": [
        "task1",
        "task2"
    ],

    "pending_files": [
        "file1",
        "file2"
    ],

    "file_dependencies": {
        "file": ["dependency"]
    }
}
"""

def planner_node(state: AgentState) -> AgentState:
    """ This Node is to Plan Out the Before the Actual Implementation Begins.
    It Subdivides the Goal into Multiple 
    """

    
    user_goal = state["user_goal"]

    structured_llm = llm.with_structured_output(PlannerOutput)


    parsed = structured_llm.invoke(
        [
            HumanMessage(
                content = f"""
                {PLANNER_PROMPT}

                USER GOAL:
                {user_goal}
            """
            )
        ]
    )

    
    return {

    "plan": parsed.plan,

    "pending_files": parsed.pending_files,

    "file_dependencies":
        parsed.file_dependencies,

    "current_task":
        parsed.plan[0],

    "current_task_completed":
        False,

    "current_agent":
        "planner"
}