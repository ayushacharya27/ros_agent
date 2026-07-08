from AgentState.AgentState import AgentState
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
from tools.web_scraper import search_ros2_docs, scrape_ros2_page
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

# LLM Definition

builder_tools = [
    search_ros2_docs,
    scrape_ros2_page
]

'''planner_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
).bind_tools(builder_tools)'''


planner_llm = ChatMistralAI(
    model="codestral-latest",
    temperature=0.2
).bind_tools(builder_tools)


PLANNER_PROMPT = """
You are a ROS2 planning agent.



Your job is to read the user's goal and create a high-level plan.
Path is Given to You

RULES:
1. Return a high-level plan only — no code, no implementation details
2. Use Python for all ROS2 implementations
3. Each task should be one clear action

Good plan example for "create a ROS2 publisher node":
- Initialize ROS2 workspace at ~/ros2_ws
- Create ROS2 Python package called my_pkg  
- Create publisher node file
- Build workspace with colcon
- Verify build succeeded

Bad plan example:
- Write import statements
- Define __init__
- Call rclpy.init()
- Create node class
- Define timer callback

Write the plan as a simple numbered list.
Nothing else.
"""


def planner_node(state: AgentState):
    response = planner_llm.invoke([
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=f"User Goal: {state['user_goal']}\nWorkspace path: {state['workspace_path']}")
    ])
    
    return {"messages": [response]}
