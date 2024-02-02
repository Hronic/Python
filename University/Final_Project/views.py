import tkinter as tk
from tkinter import ttk, Text
import controller
import sys
from tkcalendar import Calendar
from datetime import datetime


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

    def CloseOpen(self, openWindow):
        # Ogólna funkcja do zamykania obecnego okna i otwierania wskazanego
        # parametry opcjonalne param1=None oraz param2=None
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
        self.btnFind = ttk.Button(self, text="Szukaj", command=lambda: self.OpenFindRecords())
        self.btnFind.grid(column=1, row=5, sticky=tk.S, padx=5, pady=5)
        self.btnFind.grid_remove()

        # Exit button
        btnExit = ttk.Button(self, text="Wyjście", command=lambda: self.CloseWindow())
        btnExit.grid(column=2, row=5, sticky=tk.SE, padx=5, pady=5)

    def on_country_selected(self, event):
        selected_country = self.selected_country.get()  # Wybrany kraj
        # Ustawienie nowych wartości dla Combobox z miastami
        self.cbo_selected_city['values'] = controller.GetCitiesForCountry(selected_country)
        self.cbo_selected_city.bind('<<ComboboxSelected>>', self.on_city_selected)

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

    def on_city_selected(self, event):
        # Aktualizacja widoczności przycisku
        self.update_btnFind_visibility()

    def update_btnFind_visibility(self):
        selected_country = self.selected_country.get()
        selected_city = self.selected_city.get()
        if selected_country and selected_city:
            self.btnFind.grid()
            self.btnFind.grid(column=1, row=5, sticky=tk.S, padx=5, pady=5)
        else:
            self.btnFind.grid_remove()

    def OpenFindRecords(self):
        selectedCountry = self.cbo_selected_country.get()
        selectedCity = self.cbo_selected_city.get()
        if not selectedCountry or not selectedCity:
            print("Wybierz kraj i miasto przed otwarciem formularza.")
            return
        findRecordsWindow = FindRecords(selectedCountry, selectedCity)
        self.destroy()
        findRecordsWindow.mainloop()


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
        # Additional buttons
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
            # tworzy nowego użytkownika
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
        self.MyOpinions = ttk.Button(self, text="Moje opinie", command=lambda: self.CloseOpen("MyOpinions"))
        self.MyOpinions.grid(column=1, row=1, sticky=tk.NS, padx=5, pady=5)
        self.MyReviews = ttk.Button(self, text="Moje rezerwacje", command=lambda: self.CloseOpen("MyReservations"))
        self.MyReviews.grid(column=1, row=2, sticky=tk.NS, padx=5, pady=5)
        self.MyReviews = ttk.Button(self, text="Usuń konto", command=lambda: self.DeleteData())
        self.MyReviews.grid(column=1, row=3, sticky=tk.NS, padx=5, pady=5)
        self.MainPage = ttk.Button(self, text="Strona główna", command=lambda: self.CloseOpen("MainPage"))
        self.MainPage.grid(column=1, row=4, sticky=tk.NS, padx=5, pady=5)

    def DeleteData(self):
        # Usuniecie/anonimizacja danych + wylogowanie
        controller.DeletePersonalAccount()
        controller.USER_LOGGED_IN = False
        controller.USER_LOGGED_ID = None
        self.CloseOpen("MainPage")


class PersonalData(InputPersonalData):
    def __init__(self):
        super().__init__()
        self.title('Moje dane')

        self.InfoLabel = ttk.Label(self, text="Dane są już zajęte!")
        self.InfoLabel.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.InfoLabel.grid_remove()

        self.SaveData = ttk.Button(self, text="Zapisz dane", command=lambda: self.SaveNewData())
        self.SaveData.grid(column=1, row=7, sticky=tk.NS, padx=5, pady=5)
        self.MainPage = ttk.Button(self, text="Strona główna", command=lambda: self.CloseOpen("MainPage"))
        self.MainPage.grid(column=0, row=7, sticky=tk.NS, padx=5, pady=5)

        # Załaduj dane
        arrData = controller.LoadPersonalDataIntoForm()
        self.loginEntry.insert(0, arrData[6])
        self.passwordEntry.insert(0, arrData[7])
        self.emailEntry.insert(0, arrData[4])
        self.nameEntry.insert(0, arrData[1])
        self.surnameEntry.insert(0, arrData[2])
        self.peselEntry.insert(0, arrData[3])

    def SaveNewData(self):
        strLogin = self.loginEntry.get()
        strPassword = self.passwordEntry.get()
        strEmail = self.emailEntry.get()
        strName = self.nameEntry.get()
        strSurname = self.surnameEntry.get()
        strPesel = self.peselEntry.get()
        blnDataExists = controller.CheckIfNewDataIsAvailable(strPesel, strEmail, strLogin)
        if blnDataExists:
            self.InfoLabel.grid_remove()
            self.InfoLabel = ttk.Label(self, text="Dane są już zajęte!")
            self.InfoLabel.grid()
            print("Wskazane dane już są zajęte.")
        else:
            self.InfoLabel.grid_remove()
            self.InfoLabel = ttk.Label(self, text="Zapisano dane!")
            self.InfoLabel.grid()
            controller.UpdatePersonalAccount(strName, strSurname, strPesel, strEmail, strLogin, strPassword)


class MyOpinions(CenteredWindow):
    def __init__(self):
        super().__init__()
        WINDOW_SIZE_NORMAL = "600x250"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Moje opinie')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)

        self.goBackButton = ttk.Button(self, text="Cofnij", command=lambda: self.CloseOpen("PersonalPanel"))
        self.goBackButton.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.recordsListbox = tk.Listbox(self, width=50, height=10)
        self.recordsListbox.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=10, pady=10)

        opinionsData = controller.getUserOpinions(controller.USER_LOGGED_ID)

        # Wyświetl opinie w self.records_listbox
        # opinionId,	userId,	opinionTypeDicId, reviewedEntryId, creationDate, opinionValue, stars
        for opinion in opinionsData:
            opinionType = controller.opinionIdToOpinionName(opinion[2])
            formatted_opinion = f"Opinia {opinionType}, , utworzona: {opinion[4]}, treść: {opinion[5]}, wartość: {opinion[6]}"
            self.recordsListbox.insert(tk.END, formatted_opinion)

        self.exitAppButton = ttk.Button(self, text="Wyjście", command=lambda: self.CloseWindow())
        self.exitAppButton.grid(column=2, row=2, sticky=tk.E, padx=5, pady=5)


class MyReservations(CenteredWindow):
    def __init__(self):
        super().__init__()
        WINDOW_SIZE_NORMAL = "1000x300"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Moje rezerwacje')

        self.reservationIds = []
        self.reservationData = []
        self.selectedReservationId = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)

        self.goBackButton = ttk.Button(self, text="Cofnij", command=lambda: self.CloseOpen("PersonalPanel"))
        self.goBackButton.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.addOpinion = ttk.Button(self, text="Dodaj opinie", command=lambda: self.AddOpinion())
        self.addOpinion.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)

        self.recordsListbox = tk.Listbox(self, width=50, height=10)
        self.recordsListbox.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.recordsListbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        self.InfoLabel = ttk.Label(self,
                                   text="Nie wybrano rezerwacji. Proszę zaznaczyć rezerwacje przed dodaniem opinii.")
        self.InfoLabel.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

        reservationData = controller.getUserReservations(controller.USER_LOGGED_ID)
        # Wyświetl opinie w self.records_listbox
        for reservation in reservationData:
            # Pomijaj kolumnę opinionId (0), userId (1) i zamień opinionTypeDicId
            reservationId = reservation[0]
            self.reservationIds.append(reservationId)
            finalPrice, discountId, comments, reservationDate, status, specificServiceId = reservation[1], reservation[
                2], reservation[3], reservation[4], reservation[5], reservation[6]
            officeId = controller.getOfficeIdFromSpecificService(specificServiceId)
            list_ids, formattedOffices = controller.getSpecificOfficeInfo(officeId)
            formattedReservation = f"Rezerwacja w cenie  {finalPrice} PLN, dnia: {reservationDate}. Status: {status}, gabinet: {formattedOffices}, komentarze: {comments}"
            self.reservationData.append(formattedReservation)
            self.recordsListbox.insert(tk.END, formattedReservation)

        self.exitAppButton = ttk.Button(self, text="Wyjście", command=lambda: self.CloseWindow())
        self.exitAppButton.grid(column=2, row=2, sticky=tk.E, padx=5, pady=5)

    def on_listbox_select(self, event):
        selectedLine = self.recordsListbox.curselection()
        if selectedLine:
            self.InfoLabel.grid_remove()
            selectedReservation = self.recordsListbox.get(selectedLine)  # Pobierz zaznaczony gabinet
            for i, x in enumerate(self.reservationData):
                if x == selectedReservation:
                    self.selectedReservationId = self.reservationIds[i]
                    break

    def AddOpinion(self):
        if self.selectedReservationId:
            self.InfoLabel.grid_remove()
            addOpinionWindow = AddOpinion(self.selectedReservationId)
            addOpinionWindow.mainloop()
        else:
            self.InfoLabel.grid()
            print("Nie wybrano rezerwacji. Proszę zaznaczyć rezerwacje przed dodaniem opinii.")


class AddOpinion(CenteredWindow):
    def __init__(self, selectedReservationId):
        super().__init__()
        WINDOW_SIZE_NORMAL = "660x220"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Dodaj opinie')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.opinionStars = 0
        self.opinionType = None
        self.opinionEntity = None

        self.InfoLabelChoice = ttk.Label(self, text="Co oceniasz?")
        self.InfoLabelChoice.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)

        self.opinionTypeSelected = tk.StringVar()
        self.cboSelectedOpinionType = ttk.Combobox(self, textvariable=self.opinionTypeSelected)
        self.cboSelectedOpinionType.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.cboSelectedOpinionType['values'] = tuple(controller.GetOpinionTypes())
        self.cboSelectedOpinionType.bind('<<ComboboxSelected>>', self.onOpinionTypeSelected)

        self.InfoLabelStars = ttk.Label(self, text="Wybierz ocenę")
        self.InfoLabelStars.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)

        self.opinionStarsSelected = tk.IntVar()
        self.cboSelectedStars = ttk.Combobox(self, textvariable=self.opinionStarsSelected)
        self.cboSelectedStars.grid(column=3, row=0, sticky=tk.W, padx=5, pady=5)
        availableValues = [1, 2, 3, 4, 5]
        self.cboSelectedStars['values'] = tuple(availableValues)
        self.cboSelectedStars.bind('<<ComboboxSelected>>', self.onStarsSelected)

        self.text = Text(self, height=8)
        self.text.grid(column=0, row=1, columnspan=4, sticky="nsew", padx=10, pady=10)
        self.text.insert('1.0', 'Wprowadź opinie')

        self.labelError = ttk.Label(self, text="Co oceniasz?")
        self.labelError.grid(column=0, row=4, sticky=tk.E, padx=5, pady=5)
        self.labelError.grid_remove()

        self.SaveOpinion = ttk.Button(self, text="Dodaj opinie",
                                      command=lambda: self.SaveOpinionInDatabase(selectedReservationId))
        self.SaveOpinion.grid_remove()

        self.closeWindow = ttk.Button(self, text="Zamknij okno", command=lambda: self.destroy())
        self.closeWindow.grid(column=3, row=5, sticky=tk.E, padx=5, pady=5)

    def SaveOpinionInDatabase(self, selectedReservationId):
        textContent = self.text.get('1.0', 'end')
        self.opinionType = controller.opinionNameToOpinionId(self.opinionType)
        self.opinionEntity = controller.getOpinionatedEntity(self.opinionType, selectedReservationId)
        controller.saveOpinionToDatabase(textContent, self.opinionType, self.opinionEntity, self.opinionStars)
        self.destroy()

    def onOpinionTypeSelected(self, event):
        self.opinionType = self.cboSelectedOpinionType.get()
        self.VerifyComboBoxes()

    def onStarsSelected(self, event):
        self.opinionStars = self.cboSelectedStars.get()
        self.VerifyComboBoxes()

    def VerifyComboBoxes(self):
        if self.opinionStars != 0 and self.opinionType:
            self.SaveOpinion.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        else:
            self.SaveOpinion.grid_remove()


class FindRecords(CenteredWindow):
    def __init__(self, country, city):
        super().__init__()
        self.selected_office = None
        self.selected_Office_Id = None
        WINDOW_SIZE_NORMAL = "800x290"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Wyniki wyszukiwania')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.goBackButton = ttk.Button(self, text="Cofnij", command=lambda: self.CloseOpen("MainPage"))
        self.goBackButton.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.reserveOffice = ttk.Button(self, text="Zarezerwuj", command=lambda: self.MakeReservation())
        self.reserveOffice.grid(column=4, row=0, sticky=tk.W, padx=5, pady=5)
        self.notLoggedInLabel = ttk.Label(self, text="Musisz się zalogować, aby móc rezerwować!")
        self.notLoggedInLabel.grid(column=4, row=0, sticky=tk.W, padx=5, pady=5)

        if controller.USER_LOGGED_IN:  # Zależnie od statusu zalogowania pokaż/ukryj przycisk
            self.reserveOffice.grid()
            self.notLoggedInLabel.grid_remove()
        else:
            self.reserveOffice.grid_remove()
            self.notLoggedInLabel.grid()

        self.lookOpinions = ttk.Button(self, text="Zobacz opinie", command=lambda: self.OpenOpinionsWindow())
        self.lookOpinions.grid(column=2, row=7, sticky=tk.W, padx=5, pady=5)
        self.exitApp = ttk.Button(self, text="Wyjście", command=lambda: self.CloseWindow())
        self.exitApp.grid(column=4, row=7, sticky=tk.W, padx=5, pady=5)

        self.recordsListbox = tk.Listbox(self, width=50, height=10)
        self.recordsListbox.grid(column=0, row=2, columnspan=5, sticky="nsew", padx=10, pady=10)
        self.recordsListbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        self.listOfIds, self.officesData = controller.getOfficesData(country, city)
        for office in self.officesData:
            self.recordsListbox.insert(tk.END, office)

    def on_listbox_select(self, event):
        selected_index = self.recordsListbox.curselection()
        if selected_index:
            # Pobierz zaznaczony gabinet
            self.selected_office = self.recordsListbox.get(selected_index)
            for i, x in enumerate(self.officesData):
                if x == self.selected_office:
                    self.selected_Office_Id = self.listOfIds[i]
                    break

    def OpenOpinionsWindow(self):
        # Sprawdź, czy został wybrany gabinet i otwórz opinie jeżeli tak
        if self.selected_office:
            opinions_window = OpinionWindow(self.selected_Office_Id)
            opinions_window.mainloop()
        else:
            print("Nie wybrano gabinetu. Proszę zaznaczyć gabinet przed otwarciem opinii.")

    def MakeReservation(self):
        # Sprawdź, czy został wybrany gabinet
        if self.selected_office:
            opinions_window = MakeReservation(self.selected_Office_Id)
            opinions_window.mainloop()
        else:
            print("Nie wybrano gabinetu. Proszę zaznaczyć gabinet przed otwarciem opinii.")


class OpinionWindow(CenteredWindow):
    def __init__(self, indicatedOffice):
        super().__init__()
        WINDOW_SIZE_NORMAL = "800x290"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Opinie gabinetu')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.InfoLabel = ttk.Label(self, text="Opinie gabinetu:")
        self.InfoLabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.recordsListbox = tk.Listbox(self, width=50, height=10)
        self.recordsListbox.grid(column=0, row=1, columnspan=5, sticky="nsew", padx=10, pady=10)
        opinionData = controller.get_office_opinions(indicatedOffice)
        for opinion in opinionData:
            self.recordsListbox.insert(tk.END, opinion)

        self.closeWindowButton = ttk.Button(self, text="Zamknij okno", command=self.destroy)
        self.closeWindowButton.grid(column=5, row=21, sticky=tk.W, padx=5, pady=5)


class MakeReservation(CenteredWindow):
    def __init__(self, indicatedOffice):
        super().__init__()
        self.selected_date_label = None
        self.selectedDate = None
        self.discountInserted = None

        WINDOW_SIZE_NORMAL = "450x260"
        self.GeneralWindowOptions()
        self.geometry(WINDOW_SIZE_NORMAL)
        self.title('Wykonaj rezerwacje')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.InfoLabel = ttk.Label(self, text="Wykonaj rezerwacje dla gabinetu:")
        self.InfoLabel.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        listOfIds, ListOfOfficeData = controller.getSpecificOfficeInfo(indicatedOffice)
        self.OfficeInfo = ttk.Label(self, text=ListOfOfficeData[0])
        self.OfficeInfo.grid(column=0, row=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.discountLabel = ttk.Label(self, text="Wprowadź kod rabatowy:")
        self.discountLabel.grid(column=0, row=2, columnspan=1, sticky="nsew", padx=5, pady=5)
        self.discountValue = ttk.Entry(self)
        self.discountValue.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.selected_date_label = ttk.Label(self, text="Wybierz datę!")
        self.selected_date_label.grid(column=0, row=3, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.btnChooseDate = ttk.Button(self, text="Wybierz datę", command=self.choose_date)
        self.btnChooseDate.grid(column=0, row=4, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.exitApp = ttk.Button(self, text="Zarezerwuj", command=lambda: self.MakeReservationForDate(listOfIds))
        self.exitApp.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.closeWindow = ttk.Button(self, text="Zamknij Okno", command=self.destroy)
        self.closeWindow.grid(column=1, row=7, sticky=tk.E, padx=5, pady=5)

    def choose_date(self):
        date_chooser = DateChooser(self, self.on_date_selected)

    def on_date_selected(self, selected_date):
        parsed_date = datetime.strptime(selected_date, "%m/%d/%y")
        formatted_date = parsed_date.strftime("%d-%m-%Y")
        parsed_date = datetime.strptime(formatted_date, "%d-%m-%Y")
        current_date = datetime.now()
        if parsed_date < current_date:
            self.selected_date_label.config(text="Data nie może być wsteczna!")
            self.selectedDate = None
        else:
            self.selected_date_label.config(text=f"Wybrana data: {formatted_date}")
            self.selectedDate = formatted_date

    def MakeReservationForDate(self, officeId):
        self.discountInserted = self.discountValue.get()
        if self.selectedDate is None:
            self.selected_date_label.config(text="Nie wybrano daty rezerwacji!")
            print("Nie wybrano daty rezerwacji!")
        else:
            blnProperDate = controller.isDateNotHoliday(self.selectedDate)
            if blnProperDate:
                controller.MakeSpecificReservation(officeId, self.selectedDate, self.discountInserted)
                self.destroy()
            else:
                self.selected_date_label.config(text="Wybrana data jest świętem!")
                print("Wybrana data jest świętem!")


class DateChooser(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Wybierz datę")
        self.geometry("300x300")
        current_date = datetime.now().date()
        self.cal = Calendar(self, selectmode="day", year=current_date.year, month=current_date.month,
                            day=current_date.day)
        self.cal.pack(pady=20)

        btn_ok = ttk.Button(self, text="OK", command=lambda: self.on_ok(callback))
        btn_ok.pack(pady=10)

    def on_ok(self, callback):
        selected_date = self.cal.get_date()
        if selected_date:
            callback(selected_date)
            self.destroy()
