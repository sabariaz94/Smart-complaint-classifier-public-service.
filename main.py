import questionary
from rich.console import Console
from rich.table import Table

from features.classifier.classifier import classify_complaint
import subprocess
import sys
from features.complaints.complaints import add_complaint, load_complaints, search_complaints, export_to_csv, export_to_json
from features.analytics import analytics

console = Console()

def file_complaint():
    """Files a new complaint."""
    complaint_text = questionary.text("Please describe your complaint:").ask()

    if not complaint_text:
        console.print("[yellow]Complaint description cannot be empty.[/yellow]")
        return

    with console.status("[bold green]Analyzing your complaint...[/bold green]"):
        classification = classify_complaint(complaint_text)

    if not classification:
        console.print("[red]Failed to classify the complaint. Please try again.[/red]")
        return

    console.print("\n[bold]Complaint Analysis:[/bold]")
    console.print(f"  [bold]Category:[/bold] {classification['category']}")
    console.print(f"  [bold]Priority:[/bold] {classification['priority']}")
    console.print(f"  [bold]Summary:[/bold] {classification['summary']}")
    console.print(f"  [bold]Keywords:[/bold] {', '.join(classification['keywords'])}")
    console.print(f"  [bold]Confidence:[/bold] {classification['confidence']:.2f}")

    confirm = questionary.confirm("Do you want to file this complaint?").ask()

    if confirm:
        add_complaint(
            classification["category"],
            classification["priority"],
            classification["summary"],
            classification["keywords"],
            classification["confidence"],
        )
        console.print("\n[green]Complaint filed successfully![/green]")
    else:
        console.print("\n[yellow]Complaint not filed.[/yellow]")


def view_all_complaints():
    """Views all complaints."""
    complaints = load_complaints()
    if not complaints:
        console.print("[yellow]No complaints found.[/yellow]")
        return

    table = Table(title="All Complaints")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Timestamp", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Summary", style="white")

    for complaint in complaints:
        table.add_row(
            complaint["id"],
            complaint["timestamp"],
            complaint["category"],
            complaint["priority"],
            complaint["summary"],
        )
    
    console.print(table)


def search_complaints():
    """Searches for complaints."""
    keyword = questionary.text("Enter a keyword to search:").ask()
    if not keyword:
        console.print("[yellow]Search keyword cannot be empty.[/yellow]")
        return
    
    results = search_complaints(keyword)
    
    if not results:
        console.print(f"[yellow]No complaints found matching '{keyword}'.[/yellow]")
        return

    table = Table(title=f"Complaints matching '{keyword}'")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Timestamp", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Summary", style="white")

    for complaint in results:
        table.add_row(
            complaint["id"],
            complaint["timestamp"],
            complaint["category"],
            complaint["priority"],
            complaint["summary"],
        )
    
    console.print(table)


def export_data():
    """Exports data to CSV/JSON."""
    if not load_complaints():
        console.print("[yellow]No complaints to export.[/yellow]")
        return

    export_format = questionary.select(
        "Choose an export format:",
        choices=["CSV", "JSON"],
    ).ask()

    if not export_format:
        return

    filename = questionary.text(f"Enter a filename for the {export_format} export:").ask()
    if not filename:
        console.print("[yellow]Filename cannot be empty.[/yellow]")
        return

    if export_format == "CSV":
        if not filename.endswith(".csv"):
            filename += ".csv"
        success = export_to_csv(filename)
    else:
        if not filename.endswith(".json"):
            filename += ".json"
        success = export_to_json(filename)

    if success:
        console.print(f"[green]Data exported successfully to {filename}[/green]")
    else:
        console.print("[red]Failed to export data.[/red]")

def analytics_dashboard():
    """Shows the analytics dashboard."""
    console.print("[bold green]Starting analytics dashboard...[/bold green]")
    
    # Get the path to the analytics script
    script_path = analytics.__file__
    
    # Run streamlit as a separate process
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", script_path])


def main():
    """Main function to run the CLI."""
    while True:
        console.print("\n[bold cyan]Smart Complaint Classifier[/bold cyan]")
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "File a Complaint",
                "View All Complaints",
                "Search Complaints",
                "Export Data",
                "Analytics Dashboard",
                "Exit",
            ],
        ).ask()

        if choice == "File a Complaint":
            file_complaint()
        elif choice == "View All Complaints":
            view_all_complaints()
        elif choice == "Search Complaints":
            search_complaints()
        elif choice == "Export Data":
            export_data()
        elif choice == "Analytics Dashboard":
            analytics_dashboard()
        elif choice == "Exit" or choice is None:
            break

if __name__ == "__main__":
    main()