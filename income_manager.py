"""
Income Manager Module for SmartBudget Application

This module handles all income-related operations including
setting monthly income and validation.
"""


class IncomeManager:
    """
    Manages income input and validation for the budget application.
    
    Attributes:
        monthly_income (float): The user's monthly income amount
    """
    
    def __init__(self):
        """Initialize the IncomeManager with zero income."""
        self.monthly_income = 0.0
    
    def set_income(self, amount):
        """
        Set the monthly income amount.
        
        Args:
            amount (float): The monthly income amount
            
        Returns:
            bool: True if income was set successfully, False otherwise
            
        Raises:
            ValueError: If amount is negative or not a valid number
        """
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Income cannot be negative")
            self.monthly_income = amount
            return True
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid income amount: {e}")
    
    def get_income(self):
        """
        Get the current monthly income.
        
        Returns:
            float: The current monthly income amount
        """
        return self.monthly_income
    
    def has_income_set(self):
        """
        Check if income has been set.
        
        Returns:
            bool: True if income is greater than 0, False otherwise
        """
        return self.monthly_income > 0
    
    def reset_income(self):
        """Reset the income to zero."""
        self.monthly_income = 0.0
