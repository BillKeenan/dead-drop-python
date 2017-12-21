from deadWeb.dead import app
from config import main

if __name__ == "__main__":
    app.run(debug=main.DEBUG,host= main.HOST,port=main.PORT)
