import sqlite3

DATABASE_NAME = "PorownywarkaStomatologiczna.db"
USER_LOGGED_IN = False
USER_LOGGED_ID = None
def GetCountriesFromTable():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT countryName FROM CountryDic')
    allCountries = cursor.fetchall()
    countriesNames = [country[0] for country in allCountries]
    conn.close()
    return countriesNames


def GetCitiesForCountry(strCountryName):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CountryDic WHERE countryName = ?", (strCountryName,))
    oneCountry = cursor.fetchall()
    countryId = oneCountry[0][0]  # get countryId
    cursor.execute("SELECT * FROM 'CityDic' WHERE countryDicID = ?", (countryId,))
    allCities = cursor.fetchall()
    citiesName = [city[2] for city in allCities]
    conn.close()
    return citiesName


def VerifyLogIn(username, password):
    #Sprawdza, czy dane do logowania + hasło są poprawne
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE login = ? AND password = ? AND isBlocked = 0", (username, password))
    user_data = cursor.fetchone()
    if user_data is None:
        cursor.execute("SELECT * FROM Admin WHERE login = ? AND password = ? AND isBlocked = 0", (username, password))
        user_data = cursor.fetchone()
    conn.close()
    if user_data:
        print("Zalogowano pomyślnie!")
        global USER_LOGGED_IN  # określenie jako zmaiennej globalnej
        global USER_LOGGED_ID
        USER_LOGGED_IN = True  # zmiana wartości na zalogowanie
        USER_LOGGED_ID = GetUserId(username)
        return USER_LOGGED_IN
    else:
        print("Błędny login lub hasło. Spróbuj ponownie.")
        return USER_LOGGED_IN

def GetUserId(strLogin):
    #Zwraca Id użytkownika o danym loginie
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE login = ?", (strLogin,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data is None:
        return None
    else:
        return user_data[0]

def isUserDuplicate(strLogin, strEmail, strPesel):
    #Sprawdza, czy istnieje użytkownik o danym loginie, mailu lub peselu
    query = "SELECT EXISTS (SELECT 1 FROM User WHERE login = ? OR email = ? OR pesel = ? LIMIT 1);"
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(query, (strLogin, strEmail, strPesel))
    result = cursor.fetchone()[0]
    conn.close()
    blnResult = bool(result)
    return blnResult

def CreateNewUserRecord(strName, strSurname, strPesel, strEmail, strLogin, strPassword):
    #Tworzy nowy rekord użytkownika
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    sql_insert_user = '''
        INSERT INTO User (name, surname, pesel, email, isBlocked, login, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(sql_insert_user, (strName, strSurname, strPesel, strEmail, 0, strLogin, strPassword))
    conn.commit()
    conn.close()

def LoadPersonalDataIntoForm():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    global USER_LOGGED_ID
    cursor.execute("SELECT * FROM User WHERE userId = ?", (USER_LOGGED_ID,))
    userData = cursor.fetchone()
    conn.close()
    if userData:
        return list(userData)
    else:
        return None

def DeletePersonalAccount():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    global USER_LOGGED_ID
    update_user_query = """
        UPDATE User
        SET name = NULL, surname = NULL, pesel = NULL, email = NULL, isBlocked = 1, login = NULL, password = NULL
        WHERE userId = ?
    """
    cursor.execute(update_user_query, (USER_LOGGED_ID,))
    conn.commit()
    conn.close()

def CheckIfNewDataIsAvailable(newPesel, newEmail, newLogin):
    #Sprawdza, czy istnieje w systmeie inna osoba, która zajmuje już wskazany pesel, mail lub login
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    check_user_query = """
        SELECT userId
        FROM User
        WHERE (pesel = ? OR login = ? OR email = ?) AND userId != ?
    """
    cursor.execute(check_user_query, (newPesel, newLogin, newEmail, USER_LOGGED_ID))
    existing_user = cursor.fetchone()
    conn.close()
    return existing_user is not None
def UpdatePersonalAccount(newName, newSurname, newPesel, newEmail, newLogin, newPassword):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    global USER_LOGGED_ID
    update_user_query = """
        UPDATE User
        SET name = ?, surname = ?, pesel = ?, email = ?, login = ?, password = ?
        WHERE userId = ?
    """
    cursor.execute(update_user_query, (newName, newSurname, newPesel, newEmail, newLogin, newPassword, USER_LOGGED_ID))
    conn.commit()
    conn.close()