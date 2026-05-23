from AgentState.AgentState import AgentState
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage


load_dotenv()


#GOOGLE_API_KEY="AIzaSyCX5Bz6pGhIMYWX9WwCALF8dLhMVVd5Gq0"

'''REASONER_PROMPT = """
You are the supervisor agent of an autonomous ROS2 engineering system.

Your job:
- inspect current workspace state
- decide which specialized agent should act next

Available agents:
- planner_agent
- builder_agent
- coder_agent
- runner_agent
- debugger_agent
- github_agent

Rules:
(Note these are just the Instructions, make your own logic)
1. If no plan exists:
choose planner

2. If workspace is not initialized:
choose builder

3. If files need implementation:
choose coder

4. If code is ready for validation:
choose runner

5. If build/test failed:
choose debugger

Return ONLY one word:

planner
builder
finish

coder 
runner
debugger



"""
'''

REASONER_PROMPT = """
You are the supervisor agent of an autonomous ROS2 engineering system.

Your job:
- inspect the current workspace state
- decide which agent should act next

IMPORTANT:
Currently ONLY these agents are implemented:
- planner
- builder

So NEVER return:
- coder
- runner
- debugger
- github_agent

If planning is complete AND workspace setup is complete:
return:
finish

Routing Rules:

1. If no plan exists:
return:
planner

2. If workspace is not initialized:
return:
builder

3. If planning and at least workspace initialization(just the src and the ws) are complete:
return:
finish

Return ONLY one word.

Allowed outputs:
- planner
- builder
- finish
"""

llm = ChatMistralAI(
    model="codestral-latest",
    temperature=0.2
)

def reasoner_node(state: AgentState) -> AgentState:
    # For Debugging
    print("\n===== REASONER =====")

    print("PLAN:")
    print(state.get("plan"))

    print("\nBUILD STATUS:")
    print(state.get("execution_logs"))

    print("\nWorkspace summary:")
    print(state.get("workspace_summary"))
    
    print("\nCurrent Update Happening in:")
    print(state.get("workspace_path"))



    response = llm.invoke(
        [ HumanMessage(
        content = f"""
            {REASONER_PROMPT}
        
            Current State:
            Plan:
                {state.get("plan")}

            Build_Status:
                {state.get("execution_logs")}

            Errors:
                {state.get("errors")}

            Github Commit:
                {state.get("github_summary")}

            
            
        """
        )]
    )


    next_agent = response.content.strip()
    print(next_agent)
    return {

        "next_agent":
            next_agent,

        "current_agent":
            "reasoner"
    }