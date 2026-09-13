# SmartBudget - Personal Budgeting Assistant

A comprehensive desktop application for personal budget management built with Python and tkinter.

## Features

### Core Functionality
- **Income Management**: Set and track monthly income
- **Expense Tracking**: Add expenses with categories and descriptions
- **Budget Calculations**: Automatic calculation of totals, balance, and savings progress
- **Savings Goals**: Set monthly savings targets and monitor progress
- **Smart Warnings**: Get alerts when approaching budget limits or overspending
- **Report Generation**: Create detailed budget reports and export to text files

### Categories
- Food
- Transport
- Bills
- Entertainment
- Healthcare
- Shopping
- Miscellaneous

## Requirements

### System Requirements
- Windows operating system
- Python 3.6 or higher
- tkinter (usually included with Python)

### Dependencies
- Python Standard Library only (no external packages required)

## Installation & Setup

1. **Download the SmartBudget files**:
   ```
   smartbudget/
   ├── main.py               # Entry point
   ├── ui.py                 # GUI interface
   ├── income_manager.py     # Income management
   ├── expense_manager.py    # Expense management
   ├── budget_calculator.py  # Budget calculations
   ├── report_generator.py   # Report generation
   ├── data/                 # Report storage directory
   └── README.md             # This file
   ```

2. **Ensure Python is installed**:
   - Download from [python.org](https://python.org) if needed
   - Verify installation: `python --version`

3. **Run the application**:
   ```bash
   cd smartbudget
   python main.py
   ```

## Usage Guide

### Getting Started

1. **Launch the Application**:
   - Run `python main.py` from the smartbudget directory
   - The welcome message will explain basic features

2. **Set Your Monthly Income**:
   - Enter your monthly income in the "Monthly Income" section
   - Click "Set Income" to save

3. **Add Expenses**:
   - Select a category from the dropdown
   - Enter the expense amount
   - Optionally add a description
   - Click "Add Expense"

4. **Set Savings Goal** (Optional):
   - Enter your monthly savings target
   - Click "Set Goal" to track progress

### Main Interface Sections

#### Monthly Income
- **Purpose**: Track your monthly earnings
- **Usage**: Enter amount and click "Set Income"
- **Display**: Shows current income below input field

#### Add Expense
- **Category**: Select from predefined categories
- **Amount**: Enter expense amount (required)
- **Description**: Optional details about the expense
- **List**: View all added expenses in the table below

#### Savings Goal
- **Purpose**: Set and monitor savings targets
- **Display**: Shows goal amount, progress percentage, and status
- **Color Coding**: Green for met goals, orange for unmet

#### Budget Summary
- **Total Expenses**: Sum of all expenses across categories
- **Remaining Balance**: Income minus total expenses
- **Color Coding**: Green for positive balance, red for negative
- **Alerts**: Real-time warnings and recommendations

### Buttons & Actions

#### Main Action Buttons
- **Refresh Summary**: Update all calculations and displays
- **Clear All Expenses**: Remove all expense entries (with confirmation)
- **Generate Report**: Create and view detailed budget report
- **Export Report**: Save report to custom location as .txt file

### Warning System

The application provides intelligent warnings:

#### Overspending Alerts
- **Red Alert**: When expenses exceed income
- **Popup Warning**: Critical overspending notifications
- **Visual Indicators**: Red text for negative balances

#### Budget Warnings
- **Threshold Warning**: When spending exceeds 80% of income
- **Savings Alerts**: When falling short of savings goals
- **Color-coded Status**: Visual feedback in summary section

### Report Features

#### Generated Reports Include:
- Income summary
- Detailed expense breakdown by category
- Individual expense items with descriptions
- Budget analysis and ratios
- Savings goal progress
- Financial warnings and alerts
- Personalized recommendations

#### Export Options:
- **Auto-generated filename**: `budget_report_YYYYMMDD_HHMMSS.txt`
- **Custom filename**: Choose your own name and location
- **Text format**: Compatible with any text editor
- **Saved reports**: Stored in the `data/` directory

## Application Architecture

### Modular Design (Single Responsibility Principle)

#### IncomeManager (`income_manager.py`)
- Handles income input and validation
- Manages monthly income data
- Provides income-related calculations

#### ExpenseManager (`expense_manager.py`)
- Manages expense categories and entries
- Calculates category and total expenses
- Handles expense validation and storage

#### BudgetCalculator (`budget_calculator.py`)
- Performs budget calculations and analysis
- Manages savings goals and progress tracking
- Generates warnings and financial alerts

#### ReportGenerator (`report_generator.py`)
- Creates formatted budget reports
- Handles file export operations
- Manages report storage and retrieval

#### UI (`ui.py`)
- tkinter-based graphical user interface
- Integrates all manager classes
- Provides user interaction and display

#### Main (`main.py`)
- Application entry point
- Dependency checking
- Error handling and initialization

## Tips for Effective Budgeting

### Best Practices
1. **Set Realistic Income**: Use your actual take-home pay
2. **Track Everything**: Record all expenses, no matter how small
3. **Use Descriptions**: Add details to remember what expenses were for
4. **Regular Reviews**: Generate reports monthly to analyze spending
5. **Set Achievable Goals**: Start with modest savings targets

### Using Categories Effectively
- **Food**: Groceries, dining out, snacks
- **Transport**: Gas, public transit, car maintenance
- **Bills**: Utilities, phone, internet, subscriptions
- **Entertainment**: Movies, games, hobbies
- **Healthcare**: Medical expenses, prescriptions, insurance
- **Shopping**: Clothing, household items, gifts
- **Miscellaneous**: Everything else

### Warning Interpretation
- **80% Threshold**: Consider reducing expenses when reached
- **Overspending**: Immediate action required to avoid debt
- **Savings Shortfall**: Adjust expenses or income to meet goals

## Troubleshooting

### Common Issues

#### Application Won't Start
- **Check Python Installation**: Ensure Python 3.6+ is installed
- **Verify File Structure**: All .py files must be in same directory
- **Check Dependencies**: All modules should import without errors

#### GUI Display Issues
- **Window Too Small**: Resize window or check screen resolution
- **Missing Elements**: Try refreshing with "Refresh Summary" button
- **Font Problems**: tkinter uses system fonts automatically

#### Data Issues
- **Expenses Not Saving**: Check for error messages in expense input
- **Reports Not Generating**: Ensure `data/` directory exists
- **Export Failures**: Verify write permissions for chosen directory

### Error Messages

#### Input Validation Errors
- **"Income cannot be negative"**: Enter positive numbers only
- **"Invalid expense amount"**: Check for valid numeric input
- **"Invalid category"**: Select from dropdown categories only

#### File Operation Errors
- **"Failed to save report"**: Check disk space and permissions
- **"Missing dependency"**: Ensure all .py files are present

## Technical Details

### File Storage
- **Reports**: Saved in `data/` subdirectory
- **Format**: Plain text (.txt) files
- **Encoding**: UTF-8 for broad compatibility
- **Naming**: Automatic timestamps prevent overwrites

### Data Validation
- **Numeric Inputs**: Automatic conversion and validation
- **Negative Values**: Prevented for income and expenses
- **Category Validation**: Restricted to predefined list
- **Error Handling**: User-friendly error messages

### Performance
- **Memory Usage**: Minimal - stores data in memory only
- **File Size**: Reports are lightweight text files
- **Response Time**: Instant updates for all calculations
- **Scalability**: Handles hundreds of expense entries efficiently

## Version Information

- **Version**: 1.0
- **Python Compatibility**: 3.6+
- **GUI Framework**: tkinter
- **Platform**: Windows (primary), cross-platform compatible
- **License**: Open source

## Support

For questions or issues:
1. Check this README for common solutions
2. Verify all files are present and Python is correctly installed
3. Review error messages for specific guidance
4. Ensure proper file permissions for report exports

## Contributing

SmartBudget follows clean code principles:
- **Modular Design**: Each class has a single responsibility
- **Clear Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Robust validation and user feedback
- **Intuitive Interface**: User-friendly GUI design

---

**SmartBudget** - Making personal finance management simple and effective!
