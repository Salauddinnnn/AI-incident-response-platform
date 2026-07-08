import subprocess


def run_auto_heal():
    actions = []

    try:
        # Basic safe healing action for local/demo environment
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            actions.append("Docker service is reachable")
        else:
            actions.append("Docker check failed")

    except Exception as e:
        actions.append(f"Auto-heal check failed: {str(e)}")

    return actions