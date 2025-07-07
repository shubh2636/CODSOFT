import tkinter as tk
from tkinter import ttk, messagebox
import math
from tkinter import scrolledtext

class AdvancedCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator with GST")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = tk.StringVar()
        self.result_var = tk.StringVar()
        self.gst_slabs = {
            "Exempt (0%)": 0,
            "5%": 5,
            "12%": 12,
            "18%": 18,
            "28%": 28
        }
        self.selected_gst = tk.StringVar(value="18%")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), padding=5)
        self.style.configure('TLabel', font=('Arial', 12))
        
        # Create UI
        self.create_display()
        self.create_gst_panel()
        self.create_buttons()
        self.create_history_panel()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.handle_key_press)
        
    def create_display(self):
        # Display frame
        display_frame = ttk.Frame(self.root, padding=10)
        display_frame.pack(fill=tk.X)
        
        # Entry for current input
        self.entry = ttk.Entry(display_frame, textvariable=self.current_input, 
                             font=('Arial', 24), justify='right')
        self.entry.pack(fill=tk.X, pady=5)
        self.entry.focus_set()
        
        # Result label
        result_label = ttk.Label(display_frame, textvariable=self.result_var,
                               font=('Arial', 18), anchor='e')
        result_label.pack(fill=tk.X, pady=5)
    
    def create_gst_panel(self):
        # GST frame
        gst_frame = ttk.LabelFrame(self.root, text="GST Calculator", padding=10)
        gst_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # GST Slab dropdown
        ttk.Label(gst_frame, text="Select GST Slab:").grid(row=0, column=0, sticky='w')
        gst_menu = ttk.Combobox(gst_frame, textvariable=self.selected_gst, 
                               values=list(self.gst_slabs.keys()), state='readonly')
        gst_menu.grid(row=0, column=1, padx=5, sticky='ew')
        
        # GST Buttons
        btn_frame = ttk.Frame(gst_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Add GST", command=self.add_gst).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove GST", command=self.remove_gst).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Calculate GST", command=self.calculate_gst).pack(side=tk.LEFT, padx=5)
    
    def create_buttons(self):
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Button layout
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3), ('√', 0, 4),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3), ('x²', 1, 4),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3), ('x!', 2, 4),
            ('0', 3, 0), ('.', 3, 1), ('C', 3, 2), ('+', 3, 3), ('=', 3, 4),
            ('(', 4, 0), (')', 4, 1), ('%', 4, 2), ('//', 4, 3), ('⌫', 4, 4)
        ]
        
        for (text, row, col) in buttons:
            btn = ttk.Button(button_frame, text=text, 
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            button_frame.rowconfigure(row, weight=1)
            button_frame.columnconfigure(col, weight=1)
    
    def create_history_panel(self):
        # History frame
        history_frame = ttk.LabelFrame(self.root, text="Calculation History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=5, 
                                                    font=('Arial', 10), wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.history_text.configure(state='disabled')
    
    def handle_key_press(self, event):
        key = event.char
        keys_mapping = {
            '\r': '=',
            '\x08': '⌫',
            '\x1b': 'C'
        }
        
        if key in keys_mapping:
            self.on_button_click(keys_mapping[key])
        elif key in '0123456789+-*/.()%':
            self.on_button_click(key)
        elif event.keysym == 'Escape':
            self.on_button_click('C')
        elif event.keysym == 'BackSpace':
            self.on_button_click('⌫')
        elif event.keysym == 'Return':
            self.on_button_click('=')
    
    def on_button_click(self, button_text):
        current = self.current_input.get()
        
        try:
            if button_text == 'C':
                self.current_input.set('')
                self.result_var.set('')
            elif button_text == '⌫':
                self.current_input.set(current[:-1])
            elif button_text == '=':
                self.calculate_result()
            elif button_text == '√':
                self.current_input.set(f"math.sqrt({current})")
            elif button_text == 'x²':
                self.current_input.set(f"({current})**2")
            elif button_text == 'x!':
                self.current_input.set(f"math.factorial(int({current}))")
            else:
                self.current_input.set(current + button_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.entry.focus_set()
    
    def calculate_result(self):
        try:
            expression = self.current_input.get()
            if not expression:
                return
                
            result = eval(expression, {'math': math})
            self.result_var.set(f"= {result}")
            self.add_to_history(f"{expression} = {result}")
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))
    
    def add_to_history(self, entry):
        self.history_text.configure(state='normal')
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.configure(state='disabled')
        self.history_text.see(tk.END)
    
    def get_gst_rate(self):
        return self.gst_slabs[self.selected_gst.get()]
    
    def add_gst(self):
        try:
            amount = float(self.current_input.get())
            gst_rate = self.get_gst_rate()
            gst_amount = amount * gst_rate / 100
            total = amount + gst_amount
            self.result_var.set(f"Original: ₹{amount:.2f}\nGST ({gst_rate}%): ₹{gst_amount:.2f}\nTotal: ₹{total:.2f}")
            self.add_to_history(f"Added {gst_rate}% GST to {amount} = {total}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount first")
    
    def remove_gst(self):
        try:
            total_amount = float(self.current_input.get())
            gst_rate = self.get_gst_rate()
            base_amount = total_amount / (1 + gst_rate/100)
            gst_amount = total_amount - base_amount
            self.result_var.set(f"Total: ₹{total_amount:.2f}\nGST ({gst_rate}%): ₹{gst_amount:.2f}\nBase: ₹{base_amount:.2f}")
            self.add_to_history(f"Removed {gst_rate}% GST from {total_amount} = {base_amount}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount first")
    
    def calculate_gst(self):
        try:
            amount = float(self.current_input.get())
            gst_rate = self.get_gst_rate()
            gst_amount = amount * gst_rate / 100
            total = amount + gst_amount
            self.result_var.set(f"Amount: ₹{amount:.2f}\nGST ({gst_rate}%): ₹{gst_amount:.2f}\nTotal: ₹{total:.2f}")
            self.add_to_history(f"Calculated {gst_rate}% GST for {amount} = {gst_amount}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount first")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculatorGUI(root)
    root.mainloop()