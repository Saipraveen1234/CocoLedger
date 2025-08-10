#!/usr/bin/env python3
"""
Coconut Calculator CLI - Command Line Interface for testing coconut calculations.
"""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich import box

from app.models.calculation import CalculationInput
from app.services.calculation_service import CoconutCalculationService

console = Console()
calculation_service = CoconutCalculationService()


def print_banner():
    """Print application banner."""
    banner = Text("🥥 Coconut Calculator CLI 🥥", style="bold green")
    console.print(Panel(banner, box=box.DOUBLE, padding=(1, 1)))


def print_calculation_result(result):
    """Print calculation result in a beautiful format."""
    # Create summary table
    summary_table = Table(title="📊 Calculation Summary", box=box.ROUNDED)
    summary_table.add_column("Metric", style="cyan", no_wrap=True)
    summary_table.add_column("Value", style="magenta")
    
    summary_table.add_row("Total Coconuts", f"{result.input_data.total_coconuts:,}")
    summary_table.add_row("Price per Coconut", f"₹{result.input_data.price_per_coconut:.2f}")
    summary_table.add_row("Wastage Coconuts", f"{result.wastage_coconuts:,}")
    summary_table.add_row("Sellable Coconuts", f"{result.sellable_coconuts:,}")
    summary_table.add_row("Gross Revenue", f"₹{result.gross_revenue:,.0f}")
    summary_table.add_row("Tax Amount", f"₹{result.tax_amount:,.0f}")
    summary_table.add_row("Labor Cost", f"₹{result.labor_cost:,.0f}")
    summary_table.add_row("Net Profit", f"₹{result.net_profit:,.0f}", style="bold green")
    summary_table.add_row("Profit Margin", f"{result.profit_margin_percentage:.2f}%", style="bold yellow")
    
    console.print()
    console.print(summary_table)
    
    # Create detailed breakdown table
    breakdown_table = Table(title="📋 Calculation Breakdown", box=box.ROUNDED)
    breakdown_table.add_column("Step", style="cyan", width=4)
    breakdown_table.add_column("Description", style="yellow")
    breakdown_table.add_column("Calculation", style="white")
    breakdown_table.add_column("Result", style="green", justify="right")
    
    for step in result.calculation_steps:
        breakdown_table.add_row(
            str(step.step),
            step.description,
            step.calculation,
            f"₹{step.result:,.0f}" if step.step >= 3 else f"{step.result:,.0f}"
        )
    
    console.print()
    console.print(breakdown_table)


def get_input_interactive():
    """Get calculation input interactively from user."""
    console.print("\n[bold cyan]Enter Calculation Parameters:[/bold cyan]")
    
    total_coconuts = IntPrompt.ask(
        "Total number of coconuts",
        default=10000
    )
    
    price_per_coconut = FloatPrompt.ask(
        "Price per coconut (₹)",
        default=20.0
    )
    
    # Advanced settings with defaults
    console.print("\n[dim]Advanced Settings (press Enter for defaults):[/dim]")
    
    wastage_percentage = FloatPrompt.ask(
        "Wastage percentage",
        default=2.2
    )
    
    tax_percentage = FloatPrompt.ask(
        "Tax percentage",
        default=1.0
    )
    
    labor_percentage = FloatPrompt.ask(
        "Labor percentage",
        default=11.0
    )
    
    return CalculationInput(
        total_coconuts=total_coconuts,
        price_per_coconut=price_per_coconut,
        wastage_percentage=wastage_percentage,
        tax_percentage=tax_percentage,
        labor_percentage=labor_percentage
    )


def print_history():
    """Print calculation history."""
    history = calculation_service.get_calculations_history()
    
    if not history:
        console.print("\n[yellow]No calculations in history.[/yellow]")
        return
    
    history_table = Table(title="📚 Calculation History", box=box.ROUNDED)
    history_table.add_column("Date", style="cyan")
    history_table.add_column("Coconuts", style="yellow", justify="right")
    history_table.add_column("Price/Unit", style="white", justify="right")
    history_table.add_column("Gross Revenue", style="blue", justify="right")
    history_table.add_column("Net Profit", style="green", justify="right")
    history_table.add_column("Margin %", style="magenta", justify="right")
    
    for calc in history:
        history_table.add_row(
            calc.created_at.strftime("%Y-%m-%d %H:%M"),
            f"{calc.total_coconuts:,}",
            f"₹{calc.price_per_coconut:.2f}",
            f"₹{calc.gross_revenue:,.0f}",
            f"₹{calc.net_profit:,.0f}",
            f"{calc.profit_margin_percentage:.1f}%"
        )
    
    console.print()
    console.print(history_table)


@click.group()
def cli():
    """Coconut Calculator CLI - Calculate profits for coconut vendors."""
    print_banner()


@cli.command()
@click.option('--coconuts', '-c', type=int, help='Total number of coconuts')
@click.option('--price', '-p', type=float, help='Price per coconut in rupees')
@click.option('--wastage', '-w', type=float, default=2.2, help='Wastage percentage (default: 2.2)')
@click.option('--tax', '-t', type=float, default=1.0, help='Tax percentage (default: 1.0)')
@click.option('--labor', '-l', type=float, default=11.0, help='Labor percentage (default: 11.0)')
def calculate(coconuts, price, wastage, tax, labor):
    """Calculate coconut vendor profit."""
    try:
        if coconuts is None or price is None:
            # Interactive mode
            input_data = get_input_interactive()
        else:
            # Command line mode
            input_data = CalculationInput(
                total_coconuts=coconuts,
                price_per_coconut=price,
                wastage_percentage=wastage,
                tax_percentage=tax,
                labor_percentage=labor
            )
        
        # Validate input
        errors = calculation_service.validate_input(input_data)
        if errors:
            console.print("\n[bold red]Validation Errors:[/bold red]")
            for error in errors:
                console.print(f"❌ {error}")
            return
        
        # Perform calculation
        result = calculation_service.calculate(input_data)
        
        # Display result
        print_calculation_result(result)
        
        console.print(f"\n[dim]Calculation ID: {result.calculation_id}[/dim]")
        
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")


@cli.command()
def history():
    """Show calculation history."""
    print_history()


@cli.command()
def example():
    """Run example calculation (from your specification)."""
    console.print("\n[bold cyan]Running Example Calculation:[/bold cyan]")
    console.print("Coconuts = 10,000 nuts")
    console.print("Price = ₹20 per coconut")
    console.print("Wastage = 2.2%, Tax = 1%, Labor = 11%")
    
    input_data = CalculationInput(
        total_coconuts=10000,
        price_per_coconut=20.0,
        wastage_percentage=2.2,
        tax_percentage=1.0,
        labor_percentage=11.0
    )
    
    result = calculation_service.calculate(input_data)
    print_calculation_result(result)
    
    # Verify against expected result
    expected_net_profit = 192544
    actual_net_profit = result.net_profit
    
    console.print(f"\n[bold]Verification:[/bold]")
    console.print(f"Expected Net Profit: ₹{expected_net_profit:,}")
    console.print(f"Calculated Net Profit: ₹{actual_net_profit:,.0f}")
    
    if abs(actual_net_profit - expected_net_profit) < 1:
        console.print("[bold green]✅ Calculation matches expected result![/bold green]")
    else:
        console.print("[bold red]❌ Calculation doesn't match expected result![/bold red]")


@cli.command()
def interactive():
    """Start interactive calculation mode."""
    while True:
        try:
            console.print("\n" + "="*50)
            input_data = get_input_interactive()
            
            # Validate and calculate
            errors = calculation_service.validate_input(input_data)
            if errors:
                console.print("\n[bold red]Validation Errors:[/bold red]")
                for error in errors:
                    console.print(f"❌ {error}")
                continue
            
            result = calculation_service.calculate(input_data)
            print_calculation_result(result)
            
            # Ask if user wants to continue
            continue_calc = Prompt.ask(
                "\nDo you want to perform another calculation?",
                choices=["y", "n"],
                default="y"
            )
            
            if continue_calc.lower() == 'n':
                break
                
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Goodbye! 🥥[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")


if __name__ == "__main__":
    cli()