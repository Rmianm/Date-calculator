import tkinter as tk
from tkinter import messagebox
import unicodedata
import pygame
from PIL import Image, ImageTk


def window_resize(window, width_window, lenght_window):
    width_screen = window.winfo_screenwidth()
    lenght_screen = window.winfo_screenheight()
    x = int((width_screen/2) - (width_window/2))
    y = int((lenght_screen/2) - (lenght_window/2))
    return window.geometry(f'{width_window}x{lenght_window}+{x}+{y}')


class Inputs:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Calendar')
        self.window.geometry('800x500')
        self.window.config(bg='#fcfcfc')
        self.window.resizable(width=0, height=0)
        window_resize(self.window, 800, 500)

        # frame logo (sin imagen)
        frame_image = tk.Frame(self.window, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#40E0D0')
        frame_image.pack(side='left', expand=tk.NO, fill=tk.BOTH)

        title = tk.Label(frame_image, text="Hello curious people", font=('Times', 30), fg="#2F4F4F", pady=15, bg='#40E0D0')
        title.pack(side='top', fill=tk.X)

        # Cargar imagen
        image_path = "planeta.png"  # Asegúrate de que el archivo esté en la misma carpeta o coloca la ruta completa
        img = Image.open(image_path)
        img = img.resize((200, 200))  # Ajusta el tamaño si es necesario
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen debajo del título
        label_img = tk.Label(frame_image, image=img, bg='#40E0D0')
        label_img.image = img  # Referencia para evitar que Python elimine la imagen
        label_img.pack(side='top', pady=50) 
    

        # frame form
        frame_form = tk.Frame(self.window, bd=0, relief=tk.SOLID, bg='#FAF0E6')
        frame_form.pack(side='left', expand=tk.YES, fill=tk.BOTH)

        rows = 7
        cols = 3
        for i in range(rows):
            frame_form.rowconfigure(i, weight=1)
        for j in range(cols):
            frame_form.columnconfigure(j, weight=1)

        label_title = tk.Label(frame_form, text="Please enter a date like 13 december 2000",
                               font=("Courier", 12), bg='#FAF0E6', anchor='w', justify="left")
        label_title.grid(row=0, column=0, columnspan=2, pady=8)
        label_title.update_idletasks()
        label_title.config(wraplength=frame_form.winfo_width() - 20)

        Day = tk.Label(frame_form, text='Day: ', font=("Courier", 12), bg='#FAF0E6')
        Day.grid(row=1, column=0, pady=5, sticky='e')

        input_day = tk.Entry(frame_form, font=('Georgia', 12))
        input_day.grid(row=1, column=1, padx=1)

        Month = tk.Label(frame_form, text='Month: ', font=("Courier", 12), bg='#FAF0E6')
        Month.grid(row=2, column=0, sticky='e')

        input_month = tk.Entry(frame_form, font=('Georgia', 12))
        input_month.grid(row=2, column=1)

        Year = tk.Label(frame_form, text='Year: ', font=("Courier", 12), bg='#FAF0E6')
        Year.grid(row=3, column=0, sticky='e')

        input_year = tk.Entry(frame_form, font=('Georgia', 12))
        input_year.grid(row=3, column=1)

        label_result = tk.Label(frame_form, font=('Georgia', 12, 'bold'), pady=10, bg='#FAF0E6')
        label_result.grid(row=6, column=0, columnspan=2)

        # Diccionario para semanas y meses
        weeks = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
        months = {'january': 0, 'february': 3, 'march': 3, 'april': 6, 'may': 1, 'june': 4,
                  'july': 6, 'august': 2, 'september': 5, 'october': 0, 'november': 3, 'december': 5}
        year_code = {'19': 0, '20': 6}

        def day():
            try:
                day_ = input_day.get()
                if day_ == "":
                    label_result['text'] = "Missing day"
                    messagebox.showwarning('Error', 'Missing values')
                else:
                    return int(day_)
            except:
                messagebox.showerror('Error', 'Wrong values')

        def month():
            try:
                month_ = input_month.get().lower()
                month_ = ''.join(c for c in unicodedata.normalize('NFD', month_) if unicodedata.category(c) != 'Mn')

                if month_ == "" or month_ not in months:
                    label_result['text'] = "Wrong format"
                    messagebox.showwarning('Error', 'Wrong format')
                else:
                    return month_
            except:
                messagebox.showerror('Error', 'Wrong values')

        def year():
            try:
                year_ = input_year.get()
                if year_ == "" or not year_.isdigit() or len(year_) != 4:
                    label_result['text'] = "Invalid year format"
                    messagebox.showwarning('Error', 'Insert a correct number')
                else:
                    return year_
            except:
                messagebox.showerror('Error')

        def result():
            day_ = day()
            month_ = month()
            year_ = year()

            if day_ and month_ and year_:
                if (int(year_) % 4 == 0 and (month_ == "january" or month_ == 'february')) or (int(year_) % 4 == 0 and (int(year_) % 4 == 0 and int(year_) % 100 == 0 and int(year_) % 400 == 0) and (month_ == "january" or month_ == 'february')):
                    result_date = f"💡 {weeks.get(((day_ + year_code.get(year_[0:2]) + months.get(month_) + int(year_[-2:]) % 7 + int(year_[-2:]) // 4) % 7) - 1)} is what you're looking for"
                else:
                    result_date = f"💡 {weeks.get((day_ + year_code.get(year_[0:2]) + months.get(month_) + int(year_[-2:]) % 7 + int(year_[-2:]) // 4) % 7)} is what you're looking for"
                label_result['text'] = result_date

        # Botón para mostrar el resultado
        button_result = tk.Button(frame_form, text='Result', bg='#9400D3', fg='white', font=('Georgia', 15), width=15, command=result, relief='raised', borderwidth=10)
        button_result.grid(row=4, column=0, pady=10, columnspan=2)


        self.window.mainloop()
    
        


if __name__ == "__main__":
    app = Inputs()
    



    


