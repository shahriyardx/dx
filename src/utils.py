import subprocess


def run_command(commands, type="check_output"):
    try:
        if type == "check_output":
            print(subprocess.check_output(commands).decode("ascii"))

        if type == "call":
            subprocess.call(commands)
    except Exception as e:
        print(e)


def get_current_branch(repo_path="."):
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None
