from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages




class AgentState(TypedDict):

    # Its for storing the HumanMessages or AIMessages
    messages: Annotated[list[AnyMessage], add_messages]

    # Ultimately what have to be achieved
    user_goal: str
    
    # Path is Important Initially
    workspace_path: str

    commands_list: list[str]

    


    