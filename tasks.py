from pathlib import Path

from invoke import Context, task

MAIN_DIRECTORY_PATH = Path(__file__).parent


@task
def format(context: Context):
    """Run RUFF to format all Python files."""

    exec_cmds = ["ruff format .", "ruff check . --fix"]
    with context.cd(MAIN_DIRECTORY_PATH):
        for cmd in exec_cmds:
            context.run(cmd)


@task
def lint_mypy(context: Context):
    """Run Linter to check all Python files."""
    print(" - Check code with mypy")
    exec_cmd = "mypy --show-error-codes nornir_dispatch"
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task
def lint_ruff(context: Context):
    """Run Linter to check all Python files."""
    print(" - Check code with ruff")
    exec_cmd = "ruff check ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="lint")
def lint(context: Context):
    """Run all linters."""
    lint_ruff(context)
    lint_mypy(context)


@task(name="tests")
def tests(context: Context):
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run("pytest -v ./tests/")
