from abc import ABC

class PersonalData(ABC):
    def __init__(self, name, surname, pesel, email):
        self.name = name
        self.surname = surname
        self.pesel = pesel
        self.email = email

class User(PersonalData):
    def __init__(self, name, surname, pesel, email, isBlocked, login, password, userId):
        super().__init__(name, surname, pesel, email)
        self.isBlocked = isBlocked
        self.login = login
        self.password = password
        self.userId = userId

    def getMyOpinions(self):
        return None

    def getMyReservations(self):
        return None

class Admin(User):
    def __init__(self, name, surname, pesel, email, isBlocked, login, password, userId, phoneNumber, roleDicId):
        super().__init__(name, surname, pesel, email, isBlocked, login, password, userId)
        self.phoneNumber = phoneNumber
        self.roleDicId = roleDicId

class RoleDic():
    def __init__(self, roleDicId, roleName):
        self.roleDicId = roleDicId
        self.roleName = roleName

class DoctorGeneral(ABC):
    def __init__(self, activeAccount, doctorId, email, login, password, name, surname, phone):
        self.activeAccount = activeAccount
        self.doctorId = doctorId
        self.email = email
        self.login = login
        self.name = name
        self.surname = surname
        self.password = password
        self.phone = phone

class Dentist(DoctorGeneral):
    def __init__(self, activeAccount, doctorId, email, login, password, name, surname, phone, isDentalProsthetics, isDentalSurgery, isOrthodontics, isPediatricDentist, licenseNumber):
        super().__init__(activeAccount, doctorId, email, login, password, name, surname, phone)
        self.isDentalProsthetics = isDentalProsthetics
        self.isDentalSurgery = isDentalSurgery
        self.isOrthodontics = isOrthodontics
        self.isPediatricDentist = isPediatricDentist
        self.licenseNumber = licenseNumber

class Opinion():
    def __init__(self, opinionId, userId, opinionTypeDicId, reviewedEntryId, creationDate, opinionValue, stars):
        self.opinionId = opinionId
        self.userId = userId
        self.opinionTypeDicId = opinionTypeDicId
        self.reviewedEntryId = reviewedEntryId
        self.creationDate = creationDate
        self.opinionValue = opinionValue
        self.stars = stars

    def getForeignEntityId(self):
        return None

    def getOpinionType(self):
        return None

    def getOpinionValue(self):
        return None

class OpinionTypeDic():
    def __init__(self, opinionTypeDicId, opinionTypeName):
        self.opinionTypeDicId = opinionTypeDicId
        self.opinionTypeName = opinionTypeName

class ServiceTypeGeneral():
    def __init__(self, serviceTypeGeneralId, serviceName, serviceDescription):
        self.serviceTypeGeneralId = serviceTypeGeneralId
        self.serviceName = serviceName
        self.serviceDescription = serviceDescription

class Office():
    def __init__(self, officeId, cityDicId, countryDicId, address, isActive, isNFZAvailable, officeName, postCode, webPageAddress):
        self.officeId = officeId
        self.address = address
        self.cityDicId = cityDicId
        self.countryDicId = countryDicId
        self.isActive = isActive
        self.isNFZAvailable = isNFZAvailable
        self.officeName = officeName
        self.postCode = postCode
        self.webPageAddress = webPageAddress

class CityDic():
    def __init__(self, cityDicId, cityName):
        self.cityDicId = cityDicId
        self.cityName = cityName

class CountryDic():
    def __init__(self, countryDicId, countryName):
        self.countryDicId = countryDicId
        self.countryName = countryName

class Discount():
    def __init__(self, officeId, discountId, discountCode, discountValue, isActive, isValue):
        self.officeId = officeId
        self.discountId = discountId
        self.discountCode = discountCode
        self.discountValue = discountValue
        self.isActive = isActive
        self.isValue = isValue

    def deactivate(self):
        self.isActive = False

class Calendar():
    def __init__(self, calendarId, description, excludedDate):
        self.calendarId = calendarId
        self.description = description
        self.excludedDate = excludedDate

class Reservation():
    def __init__(self, finalPrice, discountId, otherComments, reservationDate, reservationId, reservationStatus, SpecificServiceId, userId):
        self.finalPrice = finalPrice
        self.discountId = discountId
        self.otherComments = otherComments
        self.reservationDate = reservationDate
        self.reservationId = reservationId
        self.reservationStatus = reservationStatus
        self.SpecificServiceId = SpecificServiceId
        self.userId = userId

    def cancel(self):
        self.reservationStatus = False

class SpecificService():
    def __init__(self, dentistId, officeId, price, serviceTypeGeneralId, specificServiceId):
        self.dentistId = dentistId
        self.officeId = officeId
        self.price = price
        self.serviceTypeGeneralId = serviceTypeGeneralId
        self.specificServiceId = specificServiceId

    def setPrice(self, newPrice):
        self.price = newPrice