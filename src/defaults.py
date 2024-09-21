from rich.style import Style
from rich.console import Console
from rich.theme import Theme

ERROR_STYLE = Style.parse("bold red")
SUCCESS_STYLE = Style.parse("bold green")

CUSTOM_THEME = Theme({
    "info": "dim cyan",
    "error": "bold red",
    "success": "bold green"
        })

CONSOLE = Console(theme=CUSTOM_THEME)
