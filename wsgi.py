from deadWeb.dead import APP
from config import main

if __name__ == "__main__":
    APP.run(debug=main.DEBUG, host=main.HOST, port=main.PORT)
