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
        # Ask user for cycle size for averaging
        cycle_size = simpledialog.askinteger("Cycle Size", "Enter number of points per friction cycle to average:", initialvalue=5, minvalue=1, maxvalue=len(frictions))
        if not cycle_size:
            messagebox.showerror("Error", "Invalid cycle size entered.")
            exit()
        averaged_friction = average_over_cycles([abs(f) for f in frictions], cycle_size)
        averaged_times = average_over_cycles(times, cycle_size)
        result_lines = [
            "Averaged_Time\tAveraged_Friction\tAveraged_Coefficient_of_Friction"
        ]
        for t, f in zip(averaged_times, averaged_friction):
            mu = coefficient_of_friction(abs(f), normal_force)
            result_lines.append(f"{t:.6f}\t{f:.6f}\t{mu:.6f}")
        messagebox.showinfo("Result", "Averaged friction and coefficient of friction calculated over cycles.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        exit()

    # File save dialog
    export_filename = filedialog.asksaveasfilename(
        title="Export averaged coefficient of friction vs time",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if export_filename:
        with open(export_filename, 'w') as f:
            f.write('\n'.join(result_lines))
        messagebox.showinfo("Exported", f"Result exported to {export_filename}")
