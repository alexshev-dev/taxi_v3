import platform

import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
from datetime import datetime
from fpdf import FPDF, XPos, YPos
import sys
import os


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# === Шлях до файлу saved_info.json ===
def get_data_path(app_name: str = "TaxiApp"):
    system = platform.system()
    if system == "Windows":
        base_dir = os.path.join(os.environ["APPDATA"], app_name)
    elif system == "Darwin":  # macOS
        base_dir = os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)
    else:  # Linux або інше
        base_dir = os.path.join(os.path.expanduser("~/.local/share"), app_name)

    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "data.json")

fname = get_data_path()

# fname = 'saved_info.json'


data_window = None

root = ctk.CTk()
root.title('Taксі')
root.attributes('-topmost', False)  # Встановлюємо поверх усіх вікон
root.focus_force()
root_width = 410
root_height = 760
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
frame = ctk.CTkFrame(root, width=420, height=720, fg_color=bg_color)
frame.place(x=0, y=40)

# ===== Отримати поточну дату =====
months_ukr = ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
              'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень']
current_month_index = datetime.now().month - 1

days = [str(i).zfill(2) for i in range(1, 32)]
months = [str(i).zfill(2) for i in months_ukr]
years = [str(i) for i in range(2024, datetime.now().year + 1)]

# ===== Отримати час =====
start_times = [f"{h:02}:00" for h in range(0, 24)]
break_times = [f"{h:02}:00" for h in range(0, 11)]
end_times = [f"{h:02}:00" for h in range(0, 24)]

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

day_box.place(x=10, y=26)
month_box.place(x=90, y=26)
year_box.place(x=200, y=26)

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

        ok_btn.place(x=10, y=590)
        show_btn.place(x=145, y=590)
        exit_btn.place(x=280, y=590)

        frame.place(x=0, y=40)
        root.geometry('410x680')

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

        ok_btn.place(x=10, y=670)
        show_btn.place(x=145, y=670)
        exit_btn.place(x=280, y=670)

        frame.place(x=0, y=40)
        root.geometry('410x760')


check = ctk.CTkCheckBox(
    master=root,
    text='Km-версія',
    variable=is_checked,
    command=choose_mode,
    onvalue=True,
    offvalue=False
)

check.place(x=300, y=28)


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
        user_input4 = entry4.get()
        if not user_input4:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Пробіг за зміну км' ")
            return
    else:
        user_input4 = entry4.get()
        if not user_input4:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Пробіг за зміну miles' ")
            return

    if is_checked.get():
        user_input6 = entry6.get()
        if not user_input6:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Витрата палива л/км' ")
            return
    else:
        user_input6 = entry6.get()
        if not user_input6:
            messagebox.showerror("Помилка", "Введіть дані в поле  'Витрата палива mpg ")
            return

    user_input8 = entry8.get()
    if not user_input8:
        messagebox.showerror("Помилка", "Введіть дані в поле  'Ціна палива' ")
        return

    user_input10 = entry10.get()
    if not user_input10:
        messagebox.showerror("Помилка", "Введіть дані в поле  'Дохід за зміну' ")
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
            entry5.configure(state='normal')
            entry5.delete(0, 'end')
            entry5.insert(0, f"{km} км")
            entry5.configure(state='disabled')

            mpg = float(user_input6)
            if mpg <= 0:
                raise ValueError("MPG не може дорівнювати 0")
            lkm = round(235.21 / mpg, 1)
            entry7.configure(state='normal')
            entry7.delete(0, 'end')
            entry7.insert(0, f"{lkm} л")
            entry7.configure(state='disabled')

    except ValueError as e:
        messagebox.showerror("Помилка", str(e))
        return

    # Підрахунок АМОРТИЗАЦІЇ
    amo = float(user_input10) * 0.1
    if amo <= 0:
        raise ValueError("Амортизація авто не може бути меньше чи дорівнювати 0")
    entry9.configure(state='normal')
    entry9.delete(0, 'end')
    entry9.insert(0, f"{round(amo, 2)} грн")
    entry9.configure(state='disabled')

    # Підрахунок витрачених літрів за зміну
    f_cons = float(lkm * km) / 100
    entry12.configure(state='normal')
    entry12.delete(0, 'end')
    entry12.insert(0, f"{round(f_cons, 2)} л")
    entry12.configure(state='disabled')

    # Підрахунок коштів витрачених на паливо за зміну
    f_price = f_cons * float(user_input8)
    entry13.configure(state='normal')
    entry13.delete(0, 'end')
    entry13.insert(0, f"{round(f_price, 2)} грн")
    entry13.configure(state='disabled')

    # Підрахунок ЧИСТОГО ЗАРОБІТКУ
    try:
        cost = f_cons * float(user_input8)
        salary = float(user_input10) - cost - amo
        if salary <= 0:
            raise ValueError
        entry11.configure(state='normal')
        entry11.delete(0, 'end')
        entry11.insert(0, f"{round(salary, 2)} грн")
        entry11.configure(state='disabled')
    except ValueError:
        messagebox.showerror("Помилка", "Заробіток за зміну не може бути менше чи дорівнювати нулю.\n"
                                        "Відредагуйте значення\n 'Витрата палива' або 'Дохід за зміну'")
        entry10.focus_set()
        return

    # Підрахунок ціни за кілометр
    km_price = salary / float(km)
    entry14.configure(state='normal')
    entry14.delete(0, 'end')
    entry14.insert(0, f"{round(km_price)} грн")
    entry14.configure(state='disabled')

    data = {
        "Дата": f"{get_selected_date()}",
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
        "Дохід за зміну": f"{user_input10} грн",
        "Заробіток за зміну": f"{round(salary, 2)} грн",

    }

    try:
        with open(fname, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


# ===== Show saved data =====
def show_data():
    global data_window

    if data_window:
        data_window.destroy()

    try:
        with open(fname, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        output = ""
        for entry in existing_data:
            output += (
                f"--- {entry['Дата']} ---\n"
                # f"Початок зміни: {entry['Початок зміни']}\n"
                # f"Перерва: {entry['Перерва']}\n"
                # f"Кінець зміни: {entry['Кінець зміни']}\n"
                f"Тривалість зміни: {entry['Тривалість зміни']}\n"
                # f"Пробіг за зміну в милях: {entry['Пробіг за зміну в милях']}\n"
                f"Пробіг за зміну: {entry['Пробіг за зміну в кілометрах']}\n"
                # f"Витрата палива MPG: {entry['Витрата палива MPG']}\n"
                f"Витрата палива: {entry['Витрата палива']}\n"
                f"Витрачено палива: {entry['Витрачено палива']}\n"
                f"Ціна палива: {entry['Ціна палива']}\n"
                f"Ціна за кілометр: {entry['Ціна за кілометр']}\n"
                f"Вартість витраченого палива: {entry['Вартість витраченого палива']}\n"
                # f"Дохід за зміну: {entry['Дохід за зміну']}\n"
                "-------------------------------------\n"
                f"Заробіток за зміну: {entry['Заробіток за зміну']}\n"

                "-------------------------------------\n\n"
            )

        # ==== Window =====
        data_window = ctk.CTkToplevel(root)
        data_window.title("Збережені дані")
        data_frame = ctk.CTkFrame(data_window, width=350, height=760)
        data_frame.place(x=0, y=0)
        text_box = ctk.CTkTextbox(data_frame, width=350, height=760, fg_color=bg_color)
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
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
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
                with open(fname, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                messagebox.showerror("Помилка", "Немає даних для експорту")
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.add_font('DejaVu', '', '/Users/dim/PythonProjects/Taxi/DejaVuSans.ttf')
            pdf.set_font('DejaVu', '', 14)


            for entry in existing_data:
                pdf.cell(0, 10, f"Дата: {entry['Дата']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Тривалість зміни: {entry['Тривалість зміни']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Пробіг за зміну: {entry['Пробіг за зміну в кілометрах']}",new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Витрата палива: {entry['Витрата палива']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Витрачено палива: {entry['Витрачено палива']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Ціна палива: {entry['Ціна палива']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Ціна за кілометр: {entry['Ціна за кілометр']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Вартість витраченого палива: {entry['Вартість витраченого палива']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, f"Заробіток за зміну: {entry['Заробіток за зміну']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(0, 10, "-" * 50, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(5)

            pdf.output(file_path)
            messagebox.showinfo("Успіх", f"Дані збережені у {file_path}")

        clear_btn_data = ctk.CTkButton(data_window, width=120, text="Видалити", command=clear_data)
        print_btn_data = ctk.CTkButton(data_window, width=70, text='PDF', command=save_data_to_pdf, fg_color='#ce1313', hover_color='#b01818')
        exit_btn_data = ctk.CTkButton(data_window, width=120, text='Закрити', command=confirm_exit_from_data)
        separator_3 = ctk.CTkFrame(data_window, height=1, fg_color="gray", width=350)

        def km_size():
            w, h = 350, 680
            data_window.resizable(False, False)
            x_w = int((screen_width_w - w) / 1.5)
            y_w = int((screen_height_w - h) / 3.33)
            data_window.geometry(f"{w}x{h}+{x_w}+{y_w}")
            text_box.configure(height=610)
            separator_3.place(x=0, y=610)
            clear_btn_data.place(x=10, y=630)
            exit_btn_data.place(x=220, y=630)
            print_btn_data.place(x=140, y=630)

        def mile_size():
            w, h = 350, 760
            data_window.resizable(False, False)
            x_w = int((screen_width_w - w) / 1.5)
            y_w = int((screen_height_w - h) / 2.6)
            data_window.geometry(f"{w}x{h}+{x_w}+{y_w}")
            text_box.configure(height=690)
            separator_3.place(x=0, y=690)
            clear_btn_data.place(x=10, y=710)
            exit_btn_data.place(x=220, y=710)
            print_btn_data.place(x=140, y=710)

        if is_checked.get():
            km_size()
        else:
            mile_size()

    except FileNotFoundError:
        messagebox.showerror("Помилка", f"Файл {fname} не знайдено.")
    except json.JSONDecodeError:
        messagebox.showerror("Помилка", f"Файл {fname} містить некоректні дані.")


# ===== Exit confirmation =====
def confirm_exit():
    if messagebox.askokcancel("Вихід", "Ви дійсно хочете вийти?"):
        root.quit()


# ===== Buttons =====
ok_btn = ctk.CTkButton(frame, width=120, text='Зберегти', command=save_data)
ok_btn.place(x=10, y=670)

show_btn = ctk.CTkButton(frame, width=120, text='Показати', command=show_data)
show_btn.place(x=145, y=670)

exit_btn = ctk.CTkButton(frame, width=120, text='Вихід', command=confirm_exit)
exit_btn.place(x=280, y=670)
#====================


root.mainloop()
