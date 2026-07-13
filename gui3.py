import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class BillingSystem:
    def __init__(self, root):
        self.root = root
        
        # Title bar සහ icon ඉවත් කිරීම
        self.root.overrideredirect(True)
        self.root.geometry("950x750+150+50")
        
        self.is_maximized = False
        
        # Shop Menu Data
        self.menu = {
            "Slippers": 1200.00,
            "Necklace": 450.00,
            "Bracelet": 350.00,
            "Flower Bouquet": 1500.00,
            "Teddy Bear": 950.00,
            "Chocolates": 250.00
        }
        
        self.cart = []
        self.total_amount = 0.0
        
        self.create_custom_title_bar()
        self.create_widgets()

    def create_custom_title_bar(self):
        self.title_bar = tk.Frame(self.root, bg="#eeeeee", height=30)
        self.title_bar.pack(fill="x", side="top")
        
        title_label = tk.Label(self.title_bar, text="  K & K Fancy Shop - Billing System", bg="#eeeeee", fg="#333333", font=("Helvetica", 10))
        title_label.pack(side="left", pady=5)
        
        btn_font = ("Helvetica", 10)
        btn_w = 4
        
        close_button = tk.Button(self.title_bar, text="✕", bg="#eeeeee", fg="#333333", borderwidth=0, font=btn_font, width=btn_w, command=self.root.destroy, activebackground="#f44336", activeforeground="white")
        close_button.pack(side="right", fill="y")
        
        self.max_button = tk.Button(self.title_bar, text="▢", bg="#eeeeee", fg="#333333", borderwidth=0, font=btn_font, width=btn_w, command=self.toggle_maximize, activebackground="#ddd", activeforeground="#333")
        self.max_button.pack(side="right", fill="y")
        
        min_button = tk.Button(self.title_bar, text="—", bg="#eeeeee", fg="#333333", borderwidth=0, font=btn_font, width=btn_w, command=self.minimize_window, activebackground="#ddd", activeforeground="#333")
        min_button.pack(side="right", fill="y")
        
        self.title_bar.bind("<Button-1>", self.get_pos)
        self.title_bar.bind("<B1-Motion>", self.move_window)
        title_label.bind("<Button-1>", self.get_pos)
        title_label.bind("<B1-Motion>", self.move_window)

    def get_pos(self, event):
        if not self.is_maximized:
            self.xwin = event.x
            self.ywin = event.y

    def move_window(self, event):
        if not self.is_maximized:
            self.root.geometry(f'+{event.x_root - self.xwin}+{event.y_root - self.ywin}')

    def minimize_window(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state('iconic')
        self.root.bind("<FocusIn>", self.on_deiconify)

    def on_deiconify(self, event):
        self.root.update_idletasks()
        if self.root.state() == 'normal':
            self.root.overrideredirect(True)
            self.root.unbind("<FocusIn>")

    def toggle_maximize(self):
        if not self.is_maximized:
            self.prev_geometry = self.root.geometry()
            self.root.state('zoomed') 
            self.max_button.config(text="⧉")
            self.is_maximized = True
        else:
            self.root.state('normal')
            self.root.geometry(self.prev_geometry)
            self.max_button.config(text="▢")
            self.is_maximized = False

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bd=1, relief="solid")
        main_frame.pack(fill="both", expand=True)
        
        title_label = tk.Label(main_frame, text="K & K FANCY SHOP", font=("Helvetica", 18, "bold"), fg="purple")
        title_label.pack(pady=(20, 5))
        
        input_frame = tk.Frame(main_frame, padx=15, pady=15)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(input_frame, text="Customer Name:", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.customer_entry = tk.Entry(input_frame, font=("Helvetica", 10), width=25)
        self.customer_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(input_frame, text="Select Item:", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.item_combo = ttk.Combobox(input_frame, values=list(self.menu.keys()), font=("Helvetica", 10), state="readonly", width=23)
        self.item_combo.grid(row=1, column=1, pady=5, padx=5)
        self.item_combo.current(0)
        
        tk.Label(input_frame, text="Quantity:", font=("Helvetica", 10)).grid(row=1, column=2, sticky="w", pady=5, padx=15)
        self.qty_entry = tk.Entry(input_frame, font=("Helvetica", 10), width=8)
        self.qty_entry.grid(row=1, column=3, pady=5)
        self.qty_entry.insert(0, "1")
        
        add_btn = tk.Button(input_frame, text="Add to Cart", font=("Helvetica", 10, "bold"), bg="#4CAF50", fg="white", command=self.add_to_cart, width=15)
        add_btn.grid(row=1, column=4, padx=20)

        middle_frame = tk.Frame(main_frame, pady=10)
        middle_frame.pack(padx=20, fill="both", expand=True)
        
        cart_sub_frame = tk.Frame(middle_frame)
        cart_sub_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        tk.Label(cart_sub_frame, text="Cart Items (Added List):", font=("Helvetica", 11, "bold"), fg="green").pack(anchor="w")
        self.cart_listbox = tk.Listbox(cart_sub_frame, font=("Courier", 11), bg="#f4fbf4")
        self.cart_listbox.pack(fill="both", expand=True, pady=5)
        
        invoice_sub_frame = tk.Frame(middle_frame)
        invoice_sub_frame.grid(row=0, column=2, sticky="nsew")
        
        tk.Label(invoice_sub_frame, text="Final Invoice Preview:", font=("Helvetica", 11, "bold"), fg="blue").pack(anchor="w")
        
        invoice_scroll = tk.Scrollbar(invoice_sub_frame)
        invoice_scroll.pack(side="right", fill="y")
        
        self.invoice_text = tk.Text(invoice_sub_frame, font=("Courier", 11), bg="#f9f9f9", yscrollcommand=invoice_scroll.set)
        self.invoice_text.pack(side="left", fill="both", expand=True, pady=5)
        invoice_scroll.config(command=self.invoice_text.yview)
        
        middle_frame.grid_columnconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(2, weight=1)
        middle_frame.grid_rowconfigure(0, weight=1)
        
        bottom_frame = tk.Frame(main_frame, pady=15)
        bottom_frame.pack(padx=20, fill="x")
        
        self.total_label = tk.Label(bottom_frame, text="Total Amount: LKR 0.00", font=("Helvetica", 14, "bold"), fg="red")
        self.total_label.pack(side="left")
        
        clear_btn = tk.Button(bottom_frame, text="Clear All", font=("Helvetica", 10, "bold"), bg="#f44336", fg="white", command=self.clear_all, width=12)
        clear_btn.pack(side="right", padx=5)
        
        generate_btn = tk.Button(bottom_frame, text="Generate Bill", font=("Helvetica", 10, "bold"), bg="#FF9800", fg="white", command=self.generate_bill, width=15)
        generate_btn.pack(side="right", padx=5)

    def add_to_cart(self):
        item = self.item_combo.get()
        qty_str = self.qty_entry.get()
        
        try:
            qty = int(qty_str)
            if qty <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for quantity.")
            return
            
        price = self.menu[item]
        item_total = price * qty
        self.total_amount += item_total
        
        self.cart.append({
            "item": item,
            "price": price,
            "quantity": qty,
            "total": item_total
        })
        
        self.cart_listbox.insert(tk.END, f"{item:<15} x{qty:<4} LKR {item_total:.2f}")
        self.total_label.config(text=f"Total Amount: LKR {self.total_amount:.2f}")
        
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")

    def generate_bill(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Your cart is empty! Please add items first.")
            return
            
        customer = self.customer_entry.get().strip()
        if not customer:
            customer = "Valued Customer"
            
        bill_txt = f"==================================================\n"
        bill_txt += f"               K & K FANCY SHOP                   \n"
        bill_txt += f"==================================================\n"
        bill_txt += f"Customer: {customer}\n"
        bill_txt += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill_txt += f"--------------------------------------------------\n"
        bill_txt += f"{'Item':<18}{'Qty':<6}{'Price':<12}{'Total':<12}\n"
        bill_txt += f"--------------------------------------------------\n"
        
        for p in self.cart:
            bill_txt += f"{p['item']:<18}{p['quantity']:<6}{p['price']:<12.2f}{p['total']:<12.2f}\n"
            
        bill_txt += f"--------------------------------------------------\n"
        bill_txt += f"Total Amount: LKR {self.total_amount:.2f}\n"
        bill_txt += f"==================================================\n"
        bill_txt += f"            Thank You! Come Again.                \n"
        bill_txt += f"==================================================\n"
        
        self.invoice_text.delete("1.0", tk.END)
        self.invoice_text.insert(tk.END, bill_txt)

    def clear_all(self):
        self.cart.clear()
        self.total_amount = 0.0
        self.customer_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        self.cart_listbox.delete(0, tk.END)
        self.invoice_text.delete("1.0", tk.END)
        self.total_label.config(text="Total Amount: LKR 0.00")
        self.item_combo.current(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingSystem(root)
    root.mainloop()