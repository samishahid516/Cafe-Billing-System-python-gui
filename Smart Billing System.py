import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# CONSTANTS: Menu Items and Prices

MENU_ITEMS = {
    "Tea":        80,
    "Coffee":     120,
    "Sandwich":   180,
    "Burger":     250,
    "Fries":      150,
    "Juice":      130,
    "Cake Slice": 200,
    "Pasta":      280,
}

# AI Rule: Item suggestions (related items)
ITEM_SUGGESTIONS = {
    "Tea":        "Sandwich or Cake Slice",
    "Coffee":     "Cake Slice or Sandwich",
    "Sandwich":   "Tea or Coffee",
    "Burger":     "Fries or Juice",
    "Fries":      "Burger or Juice",
    "Juice":      "Burger or Sandwich",
    "Cake Slice": "Coffee or Tea",
    "Pasta":      "Juice or Fries",
}

TAX_RATE = 0.05  # 5% tax

# AI DECISION RULE: Auto-Discount Logic

def ai_discount_rule(subtotal: float, quantity: int) -> tuple[float, str]:

    if subtotal > 1000:
        return 15.0, "Big Spender Reward (>Rs.1000)"
    elif subtotal > 500:
        return 10.0, "Valued Customer Reward (>Rs.500)"
    elif quantity >= 5:
        return 8.0,  "Bulk Order Discount (qty ≥ 5)"
    elif quantity >= 3:
        return 5.0,  "Multi-Item Discount (qty ≥ 3)"
    else:
        return 0.0,  "No discount applied"


# MAIN APPLICATION CLASS

class SmartBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("☕ Smart Cafe Billing System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a2e")

        # Color palette
        self.bg_dark   = "#1a1a2e"
        self.bg_card   = "#16213e"
        self.accent    = "#e94560"
        self.accent2   = "#0f3460"
        self.text_main = "#eaeaea"
        self.text_mute = "#a0a0b0"
        self.green     = "#00d4aa"

        self._build_ui()

    #  BUILD FULL UI
    def _build_ui(self):
        #  Title Bar
        title_frame = tk.Frame(self.root, bg=self.accent, pady=10)
        title_frame.pack(fill="x")

        tk.Label(
            title_frame,
            text="☕  SMART CAFE BILLING SYSTEM",
            font=("Courier New", 18, "bold"),
            bg=self.accent,
            fg="white"
        ).pack(side="left", padx=20)

        # Live clock label
        self.clock_lbl = tk.Label(
            title_frame,
            text="",
            font=("Courier New", 11),
            bg=self.accent,
            fg="white"
        )
        self.clock_lbl.pack(side="right", padx=20)
        self._update_clock()

        # ── Main two-column layout
        main_frame = tk.Frame(self.root, bg=self.bg_dark)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Left panel: input form
        self._build_input_panel(main_frame)

        # Right panel: receipt output
        self._build_receipt_panel(main_frame)

    # ── LEFT PANEL: Input Form ───────────────
    def _build_input_panel(self, parent):
        left = tk.Frame(parent, bg=self.bg_card, bd=0,
                        highlightbackground=self.accent2, highlightthickness=1)
        left.pack(side="left", fill="both", expand=False,
                  padx=(0, 8), pady=0, ipadx=10, ipady=10)

        tk.Label(left, text="CUSTOMER & ORDER DETAILS",
                 font=("Courier New", 11, "bold"),
                 bg=self.bg_card, fg=self.accent).grid(
            row=0, column=0, columnspan=2, pady=(10, 15), padx=10)

        # Helper to create a labelled entry row
        def lbl_entry(row, label, var_attr):
            tk.Label(left, text=label, font=("Courier New", 10),
                     bg=self.bg_card, fg=self.text_mute, anchor="w"
                     ).grid(row=row, column=0, sticky="w", padx=12, pady=4)
            entry = tk.Entry(left, font=("Courier New", 11),
                             bg="#0d1b2a", fg=self.text_main,
                             insertbackground=self.accent,
                             relief="flat", bd=4, width=22)
            entry.grid(row=row, column=1, padx=10, pady=4, sticky="ew")
            setattr(self, var_attr, entry)

        lbl_entry(1, "Customer Name  :", "ent_name")
        lbl_entry(2, "Contact Number :", "ent_contact")

        # Item dropdown
        tk.Label(left, text="Select Item     :", font=("Courier New", 10),
                 bg=self.bg_card, fg=self.text_mute, anchor="w"
                 ).grid(row=3, column=0, sticky="w", padx=12, pady=4)

        self.item_var = tk.StringVar(value="Select an item")
        item_names = list(MENU_ITEMS.keys())
        self.item_menu = ttk.Combobox(
            left, textvariable=self.item_var,
            values=item_names, state="readonly",
            font=("Courier New", 11), width=20
        )
        self.item_menu.grid(row=3, column=1, padx=10, pady=4, sticky="ew")
        self.item_menu.bind("<<ComboboxSelected>>", self._on_item_select)

        # Price (auto-filled)
        tk.Label(left, text="Item Price (Rs):", font=("Courier New", 10),
                 bg=self.bg_card, fg=self.text_mute, anchor="w"
                 ).grid(row=4, column=0, sticky="w", padx=12, pady=4)
        self.ent_price = tk.Entry(left, font=("Courier New", 11),
                                  bg="#0d1b2a", fg=self.green,
                                  insertbackground=self.accent,
                                  relief="flat", bd=4, width=22, state="readonly")
        self.ent_price.grid(row=4, column=1, padx=10, pady=4, sticky="ew")

        lbl_entry(5, "Quantity        :", "ent_qty")

        # AI suggestion label
        self.suggest_var = tk.StringVar(value="")
        tk.Label(left, text="AI Suggestion  :", font=("Courier New", 10),
                 bg=self.bg_card, fg=self.text_mute, anchor="w"
                 ).grid(row=6, column=0, sticky="w", padx=12, pady=4)
        tk.Label(left, textvariable=self.suggest_var,
                 font=("Courier New", 9, "italic"),
                 bg=self.bg_card, fg=self.green, wraplength=160, justify="left"
                 ).grid(row=6, column=1, padx=10, pady=2, sticky="w")

        # AI discount info
        self.discount_info_var = tk.StringVar(value="")
        tk.Label(left, text="AI Discount Rule:", font=("Courier New", 10),
                 bg=self.bg_card, fg=self.text_mute, anchor="w"
                 ).grid(row=7, column=0, sticky="nw", padx=12, pady=4)
        tk.Label(left, textvariable=self.discount_info_var,
                 font=("Courier New", 9, "italic"),
                 bg=self.bg_card, fg="#f0c040", wraplength=160, justify="left"
                 ).grid(row=7, column=1, padx=10, pady=2, sticky="w")

        # Separator
        tk.Frame(left, bg=self.accent2, height=1).grid(
            row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # ── Action Buttons
        btn_frame = tk.Frame(left, bg=self.bg_card)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=6)

        btn_cfg = dict(font=("Courier New", 10, "bold"),
                       relief="flat", cursor="hand2",
                       padx=10, pady=6, bd=0)

        tk.Button(btn_frame, text="🧾 Generate Receipt",
                  bg=self.accent, fg="white",
                  command=self.generate_receipt,
                  **btn_cfg).grid(row=0, column=0, padx=6, pady=4)

        tk.Button(btn_frame, text="🗑  Clear",
                  bg=self.accent2, fg=self.text_main,
                  command=self.clear_all,
                  **btn_cfg).grid(row=0, column=1, padx=6, pady=4)

        tk.Button(btn_frame, text="💾 Save Receipt",
                  bg="#0f5e3e", fg="white",
                  command=self.save_receipt,
                  **btn_cfg).grid(row=1, column=0, padx=6, pady=4)

        tk.Button(btn_frame, text="🚪 Exit",
                  bg="#333355", fg=self.text_mute,
                  command=self.confirm_exit,
                  **btn_cfg).grid(row=1, column=1, padx=6, pady=4)

    # ── RIGHT PANEL: Receipt Output ──────────
    def _build_receipt_panel(self, parent):
        right = tk.Frame(parent, bg=self.bg_card, bd=0,
                         highlightbackground=self.accent2, highlightthickness=1)
        right.pack(side="left", fill="both", expand=True, pady=0, ipadx=10, ipady=10)

        tk.Label(right, text="RECEIPT PREVIEW",
                 font=("Courier New", 11, "bold"),
                 bg=self.bg_card, fg=self.accent).pack(pady=(10, 6))

        # Scrollable text widget for receipt
        txt_frame = tk.Frame(right, bg=self.bg_card)
        txt_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(txt_frame)
        scrollbar.pack(side="right", fill="y")

        self.receipt_text = tk.Text(
            txt_frame,
            font=("Courier New", 10),
            bg="#090e1a",
            fg=self.green,
            insertbackground=self.green,
            relief="flat",
            bd=6,
            wrap="word",
            yscrollcommand=scrollbar.set,
            state="disabled"
        )
        self.receipt_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.receipt_text.yview)

        # Default placeholder
        self._show_placeholder()

    # PLACEHOLDER TEXT
    def _show_placeholder(self):
        placeholder = (
        )
        self._write_receipt(placeholder)

    # LIVE CLOCK
    def _update_clock(self):
        now = datetime.now().strftime("%d-%b-%Y  %H:%M:%S")
        self.clock_lbl.config(text=f"🕐 {now}")
        self.root.after(1000, self._update_clock)

    # ITEM SELECTION HANDLER
    def _on_item_select(self, event=None):
        #  Auto-fill price and show AI suggestion when item selected.
        item = self.item_var.get()
        if item in MENU_ITEMS:
            # Auto-fill price (readonly)
            self.ent_price.config(state="normal")
            self.ent_price.delete(0, tk.END)
            self.ent_price.insert(0, str(MENU_ITEMS[item]))
            self.ent_price.config(state="readonly")

            # AI item suggestion
            suggestion = ITEM_SUGGESTIONS.get(item, "")
            self.suggest_var.set(f"Try also: {suggestion}")

        # Update AI discount preview if qty already entered
        self._preview_discount()

    # DISCOUNT PREVIEW
    def _preview_discount(self, event=None):
        # Show which AI discount rule would apply given current input.
        try:
            qty = int(self.ent_qty.get())
            item = self.item_var.get()
            if item in MENU_ITEMS and qty > 0:
                subtotal = MENU_ITEMS[item] * qty
                pct, reason = ai_discount_rule(subtotal, qty)
                if pct > 0:
                    self.discount_info_var.set(f"{pct}% → {reason}")
                else:
                    self.discount_info_var.set("No discount at this amount")
            else:
                self.discount_info_var.set("")
        except ValueError:
            self.discount_info_var.set("")

    #  INPUT VALIDATION
    def _validate_inputs(self) -> bool:
        # Validate all form fields. Shows messagebox on failure.
        name    = self.ent_name.get().strip()
        contact = self.ent_contact.get().strip()
        item    = self.item_var.get()
        qty_str = self.ent_qty.get().strip()

        # Name check
        if not name:
            messagebox.showerror("Validation Error", "Customer name cannot be empty.")
            self.ent_name.focus_set()
            return False
        if not name.replace(" ", "").isalpha():
            messagebox.showerror("Validation Error",
                                 "Customer name should contain letters only.")
            self.ent_name.focus_set()
            return False

        # Contact check
        if not contact:
            messagebox.showerror("Validation Error", "Contact number cannot be empty.")
            self.ent_contact.focus_set()
            return False
        if not contact.isdigit() or len(contact) not in (10, 11):
            messagebox.showerror("Validation Error",
                                 "Contact number must be 10 or 11 digits.")
            self.ent_contact.focus_set()
            return False

        # Item check
        if item not in MENU_ITEMS:
            messagebox.showerror("Validation Error", "Please select a valid menu item.")
            return False

        # Quantity check
        if not qty_str:
            messagebox.showerror("Validation Error", "Quantity cannot be empty.")
            self.ent_qty.focus_set()
            return False
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error",
                                 "Quantity must be a positive whole number.")
            self.ent_qty.focus_set()
            return False

        return True

    # GENERATE RECEIPT
    def generate_receipt(self):
        #  Validate inputs, compute bill, display receipt.
        if not self._validate_inputs():
            return

        # Gather inputs
        name    = self.ent_name.get().strip()
        contact = self.ent_contact.get().strip()
        item    = self.item_var.get()
        price   = MENU_ITEMS[item]
        qty     = int(self.ent_qty.get().strip())
        now     = datetime.now()

        # Calculations
        subtotal          = price * qty
        discount_pct, discount_reason = ai_discount_rule(subtotal, qty)
        discount_amount   = round(subtotal * discount_pct / 100, 2)
        after_discount    = subtotal - discount_amount
        tax_amount        = round(after_discount * TAX_RATE, 2)
        grand_total       = round(after_discount + tax_amount, 2)
        suggestion        = ITEM_SUGGESTIONS.get(item, "N/A")

        # Build receipt string
        line  = "─" * 38
        dline = "═" * 38
        receipt = f"""
{dline}
        ☕  SMART CAFE BILLING SYSTEM
{dline}
  Date  : {now.strftime("%d-%B-%Y")}
  Time  : {now.strftime("%I:%M:%S %p")}
{line}
  CUSTOMER DETAILS
{line}
  Name    : {name}
  Contact : {contact}
{line}
  ORDER DETAILS
{line}
  Item      : {item}
  Unit Price: Rs. {price:.2f}
  Quantity  : {qty}
{line}
  BILLING SUMMARY
{line}
  Subtotal         : Rs. {subtotal:.2f}
  AI Discount ({discount_pct:.0f}%): Rs. {discount_amount:.2f}
    → {discount_reason}
  After Discount   : Rs. {after_discount:.2f}
  Tax ({TAX_RATE*100:.0f}%)           : Rs. {tax_amount:.2f}
{dline}
  TOTAL PAYABLE    : Rs. {grand_total:.2f}
{dline}
  🤖 AI Suggestion:
     You might also enjoy: {suggestion}
{line}
   Thank you for visiting Smart Cafe!
        Visit again soon ☕
{dline}
"""
        self._write_receipt(receipt)

    # ── WRITE TO RECEIPT TEXT WIDGET ─────────
    def _write_receipt(self, text: str):
        self.receipt_text.config(state="normal")
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, text)
        self.receipt_text.config(state="disabled")

    # CLEAR ALL
    def clear_all(self):
        # Reset all input fields and receipt area.
        for entry in (self.ent_name, self.ent_contact, self.ent_qty):
            entry.delete(0, tk.END)

        self.item_var.set("Select an item")
        self.ent_price.config(state="normal")
        self.ent_price.delete(0, tk.END)
        self.ent_price.config(state="readonly")
        self.suggest_var.set("")
        self.discount_info_var.set("")
        self._show_placeholder()

    # SAVE RECEIPT
    def save_receipt(self):
        # Save the receipt text to a .txt file.
        content = self.receipt_text.get("1.0", tk.END).strip()
        if not content or "Fill in customer" in content:
            messagebox.showwarning("Nothing to Save",
                                   "Please generate a receipt first.")
            return
        filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved",
                                f"Receipt saved successfully as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file:\n{e}")

    # EXIT CONFIRMATION
    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


# ENTRY POINT

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBillingApp(root)

    # Bind quantity entry to live discount preview
    app.ent_qty.bind("<KeyRelease>", lambda e: app._preview_discount())

    root.protocol("WM_DELETE_WINDOW", app.confirm_exit)
    root.mainloop()