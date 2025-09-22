import tkinter as tk
from tkinter import filedialog, messagebox

def filter_sequences(input_file, output_file, size, mode):
    try:
        with open(input_file, 'r') as input, open(output_file, 'w') as output:
            sequence = ""
            header = ""
            for line in input:
                if line.startswith(">"):  # Found a header
                    if sequence and ((mode == "equal" and len(sequence) == size) or 
                                       (mode == "smaller" and len(sequence) < size) or 
                                       (mode == "larger" and len(sequence) > size)):
                        output.write(header + sequence + "\n")  # Save the sequence to the output file
                    header = line  # Store the new header
                    sequence = ""  # Reset the sequence
                else:
                    sequence += line.strip()  # Add bases to the current sequence
            # Check the last sequence in the file
            if sequence and ((mode == "equal" and len(sequence) == size) or 
                               (mode == "smaller" and len(sequence) < size) or 
                               (mode == "larger" and len(sequence) > size)):
                output.write(header + sequence + "\n")
        messagebox.showinfo("Success", f"Sequences of size {size} were saved to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_file():
    input_file = filedialog.askopenfilename(title="Select Input File")
    if input_file:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, input_file)

def execute_filter():
    input_file = entry_file.get()
    try:
        size = int(entry_size.get())
        if size <= 0:
            raise ValueError("Size must be greater than zero.")
        mode = variable.get()
        output_file = filedialog.asksaveasfilename(title="Save As", defaultextension=".txt")
        if output_file:
            filter_sequences(input_file, output_file, size, mode)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Graphical interface
root = tk.Tk()
root.title("Seq Sizer - Sequence Filter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Field to select the input file
label_file = tk.Label(frame, text="Input File:")
label_file.grid(row=0, column=0, sticky="w")

entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=0, column=1)

button_select = tk.Button(frame, text="Select", command=select_file)
button_select.grid(row=0, column=2)

# Field to enter the desired size
label_size = tk.Label(frame, text="Desired Size:")
label_size.grid(row=1, column=0, sticky="w")

entry_size = tk.Entry(frame, width=10)
entry_size.grid(row=1, column=1, sticky="w")

# Field to select the filter mode
label_mode = tk.Label(frame, text="Filter Mode:")
label_mode.grid(row=2, column=0, sticky="w")

variable = tk.StringVar(frame)
variable.set("equal")  # Default value

option_equal = tk.Radiobutton(frame, text="Equal to", variable=variable, value="equal")
option_equal.grid(row=2, column=1, sticky="w")

option_smaller = tk.Radiobutton(frame, text="Smaller than", variable=variable, value="smaller")
option_smaller.grid(row=3, column=1, sticky="w")

option_larger = tk.Radiobutton(frame, text="Larger than", variable=variable, value="larger")
option_larger.grid(row=4, column=1, sticky="w")

# Button to execute the filter
button_execute = tk.Button(frame, text="Execute Filter", command=execute_filter)
button_execute.grid(row=5, column=1, pady=10)

root.mainloop()