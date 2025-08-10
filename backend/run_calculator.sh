#!/bin/bash
# Convenience script to run the coconut calculator CLI

# Activate virtual environment
source venv/bin/activate

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo "🥥 Coconut Calculator CLI"
    echo "========================="
    echo
    echo "Available commands:"
    echo "  example       - Run the example calculation"
    echo "  interactive   - Start interactive mode"
    echo "  calculate     - Calculate with parameters"
    echo "  history       - Show calculation history"
    echo "  help          - Show detailed help"
    echo
    echo "Usage: ./run_calculator.sh [command] [options]"
    echo
    echo "Examples:"
    echo "  ./run_calculator.sh example"
    echo "  ./run_calculator.sh interactive"
    echo "  ./run_calculator.sh calculate --coconuts 5000 --price 25"
    echo "  ./run_calculator.sh help"
    exit 0
fi

# Special case for help
if [ "$1" = "help" ]; then
    python coconut_calculator_cli.py --help
    exit 0
fi

# Run the CLI with provided arguments
python coconut_calculator_cli.py "$@"