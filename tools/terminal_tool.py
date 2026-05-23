from langchain_core.tools import tool

import subprocess


@tool
def run_terminal_command(
    command: str,
    cwd: str
) -> str:
    """
    Executes terminal commands inside a workspace.

    Use for:
    - creating directories
    - creating ROS2 packages
    - touching files
    - colcon build
    - ROS2 setup commands
    """

    result = subprocess.run(

        command,

        shell=True,

        cwd=cwd,

        capture_output=True,

        text=True
    )

    return f"""

STDOUT:
{result.stdout}

STDERR:
{result.stderr}

RETURN CODE:
{result.returncode}
"""