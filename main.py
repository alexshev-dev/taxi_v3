import json
import os
import platform
import re
from datetime import datetime
from tkinter import messagebox, filedialog

import customtkinter as ctk
from fpdf import FPDF, XPos, YPos

from simpleeval import simple_eval

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# === Шлях до файлу===
# def get_data_path(app_name = "TaxiApp"):
#     system = platform.system()
#     if system == "Windows":
#         base_dir = os.path.join(os.environ["APPDATA"], app_name)
#     elif system == "Darwin":  # macOS
#         base_dir = os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)
#     else:  # Linux або інше
#         base_dir = os.path.join(os.path.expanduser("~/.local/share"), app_name)
#
#     os.makedirs(base_dir, exist_ok=True)
#     return os.path.join(base_dir, "data.json")
#
#
# fname = get_data_path()

fname = "/Users/dim/PythonProjects/Taxi_testing/data/data.json"

data_window = None

root = ctk.CTk()
root.title('TAXI V 3.0')
root.attributes('-topmost', False)  # Встановлюємо поверх усіх вікон
root.focus_force()
root_width = 410
root_height = 790
root.resizable(False, False)

# ==== Отримати розмір екрана ====
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# ==== Розрахунок координат для центрування ====
x = int((screen_width - root_width) / 2.7)
y = int((screen_height - root_height) / 2.6)

root.geometry(f"{root_width}x{root_height}+{x}+{y}")

# ==== Frame ====
bg_color = ctk.ThemeManager.theme["CTk"]["fg_color"]
frame = ctk.CTkFrame(root, width=410, height=720, fg_color=bg_color)
frame.place(x=0, y=75)

# ===== Отримати поточну дату =====
months_ukr = {
    1: "Січня",
    2: "Лютого",
    3: "Березня",
    4: "Квітня",
    5: "Травня",
    6: "Червня",
    7: "Липня",
    8: "Серпня",
    9: "Вересня",
    10: "Жовтня",
    11: "Листопада",
    12: "Грудня",
}

month_nazv = {
    "Січень": "Січня",
    "Лютий": "Лютого",
    "Березень": "Березня",
    "Квітень": "Квітня",
    "Травень": "Травня",
    "Червень": "Червня",
    "Липень": "Липня",
    "Серпень": "Серпня",
    "Вересень": "Вересня",
    "Жовтень": "Жовтня",
    "Листопад": "Листопада",
    "Грудень": "Грудня",
}
current_month_index = datetime.now().month

days = [str(i).zfill(2) for i in range(1, 32)]
months = list(months_ukr.values())
years = [str(i) for i in range(2024, datetime.now().year + 1)]

# ===== Отримати час =====
start_times = [f"{h:02}:00" for h in range(0, 24)]
break_times = [f"{h:02}:00" for h in range(0, 11)]
end_times = [f"{h:02}:00" for h in range(0, 24)]

# ===== Блок автомобіль =====
auto_data = {
    "Audi": {
        "A1": [""], "A3": [""], "A4": [""], "A4 Allroad": [""], "A5": [""],
        "A6": [""], "A6 Allroad": [""], "A7": [""], "A8": [""], "Q2": [""],
        "Q3": [""], "Q4": [""], "Q4 e-tron": [""], "Q5": [""], "Q5 e-tron": [""],
        "Q6 e-tron": [""], "Q7": [""], "Q8": [""], "Q8 e-tron": [""]
    },
    "BMW": {
        "1 Series": [], "2 Series": [], "3 Series": [], "4 Series": [], "5 Series": [],
        "6 Series": [], "7 Series": [], "8 Series": [], "X1": [], "X3": [],
        "X5": [], "X6": [], "Z4": [], "i3": [], "i4": [], "iX": []
    },
    "Chevrolet": {
        "Aveo": [], "Camaro": [], "Captiva": [], "Cruze": [], "Epica": [],
        "Lacetti": [], "Malibu": [], "Niva": [], "Orlando": [], "Spark": [],
        "Tahoe": []
    },
    "Citroen": {
        "Berlingo": [], "C1": [], "C2": [], "C3": [], "C3 Aircross": [],
        "C4": [], "C4 Picasso": [], "C5": [], "C6": [], "DS3": [],
        "DS4": [], "DS5": []
    },
    "Ford": {
        "C-Max": [], "Ecosport": [], "Edge": [], "Escape": [], "Explorer": [],
        "F-150": [], "Fiesta": [], "Focus": [], "Fusion": [], "Galaxy": [],
        "Kuga": [], "Mondeo": [], "Mustang": [], "S-Max": [], "Transit": []
    },
    "Honda": {
        "Accord": ["КА5869КВ", ""], "Civic": [], "CR-V": [], "Fit/Jazz": [],
        "FR-V": [], "Insight": [], "Jazz": [], "Legend": [], "Odyssey": [],
        "Pilot": [], "Element": [], "Fit Shuttle": [], "Brio": [], "City": [],
        "CR-Z": [], "HR-V": []
    },
    "Hyundai": {
        "Accent": [], "Creta": [], "Elantra": [], "i10": [], "i20": [],
        "i30": [], "ix35": [], "Kona": [], "Santa Fe": [], "Solaris": [],
        "Sonata": [], "Tucson": [], "Venue": []
    },
    "Kia": {
        "Ceed": [], "Cerato": [], "Niro": [], "Optima": [], "K5": ["Саченко"], "K7": [], "Picanto": [],
        "Rio": [], "Seltos": [], "Sorento": [], "Soul": [], "Sportage": [],
        "Stinger": []
    },
    "Lexus": {
        "CT": [], "ES": [], "GS": [], "GX": [], "IS": [],
        "LC": [], "LS": [], "LX": [], "NX": [], "RC": [],
        "RX": [], "UX": []
    },
    "Marcedes-Benz": {
        "A-Class": [], "B-Class": [], "C-Class": [], "CLA": [], "CLS": [],
        "E-Class": [], "G-Class": [], "GLA": [], "GLB": [], "GLC": [],
        "GLE": [], "GLS": [], "S-Class": [], "SL": [], "V-Class": [],
        "Vito": [], "Sprinter": []
    },
    "Mazda": {
        "2": [], "3": [], "5": [], "6": [], "CX-3": [],
        "CX-5": [], "CX-7": [], "CX-9": [], "MX-5": []
    },
    "Mitsubishi": {
        "ASX": [], "Colt": [], "Eclipse Cross": [], "Galant": [], "L200": [],
        "Lancer": [], "Outlander": [], "Pajero": [], "Space Star": []
    },
    "Nissan": {
        "Almera": [], "Ariya": [], "Juke": [], "Leaf": [], "Micra": [],
        "Murano": [], "Navara": [], "Note": [], "Pathfinder": [], "Patrol": [],
        "Qashqai": [], "Rogue": [], "Sentra": [], "Terrano": [], "X-Trail": []
    },
    "Opel": {
        "Astra": [], "Corsa": [], "Insignia": [], "Meriva": [], "Mokka": [],
        "Vectra": [], "Zafira": []
    },
    "Peugeot": {
        "106": [], "206": [], "207": [], "208": [], "3008": [],
        "301": [], "307": [], "308": [], "407": [], "5008": []
    },
    "Renault": {
        "Arkana": [], "Captur": [], "Clio": [], "Duster": [], "Espace": [],
        "Kangoo": [], "Koleos": [], "Laguna": [], "Logan": [], "Megane": [],
        "Scenic": [], "Talisman": [], "Trafic": []
    },
    "Skoda": {
        "Citigo": [], "Fabia": [], "Kamiq": [], "Karoq": [], "Kodiaq": [],
        "Octavia": [], "Rapid": [], "Roomster": [], "Scala": [], "Superb": [],
        "Yeti": []
    },
    "SsangYong": {
        "Actyon": [], "Korando": [], "Kyron": [], "Rexton": [], "Tivoli": []
    },
    "Tesla": {
        "Model 3": [], "Model S": [], "Model X": [], "Model Y": [], "Cybertruck": []
    },
    "Toyota": {
        "Allex": [], "Allion": [], "Alphard": [], "Avalon": [], "Avensis": [],
        "C-HR": [], "Camry": [], "Corsa": [], "Harrier": [], "iQ": [],
        "Matrix": [], "Mirai": [], "Previa": [], "Prius": [],
        "Prius Plug-in Hybrid": [], "Prius Plus / v": [], "RAV4": [], "RAV4 EV": [],
        "Sienna": [], "Venza": [], "Yaris": [], "Yaris Cross": [], "Yaris Verso": []
    },
    "Volkswagen": {
        "Amarok": [], "Arteon": [], "Beetle": [], "Caddy": [], "Golf": [],
        "Jetta": [], "Passat": [], "Polo": [], "T-Cross": [], "T-Roc": [],
        "Tiguan": [], "Touareg": [], "Touran": [], "Transporter": [], "Up!": []
    },
    "Volvo": {
        "C30": [], "C70": [], "S40": [], "S60": [], "S80": [],
        "S90": [], "V40": [], "V50": [], "V60": [], "V90": [],
        "XC40": [], "XC60": [], "XC70": [], "XC90": []
    }
}


def choice_brand(brand):
    models = list(auto_data.get(brand, {}).keys())
    car_box_model.configure(values=models)
    car_box_model.set("Модель авто")
    car_box_number.set("Номер авто")
    car_box_number.configure(values=[])


def choice_model(model):
    brand = car_box_brand.get()
    numbers = auto_data.get(brand, {}).get(model, [])
    car_box_number.configure(values=numbers)
    car_box_number.set("Номер авто")


# ===== Labels =====
label1 = ctk.CTkLabel(frame, text='Початок зміни:', text_color='white')
label2 = ctk.CTkLabel(frame, text='Перерва: ', text_color='white')
label3 = ctk.CTkLabel(frame, text='Кінець зміни: ', text_color='white')
label4 = ctk.CTkLabel(frame, text='Пробіг за зміну miles: ', text_color='white')
label5 = ctk.CTkLabel(frame, text='Пробіг за зміну км: ', text_color='white')
label6 = ctk.CTkLabel(frame, text='Витрата палива mpg: ', text_color='white')
label7 = ctk.CTkLabel(frame, text='Витрата палива л/км: ', text_color='white')
label8 = ctk.CTkLabel(frame, text='Ціна палива: ', text_color='white')
label9 = ctk.CTkLabel(frame, text='Амортизація авто 10%: ', text_color='white')
label10 = ctk.CTkLabel(frame, text='Дохід за зміну: ', text_color='white')
label11 = ctk.CTkLabel(frame, text='Заробіток за зміну:', text_color='white')
label12 = ctk.CTkLabel(frame, text='Витрачено палива: ', text_color='white')
label13 = ctk.CTkLabel(frame, text='Ціна витраченого палива: ', text_color='white')
label14 = ctk.CTkLabel(frame, text='Ціна за кілометр: ', text_color='white')

label1.place(x=10, y=40)
label2.place(x=10, y=80)
label3.place(x=10, y=120)
label4.place(x=10, y=160)
label5.place(x=10, y=340)
label6.place(x=10, y=200)
label7.place(x=10, y=380)
label8.place(x=10, y=240)
label9.place(x=10, y=420)
label10.place(x=10, y=280)
label11.place(x=10, y=600)
label12.place(x=10, y=460)
label13.place(x=10, y=500)
label14.place(x=10, y=540)

# ===== Comboboxes =====
day_box = ctk.CTkComboBox(root, values=days, width=70)
month_box = ctk.CTkComboBox(root, values=months, width=100)
year_box = ctk.CTkComboBox(root, values=years, width=90)

car_box_brand = ctk.CTkComboBox(root, values=list(auto_data.keys()), command=choice_brand, width=120)
car_box_brand.set("Honda")
car_box_model = ctk.CTkComboBox(root, values=list(auto_data['Honda'].keys()), command=choice_model, width=120)
car_box_model.set("Accord")
car_box_number = ctk.CTkComboBox(root, values=list(auto_data['Honda']['Accord']), width=120)
car_box_number.set("КА5869КВ")

day_box.place(x=10, y=26)
month_box.place(x=90, y=26)
year_box.place(x=200, y=26)

car_box_brand.place(x=10, y=70)
car_box_model.place(x=145, y=70)
car_box_number.place(x=280, y=70)

day_box.set(datetime.now().strftime('%d'))
month_box.set(months_ukr[current_month_index])
year_box.set(datetime.now().strftime('%Y'))

# ===== Entrys =====
entry1 = ctk.CTkComboBox(frame, values=start_times, width=220)
entry2 = ctk.CTkComboBox(frame, values=break_times, width=220)
entry3 = ctk.CTkComboBox(frame, values=end_times, width=220)
entry4 = ctk.CTkEntry(frame, width=220)
entry6 = ctk.CTkEntry(frame, width=220)
entry8 = ctk.CTkEntry(frame, width=220)
entry10 = ctk.CTkEntry(frame, width=220)

entry5 = ctk.CTkEntry(frame, fg_color='silver', text_color='black', width=220)
entry5.insert(0, "")
entry5.configure(state="disabled")

entry7 = ctk.CTkEntry(frame, fg_color='silver', text_color='black', width=220)
entry7.insert(0, "")
entry7.configure(state="disabled")

entry9 = ctk.CTkEntry(frame, fg_color='silver', text_color='black', width=220)
entry9.insert(0, "")
entry9.configure(state="disabled")

entry11 = ctk.CTkEntry(frame, fg_color='silver', text_color='black', width=220)
entry11.insert(0, "")
entry11.configure(state="disabled")

entry12 = ctk.CTkEntry(frame, fg_color='silver', text_color='black', width=220)
entry12.insert(0, "")
entry12.configure(state="disabled")

entry13 = ctk.CTkEntry(frame, fg_color='silver', text_color='black', width=220)
entry13.insert(0, "")
entry13.configure(state="disabled")

entry14 = ctk.CTkEntry(frame, fg_color='silver', text_color='black', width=220)
entry14.insert(0, "")
entry14.configure(state="disabled")
entry1.place(x=180, y=40)  # Початок зміни
entry2.place(x=180, y=80)  # Перерва
entry3.place(x=180, y=120)  # Кінець зміни
entry4.place(x=180, y=160)  # Пробіг за зміну miles
entry5.place(x=180, y=340)  # Пробіг за зміну км
entry6.place(x=180, y=200)  # Витрата палива mpg
entry7.place(x=180, y=380)  # Витрата палива л/км
entry8.place(x=180, y=240)  # Ціна палива
entry9.place(x=180, y=420)  # Амортизація авто
entry10.place(x=180, y=280)  # Дохід за зміну
entry11.place(x=180, y=600)  # Заробіток за зміну
entry12.place(x=180, y=460)  # Витрачено палива
entry13.place(x=180, y=500)  # Ціна витраченого палива
entry14.place(x=180, y=540)  # Ціна за кілометр

# # ===== Separators =====
separator = ctk.CTkFrame(frame, height=1, fg_color="gray", width=450)
separator.place(x=0, y=325)

separator_2 = ctk.CTkFrame(frame, height=1, fg_color="gray", width=450)
separator_2.place(x=0, y=650)

# ===== Mode Switcher =====
is_checked = ctk.BooleanVar(value=False)


def get_selected_date():
    return f"{day_box.get()} {month_box.get()} {year_box.get()}"


def on_month_change(stat_month):
    if stat_month == "Весь період":
        show_data(selected_month=None)
    else:
        rodov_month = month_nazv.get(stat_month)
        show_data(selected_month=rodov_month)


def get_selected_car():
    return f"{car_box_brand.get()} {car_box_model.get()} {car_box_number.get()}"


def clear_all_fields():
    combo_boxes = [entry1, entry2, entry3]
    entries = [
        entry4, entry5, entry6,
        entry7, entry8, entry9,
        entry10, entry11, entry12,
        entry13, entry14]
    for combo in combo_boxes:
        combo.set('00:00')
    for entry in entries:
        entry.configure(state='normal')
        entry.delete(0, 'end')
        if entry in [entry5, entry7, entry9, entry11, entry12, entry13, entry14]:
            entry.configure(state='disabled')


def choose_mode():
    clear_all_fields()

    if is_checked.get():
        label4.configure(text='Пробіг за зміну км: ', text_color='white')
        label6.configure(text='Витрата палива л/км: ', text_color='white')

        label5.place_forget(), entry5.place_forget()
        label7.place_forget(), entry7.place_forget()
        label9.place(x=10, y=340), entry9.place(x=180, y=340)
        label12.place(x=10, y=380), entry12.place(x=180, y=380)
        label13.place(x=10, y=420), entry13.place(x=180, y=420)
        label14.place(x=10, y=460), entry14.place(x=180, y=460)
        label11.place(x=10, y=520), entry11.place(x=180, y=520)

        separator_2.place(x=0, y=570)

        ok_btn.place(x=7, y=590)
        option_menu.place(x=135, y=665)
        exit_btn.place(x=283, y=590)

        frame.place(x=0, y=75)
        root.geometry('410x710')

    else:
        label4.configure(text='Пробіг за зміну miles: ', text_color='white')
        label6.configure(text='Витрата палива mpg: ', text_color='white')

        label5.place(x=10, y=340), entry5.place(x=180, y=340)
        label7.place(x=10, y=380), entry7.place(x=180, y=380)
        label9.place(x=10, y=420), entry9.place(x=180, y=420)
        label12.place(x=10, y=460), entry12.place(x=180, y=460)
        label13.place(x=10, y=500), entry13.place(x=180, y=500)
        label14.place(x=10, y=540), entry14.place(x=180, y=540)
        label11.place(x=10, y=600), entry11.place(x=180, y=600)

        separator_2.place(x=0, y=650)

        ok_btn.place(x=7, y=670)
        option_menu.place(x=135, y=745)
        exit_btn.place(x=283, y=670)

        frame.place(x=0, y=75)
        root.geometry('410x790')


check = ctk.CTkCheckBox(
    master=root,
    text='Km-версія',
    variable=is_checked,
    command=choose_mode,
    onvalue=True,
    offvalue=False
)

check.place(x=300, y=28)


def update_etry(entry, value):
    entry.configure(state='normal')
    entry.delete(0, 'end')
    entry.insert(0, value)
    entry.configure(state='disabled')


# ===== Saving data =====
def save_data():
    user_input1 = entry1.get()
    if not user_input1:
        messagebox.showerror("Помилка", "Введіть дані в поле 'Початок зміни'")
        return
    start_time = int(user_input1.split(':')[0])

    user_input2 = entry2.get()
    break_time = int(user_input2.split(':')[0]) if user_input2 else 0

    user_input3 = entry3.get()
    if not user_input3:
        messagebox.showerror("Помилка", "Введіть дані в поле 'Кінець зміни'")
        return
    end_time = int(user_input3.split(':')[0])

    if end_time < start_time:
        all_time = (24 - start_time + end_time) - break_time
    else:
        all_time = end_time - start_time - break_time

    if all_time <= 0:
        messagebox.showerror("Помилка", "Загальний час не може бути 0 або менше")
        return

    if is_checked.get():
        user_input4 = entry4.get().strip()
        if not user_input4:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Пробіг за зміну км' ")
            return
    else:
        user_input4 = entry4.get().strip()
        if not user_input4:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Пробіг за зміну miles' ")
            return

    if is_checked.get():
        user_input6 = entry6.get().strip()
        if not user_input6:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Витрата палива л/км' ")
            return
    else:
        user_input6 = entry6.get().strip()
        if not user_input6:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Витрата палива mpg ")
            return

    user_input8 = entry8.get().strip()
    if not user_input8:
        messagebox.showerror("Помилка", "Введіть дані в поле  'Ціна палива' ")
        entry8.focus_set()
        return
    try:
        fuel_price = float(user_input8)
    except ValueError:
        messagebox.showerror("Помилка", "Поле 'Ціна палива' має бути числом")
        entry8.focus_set()
        return

    user_input10 = entry10.get().strip()
    if not user_input10:
        messagebox.showerror("Помилка", "Введіть дані в поле  'Дохід за зміну' ")
        return

    if not re.fullmatch(r"[\d\s.+\-]+", user_input10):
        messagebox.showerror("Помилка", "Поле 'Дохід за зміну' має містити лише числовий вираз")
        return

    try:
        evaluated_value = simple_eval(user_input10)
        if evaluated_value <= 0:
            messagebox.showerror("Помилка", "Дохід за зміну має бути більше нуля")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Поле 'Дохід за зміну' має містити лише числовий вираз")
        return

    try:
        if is_checked.get():  # KM mode
            km = float(user_input4)
            lkm = float(user_input6)
        else:  # MPG mode
            miles = float(user_input4)
            if miles <= 0:
                raise ValueError("Милі не можуть дорівнювати 0")
            km = round(miles * 1.6, 1)
            update_etry(entry5, f"{km} км")

            mpg = float(user_input6)
            if mpg <= 0:
                raise ValueError("MPG не може дорівнювати 0")
            lkm = round(235.21 / mpg, 1)
            update_etry(entry7, f"{lkm} л")

    except ValueError as e:
        messagebox.showerror("Помилка", str(e))
        return

    # Підрахунок АМОРТИЗАЦІЇ
    amo = evaluated_value * 0.1
    update_etry(entry9, f"{round(amo, 2)} грн")

    # Підрахунок витрачених літрів за зміну
    f_cons = float(lkm * km) / 100
    update_etry(entry12, f"{round(f_cons, 2)} л")

    # Підрахунок коштів витрачених на паливо за зміну

    f_price = f_cons * float(user_input8)
    update_etry(entry13, f"{round(f_price, 2)} грн")

    # Підрахунок ЧИСТОГО ЗАРОБІТКУ
    try:
        cost = f_cons * fuel_price
        salary = evaluated_value - cost - amo
        if salary <= 0:
            raise ValueError("Заробіток за зміну не може бути менше чи дорівнювати нулю")
        update_etry(entry11, f"{round(salary, 2)} грн")

    except ValueError:
        messagebox.showerror("Помилка", "Заробіток за зміну не може бути менше чи дорівнювати нулю")
        entry10.focus_set()
        return

    # Підрахунок ціни за кілометр
    km_price = salary / float(km)
    update_etry(entry14, f"{round(km_price)} грн")

    data = {
        "Дата": f"{get_selected_date()}",
        "АВТО": f"{get_selected_car()}",
        "Початок зміни": f"{user_input1} год",
        "Перерва": f"{user_input2} год",
        "Кінець зміни": f"{user_input3} год ",
        "Тривалість зміни": f"{all_time} год",
        "Пробіг за зміну в милях": f"{user_input4} миль ",
        "Пробіг за зміну в кілометрах": f"{round(km, 2)} км",
        "Витрата палива MPG": f"{user_input6} mpg",
        "Витрата палива": f"{round(lkm, 2)} л",
        "Витрачено палива": f"{round(f_cons, 2)} л",
        "Ціна палива": f"{user_input8} грн",
        "Ціна за кілометр": f"{round(km_price, 2)}",
        "Вартість витраченого палива": f"{round(f_price, 2)} грн",
        "Дохід за зміну": f"{evaluated_value} грн",
        "Заробіток за зміну": f"{round(salary, 2)} грн",
    }

    try:
        with open(fname, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            if not isinstance(existing_data, list):
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


# ===== Show saved data =====
def show_data(selected_month=None):
    global data_window

    if data_window:
        data_window.destroy()

    try:
        with open(fname, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Помилка", "Немає даних для відображення")
        return

    output = ""
    total_income = 0.0

    for entry in existing_data:
        # Фільтр за місяцем, якщо заданий
        if selected_month:
            parts = entry['Дата'].split()
            if len(parts) != 3 or parts[1] != selected_month:
                continue

        income = float(entry['Заробіток за зміну'].replace("грн", "").strip())
        total_income += income

        output += (
                f"\t    --- {entry['Дата']} ---".upper() + "\n"
                                                           f"\t{entry.get('АВТО', '')}".upper() + "\n"
                # f"Початок зміни: {entry['Початок зміни']}\n"
                # f"Перерва: {entry['Перерва']}\n"
                # f"Кінець зміни: {entry['Кінець зміни']}\n"
                f"1. Тривалість зміни: {entry['Тривалість зміни']}\n"
                # f"Пробіг за зміну в милях: {entry['Пробіг за зміну в милях']}\n"
                f"2. Пробіг за зміну: {entry['Пробіг за зміну в кілометрах']}\n"
                # f"Витрата палива MPG: {entry['Витрата палива MPG']}\n"
                f"3. Витрата палива: {entry['Витрата палива']}\n"
                f"4. Витрачено палива: {entry['Витрачено палива']}\n"
                # f"Ціна палива: {entry['Ціна палива']}\n"
                # f"Ціна за кілометр: {entry['Ціна за кілометр']}\n"
                f"5. Вартість витраченого палива: {entry['Вартість витраченого палива']}\n"
                f"6. Дохід за зміну: {entry['Дохід за зміну']}\n"
                "------------------------------------------------------\n"
                f"Заробіток за зміну: {entry['Заробіток за зміну']}\n"
                "------------------------------------------------------\n\n"
        )

    output += f"🔸 Загальний заробіток за всі зміни: {round(total_income, 2)} грн\n"

    # ==== Window =====
    data_window = ctk.CTkToplevel(root)
    data_window.title("Статистика")
    data_frame = ctk.CTkFrame(data_window, width=350, height=790)
    data_frame.place(x=0, y=0)

    text_box = ctk.CTkTextbox(data_frame, width=350, height=790, fg_color=bg_color)
    text_box.insert('0.0', output)
    text_box.configure(state="disabled")
    text_box.place(x=0, y=0)

    # ==== Get screen size ===
    screen_width_w = data_window.winfo_screenwidth()
    screen_height_w = data_window.winfo_screenheight()

    def confirm_exit_from_data():
        data_window.destroy()

    def clear_data():
        response = messagebox.askquestion('Видалити', 'Дані буде остаточно втрачено. Видалити все одно?')
        if response == 'yes':
            text_box.configure(state='normal')
            text_box.delete(0.0, 'end')
            text_box.configure('disabled')
            with open(fname, 'w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False, indent=4)
        else:
            return

    def save_data_to_pdf():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            title="Зберегти звіт як"
        )
        if not file_path:
            return
        try:
            with open(fname, 'r', encoding='utf-8') as file:
                saved_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Помилка", "Немає даних для експорту")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', '/Users/dim/PythonProjects/Taxi_testing/fonts/djsans/DejaVuSans.ttf')
        pdf.add_font('DejaVuBold', '', '/Users/dim/PythonProjects/Taxi_testing/fonts/djsans/DejaVuSans-Bold.ttf')

        pdf.set_font('DejaVuBold', '', 22)
        pdf.cell(0, 10, "Статистика", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.set_title("Статистика")
        pdf.ln(10)

        pdf.set_font('DejaVu', '', 14)
        for data in saved_data:
            pdf.cell(0, 10, f"Дата: {data['Дата']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            pdf.cell(0, 10, f"Транспортний засіб: {data.get('АВТО', 'Не вказано')}", new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT, align="C")
            pdf.cell(0, 10, f"Тривалість зміни: {data['Тривалість зміни']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 10, f"Пробіг за зміну: {data['Пробіг за зміну в кілометрах']}", new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)
            pdf.cell(0, 10, f"Витрата палива: {data['Витрата палива']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 10, f"Витрачено палива: {data['Витрачено палива']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 10, f"Ціна палива: {data['Ціна палива']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 10, f"Ціна за кілометр: {data['Ціна за кілометр']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 10, f"Вартість витраченого палива: {data['Вартість витраченого палива']}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 10, f"Заробіток за зміну: {data['Заробіток за зміну']}", new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)
            pdf.cell(0, 10, "-" * 100, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(5)

        pdf.output(file_path)
        messagebox.showinfo("Успіх", f"Дані збережені  \f{file_path}")

    clear_btn_data = ctk.CTkButton(data_window, width=120, text="Видалити", command=clear_data)
    print_btn_data = ctk.CTkButton(data_window, width=70, text='PDF', command=save_data_to_pdf, fg_color='#ce1313',
                                   hover_color='#b01818')
    exit_btn_data = ctk.CTkButton(data_window, width=120, text='Закрити', command=confirm_exit_from_data)
    separator_3 = ctk.CTkFrame(data_window, height=1, fg_color="gray", width=350)

    def km_size():
        w, h = 350, 708
        data_window.resizable(False, False)
        x_w = int((screen_width_w - w) / 1.5)
        y_w = int((screen_height_w - h) / 3.33)
        data_window.geometry(f"{w}x{h}+{x_w}+{y_w}")
        text_box.configure(height=643)
        separator_3.place(x=0, y=643)
        clear_btn_data.place(x=10, y=663)
        exit_btn_data.place(x=220, y=663)
        print_btn_data.place(x=140, y=663)

    def mile_size():
        w, h = 350, 790
        data_window.resizable(False, False)
        x_w = int((screen_width_w - w) / 1.5)
        y_w = int((screen_height_w - h) / 2.6)
        data_window.geometry(f"{w}x{h}+{x_w}+{y_w}")
        text_box.configure(height=725)
        separator_3.place(x=0, y=725)
        clear_btn_data.place(x=10, y=745)
        exit_btn_data.place(x=220, y=745)
        print_btn_data.place(x=140, y=745)

    if is_checked.get():
        km_size()
    else:
        mile_size()


# ===== Exit confirmation =====
def confirm_exit():
    if messagebox.askokcancel("Вихід", "Ви дійсно хочете вийти?"):
        root.quit()


# ===== Buttons =====
ok_btn = ctk.CTkButton(frame, width=120, text='Зберегти', command=save_data)
ok_btn.place(x=7, y=670)

option_menu = ctk.CTkOptionMenu(root,
                                values=["Весь період"] + list(month_nazv.keys()),
                                command=on_month_change,
                                )
option_menu.set("     Статистика")
option_menu.place(x=135, y=745)

exit_btn = ctk.CTkButton(frame, width=120,
                         text='Вихід',
                         command=confirm_exit,
                         )
exit_btn.place(x=283, y=670)
#====================


root.mainloop()
