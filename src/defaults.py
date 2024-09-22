"""
Here are located some global variales that are shared between packages.py and
fdroid_auto.py
"""

from rich.style import Style
from rich.console import Console

ERROR_STYLE = Style.parse("bold red")
SUCCESS_STYLE = Style.parse("bold green")
CONSOLE = Console()
