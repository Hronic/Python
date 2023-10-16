# Press the green button in the gutter to run the script.
import Model

if __name__ == '__main__':
    #utworzenie obiektów adres na potrzeby atrybutów złożonych
    address1 = Model.Address("Aleje Jerozolimskie", 1, 10, "01-123")
    address2 = Model.Address("Woronicza", 2, 13, "04-123")
    address3 = Model.Address("Marszalkowska", 3, 16, "13-456")

    #utworzenie finalnych obiektów
    DentistOffice1 = Model.DentistOffice("Dentist office 1", 9.99, address1, "Mikolaj")
    DentistOffice2 = Model.DentistOffice("Dentist office 2", 14.99, address2, "Artur")
    DentistOffice3 = Model.DentistOffice("Dentist office 3", 19.99, address3, residents=["Rezydent_1", "Rezydent_2"])

    #Wyświetlenie całej ekstensji
    Model.DentistOffice.show_extent()

# todo Ekstensja - trwałość

