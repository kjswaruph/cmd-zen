"""Response formatting utilities for terminal output."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from rich import box


console = Console()


def print_header():
    """Print the application header."""
    header = Text()
    header.append("cmd", style="bold cyan")
    header.append("zen", style="bold magenta")
    header.append(" - AI-Powered Linux Assistant", style="dim")
    console.print(header)
    console.print()


def print_error(message: str):
    """
    Print an error message.
    
    Args:
        message: Error message to display
    """
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_warning(message: str):
    """
    Print a warning message.
    
    Args:
        message: Warning message to display
    """
    console.print(f"[bold yellow]Warning:[/bold yellow] {message}")


def print_success(message: str):
    """
    Print a success message.
    
    Args:
        message: Success message to display
    """
    console.print(f"[bold green]✓[/bold green] {message}")


def print_info(message: str):
    """
    Print an info message.
    
    Args:
        message: Info message to display
    """
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def format_solution(solution: str):
    """
    Format and print the AI-generated solution.
    
    Args:
        solution: The solution text from the AI
    """
    console.print()
    console.print(Panel(
        Markdown(solution),
        title="[bold cyan]Solution[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    ))
    console.print()


def show_loading(message: str = "Analyzing..."):
    """
    Create a loading spinner context.
    
    Args:
        message: Loading message to display
        
    Returns:
        Live context manager for the spinner
    """
    spinner = Spinner("dots", text=message, style="cyan")
    return Live(spinner, console=console, transient=True)


def print_input_prompt(prompt_text: str = "Describe your error or issue") -> str:
    """
    Print a styled input prompt.
    
    Args:
        prompt_text: The prompt text to display
        
    Returns:
        User input
    """
    return console.input(f"[bold cyan]?[/bold cyan] {prompt_text}: ")


def print_multiline_prompt():
    """Print instructions for multi-line input."""
    console.print()
    console.print("[bold cyan]Interactive Mode[/bold cyan]")
    console.print("Paste your error message or describe your issue.")
    console.print("Press [bold]Ctrl+D[/bold] (or [bold]Ctrl+Z[/bold] on Windows) when done.")
    console.print("─" * 60)
    console.print()
