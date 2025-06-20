import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from util.calibration.calibration_session import CalibrationSession
from util.uart_util import UARTUtil
import matplotlib
matplotlib.use('TkAgg')
import re
from collections import defaultdict

class RunView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.canvas = None
        self.ser = UARTUtil.open_port()

        label = tk.Label(self, text="Calibration", font=("Arial", 18))
        label.pack(side='top', anchor='n', pady=10)

        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("MenuView"),
                           font=("Arial", 12), width=10, height=2)
        button.pack(side='top', anchor='e')

        info_text = (
            "Select the rows you want to include.\n"
            "Click the checkbox to toggle selection. Double-click is disabled."
        )
        info_label = tk.Label(self, text=info_text, justify="left", fg="black", font=("Arial", 12))
        info_label.pack(pady=(0, 10))

        # Treeview for calibration data
        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill='both', expand=True)

        # Only two columns now: Selected and Index
        self.tree = ttk.Treeview(left_frame, columns=("Selected", "Index"), show="headings")
        self.tree.heading("Selected", text="Selected")
        self.tree.heading("Index", text="Index")
        self.tree.column("Selected", width=80, anchor="center")
        self.tree.column("Index", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Insert 50 rows with default selected state "[ ]"
        for i in range(50):
            self.tree.insert("", "end", values=("[ ]", i + 1))

        self.tree.bind("<Button-1>", self.on_click)

        button_frame = tk.Frame(self)
        button_frame.pack(side='top', anchor='e', pady=10)

    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if column != "#1":  # "Selected" column is now first
            return

        current = self.tree.set(row_id, "Selected")
        new_val = "[x]" if current.strip() == "[ ]" else "[ ]"
        self.tree.set(row_id, "Selected", new_val)

    def get_selected_indices(self):
        selected = []
        for item in self.tree.get_children():
            if self.tree.set(item, "Selected") == "[x]":
                selected.append(self.tree.set(item, "Index"))
        return selected
