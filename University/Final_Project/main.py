

from views import MainPage
import databaseAndSamples
import views

if __name__ == '__main__':
    databaseAndSamples.checkDatabaseStatus()
    #app = views.AddOpinion(1)

    app = MainPage()
    app.mainloop()
