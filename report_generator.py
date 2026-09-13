"""
Report Generator Module for SmartBudget Application

This module handles generating and exporting budget reports to text files.
"""

import os
from datetime import datetime


class ReportGenerator:
    """
    Generates and exports budget reports in text format.
    
    Handles creating comprehensive budget summaries and saving them
    to text files with proper formatting.
    """
    
    def __init__(self):
        """Initialize the ReportGenerator."""
        self.report_directory = "data"
        self._ensure_report_directory()
    
    def _ensure_report_directory(self):
        """Create the data directory if it doesn't exist."""
        if not os.path.exists(self.report_directory):
            os.makedirs(self.report_directory)
    
    def generate_report(self, income_manager, expense_manager, budget_calculator):
        """
        Generate a comprehensive budget report.
        
        Args:
            income_manager: IncomeManager instance
            expense_manager: ExpenseManager instance
            budget_calculator: BudgetCalculator instance
            
        Returns:
            str: Formatted report as string
        """
        income = income_manager.get_income()
        total_expenses = expense_manager.get_total_expenses()
        expenses_by_category = expense_manager.get_expenses_by_category()
        budget_summary = budget_calculator.get_budget_summary(income, total_expenses)
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Start building the report
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("           SMARTBUDGET - FINANCIAL REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated on: {timestamp}")
        report_lines.append("")
        
        # Income Section
        report_lines.append("INCOME SUMMARY")
        report_lines.append("-" * 30)
        report_lines.append(f"Monthly Income: ${income:.2f}")
        report_lines.append("")
        
        # Expenses Section
        report_lines.append("EXPENSE BREAKDOWN")
        report_lines.append("-" * 30)
        
        if expenses_by_category:
            for category in sorted(expenses_by_category.keys()):
                category_total = expense_manager.get_category_total(category)
                report_lines.append(f"{category:15}: ${category_total:>8.2f}")
                
                # Add individual expenses if there are any
                for i, expense in enumerate(expenses_by_category[category]):
                    if expense["description"]:
                        report_lines.append(f"  - {expense['description']}: ${expense['amount']:.2f}")
            
            report_lines.append("-" * 30)
            report_lines.append(f"{'TOTAL EXPENSES':15}: ${total_expenses:>8.2f}")
        else:
            report_lines.append("No expenses recorded.")
        
        report_lines.append("")
        
        # Budget Summary Section
        report_lines.append("BUDGET ANALYSIS")
        report_lines.append("-" * 30)
        report_lines.append(f"Monthly Income:     ${budget_summary['income']:>8.2f}")
        report_lines.append(f"Total Expenses:     ${budget_summary['total_expenses']:>8.2f}")
        report_lines.append(f"Remaining Balance:  ${budget_summary['remaining_balance']:>8.2f}")
        
        if budget_summary['remaining_balance'] >= 0:
            report_lines.append("Status: ✓ Within Budget")
        else:
            report_lines.append("Status: ⚠ Over Budget")
        
        if income > 0:
            report_lines.append(f"Expense Ratio:      {budget_summary['expense_ratio']:>7.1f}%")
        
        report_lines.append("")
        
        # Savings Goal Section
        savings_progress = budget_summary['savings_progress']
        if savings_progress['goal_amount'] > 0:
            report_lines.append("SAVINGS GOAL PROGRESS")
            report_lines.append("-" * 30)
            report_lines.append(f"Savings Goal:       ${savings_progress['goal_amount']:>8.2f}")
            report_lines.append(f"Current Savings:    ${savings_progress['current_savings']:>8.2f}")
            report_lines.append(f"Progress:           {savings_progress['progress_percentage']:>7.1f}%")
            
            if savings_progress['goal_met']:
                report_lines.append("Goal Status: ✓ Goal Achieved!")
            else:
                report_lines.append(f"Shortfall:          ${savings_progress['shortfall']:>8.2f}")
                report_lines.append("Goal Status: ⚠ Goal Not Met")
            
            report_lines.append("")
        
        # Warnings Section
        if budget_summary['warnings']:
            report_lines.append("BUDGET WARNINGS & ALERTS")
            report_lines.append("-" * 30)
            for warning in budget_summary['warnings']:
                # Remove emoji for text file compatibility
                clean_warning = warning.replace("⚠️", "WARNING:").replace("💰", "SAVINGS:")
                report_lines.append(f"• {clean_warning}")
            report_lines.append("")
        
        # Recommendations Section
        report_lines.append("FINANCIAL RECOMMENDATIONS")
        report_lines.append("-" * 30)
        
        if budget_summary['remaining_balance'] < 0:
            report_lines.append("• Reduce expenses to avoid overspending")
            report_lines.append("• Review and cut unnecessary expenses")
        elif budget_summary['expense_ratio'] > 80:
            report_lines.append("• Consider reducing expenses to improve savings")
        else:
            report_lines.append("• Good budget management!")
        
        if savings_progress['goal_amount'] > 0 and not savings_progress['goal_met']:
            report_lines.append("• Adjust expenses to meet savings goal")
        
        if not expenses_by_category:
            report_lines.append("• Start tracking expenses to improve budgeting")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("End of Report")
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def export_report(self, report_content, filename=None):
        """
        Export the report to a text file.
        
        Args:
            report_content (str): The report content to save
            filename (str): Optional custom filename
            
        Returns:
            str: Path to the saved file
            
        Raises:
            IOError: If file cannot be written
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"budget_report_{timestamp}.txt"
        
        # Ensure filename ends with .txt
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        filepath = os.path.join(self.report_directory, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(report_content)
            return filepath
        except IOError as e:
            raise IOError(f"Failed to save report: {e}")
    
    def get_saved_reports(self):
        """
        Get a list of all saved report files.
        
        Returns:
            list: List of report filenames
        """
        try:
            files = []
            for filename in os.listdir(self.report_directory):
                if filename.endswith('.txt') and filename.startswith('budget_report'):
                    files.append(filename)
            return sorted(files, reverse=True)  # Most recent first
        except OSError:
            return []
