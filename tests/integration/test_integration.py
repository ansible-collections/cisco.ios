import subprocess

import pytest


def run(ansible_project, environment):
    __tracebackhide__ = True
    args = [
        "ansible-navigator",
        "run",
        str(ansible_project.playbook),
        "-i",
        str(ansible_project.inventory),
        "--ee",
        "false",
        "--mode",
        "stdout",
        "--pas",
        str(ansible_project.playbook_artifact),
        "--ll",
        "debug",
        "--lf",
        str(ansible_project.log_file),
        "-vvv",
    ]
    process = subprocess.run(
        args=args,
        env=environment,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        check=False,
        shell=False,
    )
    if process.returncode:
        print(process.stdout.decode("utf-8"))
        print(process.stderr.decode("utf-8"))

        pytest.fail(reason=f"Integration test failed: {ansible_project.role}")


def test_integration(ansible_project, environment):
    run(ansible_project, environment)
