"""
Budget Calculator Module for SmartBudget Application

This module handles budget calculations including remaining balance,
savings goals, and budget threshold warnings.
"""


class BudgetCalculator:
    """
    Handles budget calculations, savings goals, and financial warnings.
    
    Attributes:
        savings_goal (float): The user's monthly savings goal
        budget_threshold (float): Warning threshold as percentage of income
    """
    
    def __init__(self):
        """Initialize the BudgetCalculator with default settings."""
        self.savings_goal = 0.0
        self.budget_threshold = 0.8  # 80% of income
    
    def calculate_remaining_balance(self, income, total_expenses):
        """
        Calculate the remaining balance after expenses.
        
        Args:
            income (float): Monthly income
            total_expenses (float): Total expenses
            
        Returns:
            float: Remaining balance (income - expenses)
        """
        return income - total_expenses
    
    def set_savings_goal(self, goal_amount):
        """
        Set the monthly savings goal.
        
        Args:
            goal_amount (float): The savings goal amount
            
        Returns:
            bool: True if goal was set successfully
            
        Raises:
            ValueError: If goal amount is negative
        """
        try:
            goal_amount = float(goal_amount)
            if goal_amount < 0:
                raise ValueError("Savings goal cannot be negative")
            self.savings_goal = goal_amount
            return True
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid savings goal: {e}")
    
    def get_savings_goal(self):
        """
        Get the current savings goal.
        
        Returns:
            float: The current savings goal amount
        """
        return self.savings_goal
    
    def calculate_savings_progress(self, remaining_balance):
        """
        Calculate progress towards savings goal.
        
        Args:
            remaining_balance (float): Current remaining balance
            
        Returns:
            dict: Dictionary containing progress information
        """
        if self.savings_goal == 0:
            return {
                "goal_amount": 0,
                "current_savings": remaining_balance,
                "progress_percentage": 0,
                "goal_met": False,
                "shortfall": 0
            }
        
        progress_percentage = (remaining_balance / self.savings_goal) * 100 if self.savings_goal > 0 else 0
        goal_met = remaining_balance >= self.savings_goal
        shortfall = max(0, self.savings_goal - remaining_balance)
        
        return {
            "goal_amount": self.savings_goal,
            "current_savings": remaining_balance,
            "progress_percentage": min(100, max(0, progress_percentage)),
            "goal_met": goal_met,
            "shortfall": shortfall
        }
    
    def check_budget_warnings(self, income, total_expenses, remaining_balance):
        """
        Check for budget warnings and overspending alerts.
        
        Args:
            income (float): Monthly income
            total_expenses (float): Total expenses
            remaining_balance (float): Remaining balance
            
        Returns:
            list: List of warning messages
        """
        warnings = []
        
        if income == 0:
            warnings.append("No income set. Please set your monthly income.")
            return warnings
        
        # Check if expenses exceed income
        if total_expenses > income:
            overspend = total_expenses - income
            warnings.append(f"⚠️ OVERSPENDING ALERT: You've exceeded your income by ${overspend:.2f}")
        
        # Check if expenses are approaching the threshold
        expense_ratio = total_expenses / income
        if expense_ratio >= self.budget_threshold and total_expenses <= income:
            percentage = expense_ratio * 100
            warnings.append(f"⚠️ BUDGET WARNING: You've spent {percentage:.1f}% of your income")
        
        # Check savings goal warnings
        if self.savings_goal > 0:
            if remaining_balance < self.savings_goal:
                shortfall = self.savings_goal - remaining_balance
                warnings.append(f"💰 SAVINGS ALERT: You're ${shortfall:.2f} short of your savings goal")
            elif remaining_balance < 0:
                warnings.append("💰 SAVINGS ALERT: Negative balance - savings goal cannot be met")
        
        return warnings
    
    def set_budget_threshold(self, threshold):
        """
        Set the budget warning threshold as a percentage.
        
        Args:
            threshold (float): Threshold as decimal (0.8 = 80%)
            
        Returns:
            bool: True if threshold was set successfully
        """
        try:
            threshold = float(threshold)
            if not 0 < threshold <= 1:
                raise ValueError("Threshold must be between 0 and 1")
            self.budget_threshold = threshold
            return True
        except (ValueError, TypeError):
            return False
    
    def get_budget_summary(self, income, total_expenses):
        """
        Get a comprehensive budget summary.
        
        Args:
            income (float): Monthly income
            total_expenses (float): Total expenses
            
        Returns:
            dict: Complete budget summary
        """
        remaining_balance = self.calculate_remaining_balance(income, total_expenses)
        savings_progress = self.calculate_savings_progress(remaining_balance)
        warnings = self.check_budget_warnings(income, total_expenses, remaining_balance)
        
        return {
            "income": income,
            "total_expenses": total_expenses,
            "remaining_balance": remaining_balance,
            "savings_progress": savings_progress,
            "warnings": warnings,
            "expense_ratio": (total_expenses / income * 100) if income > 0 else 0
        }
