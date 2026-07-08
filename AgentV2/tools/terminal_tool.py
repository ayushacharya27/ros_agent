import subprocess
from langchain_core.tools import tool


BLOCKED_COMMANDS = [
    "rm -rf /",
    "shutdown",
    "reboot",
    "mkfs",
    ":(){ :|:& };:"
]


@tool
def run_terminal_command(command: str, cwd: str) -> str:
    """
    Execute a terminal command safely.

    Args:
        command: Shell command to execute
        cwd: Working directory
    """

    try:

        # Basic safety check
        for blocked in BLOCKED_COMMANDS:
            if blocked in command:
                return f"BLOCKED COMMAND DETECTED: {blocked}"

        print(f"\n[RUNNING COMMAND]")
        print(command)

        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        output = []

        output.append(f"COMMAND:\n{command}")

        if stdout:
            output.append(f"\nSTDOUT:\n{stdout[:4000]}")

        if stderr:
            output.append(f"\nSTDERR:\n{stderr[:4000]}")

        output.append(f"\nEXIT CODE: {result.returncode}")

        if result.returncode == 0:
            output.append("STATUS: SUCCESS")
        else:
            output.append("STATUS: FAILED")

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "FAILED: Command timed out after 60 seconds."

    except Exception as e:
        return f"FAILED: {str(e)}"