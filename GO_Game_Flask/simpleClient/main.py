import requests
import json

turn = 2


def createGame(nick):
    response = requests.get('http://127.0.0.1:5000/create/' + nick)
    data = response.text
    return json.loads(data)['gameId']


def joinGame(nick):
    response = requests.get('http://127.0.0.1:5000/join/' + nick)
    data = response.text
    return json.loads(data)['gameId']


def getBoard(gameID):
    response = requests.get('http://127.0.0.1:5000/board/' + str(gameID))
    data = response.text
    print(json.loads(data)['board'])


def getPoints(gameID):
    response = requests.get('http://127.0.0.1:5000/points/' + str(gameID))
    data = response.text
    print(json.loads(data)['points'])


def insert(gameID):
    x = input("x:\n")
    y = input("y:\n")
    response = requests.get('http://127.0.0.1:5000/cords/' + x + ',' + y + ',' + str(gameID))
    data = response.text
    print(json.loads(data)['response'])


def leave(gameID):
    response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
    data = response.text
    print(json.loads(data)['remove'])


def getPlayers(gameID):
    response = requests.get('http://127.0.0.1:5000/players/' + str(gameID))
    data = response.text
    print("Players: " + json.loads(data)['player1'] + ", " + json.loads(data)['player2'])


def mainMenu():
    nick = ""
    while nick == "":
        nick = input("Insert nick\n")
    while True:
        choice = int(input("1.New game\n2.Join\n3.Load\n4.Exit\n"))
        if choice == 1:
            gameID = createGame(nick)
            inGameMenu(gameID, 2)

        elif choice == 2:
            gameID = joinGame(nick)
            if gameID == -1:
                print("No free games")
            else:
                inGameMenu(gameID, 1)

        elif choice == 3:
            file = open("data.txt", "r")
            text = ""
            for s in file:
                text += s
            gameID = createGame(nick)
            requests.get('http://127.0.0.1:5000/load/' + str(gameID) + "/" + text)
            inGameMenu(gameID, 2)

        elif choice == 4:
            break


def inGameMenu(gameID, color):
    while True:
        getPlayers(gameID)
        response = requests.get('http://127.0.0.1:5000/onGoing/' + str(gameID))
        data = response.text
        if json.loads(data)['onGoing'] == 0:
            leave(gameID)
            break
        response = requests.get('http://127.0.0.1:5000/checkT/' + str(gameID))
        data = response.text
        if int(json.loads(data)['turn']) == 1:
            print("White player turn")
        else:
            print("Black player turn")
        if int(json.loads(data)['turn']) == color:
            getBoard(gameID)
            getPoints(gameID)
            choice = int(input("1.Insert\n2.Pass\n3.Surrender\n"))
            if choice == 1:
                insert(gameID)
            elif choice == 2:
                response = requests.get('http://127.0.0.1:5000/pass/' + str(gameID))
                data = response.text
                if int(json.loads(data)['passCounter']) == 2:
                    break
            elif choice == 3:
                leave(gameID)
                break
            getBoard(gameID)
            getPoints(gameID)
        else:
            choice = int(input("1.Refresh\n2.Surrender\n"))
            if choice == 1:
                print("Checking...")
            elif choice == 2:
                leave(gameID)
                break


if __name__ == '__main__':
    mainMenu()
