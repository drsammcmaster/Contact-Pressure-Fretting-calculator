import math
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Function to calculate the coefficient of friction
# This function takes the friction force and normal force as inputs

#Friction force is in mN 
# Normal force is in mN 

def coefficient_of_friction(friction_force, normal_force):
    if normal_force == 0:
        raise ValueError("Normal force cannot be zero.")
    return friction_force / normal_force

def rms(values):
    if not values:
        raise ValueError("Empty list provided for RMS calculation.")
    return math.sqrt(sum(v**2 for v in values) / len(values))

def read_time_and_friction_from_file(filename):
    times = []
    frictions = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split()
                if len(parts) < 2:
                    raise ValueError("Each line must have at least two columns: time and friction.")
                time = float(parts[0])
                friction = float(parts[1])
                times.append(time)
                frictions.append(friction)
    return times, frictions

def average_over_cycles(values, cycle_size):
    """Average the values over a specified number of cycles (groups)."""
    if cycle_size < 1 or cycle_size > len(values):
        raise ValueError("Cycle size must be between 1 and the length of the values list.")
    averaged = []
    for i in range(0, len(values), cycle_size):
        group = values[i:i+cycle_size]
        avg = sum(group) / len(group)
        averaged.append(avg)
    return averaged

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # File open dialog
    filename = filedialog.askopenfilename(
        title="Select friction force data file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filename:
        messagebox.showerror("Error", "No file selected.")
        exit()

    # Normal force input dialog
    try:
        normal_force = float(simpledialog.askstring("Normal Force", "Enter the normal force (mN):"))
    except (TypeError, ValueError):
        messagebox.showerror("Error", "Invalid normal force entered.")
        exit()

    try:
        times, frictions = read_time_and_friction_from_file(filename)
        total_points = len(frictions)
        # Ask user for number of cycles
        num_cycles = simpledialog.askinteger("Number of Cycles", "Enter the number of friction cycles:", initialvalue=50, minvalue=1, maxvalue=total_points)
        if not num_cycles or num_cycles < 1:
            messagebox.showerror("Error", "Invalid number of cycles entered.")
            exit()
        points_per_cycle = total_points // num_cycles
        remainder = total_points % num_cycles

        # Split frictions into num_cycles groups, distributing remainder points to the first groups
        max_friction = []
        start = 0
        for i in range(num_cycles):
            group_size = points_per_cycle + (1 if i < remainder else 0)
            group = [abs(f) for f in frictions[start:start+group_size]]
            max_val = max(group) if group else 0
            max_friction.append(max_val)
            start += group_size

        result_lines = [
            "Cycle\tMax friction force (mN)\tMax Coefficient of Friction",
        ]
        for i, f in enumerate(max_friction, start=1):
            mu = coefficient_of_friction(f, normal_force)
            result_lines.append(f"{i}\t{f:.6f}\t{mu:.6f}")
        messagebox.showinfo("Result", "Max friction and coefficient of friction calculated per cycle.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        exit()

    # File save dialog
    export_filename = filedialog.asksaveasfilename(
        title="Export averaged coefficient of friction per cycle",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if export_filename:
        with open(export_filename, 'w') as f:
            f.write('\n'.join(result_lines))
        messagebox.showinfo("Exported", f"Result exported to {export_filename}")
