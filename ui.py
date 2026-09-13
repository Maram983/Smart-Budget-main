"""
Modern User Interface Module for SmartBudget Application

This module contains the modern GUI implementation using tkinter,
providing a sleek, contemporary interface for budget management.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
from income_manager import IncomeManager
from expense_manager import ExpenseManager
from budget_calculator import BudgetCalculator
from report_generator import ReportGenerator


def get_font(family="Segoe UI", size=10, weight="normal"):
    """Get font with fallback for compatibility."""
    # Simple fallback approach to avoid testing issues
    fallback_fonts = [
        (family, size, weight),
        ("Arial", size, weight),
        ("Helvetica", size, weight),
        ("TkDefaultFont", size)
    ]
    
    for font in fallback_fonts:
        try:
            return font
        except:
            continue
    
    # Ultimate fallback
    return ("TkDefaultFont",)


class ModernButton(tk.Canvas):
    """Modern button widget with hover effects and gradients."""
    
    def __init__(self, parent, text, command=None, bg_color="#4A90E2", hover_color="#357ABD", 
                 text_color="white", font=None, width=120, height=35):
        if font is None:
            font = get_font("Segoe UI", 10, "bold")
        super().__init__(parent, width=width, height=height, highlightthickness=0, 
                        relief="flat", bd=0, cursor="hand2")
        
        self.command = command
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.width = width
        self.height = height
        
        self.is_hovered = False
        self.draw_button()
        
        # Bind events
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def draw_button(self):
        """Draw the button with current state."""
        self.delete("all")
        
        # Choose color based on hover state
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Draw rounded rectangle
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 8, fill=color, outline="")
        
        # Draw text
        self.create_text(self.width//2, self.height//2, text=self.text, 
                        fill=self.text_color, font=self.font)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle."""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event):
        """Handle button click."""
        if self.command:
            self.command()
    
    def on_enter(self, event):
        """Handle mouse enter."""
        self.is_hovered = True
        self.draw_button()
    
    def on_leave(self, event):
        """Handle mouse leave."""
        self.is_hovered = False
        self.draw_button()


class ModernEntry(tk.Frame):
    """Modern entry widget with floating label and focus effects."""
    
    def __init__(self, parent, placeholder="", colors=None, **kwargs):
        # Get colors from parent or use defaults
        if colors is None:
            colors = {
                "surface": "#2D2D2D",
                "text_primary": "#FFFFFF",
                "text_secondary": "#B0B0B0",
                "border": "#404040",
                "primary": "#007ACC"
            }
        
        super().__init__(parent, bg=colors["surface"], relief="flat", bd=0)
        
        self.placeholder = placeholder
        self.has_focus = False
        self.colors = colors
        
        # Create entry widget with font fallback
        entry_font = get_font("Segoe UI", 11)
        
        self.entry = tk.Entry(self, font=entry_font, relief="flat", bd=0,
                             bg=colors["surface"], fg=colors["text_primary"])
        # Try to set insert color if supported
        try:
            self.entry.config(insertcolor="#4A90E2")
        except tk.TclError:
            pass  # Ignore if not supported in this tkinter version
        
        self.entry.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Configure initial appearance
        self.configure_appearance()
        
        # Bind events
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
        # Set placeholder
        if self.placeholder:
            self.set_placeholder()
    
    def configure_appearance(self):
        """Configure the visual appearance."""
        self.configure(relief="solid", bd=1, highlightthickness=1,
                      highlightcolor=self.colors["primary"], 
                      highlightbackground=self.colors["border"])
    
    def set_placeholder(self):
        """Set placeholder text."""
        self.entry.insert(0, self.placeholder)
        self.entry.configure(fg=self.colors["text_secondary"])
    
    def on_focus_in(self, event):
        """Handle focus in event."""
        self.has_focus = True
        self.configure(highlightbackground=self.colors["primary"], bd=2)
        
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=self.colors["text_primary"])
    
    def on_focus_out(self, event):
        """Handle focus out event."""
        self.has_focus = False
        self.configure(highlightbackground=self.colors["border"], bd=1)
        
        if not self.entry.get() and self.placeholder:
            self.set_placeholder()
    
    def get(self):
        """Get entry value."""
        value = self.entry.get()
        return "" if value == self.placeholder else value
    
    def set(self, value):
        """Set entry value."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.entry.configure(fg=self.colors["text_primary"])


class ExpenseGraphWidget(tk.Canvas):
    """Modern expense graph widget with interactive charts."""
    
    def __init__(self, parent, colors, width=500, height=300):
        super().__init__(parent, width=width, height=height, 
                        bg=colors["graph_bg"], highlightthickness=0, relief="flat")
        
        self.colors = colors
        self.width = width
        self.height = height
        self.expense_data = {}
        
        # Graph settings
        self.padding = 40
        self.chart_width = width - (2 * self.padding)
        self.chart_height = height - (2 * self.padding)
        
        # Animation variables
        self.animation_step = 0
        self.max_animation_steps = 30
        
        self.bind("<Motion>", self.on_mouse_move)
        self.bind("<Leave>", self.on_mouse_leave)
        
        self.draw_empty_state()
    
    def draw_empty_state(self):
        """Draw empty state when no data is available."""
        self.delete("all")
        
        # Draw background
        self.create_rectangle(0, 0, self.width, self.height, 
                            fill=self.colors["graph_bg"], outline="")
        
        # Draw empty state message
        self.create_text(self.width//2, self.height//2, 
                        text="📊 No expenses to display\nAdd some expenses to see the chart",
                        fill=self.colors["text_secondary"],
                        font=get_font("Segoe UI", 12),
                        justify="center")
    
    def update_data(self, expense_data):
        """Update the graph with new expense data."""
        self.expense_data = expense_data
        if not expense_data:
            self.draw_empty_state()
            return
        
        self.animate_chart()
    
    def animate_chart(self):
        """Animate the chart drawing."""
        self.animation_step = 0
        self.draw_animated_frame()
    
    def draw_animated_frame(self):
        """Draw one frame of the animation."""
        if self.animation_step <= self.max_animation_steps:
            progress = self.animation_step / self.max_animation_steps
            self.draw_chart(progress)
            self.animation_step += 1
            self.after(16, self.draw_animated_frame)  # ~60 FPS
    
    def draw_chart(self, animation_progress=1.0):
        """Draw the expense chart with animation support."""
        self.delete("all")
        
        if not self.expense_data:
            self.draw_empty_state()
            return
        
        # Calculate chart type based on data
        if len(self.expense_data) > 1:
            self.draw_pie_chart(animation_progress)
        else:
            self.draw_bar_chart(animation_progress)
        
        # Draw legend
        self.draw_legend()
    
    def draw_pie_chart(self, animation_progress):
        """Draw an animated pie chart for expense categories."""
        center_x = self.width // 2
        center_y = self.height // 2 - 20
        radius = min(self.chart_width, self.chart_height) // 3
        
        # Calculate angles
        total_amount = sum(self.expense_data.values())
        if total_amount == 0:
            return
        
        # Colors for different categories
        category_colors = [
            self.colors["primary"], self.colors["success"], self.colors["warning"],
            self.colors["danger"], self.colors["accent"], "#9C27B0", "#FF5722"
        ]
        
        start_angle = 0
        color_index = 0
        
        for category, amount in self.expense_data.items():
            if amount <= 0:
                continue
                
            # Calculate slice angle
            slice_angle = (amount / total_amount) * 360 * animation_progress
            
            if slice_angle > 0:
                # Draw pie slice
                color = category_colors[color_index % len(category_colors)]
                
                # Create arc
                x1 = center_x - radius
                y1 = center_y - radius
                x2 = center_x + radius
                y2 = center_y + radius
                
                self.create_arc(x1, y1, x2, y2, 
                              start=start_angle, extent=slice_angle,
                              fill=color, outline=self.colors["surface"], width=2)
                
                # Draw category label if slice is large enough
                if slice_angle > 20:
                    label_angle = math.radians(start_angle + slice_angle/2)
                    label_x = center_x + (radius * 0.7) * math.cos(label_angle)
                    label_y = center_y + (radius * 0.7) * math.sin(label_angle)
                    
                    percentage = (amount / total_amount) * 100
                    if percentage >= 5:  # Only show label if significant
                        self.create_text(label_x, label_y, 
                                       text=f"{percentage:.0f}%",
                                       fill="white",
                                       font=get_font("Segoe UI", 9, "bold"))
                
                start_angle += slice_angle
                color_index += 1
        
        # Draw center circle for modern donut chart effect
        inner_radius = radius * 0.4
        self.create_oval(center_x - inner_radius, center_y - inner_radius,
                        center_x + inner_radius, center_y + inner_radius,
                        fill=self.colors["graph_bg"], outline="")
        
        # Draw total in center
        self.create_text(center_x, center_y - 5,
                        text="Total",
                        fill=self.colors["text_secondary"],
                        font=get_font("Segoe UI", 10))
        self.create_text(center_x, center_y + 10,
                        text=f"${total_amount:.0f}",
                        fill=self.colors["text_primary"],
                        font=get_font("Segoe UI", 12, "bold"))
    
    def draw_bar_chart(self, animation_progress):
        """Draw an animated bar chart for single category."""
        # Implementation for bar chart when only one category
        category = list(self.expense_data.keys())[0]
        amount = list(self.expense_data.values())[0]
        
        # Draw simple progress bar style
        bar_width = self.chart_width * 0.6
        bar_height = 30
        bar_x = (self.width - bar_width) // 2
        bar_y = self.height // 2 - bar_height // 2
        
        # Background bar
        self.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                            fill=self.colors["surface"], outline="")
        
        # Filled bar with animation
        fill_width = bar_width * animation_progress
        self.create_rectangle(bar_x, bar_y, bar_x + fill_width, bar_y + bar_height,
                            fill=self.colors["primary"], outline="")
        
        # Labels
        self.create_text(self.width // 2, bar_y - 20,
                        text=category,
                        fill=self.colors["text_primary"],
                        font=get_font("Segoe UI", 12, "bold"))
        
        self.create_text(self.width // 2, bar_y + bar_height + 20,
                        text=f"${amount:.2f}",
                        fill=self.colors["text_primary"],
                        font=get_font("Segoe UI", 11))
    
    def draw_legend(self):
        """Draw the chart legend."""
        if not self.expense_data or len(self.expense_data) <= 1:
            return
        
        legend_x = 20
        legend_y = self.height - 100
        item_height = 20
        
        category_colors = [
            self.colors["primary"], self.colors["success"], self.colors["warning"],
            self.colors["danger"], self.colors["accent"], "#9C27B0", "#FF5722"
        ]
        
        color_index = 0
        for category, amount in self.expense_data.items():
            if amount <= 0:
                continue
                
            color = category_colors[color_index % len(category_colors)]
            
            # Color square
            self.create_rectangle(legend_x, legend_y, legend_x + 12, legend_y + 12,
                                fill=color, outline="")
            
            # Category text
            self.create_text(legend_x + 20, legend_y + 6,
                           text=f"{category}: ${amount:.0f}",
                           fill=self.colors["text_primary"],
                           font=get_font("Segoe UI", 9),
                           anchor="w")
            
            legend_y += item_height
            color_index += 1
    
    def on_mouse_move(self, event):
        """Handle mouse movement for interactivity."""
        # Could add hover effects here
        pass
    
    def on_mouse_leave(self, event):
        """Handle mouse leave."""
        # Reset any hover effects
        pass


class SmartBudgetUI:
    """
    Modern GUI class for the SmartBudget application.
    
    Features a contemporary design with advanced styling, animations,
    and modern UI patterns for an exceptional user experience.
    """
    
    def __init__(self, root):
        """
        Initialize the modern SmartBudget GUI.
        
        Args:
            root: tkinter.Tk main window
        """
        self.root = root
        self.root.title("SmartBudget Pro")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        self.root.configure(bg="#1E1E1E")
        
        # Dark mode color scheme - premium design
        self.colors = {
            "primary": "#007ACC",           # Modern blue
            "primary_dark": "#005a9e",      # Darker blue
            "secondary": "#8A8A8A",         # Neutral gray
            "success": "#4CAF50",           # Modern green
            "warning": "#FF9800",           # Vibrant orange
            "danger": "#F44336",            # Modern red
            "background": "#1E1E1E",        # Dark background
            "surface": "#2D2D2D",           # Card surfaces
            "surface_light": "#3D3D3D",     # Lighter surfaces
            "text_primary": "#FFFFFF",      # Primary text
            "text_secondary": "#B0B0B0",    # Secondary text
            "text_muted": "#808080",        # Muted text
            "border": "#404040",            # Border color
            "accent": "#FF4081",            # Pink accent
            "graph_bg": "#252525",          # Graph background
            "graph_grid": "#404040"         # Graph grid lines
        }
        
        # Initialize managers
        self.income_manager = IncomeManager()
        self.expense_manager = ExpenseManager()
        self.budget_calculator = BudgetCalculator()
        self.report_generator = ReportGenerator()
        
        # Animation variables
        self.animation_running = False
        
        # Configure modern styles
        self.setup_modern_styles()
        
        # Create modern interface
        self.create_modern_interface()
        
        # Initial update
        self.update_display()
    
    def setup_modern_styles(self):
        """Configure modern visual styles and themes."""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Modern label styles with safe fonts
        style.configure('Title.TLabel', 
                       font=get_font('Segoe UI', 24, 'bold'),
                       foreground=self.colors["text_primary"],
                       background=self.colors["background"])
        
        style.configure('Heading.TLabel',
                       font=get_font('Segoe UI', 14, 'bold'),
                       foreground=self.colors["text_primary"],
                       background=self.colors["surface"])
        
        style.configure('Body.TLabel',
                       font=get_font('Segoe UI', 10),
                       foreground=self.colors["text_secondary"],
                       background=self.colors["surface"])
        
        style.configure('Success.TLabel',
                       font=get_font('Segoe UI', 12, 'bold'),
                       foreground=self.colors["success"],
                       background=self.colors["surface"])
        
        style.configure('Warning.TLabel',
                       font=get_font('Segoe UI', 12, 'bold'),
                       foreground=self.colors["warning"],
                       background=self.colors["surface"])
        
        style.configure('Danger.TLabel',
                       font=get_font('Segoe UI', 12, 'bold'),
                       foreground=self.colors["danger"],
                       background=self.colors["surface"])
        
        # Modern frame styles
        style.configure('Card.TFrame',
                       background=self.colors["surface"],
                       relief="flat",
                       borderwidth=0)
        
        # Modern combobox
        style.configure('Modern.TCombobox',
                       font=get_font('Segoe UI', 11),
                       fieldbackground=self.colors["surface"],
                       background=self.colors["surface"],
                       borderwidth=1,
                       relief="solid")
        
        # Modern treeview
        style.configure('Modern.Treeview',
                       font=get_font('Segoe UI', 10),
                       background=self.colors["surface"],
                       foreground=self.colors["text_primary"],
                       fieldbackground=self.colors["surface"],
                       borderwidth=0,
                       relief="flat")
        
        style.configure('Modern.Treeview.Heading',
                       font=get_font('Segoe UI', 10, 'bold'),
                       background=self.colors["primary"],
                       foreground="white",
                       relief="flat")
    
    def create_modern_interface(self):
        """Create the modern interface with cards and contemporary layout."""
        # Configure root window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main scrollable canvas
        self.main_canvas = tk.Canvas(self.root, bg=self.colors["background"], 
                                    highlightthickness=0)
        self.main_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", 
                                 command=self.main_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main content frame
        self.main_frame = tk.Frame(self.main_canvas, bg=self.colors["background"])
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        
        # Create canvas window
        self.canvas_window = self.main_canvas.create_window(
            (0, 0), window=self.main_frame, anchor="nw")
        
        # Configure canvas scrolling
        self.main_canvas.bind("<Configure>", self.on_canvas_configure)
        self.main_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Create header
        self.create_modern_header()
        
        # Create dashboard layout
        self.create_dashboard_layout()
    
    def on_frame_configure(self, event):
        """Configure scroll region when frame size changes."""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Configure canvas window width when canvas size changes."""
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_modern_header(self):
        """Create modern header with branding and navigation."""
        header_frame = tk.Frame(self.main_frame, bg=self.colors["primary"], height=100)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Header content container with proper padding
        header_content = tk.Frame(header_frame, bg=self.colors["primary"])
        header_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Left side - App branding
        left_frame = tk.Frame(header_content, bg=self.colors["primary"])
        left_frame.pack(side="left", fill="y", expand=False)
        
        # App icon and title container
        title_container = tk.Frame(left_frame, bg=self.colors["primary"])
        title_container.pack(fill="both", expand=True)
        
        # Icon and title in same line
        icon_title_frame = tk.Frame(title_container, bg=self.colors["primary"])
        icon_title_frame.pack(anchor="w", pady=(5, 0))
        
        app_icon = tk.Label(icon_title_frame, text="💼", 
                          font=get_font("Segoe UI", 24), 
                          fg="white", bg=self.colors["primary"])
        app_icon.pack(side="left", padx=(0, 10))
        
        app_title = tk.Label(icon_title_frame, text="SmartBudget Pro", 
                           font=get_font("Segoe UI", 22, "bold"), 
                           fg="white", bg=self.colors["primary"])
        app_title.pack(side="left")
        
        # Subtitle on new line
        subtitle = tk.Label(title_container, text="🚀 Advanced Personal Finance Dashboard", 
                          font=get_font("Segoe UI", 11), 
                          fg="#B8E6FF", bg=self.colors["primary"])
        subtitle.pack(anchor="w", pady=(2, 0))
        
        # Center - Quick metrics
        center_frame = tk.Frame(header_content, bg=self.colors["primary"])
        center_frame.pack(side="left", fill="both", expand=True, padx=(50, 50))
        
        # Quick metrics container
        metrics_frame = tk.Frame(center_frame, bg=self.colors["primary"])
        metrics_frame.pack(anchor="center")
        
        # Current month indicator
        month_label = tk.Label(metrics_frame, text="Current Month Overview", 
                             font=get_font("Segoe UI", 10), 
                             fg="#B8E6FF", bg=self.colors["primary"])
        month_label.pack()
        
        # Right side - Status and balance
        right_frame = tk.Frame(header_content, bg=self.colors["primary"])
        right_frame.pack(side="right", fill="y")
        
        # Status container
        status_container = tk.Frame(right_frame, bg=self.colors["primary"])
        status_container.pack(anchor="e", pady=(5, 0))
        
        # Balance display - larger and more prominent
        self.quick_balance = tk.Label(status_container, text="Balance: $0.00", 
                                    font=get_font("Segoe UI", 16, "bold"), 
                                    fg="white", bg=self.colors["primary"])
        self.quick_balance.pack(anchor="e")
        
        # Status indicator with better styling
        status_frame = tk.Frame(status_container, bg=self.colors["primary"])
        status_frame.pack(anchor="e", pady=(5, 0))
        
        status_label = tk.Label(status_frame, text="Status:", 
                              font=get_font("Segoe UI", 9), 
                              fg="#B8E6FF", bg=self.colors["primary"])
        status_label.pack(side="left")
        
        self.status_indicator = tk.Label(status_frame, text="● On Track", 
                                       font=get_font("Segoe UI", 10, "bold"), 
                                       fg="#4CAF50", bg=self.colors["primary"])
        self.status_indicator.pack(side="left", padx=(5, 0))
    
    def create_dashboard_layout(self):
        """Create the main dashboard with modern card layout."""
        # Dashboard container with padding
        dashboard = tk.Frame(self.main_frame, bg=self.colors["background"])
        dashboard.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Configure grid for responsive design
        dashboard.columnconfigure(0, weight=1)
        dashboard.columnconfigure(1, weight=1)
        dashboard.columnconfigure(2, weight=1)
        
        # Row 1: Quick stats cards
        self.create_stats_cards(dashboard, 0)
        
        # Row 2: Income and expense input
        self.create_input_section(dashboard, 1)
        
        # Row 3: Expense list and budget overview
        self.create_overview_section(dashboard, 2)
        
        # Row 4: Action center
        self.create_action_center(dashboard, 3)
    
    def create_modern_card(self, parent, title, icon="", height=None):
        """Create a modern card container with shadow effect."""
        # Card container with shadow effect
        card_container = tk.Frame(parent, bg=self.colors["background"])
        
        # Shadow frame (offset) - darker for dark mode
        shadow = tk.Frame(card_container, bg="#0A0A0A", height=2)
        shadow.pack(fill="x", padx=(4, 0), pady=(4, 0))
        
        # Main card frame with dark styling
        card = tk.Frame(card_container, bg=self.colors["surface"], 
                       relief="flat", bd=1, highlightbackground=self.colors["border"],
                       highlightthickness=1)
        card.pack(fill="both", expand=True)
        
        if height:
            card.configure(height=height)
            card.pack_propagate(False)
        
        # Card header
        if title:
            header = tk.Frame(card, bg=self.colors["surface"], height=50)
            header.pack(fill="x", padx=20, pady=(15, 5))
            header.pack_propagate(False)
            
            if icon:
                icon_label = tk.Label(header, text=icon, font=("Segoe UI", 16), 
                                    fg=self.colors["primary"], bg=self.colors["surface"])
                icon_label.pack(side="left", padx=(0, 10))
            
            title_label = tk.Label(header, text=title, font=("Segoe UI", 14, "bold"), 
                                 fg=self.colors["text_primary"], bg=self.colors["surface"])
            title_label.pack(side="left", anchor="w")
        
        # Card content area
        content = tk.Frame(card, bg=self.colors["surface"])
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        return card_container, content
    
    def create_stats_cards(self, parent, row):
        """Create the quick stats cards row."""
        stats_frame = tk.Frame(parent, bg=self.colors["background"])
        stats_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)
        
        # Income card
        income_card, income_content = self.create_modern_card(stats_frame, "", height=120)
        income_card.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        income_icon = tk.Label(income_content, text="💰", font=get_font("Segoe UI", 24), 
                             bg=self.colors["surface"])
        income_icon.pack(pady=(10, 5))
        
        self.income_amount_label = tk.Label(income_content, text="$0.00", 
                                          font=get_font("Segoe UI", 18, "bold"), 
                                          fg=self.colors["success"], 
                                          bg=self.colors["surface"])
        self.income_amount_label.pack()
        
        income_label = tk.Label(income_content, text="Monthly Income", 
                              font=get_font("Segoe UI", 10), 
                              fg=self.colors["text_secondary"], 
                              bg=self.colors["surface"])
        income_label.pack()
        
        # Expenses card
        expenses_card, expenses_content = self.create_modern_card(stats_frame, "", height=120)
        expenses_card.grid(row=0, column=1, sticky="ew", padx=5)
        
        expenses_icon = tk.Label(expenses_content, text="💸", font=("Segoe UI", 24), 
                               bg=self.colors["surface"])
        expenses_icon.pack(pady=(10, 5))
        
        self.expenses_amount_label = tk.Label(expenses_content, text="$0.00", 
                                            font=("Segoe UI", 18, "bold"), 
                                            fg=self.colors["danger"], 
                                            bg=self.colors["surface"])
        self.expenses_amount_label.pack()
        
        expenses_label = tk.Label(expenses_content, text="Total Expenses", 
                                font=("Segoe UI", 10), 
                                fg=self.colors["text_secondary"], 
                                bg=self.colors["surface"])
        expenses_label.pack()
        
        # Balance card
        balance_card, balance_content = self.create_modern_card(stats_frame, "", height=120)
        balance_card.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        
        balance_icon = tk.Label(balance_content, text="📊", font=("Segoe UI", 24), 
                              bg=self.colors["surface"])
        balance_icon.pack(pady=(10, 5))
        
        self.balance_amount_label = tk.Label(balance_content, text="$0.00", 
                                           font=("Segoe UI", 18, "bold"), 
                                           fg=self.colors["primary"], 
                                           bg=self.colors["surface"])
        self.balance_amount_label.pack()
        
        balance_label = tk.Label(balance_content, text="Remaining Balance", 
                               font=("Segoe UI", 10), 
                               fg=self.colors["text_secondary"], 
                               bg=self.colors["surface"])
        balance_label.pack()
    
    def create_input_section(self, parent, row):
        """Create the modern input section with income and expenses."""
        input_frame = tk.Frame(parent, bg=self.colors["background"])
        input_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        
        # Income input card
        income_card, income_content = self.create_modern_card(input_frame, "Set Monthly Income", "💰")
        income_card.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Income input
        income_input_frame = tk.Frame(income_content, bg=self.colors["surface"])
        income_input_frame.pack(fill="x", pady=(10, 0))
        
        self.income_entry = ModernEntry(income_input_frame, placeholder="Enter monthly income...", 
                                       colors=self.colors)
        self.income_entry.pack(fill="x", pady=(0, 10))
        
        income_btn = ModernButton(income_input_frame, "Set Income", 
                                command=self.set_income, width=140, height=40)
        income_btn.pack()
        
        # Expense input card
        expense_card, expense_content = self.create_modern_card(input_frame, "Add Expense", "🛒")
        expense_card.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        # Category selection
        cat_frame = tk.Frame(expense_content, bg=self.colors["surface"])
        cat_frame.pack(fill="x", pady=(10, 5))
        
        cat_label = tk.Label(cat_frame, text="Category", font=get_font("Segoe UI", 10), 
                           fg=self.colors["text_secondary"], bg=self.colors["surface"])
        cat_label.pack(anchor="w")
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(cat_frame, textvariable=self.category_var,
                                         values=self.expense_manager.get_categories(),
                                         state="readonly", style="Modern.TCombobox")
        self.category_combo.pack(fill="x", pady=(2, 0))
        self.category_combo.set(self.expense_manager.get_categories()[0])
        
        # Amount input
        self.expense_amount_entry = ModernEntry(expense_content, placeholder="Amount...", 
                                              colors=self.colors)
        self.expense_amount_entry.pack(fill="x", pady=5)
        
        # Description input
        self.expense_desc_entry = ModernEntry(expense_content, placeholder="Description (optional)...", 
                                            colors=self.colors)
        self.expense_desc_entry.pack(fill="x", pady=(0, 10))
        
        expense_btn = ModernButton(expense_content, "Add Expense", 
                                 command=self.add_expense, width=140, height=40)
        expense_btn.pack()
    
    def create_overview_section(self, parent, row):
        """Create the overview section with expense list and savings."""
        overview_frame = tk.Frame(parent, bg=self.colors["background"])
        overview_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        overview_frame.columnconfigure(0, weight=2)
        overview_frame.columnconfigure(1, weight=1)
        
        # Expense graph card
        expense_card, expense_content = self.create_modern_card(overview_frame, "Expense Breakdown", "📊")
        expense_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Create the expense graph widget
        graph_frame = tk.Frame(expense_content, bg=self.colors["surface"])
        graph_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        self.expense_graph = ExpenseGraphWidget(graph_frame, self.colors, width=500, height=300)
        self.expense_graph.pack(fill="both", expand=True)
        
        # Add graph controls
        controls_frame = tk.Frame(expense_content, bg=self.colors["surface"])
        controls_frame.pack(fill="x", pady=(10, 0))
        
        # View toggle buttons
        view_label = tk.Label(controls_frame, text="View:", 
                            font=get_font("Segoe UI", 9), 
                            fg=self.colors["text_secondary"], 
                            bg=self.colors["surface"])
        view_label.pack(side="left", padx=(0, 10))
        
        self.chart_type_var = tk.StringVar(value="pie")
        
        pie_btn = tk.Radiobutton(controls_frame, text="Pie Chart", 
                               variable=self.chart_type_var, value="pie",
                               command=self.update_chart_type,
                               font=get_font("Segoe UI", 9),
                               fg=self.colors["text_primary"],
                               bg=self.colors["surface"],
                               selectcolor=self.colors["surface_light"],
                               activebackground=self.colors["surface"])
        pie_btn.pack(side="left", padx=(0, 10))
        
        # Recent expenses mini list (compact)
        recent_frame = tk.Frame(expense_content, bg=self.colors["surface"])
        recent_frame.pack(fill="x", pady=(15, 0))
        
        recent_label = tk.Label(recent_frame, text="Recent Transactions:", 
                              font=get_font("Segoe UI", 10, "bold"), 
                              fg=self.colors["text_primary"], 
                              bg=self.colors["surface"])
        recent_label.pack(anchor="w")
        
        # Scrollable recent expenses
        self.recent_expenses_frame = tk.Frame(recent_frame, bg=self.colors["surface"])
        self.recent_expenses_frame.pack(fill="x", pady=(5, 0))
        
        # Savings and alerts card
        savings_card, savings_content = self.create_modern_card(overview_frame, "Savings & Alerts", "🎯")
        savings_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Savings goal input
        savings_input_frame = tk.Frame(savings_content, bg=self.colors["surface"])
        savings_input_frame.pack(fill="x", pady=(10, 0))
        
        savings_label = tk.Label(savings_input_frame, text="Monthly Savings Goal", 
                               font=get_font("Segoe UI", 10), 
                               fg=self.colors["text_secondary"], bg=self.colors["surface"])
        savings_label.pack(anchor="w", pady=(0, 5))
        
        self.savings_entry = ModernEntry(savings_input_frame, placeholder="Target amount...", 
                                       colors=self.colors)
        self.savings_entry.pack(fill="x", pady=(0, 10))
        
        savings_btn = ModernButton(savings_input_frame, "Set Goal", 
                                 command=self.set_savings_goal, width=120, height=35)
        savings_btn.pack()
        
        # Savings progress display
        progress_frame = tk.Frame(savings_content, bg=self.colors["surface"])
        progress_frame.pack(fill="x", pady=(20, 0))
        
        self.savings_progress_label = tk.Label(progress_frame, text="No savings goal set", 
                                             font=("Segoe UI", 11), 
                                             fg=self.colors["text_secondary"], 
                                             bg=self.colors["surface"])
        self.savings_progress_label.pack(anchor="w")
        
        # Progress bar visualization
        self.progress_canvas = tk.Canvas(progress_frame, height=20, 
                                       bg=self.colors["surface"], highlightthickness=0)
        self.progress_canvas.pack(fill="x", pady=(10, 0))
        
        # Alerts area
        alerts_frame = tk.Frame(savings_content, bg=self.colors["surface"])
        alerts_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        alerts_label = tk.Label(alerts_frame, text="Budget Alerts", 
                              font=("Segoe UI", 11, "bold"), 
                              fg=self.colors["text_primary"], bg=self.colors["surface"])
        alerts_label.pack(anchor="w", pady=(0, 10))
        
        self.alerts_text = tk.Text(alerts_frame, height=4, wrap=tk.WORD, 
                                 font=get_font("Segoe UI", 9), bg=self.colors["surface_light"], 
                                 fg=self.colors["text_secondary"], 
                                 relief="flat", bd=0, state=tk.DISABLED)
        self.alerts_text.pack(fill="both", expand=True)
    
    def create_action_center(self, parent, row):
        """Create the action center with main buttons."""
        action_frame = tk.Frame(parent, bg=self.colors["background"])
        action_frame.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        
        # Action buttons container
        buttons_frame = tk.Frame(action_frame, bg=self.colors["background"])
        buttons_frame.pack()
        
        # Primary actions
        refresh_btn = ModernButton(buttons_frame, "🔄 Refresh", 
                                 command=self.update_display,
                                 bg_color=self.colors["primary"],
                                 hover_color=self.colors["primary_dark"],
                                 width=150, height=45)
        refresh_btn.pack(side="left", padx=5)
        
        clear_btn = ModernButton(buttons_frame, "🗑️ Clear All", 
                               command=self.clear_expenses,
                               bg_color=self.colors["warning"],
                               hover_color="#E6A043",
                               width=150, height=45)
        clear_btn.pack(side="left", padx=5)
        
        report_btn = ModernButton(buttons_frame, "📊 Generate Report", 
                                command=self.generate_report,
                                bg_color=self.colors["success"],
                                hover_color="#4CAE4C",
                                width=150, height=45)
        report_btn.pack(side="left", padx=5)
        
        export_btn = ModernButton(buttons_frame, "💾 Export Report", 
                                command=self.export_report,
                                bg_color=self.colors["secondary"],
                                hover_color="#5A6B6F",
                                width=150, height=45)
        export_btn.pack(side="left", padx=5)
    
    def draw_progress_bar(self, percentage):
        """Draw an animated progress bar."""
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        
        if width <= 1:  # Canvas not yet rendered
            return
        
        # Background
        self.progress_canvas.create_rectangle(0, 0, width, height, 
                                            fill="#E9ECEF", outline="")
        
        # Progress fill
        if percentage > 0:
            fill_width = int((percentage / 100) * width)
            color = self.colors["success"] if percentage <= 100 else self.colors["danger"]
            self.progress_canvas.create_rectangle(0, 0, fill_width, height, 
                                                fill=color, outline="")
        
        # Progress text
        text = f"{percentage:.1f}%"
        self.progress_canvas.create_text(width//2, height//2, text=text, 
                                       font=("Segoe UI", 8, "bold"), 
                                       fill="white" if percentage > 30 else self.colors["text_primary"])
    
    def update_chart_type(self):
        """Update the chart display type."""
        # Update graph with current data
        self.update_expense_graph()

    def update_expense_graph(self):
        """Update the expense graph with current data."""
        # Get expense data by category
        expenses_by_category = self.expense_manager.get_expenses_by_category()
        category_totals = {}
        
        for category, expenses in expenses_by_category.items():
            total = sum(expense['amount'] for expense in expenses)
            if total > 0:
                category_totals[category] = total
        
        # Update the graph
        self.expense_graph.update_data(category_totals)

    def update_recent_expenses_list(self):
        """Update the compact recent expenses list."""
        # Clear existing items
        for widget in self.recent_expenses_frame.winfo_children():
            widget.destroy()
        
        # Get recent expenses (last 5)
        all_expenses = []
        expenses_by_category = self.expense_manager.get_expenses_by_category()
        
        for category, expenses in expenses_by_category.items():
            for expense in expenses:
                expense_item = expense.copy()
                expense_item['category'] = category
                all_expenses.append(expense_item)
        
        # Show last 5 expenses
        recent_expenses = all_expenses[-5:] if len(all_expenses) > 5 else all_expenses
        
        if not recent_expenses:
            no_data_label = tk.Label(self.recent_expenses_frame, 
                                   text="No recent transactions", 
                                   font=get_font("Segoe UI", 9),
                                   fg=self.colors["text_muted"], 
                                   bg=self.colors["surface"])
            no_data_label.pack(anchor="w")
            return
        
        for expense in reversed(recent_expenses):  # Show newest first
            item_frame = tk.Frame(self.recent_expenses_frame, bg=self.colors["surface"])
            item_frame.pack(fill="x", pady=1)
            
            # Category and amount
            category_label = tk.Label(item_frame, 
                                    text=f"{expense['category']}: ${expense['amount']:.2f}",
                                    font=get_font("Segoe UI", 9),
                                    fg=self.colors["text_primary"], 
                                    bg=self.colors["surface"])
            category_label.pack(side="left")
            
            # Description if available
            if expense.get('description'):
                desc_label = tk.Label(item_frame, 
                                    text=f"- {expense['description'][:20]}{'...' if len(expense['description']) > 20 else ''}",
                                    font=get_font("Segoe UI", 8),
                                    fg=self.colors["text_secondary"], 
                                    bg=self.colors["surface"])
                desc_label.pack(side="right")

    # Modern action methods updated for new widgets
    
    def set_income(self):
        """Handle setting the monthly income."""
        try:
            amount = self.income_entry.get().strip()
            if not amount:
                messagebox.showerror("Error", "Please enter an income amount.")
                return
            
            self.income_manager.set_income(amount)
            self.income_entry.set("")
            self.update_display()
            self.show_success_animation()
            messagebox.showinfo("Success", f"Income set to ${self.income_manager.get_income():.2f}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def add_expense(self):
        """Handle adding a new expense."""
        try:
            category = self.category_var.get()
            amount = self.expense_amount_entry.get().strip()
            description = self.expense_desc_entry.get().strip()
            
            if not amount:
                messagebox.showerror("Error", "Please enter an expense amount.")
                return
            
            self.expense_manager.add_expense(category, amount, description)
            
            # Clear input fields
            self.expense_amount_entry.set("")
            self.expense_desc_entry.set("")
            
            self.update_display()
            self.show_success_animation()
            messagebox.showinfo("Success", f"Added ${float(amount):.2f} expense in {category}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def set_savings_goal(self):
        """Handle setting the savings goal."""
        try:
            goal = self.savings_entry.get().strip()
            if not goal:
                messagebox.showerror("Error", "Please enter a savings goal amount.")
                return
            
            self.budget_calculator.set_savings_goal(goal)
            self.savings_entry.set("")
            self.update_display()
            self.show_success_animation()
            messagebox.showinfo("Success", f"Savings goal set to ${self.budget_calculator.get_savings_goal():.2f}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def show_success_animation(self):
        """Show a brief success animation."""
        # Quick flash animation for visual feedback
        original_bg = self.root.cget("bg")
        self.root.configure(bg="#E8F5E8")
        self.root.after(100, lambda: self.root.configure(bg=original_bg))
    
    def clear_expenses(self):
        """Clear all expenses after confirmation."""
        result = messagebox.askyesno("Confirm", "Are you sure you want to clear all expenses?")
        if result:
            self.expense_manager.clear_expenses()
            self.update_display()
            messagebox.showinfo("Success", "All expenses have been cleared.")
    
    def update_display(self):
        """Update all display elements with current data and modern styling."""
        # Get current data
        income = self.income_manager.get_income()
        total_expenses = self.expense_manager.get_total_expenses()
        remaining_balance = self.budget_calculator.calculate_remaining_balance(income, total_expenses)
        
        # Update header stats
        self.quick_balance.config(text=f"Balance: ${remaining_balance:.2f}")
        
        # Update status indicator
        if remaining_balance >= 0:
            if income > 0 and (total_expenses / income) <= 0.8:
                self.status_indicator.config(text="● On Track", fg="#90EE90")
            else:
                self.status_indicator.config(text="● Warning", fg="#FFD700")
        else:
            self.status_indicator.config(text="● Over Budget", fg="#FF6B6B")
        
        # Update stats cards
        self.income_amount_label.config(text=f"${income:.2f}")
        self.expenses_amount_label.config(text=f"${total_expenses:.2f}")
        
        # Color code balance
        if remaining_balance >= 0:
            self.balance_amount_label.config(text=f"${remaining_balance:.2f}", 
                                           fg=self.colors["success"])
        else:
            self.balance_amount_label.config(text=f"${remaining_balance:.2f}", 
                                           fg=self.colors["danger"])
        
        # Update expense graph (replaces tree)
        self.update_expense_graph()
        
        # Update recent expenses list
        self.update_recent_expenses_list()
        
        # Update savings display
        self.update_modern_savings_display(remaining_balance)
        
        # Update alerts
        self.update_modern_alerts_display(income, total_expenses, remaining_balance)
    
    def update_modern_savings_display(self, remaining_balance):
        """Update the modern savings goal display with progress bar."""
        savings_progress = self.budget_calculator.calculate_savings_progress(remaining_balance)
        
        if savings_progress['goal_amount'] == 0:
            self.savings_progress_label.config(text="No savings goal set")
            self.progress_canvas.delete("all")
        else:
            progress_text = (f"Goal: ${savings_progress['goal_amount']:.2f} | "
                           f"Current: ${savings_progress['current_savings']:.2f}")
            
            if savings_progress['goal_met']:
                self.savings_progress_label.config(text=progress_text + " ✓", 
                                                 fg=self.colors["success"])
            else:
                shortfall = savings_progress['shortfall']
                self.savings_progress_label.config(
                    text=progress_text + f" (${shortfall:.2f} short)", 
                    fg=self.colors["warning"])
            
            # Update progress bar
            self.root.after(10, lambda: self.draw_progress_bar(savings_progress['progress_percentage']))
    
    def update_modern_alerts_display(self, income, total_expenses, remaining_balance):
        """Update the modern alerts display."""
        warnings = self.budget_calculator.check_budget_warnings(income, total_expenses, remaining_balance)
        
        self.alerts_text.config(state=tk.NORMAL)
        self.alerts_text.delete(1.0, tk.END)
        
        if warnings:
            # Clean warnings for better display
            clean_warnings = []
            for warning in warnings:
                clean_warning = warning.replace("⚠️", "•").replace("💰", "•")
                clean_warnings.append(clean_warning)
            
            alert_text = "\n".join(clean_warnings)
            self.alerts_text.insert(1.0, alert_text)
            self.alerts_text.config(bg="#4A3600", fg=self.colors["warning"])  # Dark warning colors
        else:
            self.alerts_text.insert(1.0, "✓ No budget warnings\nYou're doing great!")
            self.alerts_text.config(bg="#1A3D1A", fg=self.colors["success"])  # Dark success colors
        
        self.alerts_text.config(state=tk.DISABLED)
        
        # Show critical warnings
        critical_warnings = [w for w in warnings if "OVERSPENDING" in w]
        if critical_warnings:
            messagebox.showwarning("⚠️ Budget Alert", critical_warnings[0])
    

    
    def generate_report(self):
        """Generate and display a budget report."""
        try:
            report_content = self.report_generator.generate_report(
                self.income_manager, 
                self.expense_manager, 
                self.budget_calculator
            )
            
            # Show report in a new window
            self.show_report_window(report_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def export_report(self):
        """Export budget report to a text file."""
        try:
            # Ask user for filename
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Budget Report"
            )
            
            if filename:
                report_content = self.report_generator.generate_report(
                    self.income_manager, 
                    self.expense_manager, 
                    self.budget_calculator
                )
                
                # Save to specified location
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(report_content)
                
                messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")
    
    def show_report_window(self, report_content):
        """Show the report in a modern styled window."""
        report_window = tk.Toplevel(self.root)
        report_window.title("📊 Budget Report - SmartBudget Pro")
        report_window.geometry("800x650")
        report_window.configure(bg=self.colors["background"])
        report_window.resizable(True, True)
        
        # Center the window
        report_window.transient(self.root)
        report_window.grab_set()
        
        # Modern header
        header = tk.Frame(report_window, bg=self.colors["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.colors["primary"])
        header_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        title = tk.Label(header_content, text="📊 Budget Report", 
                        font=("Segoe UI", 16, "bold"), 
                        fg="white", bg=self.colors["primary"])
        title.pack(side="left")
        
        # Report content frame
        content_frame = tk.Frame(report_window, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Modern text widget with styling
        text_frame = tk.Frame(content_frame, bg=self.colors["surface"],
                             relief="solid", bd=1, highlightbackground=self.colors["border"],
                             highlightthickness=1)
        text_frame.pack(fill="both", expand=True)
        
        # Text widget
        text_widget = tk.Text(text_frame, wrap=tk.WORD, 
                             font=get_font('Consolas', 10), 
                             bg=self.colors["surface"],
                             fg=self.colors["text_primary"],
                             relief="flat", bd=0,
                             padx=15, pady=15,
                             selectbackground=self.colors["primary"],
                             selectforeground="white")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", 
                                 command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Insert and format report content
        text_widget.insert(1.0, report_content)
        text_widget.config(state=tk.DISABLED)
        
        # Modern action buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["background"])
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Button container centered
        btn_container = tk.Frame(button_frame, bg=self.colors["background"])
        btn_container.pack()
        
        close_btn = ModernButton(btn_container, "✕ Close", 
                               command=report_window.destroy,
                               bg_color=self.colors["secondary"],
                               hover_color="#5A6B6F",
                               width=120, height=40)
        close_btn.pack(side="left", padx=5)
        
        def save_report():
            """Save report from the preview window."""
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Budget Report"
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(report_content)
                    messagebox.showinfo("Success", f"Report saved to:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save report: {e}")
        
        save_btn = ModernButton(btn_container, "💾 Save As...", 
                              command=save_report,
                              bg_color=self.colors["success"],
                              hover_color="#4CAE4C",
                              width=120, height=40)
        save_btn.pack(side="left", padx=5)


def main():
    """Main function to run the modern SmartBudget application."""
    root = tk.Tk()
    
    # Modern window configuration
    root.title("SmartBudget Pro - Dark Edition")
    root.configure(bg="#1E1E1E")
    
    # Try to set window icon (optional)
    try:
        # Modern window styling for Windows
        root.wm_attributes('-transparentcolor', root['bg'])
    except tk.TclError:
        pass  # Ignore if not supported
    
    # Create the modern application
    app = SmartBudgetUI(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
