from controller import Controller
from view import View

# Старт программы
if __name__ == '__main__':
    controller = Controller()
    app = View(controller)
    app.run()
