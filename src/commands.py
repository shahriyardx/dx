import json

import aiohttp
import asyncclick as click
from dotenv import load_dotenv
from pyperclip import copy

from src.libs.aliases import ClickAliasedGroup

from .git import get_or_save_token
from .utils import get_current_branch, run_command

load_dotenv(".env")


@click.group(cls=ClickAliasedGroup)
async def dx():
    pass


@dx.command(name="git-init", aliases=["gi"])
@click.option("--files", "-f", default=".", help="files to add")
@click.option("--origin", "-o", default=None, help="origin url")
@click.option("--branch", "-b", default="main", help="default branch")
@click.option("--message", "-m", default=None, help="initial commit message")
async def git_init(files, origin, branch, message):
    run_command(["git", "init"])
    run_command(["git", "add", files])

    if branch:
        run_command(["git", "branch", "-M", branch])

    if origin:
        run_command(["git", "remote", "add", "origin", origin])

    if message:
        run_command(["git", "commit", "-m", message])


@dx.command(name="create-repo", aliases=["cr"])
@click.argument("name")
@click.option("--token", "-t", help="token", default=None)
async def create_repo(name, token):
    if not name:
        return print("Error: repository name name is required")

    token = get_or_save_token(token)
    if not token:
        return print(
            "Error: Token is not set, please use the --token flag to provide a token"
        )

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.github.com/user/repos",
            data=json.dumps(
                {
                    "name": name,
                }
            ),
            headers={"Authorization": f"token {token}"},
        ) as resp:
            data = await resp.json()
            if resp.status == 401 or resp.status == 403:
                return print(f"Error: {data['message']}")

            if data.get("errors"):
                return print(f"Error: {data['errors'][0]['message']}")

            copy(data["html_url"])
            print("Repo Created", data["html_url"])


@dx.command(name="delete-repo", aliases=["dr"])
@click.argument("name")
@click.option("--token", "-t", help="token", default=None)
async def delete_repo(name, token):
    if not name:
        return print("Error: repository name name is required")

    token = get_or_save_token(token)
    if not token:
        return print(
            "Error: Token is not set, please use the --token flag to provide a token"
        )

    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"https://api.github.com/repos/{name}",
            headers={"Authorization": f"token {token}"},
        ) as resp:
            if resp.status == 204:
                print("Repository deleted")
            elif resp.status == 403:
                print("Missing permission to delete this repository")
            elif resp.status == 404:
                print("Repository not found")
            else:
                print("Unknown error has occured")


@dx.command()
@click.option("--message", "-m", help="the commit message")
@click.option("--origin", "-o", help="the origin push")
async def push(message, origin):
    """add commit push to git in a single command"""
    if not origin:
        origin = get_current_branch()

    run_command(["git", "add", "."], "call")
    run_command(["git", "commit", "-m", message], "check_output")
    run_command(["git", "push", "-u", "origin", origin], "call")


if __name__ == "__main__":
    dx()
