import json
import os
import subprocess

import aiohttp
import asyncclick as click
from dotenv import load_dotenv
from halo import Halo

from .tree import TreeGenerator

load_dotenv(".env")


@click.group()
async def dx():
    pass


@dx.command()
@click.argument("url")
@click.option("--title", default=None, help="The title of link")
async def shorten(url, title):
    """shorten url"""
    with Halo(text="Shortening.."):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://shahriyar.dev/api/shorten",
                data=json.dumps({"url": url, "title": title}),
                headers=json.dumps(
                    {"Authorization": os.environ["PORTFOLIO_AUTH_TOKEN"]}
                ),
            ) as response:
                data = await response.json()

    success = data.get("success")
    if success:
        print(f"Shortened URL: https://shahriyar.dev/links/{data['data']['text']}")
    else:
        print(f"{data['error']}")


@dx.command()
@click.option("--search", "-s", default=None, help="search query")
async def links(search):
    """show a list of shortened links"""
    with Halo(text="Loading.."):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://shahriyar.dev/api/shorten",
                headers=json.dumps(
                    {"Authorization": os.environ["PORTFOLIO_AUTH_TOKEN"]}
                ),
            ) as response:
                data = await response.json()

    def show_links():
        if not data:
            return print(f"No links found with query: {search}")

        tree = TreeGenerator(data)
        tree.generate()

    if not search:
        return show_links()

    def check_match(link):
        if search in link["url"] or search in link["text"]:
            return link

    data = list(filter(check_match, data))
    show_links()


@dx.command(name="create-repo")
@click.argument("name")
async def create_repo(name):
    if not name:
        return print("Error: repo name is required")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://api.github.com/user/repos",
            data=json.dumps(
                {
                    "name": name,
                }
            ),
            headers={"Authorization": f"token {os.environ['GITHUB_TOKEN']}"},
        ) as resp:
            data = await resp.json()
            if data.get("errors"):
                return print("Error:", data["errors"][0]["message"])
            else:
                print("Repo Created", data["html_url"])


@dx.command()
@click.option("--message", "-m", help="the commit message")
@click.option("--origin", "-o", default="main", help="the origin push")
async def push(message, origin):
    """add commit push to git in a single command"""
    subprocess.call(["git", "add", "."])
    print(subprocess.check_output(["git", "commit", "-m", message]).decode("ascii"))
    subprocess.call(["git", "push", "origin", origin])


if __name__ == "__main__":
    dx()
