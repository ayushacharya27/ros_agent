import subprocess


def run_terminal_command(
    command: str,
    cwd: str | None = None
):

    try:

        result = subprocess.run(

            command,

            shell=True,

            cwd=cwd,

            capture_output=True,

            text=True

        )

        return {

            "success":
                result.returncode == 0,

            "stdout":
                result.stdout,

            "stderr":
                result.stderr,

            "return_code":
                result.returncode
        }

    except Exception as e:

        return {

            "success": False,

            "stderr": str(e)
        }