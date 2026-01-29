# cmd-zen

**AI-powered command-line assistant for Linux system administration**

`cmd-zen` is a Python-based CLI tool that helps you diagnose and solve Linux system administration problems using AI. Simply paste your error messages or describe your issues, and get actionable, step-by-step solutions directly in your terminal.

## Features

**AI-Powered Analysis** - Leverages OpenRouter API with DeepSeek R1 model for error diagnosis

**Focused on Linux** - Optimized for common Linux distributions (Ubuntu, Debian, RHEL, Fedora, Arch)

**Easy to Use** - Simple CLI interface with both direct and interactive modes

## Installation

### Prerequisites

- Python 3.8 or higher
- Linux operating system
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Setup

1. **Clone or download the repository**
   ```bash
   cd /home/swaruph/Workspace/cmd-zen
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the package**
   ```bash
   pip install -e .
   ```

4. **Configure your API key**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenRouter API key:
   ```bash
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

## Usage

### Quick Start

Analyze an error message directly:
```bash
cmdzen analyze "bash: docker: command not found"
```

Or without quotes for simple errors:
```bash
cmdzen analyze E: Unable to locate package nodejs
```

### Interactive Mode

For multi-line errors or complex issues, use interactive mode:
```bash
cmdzen interactive
```

Then paste your error message and press `Ctrl+D` when done.

### Examples

**Package installation error:**
```bash
cmdzen analyze "E: Unable to locate package docker-ce"
```

**Service failure:**
```bash
cmdzen analyze "Failed to start nginx.service: Unit not found"
```

**Network issue:**
```bash
cmdzen interactive
# Then paste full error output from network diagnostics
```

## How It Works

1. **Input**: You provide an error message or problem description
2. **Analysis**: The tool sends your input to OpenRouter's AI API with a specialized system prompt
3. **Solution**: AI analyzes the issue and generates step-by-step solutions
4. **Display**: Solutions are formatted beautifully in your terminal with syntax highlighting

