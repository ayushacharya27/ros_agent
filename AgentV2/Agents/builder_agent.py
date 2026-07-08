from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_mistralai import ChatMistralAI
from AgentState.AgentState import AgentState
from tools.terminal_tool import run_terminal_command
from tools.workspace_reader import read_workspace
from tools.web_scraper import search_ros2_docs, scrape_ros2_page
from dotenv import load_dotenv

load_dotenv()

BUILDER_PROMPT = """
You are a ROS2 workspace builder agent.

NOTE: The execution environment is stateless between commands.

Your task:
- Understand the current workspace

- Decide what must be built
- Generate terminal commands step-by-step


IMPORTANT:
- Always verify official ROS2 docs using the ros2_scraper agents ALWAYS!!!!
- Never generate standalone cd commands
- Every command must be directly executable
- Use full relative paths instead
- Commands are executed independently
- Shell state does not persist between commands
- Never generate standalone source commands
- If sourcing is needed, chain it:
  source install/setup.bash && ros2 run ..

Good Commands:
[
    "mkdir -p src",
    "ros2 pkg create --build-type ament_python my_pkg --dependencies rclpy",
    "touch src/my_pkg/my_pkg/publisher_node.py",
    "colcon build"
]

Bad Commands:
[
    "cd src",
    "source install/setup.bash"
]


Rules:
- Use Python ROS2 packages only
- No launch files
- Always inspect workspace first
- Always verify official ROS2 docs using the ros2_scraper agents ALWAYS!!!!
- Generate safe and valid commands only
- DO NOT execute commands yourself
- Return commands in clean order
"""


builder_tools = [
    read_workspace,
    search_ros2_docs,
    scrape_ros2_page
]

builder_tools_by_name = {t.name: t for t in builder_tools}

builder_llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.1
).bind_tools(builder_tools)


def builder_node(state: AgentState):

    messages = state["messages"]

    # STEP 1 → LLM reasoning phase
    response = builder_llm.invoke([
        SystemMessage(content=BUILDER_PROMPT),

        *messages,

        HumanMessage(content=f"""
            Workspace path:
            {state['workspace_path']}

            User goal:
            {state['user_goal']}

            Your workflow:
            1. Read workspace
            2. Check ROS2 documentation
            3. Understand what exists
            4. Decide what needs to be created
            5. Generate terminal commands ONLY

            IMPORTANT:
            Return commands as a Python list.

            Example:
            [
                "mkdir -p src/my_pkg",
                "touch src/my_pkg/setup.py"
            ]
            """)])

    messages.append(response)

    commands_list = []

    # STEP 2 → Execute only NON-terminal tools first
    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool = builder_tools_by_name[tool_name]

            try:
                result = tool.invoke(tool_call["args"])

                print(f"\n[{tool_name}]")
                print(result)

                

                tool_msg = ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
                )

                messages.append(tool_msg)

            except Exception as e:
                print(f"Tool Error: {e}")

    # STEP 3 → Ask LLM for final commands
    final_response = builder_llm.invoke([
        SystemMessage(content="""
            Generate ONLY executable terminal commands.
            Return them as a Python list.
            Do not explain anything.
        """),

        *messages
    ])

    messages.append(final_response)

    # STEP 4 → Parse commands
    try:
        commands_list = eval(final_response.content)

    except Exception as e:
        print(f"Command parsing failed: {e}")

    # STEP 5 → Execute commands separately
    for command in commands_list:

        print(f"\n[EXECUTING] {command}")

        try:
            result = run_terminal_command.invoke({
                "command": command,
                "cwd": state["workspace_path"]
            })

            print(result)

        except Exception as e:
            print(f"Execution failed: {e}")

    return {
        "messages": messages,
        "commands_list": commands_list
    }