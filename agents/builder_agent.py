from pydantic import BaseModel
from AgentState.AgentState import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
from tools.terminal_tool import run_terminal_command
from tools.web_tool import search_ros_docs


load_dotenv()

class BuilderOutput(BaseModel):
    commands: list[str] 
    workspace_path: str
    workspace_summary: str 


llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    temperature=0.2
)
llm = llm.bind_tools([
    search_ros_docs
])
structured_builder_llm = llm.with_structured_output(BuilderOutput)

BUILDER_PROMPT = """You are a ROS2 workspace builder agent.
Use the search tool ONLY for ROS2-related information.
Prefer official ROS2 conventions.
Avoid ROS1 examples.

Go one by one, like do all things to be done in src, or root folder, then go to the pkg etc...., dont do everything at once.

Your responsibilities:
- Initialize the workspace
- Create directories and required files
- Setup ROS2 package structure
- Dont Create Launch File, I dont want to Use it anyways now, build all other files also use colcon build at root too

NOTE: Use the WorkSpace Summary to See what has been done, dont wait to see the Directory Yourself.
IMPORTANT RULES:
1. You MUST output a list of exact terminal commands to perform these actions.
2. Do NOT generate or write Python/C++ code logic inside these commands.
3. Your job is ONLY workspace setup and filesystem preparation.
4. Keep execution efficient and minimal. Avoid unnecessary commands.
5. Provide an 'workspace_path' where these commands are gonna implemnted.

6. Finally Provide a WorkSpace Summary like what you did in current Iteration, like all files,so that the planner/resoner agent know ok these files are done.
"""

def builder_node(state: AgentState):
    workspace_path = state.get("workspace_path", "./")
    
    workspace_summary = state.get("workspace_summary")

    ros_context = search_ros_docs.invoke(
    "ROS2 Python Package Creation and Directory Creation"
    )   

    parsed = structured_builder_llm.invoke([
        SystemMessage(content=BUILDER_PROMPT),
        HumanMessage(content=f"Ros Context: {ros_context}\nWorkspace Summary: {workspace_summary}\nCurrent Workspace Path: {workspace_path}\n")
    ])

    actual_terminal_logs = []
    workspace_path = parsed.workspace_path

    print("\n===== BUILDER =====")
    print("\nCOMMANDS TO BE DONE")
    print(parsed.commands)
    print("\n===== BUILDER END =====")

    for command in parsed.commands:
        try:
            result = run_terminal_command.invoke({
                "command": command,
                "cwd": workspace_path
            })
            actual_terminal_logs.append(f"$ {command}\n{result}")
        except Exception as e:
            actual_terminal_logs.append(f"$ {command}\nFAILED: {str(e)}")
            break

        #parsed.commands.clear()

    return {

    "execution_logs":
        actual_terminal_logs,

    "workspace_summary":
        parsed.workspace_summary,

    "current_agent":
        "builder"
}