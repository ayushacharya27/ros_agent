from langchain.tools import tool
from duckduckgo_search import DDGS


@tool
def search_ros_docs(query: str):
    """
    Searches the web for ROS2-related documentation,
    tutorials, examples, and package references.

    Use this tool when:
    - ROS2 package structure is unclear
    - launch/system conventions are needed
    - API usage/examples are required
    - workspace setup guidance is needed

    Prefer:
    - official ROS2 documentation
    - GitHub repositories
    - ROS2 examples

    Avoid:
    - ROS1 resources
    - outdated tutorials
    - unrelated robotics frameworks
    """

    results = []

    with DDGS() as ddgs:

        for r in ddgs.text(

            query,

            max_results=5
        ):

            results.append(r["body"])

    return "\n".join(results)