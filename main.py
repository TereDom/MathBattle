from api import *
import api


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    main()
