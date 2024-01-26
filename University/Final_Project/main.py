

from views import MainPage
import controller

if __name__ == '__main__':
    controller.checkDatabaseStatus()
    app = MainPage()
    app.mainloop()
