"""
SmartBudget - Personal Budgeting Assistant

Entry point for the SmartBudget desktop application.
A comprehensive budget management tool with GUI interface.

Author: SmartBudget Development Team
Version: 1.0
"""

import sys
import tkinter as tk
from tkinter import messagebox
from ui import SmartBudgetUI


def check_dependencies():
    """
    Check if all required dependencies are available.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    try:
        # Check tkinter availability
        import tkinter
        
        # Check custom modules
        from income_manager import IncomeManager
        from expense_manager import ExpenseManager
        from budget_calculator import BudgetCalculator
        from report_generator import ReportGenerator
        
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False


def main():
    """
    Main entry point for the SmartBudget application.
    
    Initializes the GUI and starts the application event loop.
    """
    try:
        # Check dependencies
        if not check_dependencies():
            print("ERROR: Missing required dependencies.")
            print("Please ensure all SmartBudget modules are in the same directory.")
            return 1
        
        # Create main window
        root = tk.Tk()
        
        # Set application icon and properties
        root.title("SmartBudget - Personal Budgeting Assistant")
        root.minsize(600, 500)
        
        # Center the window on screen
        root.geometry("800x700")
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Initialize the application
        app = SmartBudgetUI(root)
        
        # Show welcome message
        messagebox.showinfo(
            "Welcome to SmartBudget!", 
            "Welcome to SmartBudget - Your Personal Budgeting Assistant!\n\n"
            "Features:\n"
            "• Track monthly income and expenses\n"
            "• Set and monitor savings goals\n"
            "• Get budget warnings and alerts\n"
            "• Generate and export detailed reports\n\n"
            "Start by setting your monthly income!"
        )
        
        # Start the GUI event loop
        root.mainloop()
        
        return 0
        
    except Exception as e:
        error_msg = f"Failed to start SmartBudget application: {e}"
        print(error_msg)
        
        # Try to show error in GUI if possible
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("SmartBudget Error", error_msg)
        except:
            pass  # If GUI fails, error was already printed
        
        return 1


if __name__ == "__main__":
    """Entry point when script is run directly."""
    exit_code = main()
    sys.exit(exit_code)
