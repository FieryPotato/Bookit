from Bookit.Controller import Controller
from Bookit.Model import Model
from Bookit.View import View


def main():
    app = Controller(Model(), View()).start()
    app.mainloop()


if __name__ == '__main__':
    main()
