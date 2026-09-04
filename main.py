import customtkinter as ctk

# App ki basic settings
ctk.set_appearance_mode("dark")       # dark theme
ctk.set_default_color_theme("blue")   # blue accent color

app = ctk.CTk()
app.title("Smart Calculator")
app.geometry("400x550")

# Result dikhane wala box
result_var = ctk.StringVar(value="0")
display = ctk.CTkEntry(app, textvariable=result_var, font=("Arial", 32),
                        justify="right", height=70)
display.pack(fill="x", padx=10, pady=10)

current_input = ""

def button_click(value):
    global current_input
    current_input += str(value)
    result_var.set(current_input)

def clear():
    global current_input
    current_input = ""
    result_var.set("0")

def calculate():
    global current_input
    try:
        result = str(eval(current_input))
        result_var.set(result)
        current_input = result
    except Exception:
        result_var.set("Error")
        current_input = ""

# Buttons ki list (row-wise)
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"],
]

# Buttons ko grid me lagana
button_frame = ctk.CTkFrame(app)
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

        btn = ctk.CTkButton(row_frame, text=btn_text, font=("Arial", 22),
                             command=cmd)
        btn.pack(side="left", expand=True, fill="both", padx=5, pady=5)

app.mainloop()