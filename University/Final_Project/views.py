import tkinter as tk
from tkinter import ttk
import controller

# Sources:
# https://www.pythontutorial.net/tkinter/tkinter-grid/


class CenteredWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def GeneralWindowOptions(self):         #Ogólna funkcja wywoływana po otwarciu każdego okna
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def CloseOpen(self, openWindow):        #Ogólna funkcja do zamykania obecnego okna i otwierania wskazanego
        if openWindow in globals():
            self.destroy()
            newClass = globals()[openWindow]
            newWindow = newClass()
            newWindow.mainloop()
        else:
            print(f"Klasa {openWindow} nie istnieje.")

    def CloseWindow(self):                  #Ogólna funkcja do zamykania obecnego okna
        self.destroy()


class MainPage(CenteredWindow):
    def __init__(self):
        super().__init__()
        self.windowSizeSmall = "240x130"
        self.windowSizeBig = "240x190"
        self.GeneralWindowOptions()
        self.title("Porównywarka stomatologiczna")  # nazwa okna
        self.geometry(self.windowSizeSmall)

        # lambda do utworzenia funkcji, która wywoła self.CloseOpen("Login") po kliknięciu przycisku.
        # Bez użycia lambda, funkcja self.CloseOpen("Login") zostałaby wywołana natychmiast podczas przypisywania do
        # command, a nie po kliknięciu przycisku.
        #Werytfikacja, czy użytkownik jest zalogowany
        if controller.USER_LOGGED_IN == False:
            self.btnLogIn = ttk.Button(self, text="Zaloguj", command=lambda: self.CloseOpen("Login"))
            self.btnLogIn.grid(column=2, row=0, sticky=tk.NE, padx=5, pady=5)
        else:
            self.btnLogIn = ttk.Button(self, text="Zalogowano")
            self.btnLogIn.grid(column=2, row=0, sticky=tk.NE, padx=5, pady=5)

        self.lblUDentysty = ttk.Label(text="U dentysty!")
        self.lblUDentysty.grid(column=1, row=0, sticky=tk.S, padx=5, pady=5)

        self.lblCountry = ttk.Label(text="Proszę wybrać kraj:")
        self.lblCountry.grid(column=1, row=1, sticky=tk.S, padx=5, pady=5)
        self.selected_country = tk.StringVar()
        self.cbo_selected_country = ttk.Combobox(self, textvariable=self.selected_country)
        self.cbo_selected_country['values'] = tuple(controller.GetCountriesFromTable())
        #self.cbo_selected_country['values'] = ('Polska', 'Japonia', 'test')
        self.cbo_selected_country.grid(column=1, row=2, sticky=tk.S, padx=5, pady=5)

        self.lblCity = ttk.Label(text="Proszę wybrać miasto:")
        self.lblCity.grid(column=1, row=3, sticky=tk.S, padx=5, pady=5)
        self.lblCity.grid_remove()  # całkowite ukrycie etykiety do momentu wybrania kraju

        self.selected_city = tk.StringVar()
        self.cbo_selected_city = ttk.Combobox(self, textvariable=self.selected_city, state='disabled')
        self.cbo_selected_city.grid(column=1, row=4, sticky=tk.S, padx=5, pady=5)
        self.cbo_selected_city.grid_remove()  # całkowite ukrycie kontrolki do momentu wybrania kraju

        # Ustawienie funkcji callback po zmianie wybranego kraju
        self.cbo_selected_country.bind('<<ComboboxSelected>>', self.on_country_selected)

        # Find button
        btnFind = ttk.Button(self, text="Szukaj", command=lambda: self.CloseOpen("FindRecords"))
        btnFind.grid(column=1, row=5, sticky=tk.S, padx=5, pady=5)

        # Exit button
        btnExit = ttk.Button(self, text="Wyjście", command=lambda: self.CloseWindow())
        btnExit.grid(column=2, row=5, sticky=tk.SE, padx=5, pady=5)

    def on_country_selected(self, event):
        selected_country = self.selected_country.get()      #Wybrany kraj
        # Ustawienie nowych wartości dla Combobox z miastami
        self.cbo_selected_city['values'] = controller.GetCitiesForCountry(selected_country)

        # Ukrycie lub wyświetlenie Combobox z miastami w zależności od wybranego kraju
        if selected_country:
            self.cbo_selected_city['state'] = 'readonly'
            self.cbo_selected_city.grid()
            self.geometry(self.windowSizeBig)
            self.lblCity.grid()
        else:
            self.cbo_selected_city['state'] = 'disabled'
            self.cbo_selected_city.grid_remove()
            self.geometry(self.windowSizeSmall)
            self.lblCity.grid_remove()

class Login(CenteredWindow):
    def __init__(self):
        super().__init__()
        self.GeneralWindowOptions()
        self.geometry("240x100")
        self.title('Login')

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        #self.create_widgets()

        self.username_label = ttk.Label(self, text="Login:")
        self.username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # password
        self.password_label = ttk.Label(self, text="Hasło:")
        self.password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # login button
        self.login_button = ttk.Button(self, text="Login", command=self.logInWithCredentials)
        self.login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        # login button
        self.login_button = ttk.Button(self, text="Cofnij", command=lambda: self.CloseOpen("MainPage"))
        self.login_button.grid(column=0, row=3, sticky=tk.E, padx=5, pady=5)

    def logInWithCredentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        blnPassword = controller.VerifyLogIn(username, password)

        if blnPassword:
            self.destroy()
            mainPage = MainPage()
            mainPage.mainloop()
        else:
            # blede credentiale
            pass


class FindRecords(CenteredWindow):
    pass
