from datetime import datetime

class DentistOffice:
    extent = []                                     #atrybut klasowy i jednocześnie ekstensja w ramach tej samej klasy

    def __init__(self, name, price, address, owner=None, residents=None):
        self.strDentistOfficeName = name
        self.price = price                                          #atrybut prosty
        self.address = address                                      #atrybut złożony
        self.owner = owner                                          #atrybut opcjonalny

        #residents jest atrybutem powtarzalnym i opcjonalnym
        if residents is None:
            self.residents = []                                     #tworzy pustą listę, jeśli nie przekazano rezydentów
        else:
            self.residents = residents                              #przypisuje przekazaną listę rezydentów
        self.add_DentistOffice(self)                                #dopisz utworzony gabinet do ekstensji klasy

    #przeciazenie metody presentOwnerResidents:
    def presentOwnerResidents(self, owner):
        print()

    def presentOwnerResidents(self, residents):
        print()

    def presentOwnerResidents(self, owner, residents):
        print()

    def __str__(self):                                          #przesloniecie metody __str__
        return f"Dentist office: {self.strDentistOfficeName}, id: {id(self)}"
    @classmethod
    def add_DentistOffice(cls, dentistOffice):                  #metoda klasowa dodająca gabinet do ekstensji klasy
        cls.extent.append(dentistOffice)

    @classmethod
    def remove_DentistOffice(cls, dentistOffice):
        cls.extent.remove(dentistOffice)

    @classmethod
    def show_extent(cls):                             #metoda klasowa prezentująca wszystkie gabinety z ekstensji klasy
        print(f"Extent of the class: {cls.__name__}")
        for dentistOffice in cls.extent:
            print(dentistOffice)

    def discounted_price(self):                                 #oblicza cenę po zniżce, poniżej dla 10%
        discount_percentage = 10
        discounted_price = self.price - (self.price * discount_percentage / 100)
        return discounted_price

class Address:  #klasa adres, wykorzystywana do utworzenia atrybutu złożonego
    def __init__(self, street, buildno, apartno, zipcode):
        self.strStreet = street
        self.intBuildNo = buildno
        self.intApartNo = apartno
        self.strZipCode = zipcode