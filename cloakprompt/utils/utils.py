import logging

from cloakprompt.core.redactor import TextRedactor
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.console import Group
from typing import Optional

def print_banner(console):
    """Print the application banner."""
    banner_text = Text("🔒 CLOAKPROMPT", style="bold blue")
    subtitle_head = Text("Secure text redaction for LLM interactions", style="dim")
    subtitle_tail = Text("By Kushagra Tandon", style="dim italic")

    content = Group(
        banner_text,
        subtitle_head,
        Align.right(subtitle_tail)
    )

    console.print(Panel(
        content,
        border_style="blue",
        padding=(1, 2)
    ))


def print_summary(console, redactor: TextRedactor, custom_config: Optional[str] = None):
    """Print a summary of available redaction patterns."""
    try:
        summary = redactor.get_pattern_summary(custom_config)

        table = Table(title="Redaction Patterns Summary", show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Pattern Count", justify="right", style="green")

        for category, count in summary['categories'].items():
            table.add_row(category, str(count))

        console.print(table)
        console.print(f"\nTotal patterns: {summary['total_patterns']}")

    except Exception as e:
        console.print(f"[yellow]Warning: Could not load pattern summary: {e}[/yellow]")


def setup_logging(verbose: bool = False, quiet: bool = False):
    """Configure logging based on verbosity flags."""
    if quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)