

from views import MainPage
import databaseAndSamples
import views

if __name__ == '__main__':
    databaseAndSamples.checkDatabaseStatus()
    #app = views.MakeReservation(1)  #TEST
    app = MainPage()
    app.mainloop()
