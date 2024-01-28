import sqlite3
import os

DATABASE_NAME = "PorownywarkaStomatologiczna.db"

# Do przeglądania bazy danych: https://inloop.github.io/sqlite-viewer/

def checkDatabaseStatus():
    if os.path.exists(DATABASE_NAME):
        print(f"Baza danych '{DATABASE_NAME}' istnieje.")
    else:
        createDatabase(DATABASE_NAME)
        print(f"Baza danych '{DATABASE_NAME}' została utworzona.")


def createDatabase(database_path):
    conn = sqlite3.connect(database_path)
    conn.commit()
    conn.close()
    createTables()
    createSampleData()


def createTables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Utwórz tabelę User
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            pesel TEXT,
            email TEXT,
            isBlocked INTEGER,
            login TEXT,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RoleDic (
            RoleDicId INTEGER PRIMARY KEY AUTOINCREMENT,
            RoleName TEXT
        )
    ''')
    # Utwórz tabelę Admin
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            pesel TEXT,
            email TEXT,
            isBlocked INTEGER,
            login TEXT,
            password TEXT,
            phoneNumber TEXT,
            roleDicId INTEGER,
            FOREIGN KEY (roleDicId) REFERENCES RoleDic(RoleDicId)
        )
    ''')
    # Utwórz tabelę Dentist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dentist (
            doctorId INTEGER PRIMARY KEY AUTOINCREMENT,
            activeAccount INTEGER,
            email TEXT,
            login TEXT,
            password TEXT,
            name TEXT,
            surname TEXT,
            phone TEXT,
            isDentalProsthetics INTEGER,
            isDentalSurgery INTEGER,
            isOrthodontics INTEGER,
            isPediatricDentist INTEGER,
            licenseNumber TEXT
        )
    ''')
    # Utwórz tabelę Calendar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Calendar (
            calendarId INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            excludedDate TEXT
        )
    ''')
    # Utwórz tabelę CountryDic
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CountryDic (
            countryDicId INTEGER PRIMARY KEY AUTOINCREMENT,
            countryName TEXT
        )
    ''')
    # Utwórz tabelę CityDic
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CityDic (
            cityDicId INTEGER PRIMARY KEY AUTOINCREMENT,
            countryDicId INTEGER,
            cityName TEXT,
            FOREIGN KEY (countryDicId) REFERENCES CountryDic(countryDicId)
        )
    ''')
    # Utwórz tabelę Office
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Office (
            officeId INTEGER PRIMARY KEY AUTOINCREMENT,
            cityDicId INTEGER,
            countryDicId INTEGER,
            address TEXT,
            isActive INTEGER,
            isNFZAvailable INTEGER,
            officeName TEXT,
            postCode TEXT,
            webPageAddress TEXT,
            FOREIGN KEY (cityDicId) REFERENCES CityDic(cityDicId),
            FOREIGN KEY (countryDicId) REFERENCES CountryDic(countryDicId)
        )
    ''')
    # Utwórz tabelę OpinionTypeDic
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OpinionTypeDic (
            opinionTypeDicId INTEGER PRIMARY KEY AUTOINCREMENT,
            opinionTypeName TEXT
        )
    ''')
    # Utwórz tabelę Discount
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Discount (
            discountId INTEGER PRIMARY KEY,
            officeId INTEGER,
            discountCode TEXT,
            discountValue REAL,
            isActive INTEGER,
            isValue INTEGER,
            FOREIGN KEY (officeId) REFERENCES Office(officeId)
        )
    ''')
    #Utwórz tabelę Opinion
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Opinion (
            opinionId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER,
            opinionTypeDicId INTEGER,
            reviewedEntryId INTEGER,
            creationDate TEXT,
            opinionValue TEXT,
            stars INTEGER,
            FOREIGN KEY (userId) REFERENCES User(userId),
            FOREIGN KEY (opinionTypeDicId) REFERENCES OpinionTypeDic(opinionTypeDicId)
        )
    ''')
    #Utwórz tabelę ServiceTypeGeneral
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ServiceTypeGeneral (
            serviceTypeGeneralId INTEGER PRIMARY KEY AUTOINCREMENT,
            serviceName TEXT,
            serviceDescription TEXT
        )
    ''')
    #Utwórz tabelę SpecificService
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SpecificService (
            specificServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
            dentistId INTEGER,
            officeId INTEGER,
            price REAL,
            serviceTypeGeneralId INTEGER,
            FOREIGN KEY (dentistId) REFERENCES Dentist(doctorId),
            FOREIGN KEY (officeId) REFERENCES Office(officeId),
            FOREIGN KEY (serviceTypeGeneralId) REFERENCES ServiceTypeGeneral(serviceTypeGeneralId)
        )
    ''')
    # Utwórz tabelę Reservation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservation (
            reservationId INTEGER PRIMARY KEY AUTOINCREMENT,
            finalPrice REAL,
            discountId INTEGER,
            otherComments TEXT,
            reservationDate TEXT,
            reservationStatus INTEGER,
            SpecificServiceId INTEGER,
            userId INTEGER,
            FOREIGN KEY (discountId) REFERENCES Discount(discountId),
            FOREIGN KEY (SpecificServiceId) REFERENCES SpecificService(specificServiceId),
            FOREIGN KEY (userId) REFERENCES User(userId)
        )
    ''')
    # Wprowadź zmiany, zakończ połączenie
    conn.commit()
    conn.close()


def createSampleData():  # Zapełnienie bazy danych przykłądowymi danymi
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Tabela User ========================================================================================
    users_data = [
        ('John', 'Doe', '12345678901', 'john.doe@email.com', 0, 'john_doe', 'password123'),
        ('Alice', 'Smith', '98765432101', 'alice.smith@email.com', 1, 'alice_smith', 'pass123'),
        ('Bob', 'Johnson', '11122334455', 'bob.johnson@email.com', 0, 'bob_johnson', 'secret123'),
        ('Eva', 'Williams', '55566778899', 'eva.williams@email.com', 1, 'eva_williams', 'topsecret123'),
        ('Michael', 'Davis', '99900011122', 'michael.davis@email.com', 0, 'michael_davis', 'adminpass'),
        ('Sophia', 'Taylor', '44455566677', 'sophia.taylor@email.com', 1, 'sophia_taylor', 'userpass'),
        ('Oliver', 'Brown', '88899900011', 'oliver.brown@email.com', 0, 'oliver_brown', 'mypassword'),
        ('Emma', 'Anderson', '33344455566', 'emma.anderson@email.com', 1, 'emma_anderson', 'secretpass'),
        ('James', 'White', '77788899900', 'james.white@email.com', 0, 'james_white', 'newpassword'),
        ('Ava', 'Clark', '22233344455', 'ava.clark@email.com', 1, 'ava_clark', 'testpass'),
    ]
    cursor.executemany('''
        INSERT INTO User (
            name, surname, pesel, email, isBlocked, login, password
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', users_data)

    # Tabela RoleDic ========================================================================================
    roles_data = [
        ('Administrator',),
        ('Pracownik',),
        ('Klient',),
    ]
    cursor.executemany('INSERT INTO RoleDic (RoleName) VALUES (?)', roles_data)

    # Tabela Admin ========================================================================================
    admins_data = [
        ('Dagmara', 'Jaworska', '12345678901', 'Dagmara.Jaworska@email.com', 0, 'semet', 'fQehqkywFk', '123456789', 1),
        ('Balbina', 'Kowalska', '98765432101', 'Balbina.Kowalska@email.com', 1, 'thal', 'gWGuCKLQQr', '987654321', 2),
        ('Danuta', 'Zalewska', '11122334455', 'Danuta.Zalewska@email.com', 0, 'lowern', '4VQskhHfHS', '111223344', 1),
        ('Patrycja', 'Tomaszewska', '55566778899', 'Patrycja.Tomaszewska@email.com', 1, 'urmin', 'M537xMKgd7', '555667788', 2),
        ('Czesława', 'Przybylska', '99900011122', 'Czesława.Przybylska@email.com', 0, 'mawer', '6n3MLKdMmv', '999000111', 1),
    ]
    cursor.executemany('''
        INSERT INTO Admin (
            name, surname, pesel, email, isBlocked, login, password, phoneNumber, roleDicId
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', admins_data)
    # Tabela Dentist ========================================================================================
    dentists_data = [
        (1, 1, 'doctor1@email.com', 'doctor1_login', 'password1', 'Doctor', 'One', '123456789', 1, 0, 1, 0,
         'License123'),
        (1, 2, 'doctor2@email.com', 'doctor2_login', 'password2', 'Doctor', 'Two', '987654321', 0, 1, 0, 1,
         'License456'),
        (1, 3, 'doctor3@email.com', 'doctor3_login', 'password3', 'Doctor', 'Three', '555555555', 1, 1, 1, 1,
         'License789'),
        (1, 4, 'doctor4@email.com', 'doctor4_login', 'password4', 'Doctor', 'Four', '111111111', 0, 0, 1, 0,
         'LicenseABC'),
        (1, 5, 'doctor5@email.com', 'doctor5_login', 'password5', 'Doctor', 'Five', '222222222', 1, 1, 1, 1,
         'LicenseXYZ'),
    ]
    cursor.executemany('''
        INSERT INTO Dentist (
            activeAccount, doctorId, email, login, password, name, surname, phone, isDentalProsthetics, isDentalSurgery, isOrthodontics, isPediatricDentist, licenseNumber
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dentists_data)
    # Tabela Calendar ========================================================================================
    calendar_data = [
        (1, 'Nowy Rok', '2024-01-01'),
        (2, 'Trzech Króli (Objawienie Pańskie)', '2024-01-06'),
        (3, 'Wielkanoc', '2024-03-31'),
        (4, 'Poniedziałek Wielkanocny', '2024-04-01'),
        (5, 'Święto Pracy', '2024-05-01'),
        (6, 'Święto Konstytucji 3 Maja', '2024-05-03'),
        (7, 'Zesłanie Ducha Świętego (Zielone Świątki)', '2024-05-19'),
        (8, 'Boże Ciało', '2024-05-30'),
        (9, 'Święto Wojska Polskiego, Wniebowzięcie Najświętszej Maryi Panny', '2024-08-15'),
        (10, 'Wszystkich Świętych', '2024-11-01'),
        (11, 'Święto Niepodległości', '2024-11-11'),
        (12, 'Boże Narodzenie (pierwszy dzień)', '2024-12-25'),
        (13, 'Boże Narodzenie (drugi dzień)', '2024-12-26'),
    ]
    cursor.executemany('''
        INSERT INTO Calendar (
            calendarId, description, excludedDate
        ) VALUES (?, ?, ?)
    ''', calendar_data)
    # Tabela CountryDic ========================================================================================
    countries_data = [
        (1, 'Polska'),
        (2, 'Stany Zjednoczone'),
        (3, 'Japonia'),
        (4, 'Niemcy'),
        (5, 'Francja'),
    ]
    cursor.executemany('''
        INSERT INTO CountryDic (
            countryDicId, countryName
        ) VALUES (?, ?)
    ''', countries_data)
    # Tabela CityDic ========================================================================================
    cities_data = [
        (1, 1, 'Warszawa'),
        (2, 1, 'Kraków'),
        (3, 2, 'Nowy Jork'),
        (4, 2, 'Los Angeles'),
        (5, 3, 'Tokio'),
        (6, 3, 'Kioto'),
        (7, 4, 'Berlin'),
        (8, 5, 'Paryż'),
    ]
    cursor.executemany('''
        INSERT INTO CityDic (
            cityDicId, countryDicId, cityName
        ) VALUES (?, ?, ?)
    ''', cities_data)
    # Tabela Office ========================================================================================
    offices_data = [
        (1, 1, 1, 'Marszalkowska 123', 1, 1, 'Warszawski Gabinet Ząb', '12345', 'http://www.example.com'),
        (2, 2, 1, 'Aleja 3 maja', 1, 0, 'Kraków walczy z próchnicą', '54321', 'http://www.sample.com'),
        (3, 3, 2, '6th Avenue 49', 1, 1, 'Amerykanie przeciwko chorym zębom', '67890', 'http://www.demo.com'),
        (4, 4, 2, 'Beverly Boulevard 19', 1, 0, 'Upadłe zęby', '09876', 'http://www.test.com'),
        (5, 5, 3, 'Shinjuku 13', 1, 1, 'Tokijski ząb', '13579', 'http://www.city.com'),
        (6, 6, 3, 'Yokai Street 6', 1, 0, 'Potwory próchnicy', '24680', 'http://www.site.com'),
        (7, 7, 4, 'Alexanderplatz 99', 1, 1, 'Alexander zębowy', '11223', 'http://www.visit.com'),
        (8, 8, 5, 'Pola Elizejskie 66', 1, 0, 'Marsz paryski Dental', '33445', 'http://www.explore.com'),
        (9, 1, 1, 'Bagno 5', 1, 1, 'Nawet nie poczujesz', '12345', 'http://www.example.com'),
        (10, 1, 1, 'Władysława Andera 9', 1, 0, 'Bohaterów', '12345', 'http://www.example.com'),
        (11, 1, 1, 'Koszykowa 5', 1, 0, 'PJATS', '12345', 'http://www.example.com'),
        (12, 1, 1, 'Dowcip 69', 0, 0, 'Wyrywanie na gazie', '12345', 'http://www.example.com'),
        (13, 1, 1, 'Dzika 666', 0, 1, 'Dzikie rwanie', '12345', 'http://www.example.com'),
    ]
    cursor.executemany('''
        INSERT INTO Office (
            officeId, cityDicId, countryDicId, address, isActive, isNFZAvailable, officeName, postCode, webPageAddress
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', offices_data)
    # Tabela OpinionTypeDic ========================================================================================
    opinion_types_data = [
        (1, 'Usługa'),
        (2, 'Lekarz'),
        (3, 'Gabinet'),
    ]
    cursor.executemany('''
        INSERT INTO OpinionTypeDic (
            opinionTypeDicId, opinionTypeName
        ) VALUES (?, ?)
    ''', opinion_types_data)
    #Tabela Discounts ========================================================================================
    discounts_data = [
        (1, 'Brak', 0, 1, 1),
        (1, 'SALE50', 0.5, 1, 0),
        (2, 'NEWCLIENT', 0.1, 1, 0),
        (2, 'OFFICEOPENING', 30, 1, 1),
        (3, 'WEEKENDSALE', 60, 1, 1),
    ]
    cursor.executemany('''
        INSERT INTO Discount (
            officeId, discountCode, discountValue, isActive, isValue
        ) VALUES (?, ?, ?, ?, ?)
    ''', discounts_data)
    #Tabela Opinions ========================================================================================
    opinions_data = [
        (1, 1, 1, 1, '02-01-2024', 'Bardzo dobre doświadczenie', 5),
        (2, 2, 2, 2, '01-03-2024', 'Średnie wrażenia', 3),
        (3, 3, 1, 3, '01-05-2024', 'Bardzo miła obsługa', 4),
        (4, 4, 2, 1, '01-07-2024', 'Złe doświadczenie', 2),
        (5, 5, 1, 2, '01-10-2024', 'Bardzo polecam', 5),
    ]
    cursor.executemany('''
        INSERT INTO Opinion (
            opinionId, userId, opinionTypeDicId, reviewedEntryId, creationDate, opinionValue, stars
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', opinions_data)
    # Tabela ServiceTypeGeneral ========================================================================================
    service_types_data = [
        (1, 'Dentystyka ogólna', 'Usługi stomatologiczne ogólnego charakteru'),
        (2, 'Ortodoncja', 'Korekcja wad zgryzu i układu zębów'),
        (3, 'Chirurgia stomatologiczna', 'Zabiegi chirurgiczne w stomatologii'),
    ]
    cursor.executemany('''
        INSERT INTO ServiceTypeGeneral (
            serviceTypeGeneralId, serviceName, serviceDescription
        ) VALUES (?, ?, ?)
    ''', service_types_data)
    # Tabela SpecificService ========================================================================================
    specific_services_data = [
        (1, 1, 100.0, 1),  # dentistId, officeId, price, serviceTypeGeneralId
        (2, 2, 150.0, 2),
        (1, 3, 120.0, 1),
        # Dodaj więcej przykładowych danych według potrzeb
    ]
    cursor.executemany('''
        INSERT INTO SpecificService (
            dentistId, officeId, price, serviceTypeGeneralId
        ) VALUES (?, ?, ?, ?)
    ''', specific_services_data)
    # Tabela Reservation ========================================================================================
    reservations_data = [
        (150.0, 1, 'Brak uwag', '10-01-2024', 'Potwierdzone', 1, 2),
        (200.0, 2, 'Proszę o wcześniejsze potwierdzenie', '15-02-2024', 'Oczekujące', 2, 3),
        (120.0, 3, 'Zniżka studencka', '20-03-2024', 'Anulowane', 3, 1),
    ]
    cursor.executemany('''
        INSERT INTO Reservation (
            finalPrice, discountId, otherComments, reservationDate,
            reservationStatus, SpecificServiceId, userId
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', reservations_data)


    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()