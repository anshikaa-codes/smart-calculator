import customtkinter as ctk
import math
# App settings
ctk.set_appearance_mode("black")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Calculator")
app.geometry("700x550")

# ================= MAIN LAYOUT =================
# Sidebar (left side)
sidebar = ctk.CTkFrame(app, width=150, corner_radius=0)
sidebar.pack(side="left", fill="y")

# Content area (right side) — yahan alag alag calculators dikhenge
content_area = ctk.CTkFrame(app)
content_area.pack(side="right", fill="both", expand=True)

# Logo/App name at top of sidebar
logo_label = ctk.CTkLabel(sidebar, text="🧮 Smart\nCalculator", font=("Arial", 18, "bold"))
logo_label.pack(pady=30)

# ================= FUNCTION TO SWITCH PAGES =================
def clear_content():
    for widget in content_area.winfo_children():
        widget.destroy()

def show_coming_soon(name):
    clear_content()
    label = ctk.CTkLabel(content_area, text=f"{name}\n\nComing Soon!", font=("Arial", 24))
    label.pack(expand=True)

# ================= BASIC CALCULATOR PAGE =================
def show_basic_calculator():
    clear_content()

    result_var = ctk.StringVar(value="0")
    display = ctk.CTkEntry(content_area, textvariable=result_var, font=("Arial", 32),
                            justify="right", height=70)
    display.pack(fill="x", padx=10, pady=10)

    current_input = {"value": ""}

    def button_click(value):
        current_input["value"] += str(value)
        result_var.set(current_input["value"])

    def clear():
        current_input["value"] = ""
        result_var.set("0")

    def calculate():
        try:
            result = str(eval(current_input["value"]))
            result_var.set(result)
            current_input["value"] = result
        except Exception:
            result_var.set("Error")
            current_input["value"] = ""

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"],
    ]

    button_frame = ctk.CTkFrame(content_area)
    button_frame.pack(expand=True, fill="both", padx=10, pady=10)

    for row in buttons:
        row_frame = ctk.CTkFrame(button_frame)
        row_frame.pack(expand=True, fill="both")
        for btn_text in row:
            if btn_text == "=":
                cmd = calculate
            elif btn_text == "C":
                cmd = clear
            else:
                cmd = lambda x=btn_text: button_click(x)

            btn = ctk.CTkButton(row_frame, text=btn_text, font=("Arial", 22), command=cmd)
            btn.pack(side="left", expand=True, fill="both", padx=5, pady=5)

# ================= SCIENTIFIC CALCULATOR PAGE =================
def show_scientific_calculator():
    clear_content()

    result_var = ctk.StringVar(value="0")
    display = ctk.CTkEntry(content_area, textvariable=result_var, font=("Arial", 28),
                            justify="right", height=60)
    display.pack(fill="x", padx=10, pady=10)

    current_input = {"value": ""}

    def button_click(value):
        current_input["value"] += str(value)
        result_var.set(current_input["value"])

    def clear():
        current_input["value"] = ""
        result_var.set("0")

    def calculate():
        try:
            expression = current_input["value"]
            expression = expression.replace("^", "**")
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log10")
            expression = expression.replace("ln", "math.log")
            result = str(eval(expression))
            result_var.set(result)
            current_input["value"] = result
        except Exception:
            result_var.set("Error")
            current_input["value"] = ""

    def factorial():
        try:
            n = int(current_input["value"])
            result = str(math.factorial(n))
            result_var.set(result)
            current_input["value"] = result
        except Exception:
            result_var.set("Error")
            current_input["value"] = ""

    buttons = [
        ["sin", "cos", "tan", "C"],
        ["log", "ln", "sqrt(", ")"],
        ["7", "8", "9", "("],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["^", "n!", "/", ""],
    ]

    button_frame = ctk.CTkFrame(content_area)
    button_frame.pack(expand=True, fill="both", padx=10, pady=10)

    for row in buttons:
        row_frame = ctk.CTkFrame(button_frame)
        row_frame.pack(expand=True, fill="both")
        for btn_text in row:
            if btn_text == "":
                spacer = ctk.CTkLabel(row_frame, text="")
                spacer.pack(side="left", expand=True, fill="both", padx=5, pady=5)
                continue

            if btn_text == "=":
                cmd = calculate
            elif btn_text == "C":
                cmd = clear
            elif btn_text == "n!":
                cmd = factorial
            else:
                cmd = lambda x=btn_text: button_click(x)

            btn = ctk.CTkButton(row_frame, text=btn_text, font=("Arial", 18), command=cmd)
            btn.pack(side="left", expand=True, fill="both", padx=5, pady=5)

# ================= DATE CALCULATOR PAGE =================
def show_date_calculator():
    from datetime import datetime
    clear_content()

    title = ctk.CTkLabel(content_area, text="Date Calculator", font=("Arial", 22, "bold"))
    title.pack(pady=15)

    # ---------- Section 1: Date Difference ----------
    diff_frame = ctk.CTkFrame(content_area)
    diff_frame.pack(fill="x", padx=20, pady=10)

    diff_label = ctk.CTkLabel(diff_frame, text="Date Difference (DD-MM-YYYY)", font=("Arial", 16, "bold"))
    diff_label.pack(pady=5)

    entry_row1 = ctk.CTkFrame(diff_frame)
    entry_row1.pack(pady=5)

    start_date_entry = ctk.CTkEntry(entry_row1, placeholder_text="Start date (DD-MM-YYYY)", width=200)
    start_date_entry.pack(side="left", padx=5)

    end_date_entry = ctk.CTkEntry(entry_row1, placeholder_text="End date (DD-MM-YYYY)", width=200)
    end_date_entry.pack(side="left", padx=5)

    diff_result = ctk.CTkLabel(diff_frame, text="", font=("Arial", 16))
    diff_result.pack(pady=10)

    def calculate_difference():
        try:
            d1 = datetime.strptime(start_date_entry.get(), "%d-%m-%Y")
            d2 = datetime.strptime(end_date_entry.get(), "%d-%m-%Y")
            diff = abs((d2 - d1).days)
            diff_result.configure(text=f"Difference: {diff} days")
        except Exception:
            diff_result.configure(text="Invalid date format! Use DD-MM-YYYY")

    diff_btn = ctk.CTkButton(diff_frame, text="Calculate Difference", command=calculate_difference)
    diff_btn.pack(pady=5)

    # ---------- Section 2: Age Calculator ----------
    age_frame = ctk.CTkFrame(content_area)
    age_frame.pack(fill="x", padx=20, pady=20)

    age_label = ctk.CTkLabel(age_frame, text="Age Calculator (DD-MM-YYYY)", font=("Arial", 16, "bold"))
    age_label.pack(pady=5)

    dob_entry = ctk.CTkEntry(age_frame, placeholder_text="Date of Birth (DD-MM-YYYY)", width=250)
    dob_entry.pack(pady=5)

    age_result = ctk.CTkLabel(age_frame, text="", font=("Arial", 16))
    age_result.pack(pady=10)

    def calculate_age():
        try:
            dob = datetime.strptime(dob_entry.get(), "%d-%m-%Y")
            today = datetime.now()
            years = today.year - dob.year
            months = today.month - dob.month
            days = today.day - dob.day

            if days < 0:
                months -= 1
            if months < 0:
                years -= 1
                months += 12

            age_result.configure(text=f"Age: {years} years, {months} months")
        except Exception:
            age_result.configure(text="Invalid date format! Use DD-MM-YYYY")

    age_btn = ctk.CTkButton(age_frame, text="Calculate Age", command=calculate_age)
    age_btn.pack(pady=5)
        
# ================= SIDEBAR BUTTONS =================
nav_buttons = [
    ("Basic", show_basic_calculator),
    ("Scientific", show_scientific_calculator),
    ("Date", show_date_calculator),
    ("Currency", lambda: show_coming_soon("Currency Converter")),
    ("History", lambda: show_coming_soon("History")),
]

for name, command in nav_buttons:
    btn = ctk.CTkButton(sidebar, text=name, font=("Arial", 16), command=command)
    btn.pack(pady=10, padx=20, fill="x")

# App khulte hi Basic Calculator dikhe
show_basic_calculator()

app.mainloop()