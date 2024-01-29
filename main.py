class Player:
    def __init__(self, name):
        self.name = name


class Board:
    def __init__(self, n, m):
        self.n = n
        self.m = m


class Game:
    winner = ""

    def __init__(self, player, board):
        self.board = board
        self.player = player

    # def next_turn(self):


class Menu:
    welcome = ("Welcome to Tic Tac Toe \nTo start a new game with the computer enter 'New Game' \nTo review "
               "the history of the previous games enter 'History' \nTo quit the game enter 'Quit' \n")

    def __init__(self):
        self.message = Menu.welcome
        self.query = ""

    def run(self):
        self.query = input(self.message)

        if self.query == 'New Game':
            name = input("Enter your name in a single line: ")
            player = Player(name)
            board = Board(3, 3)
            game = Game(player, board)

            return game

        elif self.query == 'History':
            history = open("history.txt")
            data = ""

            line = history.readline()
            while line:
                line = history.readline()
                data = line + "\n"

            print(data)
            query = input('To go back to the main menu enter "Menu"\n')
            while query != 'Menu':
                query = input('Invalid input! Try again\n')

            self.message = Menu.welcome
            self.run()

        elif self.query == 'Quit':
            return None

        else:
            self.message = 'Invalid input! Try again\n'
            self.run()


menu = Menu()
new_game = menu.run()

if new_game is None:
    exit(0)

# rest of the code goes here
