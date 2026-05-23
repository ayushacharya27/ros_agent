from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages



class AgentState(TypedDict):

    messages: Annotated[list[AnyMessage], add_messages]

    # files: Annotated[dict[str, str], update_files] I dont think we Need this

    # Initial/Complete Goal
    user_goal: str

    # Github Agent
    github_commands: list[str]
    github_summary: str

    # Debugger Agent
    pending_files: list[str] # Will Remove it One by One
    completed_files: list[str] # Once the Files Debugger tells okay
    validation_passed: bool
    build_logs: list[str]
    errors: list[str]

    # For Planner Agent
    plan: list[str]
    current_task: str # Adding this So that the Planner Agent Knows what to do next
    current_task_completed: bool # Is the Current Task Completed
    file_dependencies: dict[str, list[str]] # Taken Up By the Builder Agent

    # Directory/Builder Agent 
    build_logs: list[str] # Like it'll say that what all is done or not
     
    
    # Coder Agent
    current_file: str
    current_code: str
    current_file_context: str # Maybe We Need this

    # Summaries
    workspace_summary: str
    code_summary: str
    
    current_agent: str # IDK It'll be used or not
    workspace_path: str # IMPORTANT

    next_agent: str # Change in Plans, Now ill build a Reasoner agent whic diverts the flow of the Program 
    