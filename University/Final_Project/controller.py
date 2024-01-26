import sqlite3
import os
import models

#Do przeglądania bazy danych: https://inloop.github.io/sqlite-viewer/

DATABASE_NAME = "PorownywarkaStomatologiczna.db"

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
    #Utwórz tabelę User
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            userId INTEGER PRIMARY KEY,
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
            RoleDicId INTEGER PRIMARY KEY,
            RoleName TEXT
        )
    ''')
    #Utwórz tabelę Admin
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            userId INTEGER PRIMARY KEY,
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
    #Utwórz tabelę Dentist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dentist (
            doctorId INTEGER PRIMARY KEY,
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

    # Wprowadź zmiany, zakończ połączenie
    conn.commit()
    conn.close()

def createSampleData():             #Zapełnienie bazy danych przykłądowymi danymi
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    #Tabela User ========================================================================================
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

    #Tabela RoleDic ========================================================================================
    roles_data = [
        ('Administrator',),
        ('Pracownik',),
        ('Klient',),
    ]
    cursor.executemany('INSERT INTO RoleDic (RoleName) VALUES (?)', roles_data)

    #Tabela Admin ========================================================================================
    admins_data = [
        ('John', 'Doe', '12345678901', 'john.doe@email.com', 0, 'john_doe', 'password123', '123456789', 1),
        ('Alice', 'Smith', '98765432101', 'alice.smith@email.com', 1, 'alice_smith', 'pass123', '987654321', 2),
        ('Bob', 'Johnson', '11122334455', 'bob.johnson@email.com', 0, 'bob_johnson', 'secret123', '111223344', 1),
        ('Eva', 'Williams', '55566778899', 'eva.williams@email.com', 1, 'eva_williams', 'topsecret123', '555667788', 2),
        ('Michael', 'Davis', '99900011122', 'michael.davis@email.com', 0, 'michael_davis', 'adminpass', '999000111', 1),
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


    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()