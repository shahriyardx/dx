from rich import print

PIPE = "[bold green]│[/bold green]"
ELBOW = "[bold green]└──[bold green]"
TEE = "[bold green]├──[bold green]"
PIPE_PREFIX = "[bold green]│[bold green]   "
SPACE_PREFIX = "    "


class TreeGenerator:
    def __init__(self, links):
        self.links = links

    def generate(self):
        print(PIPE)

        for link in self.links:
            print(TEE, f'[bold blue]{link["text"]}[/bold blue]')
            print(PIPE_PREFIX, TEE, link["url"])
            print(
                PIPE_PREFIX,
                ELBOW,
                f'[bold green]https://shahriyar.dev/links/{link["text"]}[/bold green]',
            )

        print(ELBOW, "[bold red]END[/bold red]")
