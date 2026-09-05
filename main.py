import customtkinter as ctk
import math
import json
import os

# App settings
ctk.set_appearance_mode("black")
ctk.set_default_color_theme("blue")

# ================= HISTORY STORAGE =================
HISTORY_FILE = "data/history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history_entry(calculation, result):
    history = load_history()
    history.append({"calculation": calculation, "result": result})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

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
            expression = current_input["value"]
            result = str(eval(expression))
            save_history_entry(expression, result)
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

# ================= CURRENCY CONVERTER PAGE =================
def show_currency_converter():
    import requests
    import socket
    clear_content()

    title = ctk.CTkLabel(content_area, text="Currency Converter", font=("Arial", 22, "bold"))
    title.pack(pady=(15, 5))

    # ---------- NETWORK STATUS CHECK ----------
    def check_internet():
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    is_online = check_internet()
    status_text = "🟢 Online" if is_online else "🔴 Offline"
    status_color = "green" if is_online else "red"

    status_label = ctk.CTkLabel(content_area, text=status_text, font=("Arial", 13, "bold"), text_color=status_color)
    status_label.pack(pady=(0, 10))

    currency_options = {
        "Afghanistan - Afghani (AFN)": "AFN",
        "Albania - Lek (ALL)": "ALL",
        "Algeria - Dinar (DZD)": "DZD",
        "Andorra - Euro (EUR)": "EUR",
        "Angola - Kwanza (AOA)": "AOA",
        "Antigua and Barbuda - East Caribbean Dollar (XCD)": "XCD",
        "Argentina - Peso (ARS)": "ARS",
        "Armenia - Dram (AMD)": "AMD",
        "Australia - Dollar (AUD)": "AUD",
        "Austria - Euro (EUR)": "EUR",
        "Azerbaijan - Manat (AZN)": "AZN",
        "Bahamas - Dollar (BSD)": "BSD",
        "Bahrain - Dinar (BHD)": "BHD",
        "Bangladesh - Taka (BDT)": "BDT",
        "Barbados - Dollar (BBD)": "BBD",
        "Belarus - Ruble (BYN)": "BYN",
        "Belgium - Euro (EUR)": "EUR",
        "Belize - Dollar (BZD)": "BZD",
        "Benin - CFA Franc (XOF)": "XOF",
        "Bhutan - Ngultrum (BTN)": "BTN",
        "Bolivia - Boliviano (BOB)": "BOB",
        "Bosnia and Herzegovina - Mark (BAM)": "BAM",
        "Botswana - Pula (BWP)": "BWP",
        "Brazil - Real (BRL)": "BRL",
        "Brunei - Dollar (BND)": "BND",
        "Bulgaria - Lev (BGN)": "BGN",
        "Burkina Faso - CFA Franc (XOF)": "XOF",
        "Burundi - Franc (BIF)": "BIF",
        "Cabo Verde - Escudo (CVE)": "CVE",
        "Cambodia - Riel (KHR)": "KHR",
        "Cameroon - CFA Franc (XAF)": "XAF",
        "Canada - Dollar (CAD)": "CAD",
        "Central African Republic - CFA Franc (XAF)": "XAF",
        "Chad - CFA Franc (XAF)": "XAF",
        "Chile - Peso (CLP)": "CLP",
        "China - Yuan (CNY)": "CNY",
        "Colombia - Peso (COP)": "COP",
        "Comoros - Franc (KMF)": "KMF",
        "Congo (Republic) - CFA Franc (XAF)": "XAF",
        "Congo (DRC) - Franc (CDF)": "CDF",
        "Costa Rica - Colon (CRC)": "CRC",
        "Croatia - Euro (EUR)": "EUR",
        "Cuba - Peso (CUP)": "CUP",
        "Cyprus - Euro (EUR)": "EUR",
        "Czech Republic - Koruna (CZK)": "CZK",
        "Denmark - Krone (DKK)": "DKK",
        "Djibouti - Franc (DJF)": "DJF",
        "Dominica - East Caribbean Dollar (XCD)": "XCD",
        "Dominican Republic - Peso (DOP)": "DOP",
        "Ecuador - US Dollar (USD)": "USD",
        "Egypt - Pound (EGP)": "EGP",
        "El Salvador - US Dollar (USD)": "USD",
        "Equatorial Guinea - CFA Franc (XAF)": "XAF",
        "Eritrea - Nakfa (ERN)": "ERN",
        "Estonia - Euro (EUR)": "EUR",
        "Eswatini - Lilangeni (SZL)": "SZL",
        "Ethiopia - Birr (ETB)": "ETB",
        "Fiji - Dollar (FJD)": "FJD",
        "Finland - Euro (EUR)": "EUR",
        "France - Euro (EUR)": "EUR",
        "Gabon - CFA Franc (XAF)": "XAF",
        "Gambia - Dalasi (GMD)": "GMD",
        "Georgia - Lari (GEL)": "GEL",
        "Germany - Euro (EUR)": "EUR",
        "Ghana - Cedi (GHS)": "GHS",
        "Greece - Euro (EUR)": "EUR",
        "Grenada - East Caribbean Dollar (XCD)": "XCD",
        "Guatemala - Quetzal (GTQ)": "GTQ",
        "Guinea - Franc (GNF)": "GNF",
        "Guinea-Bissau - CFA Franc (XOF)": "XOF",
        "Guyana - Dollar (GYD)": "GYD",
        "Haiti - Gourde (HTG)": "HTG",
        "Honduras - Lempira (HNL)": "HNL",
        "Hungary - Forint (HUF)": "HUF",
        "Iceland - Krona (ISK)": "ISK",
        "India - Rupee (INR)": "INR",
        "Indonesia - Rupiah (IDR)": "IDR",
        "Iran - Rial (IRR)": "IRR",
        "Iraq - Dinar (IQD)": "IQD",
        "Ireland - Euro (EUR)": "EUR",
        "Israel - Shekel (ILS)": "ILS",
        "Italy - Euro (EUR)": "EUR",
        "Jamaica - Dollar (JMD)": "JMD",
        "Japan - Yen (JPY)": "JPY",
        "Jordan - Dinar (JOD)": "JOD",
        "Kazakhstan - Tenge (KZT)": "KZT",
        "Kenya - Shilling (KES)": "KES",
        "Kiribati - Australian Dollar (AUD)": "AUD",
        "Kosovo - Euro (EUR)": "EUR",
        "Kuwait - Dinar (KWD)": "KWD",
        "Kyrgyzstan - Som (KGS)": "KGS",
        "Laos - Kip (LAK)": "LAK",
        "Latvia - Euro (EUR)": "EUR",
        "Lebanon - Pound (LBP)": "LBP",
        "Lesotho - Loti (LSL)": "LSL",
        "Liberia - Dollar (LRD)": "LRD",
        "Libya - Dinar (LYD)": "LYD",
        "Liechtenstein - Swiss Franc (CHF)": "CHF",
        "Lithuania - Euro (EUR)": "EUR",
        "Luxembourg - Euro (EUR)": "EUR",
        "Madagascar - Ariary (MGA)": "MGA",
        "Malawi - Kwacha (MWK)": "MWK",
        "Malaysia - Ringgit (MYR)": "MYR",
        "Maldives - Rufiyaa (MVR)": "MVR",
        "Mali - CFA Franc (XOF)": "XOF",
        "Malta - Euro (EUR)": "EUR",
        "Marshall Islands - US Dollar (USD)": "USD",
        "Mauritania - Ouguiya (MRU)": "MRU",
        "Mauritius - Rupee (MUR)": "MUR",
        "Mexico - Peso (MXN)": "MXN",
        "Micronesia - US Dollar (USD)": "USD",
        "Moldova - Leu (MDL)": "MDL",
        "Monaco - Euro (EUR)": "EUR",
        "Mongolia - Tugrik (MNT)": "MNT",
        "Montenegro - Euro (EUR)": "EUR",
        "Morocco - Dirham (MAD)": "MAD",
        "Mozambique - Metical (MZN)": "MZN",
        "Myanmar - Kyat (MMK)": "MMK",
        "Namibia - Dollar (NAD)": "NAD",
        "Nauru - Australian Dollar (AUD)": "AUD",
        "Nepal - Rupee (NPR)": "NPR",
        "Netherlands - Euro (EUR)": "EUR",
        "New Zealand - Dollar (NZD)": "NZD",
        "Nicaragua - Cordoba (NIO)": "NIO",
        "Niger - CFA Franc (XOF)": "XOF",
        "Nigeria - Naira (NGN)": "NGN",
        "North Korea - Won (KPW)": "KPW",
        "North Macedonia - Denar (MKD)": "MKD",
        "Norway - Krone (NOK)": "NOK",
        "Oman - Rial (OMR)": "OMR",
        "Pakistan - Rupee (PKR)": "PKR",
        "Palau - US Dollar (USD)": "USD",
        "Panama - Balboa (PAB)": "PAB",
        "Papua New Guinea - Kina (PGK)": "PGK",
        "Paraguay - Guarani (PYG)": "PYG",
        "Peru - Sol (PEN)": "PEN",
        "Philippines - Peso (PHP)": "PHP",
        "Poland - Zloty (PLN)": "PLN",
        "Portugal - Euro (EUR)": "EUR",
        "Qatar - Riyal (QAR)": "QAR",
        "Romania - Leu (RON)": "RON",
        "Russia - Ruble (RUB)": "RUB",
        "Rwanda - Franc (RWF)": "RWF",
        "Saint Kitts and Nevis - East Caribbean Dollar (XCD)": "XCD",
        "Saint Lucia - East Caribbean Dollar (XCD)": "XCD",
        "Saint Vincent - East Caribbean Dollar (XCD)": "XCD",
        "Samoa - Tala (WST)": "WST",
        "San Marino - Euro (EUR)": "EUR",
        "Sao Tome and Principe - Dobra (STN)": "STN",
        "Saudi Arabia - Riyal (SAR)": "SAR",
        "Senegal - CFA Franc (XOF)": "XOF",
        "Serbia - Dinar (RSD)": "RSD",
        "Seychelles - Rupee (SCR)": "SCR",
        "Sierra Leone - Leone (SLE)": "SLE",
        "Singapore - Dollar (SGD)": "SGD",
        "Slovakia - Euro (EUR)": "EUR",
        "Slovenia - Euro (EUR)": "EUR",
        "Solomon Islands - Dollar (SBD)": "SBD",
        "Somalia - Shilling (SOS)": "SOS",
        "South Africa - Rand (ZAR)": "ZAR",
        "South Korea - Won (KRW)": "KRW",
        "South Sudan - Pound (SSP)": "SSP",
        "Spain - Euro (EUR)": "EUR",
        "Sri Lanka - Rupee (LKR)": "LKR",
        "Sudan - Pound (SDG)": "SDG",
        "Suriname - Dollar (SRD)": "SRD",
        "Sweden - Krona (SEK)": "SEK",
        "Switzerland - Franc (CHF)": "CHF",
        "Syria - Pound (SYP)": "SYP",
        "Taiwan - Dollar (TWD)": "TWD",
        "Tajikistan - Somoni (TJS)": "TJS",
        "Tanzania - Shilling (TZS)": "TZS",
        "Thailand - Baht (THB)": "THB",
        "Timor-Leste - US Dollar (USD)": "USD",
        "Togo - CFA Franc (XOF)": "XOF",
        "Tonga - Paanga (TOP)": "TOP",
        "Trinidad and Tobago - Dollar (TTD)": "TTD",
        "Tunisia - Dinar (TND)": "TND",
        "Turkey - Lira (TRY)": "TRY",
        "Turkmenistan - Manat (TMT)": "TMT",
        "Tuvalu - Australian Dollar (AUD)": "AUD",
        "Uganda - Shilling (UGX)": "UGX",
        "Ukraine - Hryvnia (UAH)": "UAH",
        "United Arab Emirates - Dirham (AED)": "AED",
        "United Kingdom - Pound (GBP)": "GBP",
        "United States - Dollar (USD)": "USD",
        "Uruguay - Peso (UYU)": "UYU",
        "Uzbekistan - Som (UZS)": "UZS",
        "Vanuatu - Vatu (VUV)": "VUV",
        "Vatican City - Euro (EUR)": "EUR",
        "Venezuela - Bolivar (VES)": "VES",
        "Vietnam - Dong (VND)": "VND",
        "Yemen - Rial (YER)": "YER",
        "Zambia - Kwacha (ZMW)": "ZMW",
        "Zimbabwe - Dollar (ZWL)": "ZWL",
    }
    currency_names = list(currency_options.keys())

    # ---------- FROM SECTION ----------
    from_frame = ctk.CTkFrame(content_area)
    from_frame.pack(fill="x", padx=25, pady=(5, 10))

    from_label = ctk.CTkLabel(from_frame, text="From", font=("Arial", 13), text_color="gray")
    from_label.pack(anchor="w", padx=10, pady=(8, 0))

    amount_entry = ctk.CTkEntry(from_frame, placeholder_text="Enter amount", font=("Arial", 24), height=50)
    amount_entry.pack(fill="x", padx=10, pady=(5, 5))

    from_currency = ctk.CTkOptionMenu(from_frame, values=currency_names, width=280)
    from_currency.set("India - Rupee (INR)")
    from_currency.pack(padx=10, pady=(0, 10))

    # ---------- TO SECTION ----------
    to_frame = ctk.CTkFrame(content_area)
    to_frame.pack(fill="x", padx=25, pady=10)

    to_label = ctk.CTkLabel(to_frame, text="To", font=("Arial", 13), text_color="gray")
    to_label.pack(anchor="w", padx=10, pady=(8, 0))

    result_value = ctk.CTkLabel(to_frame, text="0", font=("Arial", 24, "bold"), anchor="w")
    result_value.pack(fill="x", padx=10, pady=(5, 5))

    to_currency = ctk.CTkOptionMenu(to_frame, values=currency_names, width=280)
    to_currency.set("United States - Dollar (USD)")
    to_currency.pack(padx=10, pady=(0, 10))

    rate_info = ctk.CTkLabel(content_area, text="", font=("Arial", 12), text_color="gray")
    rate_info.pack(pady=5)

    # ---------- CONVERT LOGIC ----------
    def convert_currency():
        if not check_internet():
            status_label.configure(text="🔴 Offline", text_color="red")
            result_value.configure(text="Error")
            rate_info.configure(text="No internet connection")
            return

        status_label.configure(text="🟢 Online", text_color="green")
        try:
            amount = float(amount_entry.get())
            from_curr = currency_options[from_currency.get()]
            to_curr = currency_options[to_currency.get()]

            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url, timeout=8)
            data = response.json()

            rate = data["rates"][to_curr]
            converted = amount * rate

            result_value.configure(text=f"{converted:.2f} {to_curr}")
            rate_info.configure(text=f"1 {from_curr} = {rate:.4f} {to_curr}")
        except KeyError:
            result_value.configure(text="Error")
            rate_info.configure(text="Invalid currency selection")
        except Exception:
            result_value.configure(text="Error")
            rate_info.configure(text="Enter a valid amount")

    convert_btn = ctk.CTkButton(content_area, text="Convert", command=convert_currency,
                                  font=("Arial", 16, "bold"), width=200, height=45)
    convert_btn.pack(pady=15)

    # ---------- CREATED BY (bottom right, small) ----------
    credit_label = ctk.CTkLabel(content_area, text="BY ANSHIKA", font=("Arial", 10), text_color="gray")
    credit_label.pack(side="bottom", anchor="e", padx=15, pady=8)

    
# ================= HISTORY PAGE =================
def show_history():
    clear_content()

    title = ctk.CTkLabel(content_area, text="Calculation History", font=("Arial", 22, "bold"))
    title.pack(pady=15)

    history = load_history()

    if not history:
        empty_label = ctk.CTkLabel(content_area, text="No history yet!", font=("Arial", 16))
        empty_label.pack(pady=30)
    else:
        scroll_frame = ctk.CTkScrollableFrame(content_area, width=500, height=350)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        for entry in reversed(history):
            entry_text = f'{entry["calculation"]} = {entry["result"]}'
            entry_label = ctk.CTkLabel(scroll_frame, text=entry_text, font=("Arial", 14), anchor="w")
            entry_label.pack(fill="x", padx=10, pady=5)

    def clear_history():
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)
        show_history()

    clear_btn = ctk.CTkButton(content_area, text="Clear History", command=clear_history,
                                fg_color="red", hover_color="darkred")
    clear_btn.pack(pady=15)


# ================= SIDEBAR BUTTONS =================
nav_buttons = [
    ("Basic", show_basic_calculator),
    ("Scientific", show_scientific_calculator),
    ("Date", show_date_calculator),
    ("Currency", show_currency_converter),
    ("History", show_history),
]

for name, command in nav_buttons:
    btn = ctk.CTkButton(sidebar, text=name, font=("Arial", 16), command=command)
    btn.pack(pady=10, padx=20, fill="x")

# App khulte hi Basic Calculator dikhe
show_basic_calculator()

app.mainloop()