from api import *
import api


def main():
    app.run()


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    main()