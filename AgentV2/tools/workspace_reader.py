from langchain_core.tools import tool
import os

IGNORE_DIRS = {
    "build",
    "install",
    "log",
    ".git",
    "__pycache__",
    "ros_env",
    "venv",
    ".venv"
}


@tool
def read_workspace(workspace_path: str) -> str:
    """
    Read concise workspace structure for agent reasoning.
    It Will give You the Workspace with proper indentation, so that if you only recieve <root_folder_name>/ this means there are no files.
    """

    try:
        output = []

        abs_path = os.path.abspath(workspace_path)

        output.append(f"Workspace Root: {abs_path}\n")

        root_name = os.path.basename(abs_path)
        output.append(f"{root_name}/")

        for item in os.listdir(workspace_path):

            if item in IGNORE_DIRS:
                continue

            full_path = os.path.join(workspace_path, item)

            if os.path.isdir(full_path):

                output.append(f"  {item}/")

                try:
                    sub_items = os.listdir(full_path)

                    for sub in sub_items[:10]:
                        output.append(f"    {sub}")

                except:
                    pass

            else:
                output.append(f"  {item}")

        return "\n".join(output)

    except Exception as e:
        return f"Failed to read workspace: {str(e)}"