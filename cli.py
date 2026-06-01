import sys
import argparse
import logging
from typing import Dict, Any, Optional

# Rich imports for gorgeous CLI UX
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.style import Style

# Bot module imports
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.client import get_binance_client
from bot.orders import place_futures_order

# Initialize logging config (default logs to logs/trading_bot.log)
setup_logging()
logger = logging.getLogger("cli")

# Initialize Rich Console
console = Console()

def print_banner():
    """Prints a beautiful, premium welcome banner for the bot."""
    banner_text = Text()
    banner_text.append("=== ANTIGRAVITY BINANCE FUTURES TRADING BOT ===\n", style="bold cyan")
    banner_text.append("USDT-M Futures Testnet Integration", style="italic gold1")
    
    panel = Panel(
        banner_text,
        title="[bold white]Welcome[/bold white]",
        border_style="cyan",
        expand=False,
        padding=(1, 5)
    )
    console.print(panel)
    console.print()

def print_order_summary(params: Dict[str, Any]):
    """Displays a styled summary card of the order details to be placed."""
    table = Table(title="[bold gold1]Order Placement Summary[/bold gold1]", border_style="gold1")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="bold white")
    
    table.add_row("Symbol", params["symbol"])
    table.add_row("Side", params["side"])
    table.add_row("Order Type", params["order_type"])
    table.add_row("Quantity", str(params["quantity"]))
    if params["price"] is not None:
        table.add_row("Price", f"{params['price']} USDT")
    else:
        table.add_row("Price", "[dim italic]N/A (Market Order)[/dim italic]")
        
    console.print(table)
    console.print()

def run_interactive_ux() -> Dict[str, Any]:
    """
    Guides the user through an interactive prompt menu to collect
    and validate order parameters in real-time.
    """
    print_banner()
    console.print("[bold white]Entering Interactive Mode...[/bold white]")
    console.print("Please enter the following details to structure your order.\n")
    
    # 1. Prompt for Symbol
    while True:
        symbol = Prompt.ask("[bold cyan]Enter Symbol[/bold cyan] (e.g., BTCUSDT, ETHUSDT)").strip().upper()
        # Pre-validate Symbol format
        if symbol:
            break
        console.print("[bold red][Error] Symbol cannot be empty![/bold red]\n")
        
    # 2. Prompt for Side
    side = Prompt.ask(
        "[bold cyan]Select Side[/bold cyan]", 
        choices=["BUY", "SELL"], 
        default="BUY"
    ).upper()
    
    # 3. Prompt for Type
    order_type = Prompt.ask(
        "[bold cyan]Select Order Type[/bold cyan]", 
        choices=["MARKET", "LIMIT"], 
        default="MARKET"
    ).upper()
    
    # 4. Prompt for Quantity
    while True:
        qty_str = Prompt.ask("[bold cyan]Enter Quantity[/bold cyan]")
        try:
            qty = float(qty_str)
            if qty <= 0:
                console.print("[bold red][Error] Quantity must be a positive number![/bold red]\n")
                continue
            break
        except ValueError:
            console.print(f"[bold red][Error] Invalid numeric quantity: '{qty_str}'[/bold red]\n")
            
    # 5. Prompt for Price (only if LIMIT order)
    price_str = None
    if order_type == "LIMIT":
        while True:
            price_str = Prompt.ask("[bold cyan]Enter Price (USDT)[/bold cyan]")
            try:
                price = float(price_str)
                if price <= 0:
                    console.print("[bold red][Error] Price must be a positive number![/bold red]\n")
                    continue
                break
            except ValueError:
                console.print(f"[bold red][Error] Invalid numeric price: '{price_str}'[/bold red]\n")

    # Run the full validation check on the inputs
    is_valid, err_msg, validated_params = validate_inputs(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=str(qty),
        price=price_str
    )
    
    if not is_valid:
        console.print(Panel(f"[bold red]Validation Failed:[/bold red] {err_msg}", border_style="red"))
        sys.exit(1)
        
    return validated_params

def execute_order(validated_params: Dict[str, Any]):
    """Connects to Binance testnet and places the order, displaying logs and results."""
    # 1. Connect and initialize Client with spinner
    try:
        with console.status("[bold cyan]Connecting to Binance Futures Testnet...[/bold cyan]") as status:
            client = get_binance_client()
    except Exception as e:
        console.print()
        console.print(Panel(
            f"[bold red]Connection Error:[/bold red]\n{str(e)}", 
            title="[bold white]Initialization Failed[/bold white]",
            border_style="red"
        ))
        sys.exit(1)

    # 2. Confirm placement in interactive mode
    print_order_summary(validated_params)
    
    # 3. Execute order with spinner
    try:
        with console.status("[bold gold1]Sending order request to exchange...[/bold gold1]") as status:
            response = place_futures_order(
                client=client,
                symbol=validated_params["symbol"],
                side=validated_params["side"],
                order_type=validated_params["order_type"],
                quantity=validated_params["quantity"],
                price=validated_params["price"]
            )
            
        console.print()
        if response["success"]:
            # Success display
            success_msg = Text()
            success_msg.append("[Success] Order Placed Successfully!\n\n", style="bold spring_green3")
            
            # Details panel table
            res_table = Table(box=None, padding=(0, 2))
            res_table.add_column("Key", style="cyan")
            res_table.add_column("Value", style="bold white")
            res_table.add_row("Order ID", str(response["orderId"]))
            res_table.add_row("Status", str(response["status"]))
            res_table.add_row("Executed Qty", str(response["executedQty"]))
            res_table.add_row("Avg Price / Price", f"{response['avgPrice']} USDT")
            
            panel = Panel(
                res_table,
                title="[bold spring_green3]Receipt Details[/bold spring_green3]",
                border_style="spring_green3",
                padding=(1, 3)
            )
            console.print(panel)
            console.print("[bold spring_green3][OK] Check logs/trading_bot.log for detailed exchange response.[/bold spring_green3]")
        else:
            # Failure display
            fail_msg = (
                f"[bold red]Order Execution Failed![/bold red]\n\n"
                f"[bold yellow]Error Type:[/bold yellow] {response.get('error_type')}\n"
                f"[bold yellow]Message:[/bold yellow] {response.get('message')}\n"
                f"[bold yellow]Code:[/bold yellow] {response.get('code', 'N/A')}"
            )
            console.print(Panel(fail_msg, title="[bold white]Exchange Rejection[/bold white]", border_style="red"))
            sys.exit(1)
            
    except Exception as e:
        console.print()
        console.print(Panel(
            f"[bold red]Unexpected Order Placement Exception:[/bold red]\n{str(e)}", 
            title="[bold white]Error[/bold white]",
            border_style="red"
        ))
        sys.exit(1)

def main():
    # Setup argparse
    parser = argparse.ArgumentParser(
        description="A Python trading bot CLI for placing orders on Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument("--symbol", type=str, help="Trading symbol, e.g., BTCUSDT")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", type=str, help="Order quantity")
    parser.add_argument("--price", type=str, help="Order price (required for LIMIT orders)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive step-by-step menu UX")
    
    args = parser.parse_args()
    
    # If interactive flag is provided or NO arguments are provided, trigger Enhanced Interactive UX
    has_cli_args = any([args.symbol, args.side, args.type, args.quantity, args.price])
    
    if args.interactive or not has_cli_args:
        # Launch Interactive step-by-step UX (Bonus Option)
        validated_params = run_interactive_ux()
        
        # Display the collected parameters and ask for user confirmation
        confirm = Confirm.ask("\n[bold gold1]Confirm: Are you sure you want to place this order?[/bold gold1]", default=False)
        if not confirm:
            console.print("\n[bold yellow]Order aborted by user.[/bold yellow]")
            sys.exit(0)
            
        execute_order(validated_params)
    else:
        # Standard automated CLI runner
        # 1. Check validation
        is_valid, err_msg, validated_params = validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
        
        if not is_valid:
            console.print(Panel(f"[bold red]Validation Error:[/bold red] {err_msg}", border_style="red"))
            sys.exit(1)
            
        # 2. Run order execution
        execute_order(validated_params)

if __name__ == "__main__":
    main()
