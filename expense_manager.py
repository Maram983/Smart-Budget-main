"""
Expense Manager Module for SmartBudget Application

This module handles all expense-related operations including
adding expenses, categorizing them, and calculating totals.
"""

from collections import defaultdict


class ExpenseManager:
    """
    Manages expenses with categories and amounts for the budget application.
    
    Attributes:
        expenses (dict): Dictionary storing expenses grouped by category
        categories (list): Available expense categories
    """
    
    def __init__(self):
        """Initialize the ExpenseManager with empty expenses and default categories."""
        self.expenses = defaultdict(list)
        self.categories = [
            "Food",
            "Transport", 
            "Bills",
            "Entertainment",
            "Healthcare",
            "Shopping",
            "Miscellaneous"
        ]
    
    def add_expense(self, category, amount, description=""):
        """
        Add an expense to the specified category.
        
        Args:
            category (str): The expense category
            amount (float): The expense amount
            description (str): Optional description of the expense
            
        Returns:
            bool: True if expense was added successfully
            
        Raises:
            ValueError: If amount is negative or category is invalid
        """
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Expense amount cannot be negative")
            
            if category not in self.categories:
                raise ValueError(f"Invalid category: {category}")
            
            expense_entry = {
                "amount": amount,
                "description": description
            }
            self.expenses[category].append(expense_entry)
            return True
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid expense: {e}")
    
    def get_category_total(self, category):
        """
        Get the total amount spent in a specific category.
        
        Args:
            category (str): The expense category
            
        Returns:
            float: Total amount spent in the category
        """
        if category not in self.expenses:
            return 0.0
        return sum(expense["amount"] for expense in self.expenses[category])
    
    def get_total_expenses(self):
        """
        Calculate the total of all expenses across all categories.
        
        Returns:
            float: Total amount of all expenses
        """
        total = 0.0
        for category in self.expenses:
            total += self.get_category_total(category)
        return total
    
    def get_expenses_by_category(self):
        """
        Get all expenses organized by category.
        
        Returns:
            dict: Dictionary with categories as keys and expense lists as values
        """
        return dict(self.expenses)
    
    def get_categories(self):
        """
        Get the list of available expense categories.
        
        Returns:
            list: List of expense categories
        """
        return self.categories.copy()
    
    def clear_expenses(self):
        """Clear all expenses from all categories."""
        self.expenses.clear()
    
    def remove_expense(self, category, index):
        """
        Remove a specific expense from a category.
        
        Args:
            category (str): The expense category
            index (int): Index of the expense to remove
            
        Returns:
            bool: True if expense was removed successfully, False otherwise
        """
        try:
            if category in self.expenses and 0 <= index < len(self.expenses[category]):
                self.expenses[category].pop(index)
                return True
            return False
        except (IndexError, KeyError):
            return False
