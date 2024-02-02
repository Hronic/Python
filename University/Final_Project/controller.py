import sqlite3
from datetime import datetime

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


def GetOpinionTypes():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT opinionTypeName FROM OpinionTypeDic')
    allOpinionTypes = cursor.fetchall()
    opinionNames = [opinionType[0] for opinionType in allOpinionTypes]
    conn.close()
    return opinionNames


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
    # Sprawdza, czy dane do logowania + hasło są poprawne
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
    # Zwraca Id użytkownika o danym loginie
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
    # Sprawdza, czy istnieje użytkownik o danym loginie, mailu lub peselu
    query = "SELECT EXISTS (SELECT 1 FROM User WHERE login = ? OR email = ? OR pesel = ? LIMIT 1);"
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(query, (strLogin, strEmail, strPesel))
    result = cursor.fetchone()[0]
    conn.close()
    blnResult = bool(result)
    return blnResult


def CreateNewUserRecord(strName, strSurname, strPesel, strEmail, strLogin, strPassword):
    # Tworzy nowy rekord użytkownika
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
    # Sprawdza, czy istnieje w systmeie inna osoba, która zajmuje już wskazany pesel, mail lub login
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


def getUserOpinions(userId):
    # Metoda zwraca opinie dla użytkownika o podanym userId
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Opinion
        WHERE userId = ?
    ''', (userId,))
    opinionsData = cursor.fetchall()
    conn.close()
    return opinionsData


def saveOpinionToDatabase(opinionText, opinionTypeDicId, stars):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    global USER_LOGGED_ID
    currentDate = datetime.now().date()
    cursor.execute('''
        INSERT INTO Opinion (userId, opinionTypeDicId, reviewedEntryId, creationDate, opinionValue, stars)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (USER_LOGGED_ID, opinionTypeDicId, 1, currentDate, opinionText, stars))
    conn.close()


def getUserReservations(userId):
    # Metoda zwraca rezerwacje dla użytkownika o podanym userId
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Reservation
        WHERE userId = ?
    ''', (userId,))
    reservationData = cursor.fetchall()
    conn.close()
    return reservationData


def getOfficeIdFromSpecificService(specificServiceId):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM SpecificService
        WHERE specificServiceId = ?
    ''', (specificServiceId,))
    specificServiceData = cursor.fetchall()
    officeId = specificServiceData[0][2]
    conn.close()
    return officeId


def getOfficesData(country, city):
    # Pobierz gabinety dla danego kraju i miasta
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT officeId, officeName, address, postCode, isNFZAvailable, webPageAddress FROM Office
        WHERE cityDicId = (SELECT cityDicId FROM CityDic WHERE cityName = ?)
        AND countryDicId = (SELECT countryDicId FROM CountryDic WHERE countryName = ?)
        AND isActive = 1
    ''', (city, country))
    officesData = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in cursor.fetchall()]
    list_ids = [row[0] for row in officesData]
    formattedOffices = [
        f"{name}, na ulicy {address}, kod pocztowy: {postCode}, adres www: {webPageAddress}, {'Obsługuje NFZ' if isNFZAvailable else 'Nie obsługuje NFZ'}"
        for id, name, address, postCode, isNFZAvailable, webPageAddress in officesData
    ]
    conn.close()
    return list_ids, formattedOffices


def getSpecificOfficeInfo(officeId):
    # Pobierz informacje o konkretnym gabinecie na podstawie officeId
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.officeId, c.cityName, co.countryName, o.address, o.isNFZAvailable, o.officeName, o.address, o.postCode, o.webPageAddress
        FROM Office o
        JOIN CityDic c ON o.cityDicId = c.cityDicId
        JOIN CountryDic co ON o.countryDicId = co.countryDicId
        WHERE o.isActive = 1 AND o.officeId = ? 
    ''', (officeId,))
    officesData = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) for row in
                   cursor.fetchall()]
    list_ids = [row[0] for row in officesData]  # get Ids
    formattedOffices = [
        f"Gabinet: {officeName}, \nadres: {countryName} {cityName} {address} {postCode}, \nadres www: {webPageAddress}, \n{'Obsługuje NFZ' if isNFZAvailable else 'Nie obsługuje NFZ'}"
        for officeId, cityName, countryName, address, isNFZAvailable, officeName, address, postCode, webPageAddress in
        officesData
    ]
    conn.close()
    return list_ids, formattedOffices


def get_office_opinions(officeIdd):
    # Pobierz opinie dla danego gabinetu
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Opinion
        WHERE reviewedEntryId = ? AND opinionTypeDicId = 3
     ''', (officeIdd,))

    opinionsData = cursor.fetchall()
    formattedData = [
        f"Opinia dodana: {creationDate}, wartość oceny: {stars}, treść: {opinionValue}."
        for id, userId, opinionTypeId, reviewdEntryId, creationDate, opinionValue, stars in opinionsData
    ]
    conn.close()
    return formattedData


def MakeSpecificReservation(officeId, date, discountCode):
    officeIdReservation = officeId[0]
    global USER_LOGGED_ID
    discountId = None
    discountValue = None
    isValue = None
    finalPrice = None

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Discount
        WHERE isActive = 1 AND discountCode = ?;
    ''', (discountCode,))
    result = cursor.fetchone()
    if result:
        if isinstance(result, tuple):
            discountId = result[0]
            discountValue = result[3]
            isValue = result[5]
    else:
        discountId = 1
        print(f"Brak kodu rabatowego o kodzie: {discountCode}")

    cursor.execute('''
        SELECT * FROM SpecificService
        WHERE officeId = ?
    ''', (officeIdReservation,))
    opinionsData = cursor.fetchall()
    # specificServiceId, dentistId, officeId, price, serviceTypeGeneralId
    specificService = [(row[0], row[1], row[2], row[3], row[4]) for row in opinionsData]
    specificServiceId = specificService[0][0]
    finalPrice = specificService[0][3]
    if discountId != 1:
        if isValue == 1:
            finalPrice = finalPrice - discountValue
        else:
            finalPrice = (1 - discountValue) * finalPrice
    else:
        finalPrice = specificService[0][3]

    cursor.execute('''
        INSERT INTO Reservation (finalPrice, discountId, otherComments, reservationDate, reservationStatus, SpecificServiceId, userId)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (finalPrice, discountId, "Brak", date, "Potwierdzone", specificServiceId, USER_LOGGED_ID))
    conn.commit()
    conn.close()


def isDateNotHoliday(dateToBeValidated):
    blnDateCorrectness = True
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Calendar
    ''')
    dates = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    for singleDate in dates:
        if singleDate[2] == dateToBeValidated:
            blnDateCorrectness = False
            break
    return blnDateCorrectness
