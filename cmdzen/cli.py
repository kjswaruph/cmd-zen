"""Command-line interface for cmd-zen."""

import sys
import click
from typing import Optional

from .ai_client import OpenRouterClient
from .formatter import (
    print_header,
    print_error,
    print_success,
    print_info,
    format_solution,
    show_loading,
    print_multiline_prompt,
    console
)


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def cli(ctx, version):
    """
    cmd-zen: AI-powered Linux system administration assistant.
    
    Analyze command-line errors and system issues to get actionable solutions.
    """
    if version:
        from . import __version__
        click.echo(f"cmd-zen version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument('error_message', nargs=-1, required=False)
def analyze(error_message):
    """
    Analyze an error message or system issue.
    
    Usage:
        cmdzen analyze "error message here"
        cmdzen analyze error message without quotes
    
    Examples:
        cmdzen analyze "bash: docker: command not found"
        cmdzen analyze E: Unable to locate package nodejs
    """
    print_header()
    
    if error_message:
        error_text = ' '.join(error_message)
    else:
        print_error("No error message provided.")
        print_info("Usage: cmdzen analyze \"your error message\"")
        print_info("Or use: cmdzen interactive")
        sys.exit(1)
    
    if not error_text.strip():
        print_error("Error message cannot be empty.")
        sys.exit(1)
    
    try:
        console.print(f"[dim]Analyzing:[/dim] {error_text[:100]}{'...' if len(error_text) > 100 else ''}")
        console.print()
        
        # Create AI client and analyze
        client = OpenRouterClient()
        
        with show_loading("Consulting AI assistant..."):
            solution = client.analyze_error(error_text)
        
        # Display the solution
        format_solution(solution)
        print_success("Analysis complete!")
        
    except ValueError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to analyze error: {str(e)}")
        sys.exit(1)


@cli.command()
def interactive():
    """
    Interactive mode for multi-line error messages.
    
    Allows you to paste long error messages or describe complex issues.
    Press Ctrl+D (or Ctrl+Z on Windows) when finished.
    """
    print_header()
    print_multiline_prompt()
    
    try:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        error_text = '\n'.join(lines).strip()
        
        if not error_text:
            print_error("No input provided.")
            sys.exit(1)
        
        console.print()
        console.print("[dim]Processing your input...[/dim]")
        console.print()
        
        # Create AI client and analyze
        client = OpenRouterClient()
        
        with show_loading("Consulting AI assistant..."):
            solution = client.analyze_error(error_text)
        
        # Display the solution
        format_solution(solution)
        print_success("Analysis complete!")
        
    except KeyboardInterrupt:
        console.print()
        print_info("Cancelled by user.")
        sys.exit(0)
    except ValueError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to analyze error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
