import tkinter as tk
from tkinter import ttk
import controller
import sys

# Sources:
# https://www.pythontutorial.net/tkinter/tkinter-grid/


class CenteredWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def GeneralWindowOptions(self):  # Ogólna funkcja wywoływana po otwarciu każdego okna
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def CloseOpen(self, openWindow):  # Ogólna funkcja do zamykania obecnego okna i otwierania wskazanego
        if openWindow in globals():
            self.destroy()
            newClass = globals()[openWindow]
            newWindow = newClass()
            newWindow.mainloop()
        else:
            print(f"Klasa {openWindow} nie istnieje.")

    def CloseWindow(self):  # Ogólna funkcja do zamykania obecnego okna
        self.destroy()
        sys.exit()


class MainPage(CenteredWindow):
    def __init__(self):
        super().__init__()
        self.windowSizeStart = "270x130"
        self.windowSizeCountry = "270x190"
        self.GeneralWindowOptions()
        self.title("Porównywarka stomatologiczna")  # nazwa okna
        self.geometry(self.windowSizeStart)

        # lambda do utworzenia funkcji, która wywoła self.CloseOpen("Login") po kliknięciu przycisku.
        # Bez użycia lambda, funkcja self.CloseOpen("Login") zostałaby wywołana natychmiast podczas przypisywania do
        # command, a nie po kliknięciu przycisku.
        # Werytfikacja, czy użytkownik jest zalogowany
        if controller.USER_LOGGED_IN == False:
            self.btnLogIn = ttk.Button(self, text="Zaloguj", command=lambda: self.CloseOpen("Login"))
            self.btnLogIn.grid(column=2, row=0, sticky=tk.NE, padx=5, pady=5)
        else:
            self.btnLogIn = ttk.Button(self, text="Panel użytkownika", command=lambda: self.CloseOpen("PersonalPanel"))
            self.btnLogIn.grid(column=2, row=0, sticky=tk.NE, padx=5, pady=5)
            self.lblLoggedIn = ttk.Label(text="Zalogowano")
            self.lblLoggedIn.grid(column=2, row=1, sticky=tk.NE, padx=5, pady=5)
            self.geometry(self.windowSizeStart)

        self.lblUDentysty = ttk.Label(text="U dentysty!")
        self.lblUDentysty.grid(column=1, row=0, sticky=tk.S, padx=5, pady=5)

        self.lblCountry = ttk.Label(text="Proszę wybrać kraj:")
        self.lblCountry.grid(column=1, row=1, sticky=tk.S, padx=5, pady=5)
        self.selected_country = tk.StringVar()
        self.cbo_selected_country = ttk.Combobox(self, textvariable=self.selected_country)
        self.cbo_selected_country['values'] = tuple(controller.GetCountriesFromTable())
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
        selected_country = self.selected_country.get()  # Wybrany kraj
        # Ustawienie nowych wartości dla Combobox z miastami
        self.cbo_selected_city['values'] = controller.GetCitiesForCountry(selected_country)

        # Ukrycie lub wyświetlenie Combobox z miastami w zależności od wybranego kraju
        if selected_country:
            self.cbo_selected_city['state'] = 'readonly'
            self.cbo_selected_city.grid()
            self.geometry(self.windowSizeCountry)
            self.lblCity.grid()
        else:
            self.cbo_selected_city['state'] = 'disabled'
            self.cbo_selected_city.grid_remove()
            self.geometry(self.windowSizeStart)
            self.lblCity.grid_remove()


class Login(CenteredWindow):
    def __init__(self):
        super().__init__()
        WINDOW_SIZE_NORMAL = "250x140"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Login')

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

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

        # zarejestruj button
        self.registerButton = ttk.Button(self, text="Zarejestruj", command=lambda: self.CloseOpen("RegisterAccount"))
        self.registerButton.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        # Cofnij button
        self.goBackButton = ttk.Button(self, text="Cofnij", command=lambda: self.CloseOpen("MainPage"))
        self.goBackButton.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        self.errorLabel = ttk.Label(self, text="Błędne logowanie!")
        self.errorLabel.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.errorLabel.grid_remove()

    def logInWithCredentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        blnPassword = controller.VerifyLogIn(username, password)

        if blnPassword:
            self.destroy()
            mainPage = MainPage()
            mainPage.mainloop()
        else:
            self.errorLabel.grid()


class InputPersonalData(CenteredWindow):
    def __init__(self):
        super().__init__()
        WINDOW_SIZE_NORMAL = "260x250"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # labels
        self.login = ttk.Label(self, text="Login:")
        self.login.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.password = ttk.Label(self, text="Hasło:")
        self.password.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.email = ttk.Label(self, text="Email")
        self.email.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.name = ttk.Label(self, text="Imię:")
        self.name.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.surname = ttk.Label(self, text="Nazwisko:")
        self.surname.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.pesel = ttk.Label(self, text="Pesel:")
        self.pesel.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.Error = ttk.Label(self, text="Konto już istnieje!")
        self.Error.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.Error.grid_remove()

        # fields
        self.loginEntry = ttk.Entry(self)
        self.loginEntry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        self.passwordEntry = ttk.Entry(self)
        self.passwordEntry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
        self.emailEntry = ttk.Entry(self)
        self.emailEntry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)
        self.nameEntry = ttk.Entry(self)
        self.nameEntry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
        self.surnameEntry = ttk.Entry(self)
        self.surnameEntry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)
        self.peselEntry = ttk.Entry(self)
        self.peselEntry.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)


class RegisterAccount(InputPersonalData):
    def __init__(self):
        super().__init__()
        self.title('Zarejestruj konto')
        #Additional buttons
        self.registerButton = ttk.Button(self, text="Zarejestruj", command=lambda: self.RegisterAccount())
        self.registerButton.grid(column=1, row=7, sticky=tk.E, padx=5, pady=5)
        self.goBackButton = ttk.Button(self, text="Cofnij", command=lambda: self.CloseOpen("MainPage"))
        self.goBackButton.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)

    def RegisterAccount(self):
        strLogin = self.loginEntry.get()
        strPassword = self.passwordEntry.get()
        strEmail = self.emailEntry.get()
        strName = self.nameEntry.get()
        strSurname = self.surnameEntry.get()
        strPesel = self.peselEntry.get()
        # określa, czy dany uzytkownik juz istnieje
        blnCreated = controller.isUserDuplicate(strEmail, strLogin, strPesel)
        if blnCreated:
            self.Error.grid()
        else:
            #tworzy nowego użytkownika
            controller.CreateNewUserRecord(strName, strSurname, strPesel, strEmail, strLogin, strPassword)
            controller.USER_LOGGED_ID = controller.GetUserId(strLogin)
            controller.USER_LOGGED_IN = True
            self.CloseOpen("MainPage")


class PersonalPanel(CenteredWindow):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        WINDOW_SIZE_NORMAL = "270x180"
        self.title('Panel użytkownika')
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.MyPersonalData = ttk.Button(self, text="Moje dane", command=lambda: self.CloseOpen("PersonalData"))
        self.MyPersonalData.grid(column=1, row=0, sticky=tk.NS, padx=5, pady=5)
        self.MyOpinions = ttk.Button(self, text="Moje opinie", command=lambda: self.CloseOpen("XX"))
        self.MyOpinions.grid(column=1, row=1, sticky=tk.NS, padx=5, pady=5)
        self.MyReviews = ttk.Button(self, text="Moje recenzje", command=lambda: self.CloseOpen("XX"))
        self.MyReviews.grid(column=1, row=2, sticky=tk.NS, padx=5, pady=5)
        self.MyReviews = ttk.Button(self, text="Usuń konto", command=lambda: self.DeleteData())
        self.MyReviews.grid(column=1, row=3, sticky=tk.NS, padx=5, pady=5)
        self.MainPage = ttk.Button(self, text="Strona główna", command=lambda: self.CloseOpen("MainPage"))
        self.MainPage.grid(column=1, row=4, sticky=tk.NS, padx=5, pady=5)

    def DeleteData(self):
        #Usuniecie/anonimizacja danych + wylogowanie
        controller.DeletePersonalAccount()
        controller.USER_LOGGED_IN = False
        controller.USER_LOGGED_ID = None
        self.CloseOpen("MainPage")

class PersonalData(InputPersonalData):
    def __init__(self):
        super().__init__()
        self.title('Moje dane')
        self.SaveData = ttk.Button(self, text="Zapisz dane", command=lambda: self.SaveData())
        self.SaveData.grid(column=1, row=7, sticky=tk.NS, padx=5, pady=5)
        self.MainPage = ttk.Button(self, text="Strona główna", command=lambda: self.CloseOpen("MainPage"))
        self.MainPage.grid(column=0, row=7, sticky=tk.NS, padx=5, pady=5)
        #Załaduj dane
        arrData = controller.LoadPersonalDataIntoForm()
        self.loginEntry.insert(0, arrData[6])
        self.passwordEntry.insert(0, arrData[7])
        self.emailEntry.insert(0, arrData[4])
        self.nameEntry.insert(0, arrData[1])
        self.surnameEntry.insert(0, arrData[2])
        self.peselEntry.insert(0, arrData[3])

    def SaveData(self):
        #Sprawdź poprawność danych
        #Zapisz dane
        pass

class FindRecords(CenteredWindow):
    def __init__(self):
        super().__init__()
        WINDOW_SIZE_NORMAL = "270x145"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Panel użytkownika')


