#!/usr/bin/env python3
"""
CLI entry point for cloakprompt.

A command-line tool for redacting sensitive information from text before sending to LLMs.
"""

import logging
import os
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from cloakprompt.core.parser import ConfigParser
from cloakprompt.utils.utils import setup_logging, print_banner, print_summary
from cloakprompt.core.redactor import TextRedactor
from cloakprompt.utils.file_loader import InputLoader

# Initialize Typer app
app = typer.Typer(
    name="cloakprompt",
    help="Redact sensitive information from text before sending to LLMs",
    add_completion=False
)

# Initialize Rich console
console = Console()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.command()
def redact(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to redact"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="File to redact"),
    stdin: bool = typer.Option(False, "--stdin", help="Read from stdin"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Custom configuration file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output except errors"),
    summary: bool = typer.Option(False, "--summary", "-s", help="Show pattern summary and exit"),
    details: bool = typer.Option(True, "--details", "-d", help="Show detailed redaction information")
):
    """
    Redact sensitive information from text, files, or stdin.
    
    Examples:
        cloakprompt redact --text "my secret key is AKIA1234567890ABCDEF"
        cloakprompt redact --file config.log
        echo "secret data" | cloakprompt redact --stdin
        cloakprompt redact --file app.log --config security.yaml
    """
    try:
        # Setup logging
        setup_logging(verbose, quiet)
        
        # Print banner (unless quiet mode)
        if not quiet:
            print_banner(console)
        
        # Initialize components
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            disable=quiet
        ) as progress:
            task_id = progress.add_task("Initializing redactor...", total=None)
            
            config_parser = ConfigParser()
            redactor = TextRedactor(config_parser)
            
            progress.update(task_id, description="Redactor ready")
        
        # Show pattern summary if requested
        if summary:
            if not quiet:
                print_summary(console, redactor, config)
            return
        
        # Load input
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                disable=quiet
            ) as progress:
                progress.add_task("Loading input...", total=None)
                
                input_text = InputLoader.load_input(
                    text=text,
                    file_path=file,
                    use_stdin=stdin
                )
                
                progress.update(task_id, description="Input loaded")
                
        except Exception as e:
            console.print(f"[red]Error loading input: {e}[/red]")
            raise typer.Exit(1)
        
        # Perform redaction
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                disable=quiet
            ) as progress:
                progress.add_task("Redacting sensitive information...", total=None)
                
                if details:
                    result = redactor.redact_with_details(input_text, config)
                    redacted_text = result['redacted_text']
                    redactions = result['redactions']
                    total_redactions = result['total_redactions']
                    if file is not None:
                        file_name, file_extension = os.path.splitext(file)
                        with open(f"{file_name}_redacted{file_extension}", 'w', encoding='utf-8') as file:
                            file.write(redacted_text)
                else:
                    redacted_text = redactor.redact_text(input_text, config)
                    redactions = []
                    total_redactions = 0
                
                progress.update(task_id, description="Redaction complete")
                
        except Exception as e:
            console.print(f"[red]Error during redaction: {e}[/red]")
            raise typer.Exit(1)
        
        # Output results
        if not quiet:
            if total_redactions > 0:
                console.print(f"[green]✓ Redacted {total_redactions} sensitive items[/green]")
            else:
                console.print("[yellow]ℹ No sensitive information found[/yellow]")
        
        # Print redacted text to stdout
        if not quiet and not file:
            logger.info(f"Redacted {total_redactions} sensitive items from text")
            print(redacted_text)
        elif file and not quiet:
            print(f'Redaction completed successfully. Check the directory {os.path.dirname(file_name)}.')
        
        # Show detailed information if requested
        if details and redactions and not quiet:
            console.print("\n[bold]Redaction Details:[/bold]")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Pattern", style="cyan")
            table.add_column("Position", style="green")
            table.add_column("Replacement", style="yellow")
            
            for redaction in redactions:
                position = f"{redaction['start_pos']}-{redaction['end_pos']}"
                table.add_row(
                    redaction['pattern_name'],
                    position,
                    redaction['replacement']
                )
            
            console.print(table)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        raise typer.Exit(130)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Unexpected error: {e}[/red]")
        logger.exception("Unexpected error occurred")
        raise typer.Exit(1)


@app.command()
def patterns(
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Custom configuration file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Show available redaction patterns."""
    try:
        setup_logging(verbose)
        print_banner(console)
        
        config_parser = ConfigParser()
        redactor = TextRedactor(config_parser)
        
        print_summary(console, redactor, config)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def version():
    """Show version information."""
    console.print("🔒 CloakPrompt v1.0.0")
    console.print("Secure text redaction for LLM interactions")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
