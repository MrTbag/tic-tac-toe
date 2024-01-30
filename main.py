import random
import time


class Player:
    def __init__(self, name):
        self.name = name

    def update_history(self, winner):
        history = open("history.txt", "r")
        lines = history.readlines()

        is_new = True
        for i, line in enumerate(lines):
            tokens = line.split()
            if tokens[0] == self.name:
                is_new = False
                index = i
                win_num = tokens[1].split(':')[1]
                loss_num = tokens[2].split(':')[1]
                lines.remove(line)
                if winner == self.name:
                    win_num += 1
                else:
                    loss_num += 1
                new_line = "{0}\twins:{1}\tlosses:{2}".format(self.name, win_num, loss_num)
                lines.insert(index, new_line)
                break

        history.close()

        if not is_new:
            history = open("history.txt", "w")
            history.writelines(lines)
        else:
            history = open("history.txt", "w+")
            if winner == self.name:
                history.write("{0}\twins:{1}\tlosses:{2}".format(self.name, 1, 0))
            else:
                history.write("{0}\twins:{1}\tlosses:{2}".format(self.name, 0, 1))


class Board:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.loc = [['*' for i in range(n)] for j in range(m)]

    def print_board(self):
        for i in range(self.n):
            for j in range(self.m):
                print(self.loc[j][i], end=" ")
            print()

    @staticmethod
    def next_diagonal(point, mode, direction):
        step = [(1, 1), (1, -1)]
        x = (point[0] + step[mode][0] * direction)
        y = (point[1] + step[mode][1] * direction)

        return x, y

    def is_point_valid(self, point):
        return (0 <= point[0] < self.m) and (0 <= point[1] < self.n)


class Game:
    character = ['X', 'O']
    player_name = ['Computer', '']

    def __init__(self, player, board):
        self.board = board
        self.player = player
        self.player_name[1] = player.name
        self.turn = 0
        self.winner = ""

    def start(self):
        self.board.print_board()

        while self.winner == "":
            self.next_turn()

        self.player.update_history(self.winner)

        query = input("Enter 'Return' to return to the main menu:\n")
        while query != "Return":
            query = input("Invalid input! Try again:\n")

        return

    def next_turn(self):
        self.turn ^= 1
        if self.turn:
            print("What's your move? Choose x between 1 and {0} and y between 1 and {1}".format(self.board.m,
                                                                                                self.board.n))
            player_x = input("x = ")
            player_y = input("y = ")
            while (not player_x.isnumeric()) or (not player_y.isnumeric()):
                print("Enter integers only!")
                player_x = input("x = ")
                player_y = input("y = ")

            move = (int(player_x) - 1, int(player_y) - 1)
            while not self.board.is_point_valid(move):
                print("Invalid move! Try again:")
                player_x = int(input("x = "))
                player_y = int(input("y = "))
                move = (player_x - 1, player_y - 1)
        else:
            time.sleep(1)
            move = self.computer_move()

        self.board.loc[move[0]][move[1]] = self.character[self.turn]
        self.board.print_board()

        if self.check_winner(move):
            self.winner = self.player_name[self.turn]
            print("{0} Won!".format(self.winner))

        return

    def computer_move(self):
        x = random.randint(0, self.board.m - 1)
        y = random.randint(0, self.board.n - 1)
        while self.board.loc[x][y] != '*':
            x = random.randint(0, self.board.m - 1)
            y = random.randint(0, self.board.n - 1)

        self.board.loc[x][y] = 'X'

        return x, y

    def check_winner(self, move):

        # check row
        win1 = True
        for x in range(self.board.m):
            if self.board.loc[x][move[1]] != Game.character[self.turn]:
                win1 = False
                break

        # check column
        win2 = True
        for y in range(self.board.n):
            if self.board.loc[move[0]][y] != Game.character[self.turn]:
                win2 = False
                break

        # check diagonal mode 0
        # bottom-right
        valid3 = False
        win3 = True
        next_point = self.board.next_diagonal(move, 0, 1)
        while self.board.is_point_valid(next_point):
            valid3 = True
            if self.board.loc[next_point[0]][next_point[1]] != Game.character[self.turn]:
                win3 = False
                break
            next_point = self.board.next_diagonal(next_point, 0, 1)

        # top-left
        next_point = self.board.next_diagonal(move, 0, -1)
        while self.board.is_point_valid(next_point):
            valid3 = True
            if self.board.loc[next_point[0]][next_point[1]] != Game.character[self.turn]:
                win3 = False
                break
            next_point = self.board.next_diagonal(next_point, 0, -1)

        win3 = win3 and valid3

        # check diagonal mode 1
        # top-right
        valid4 = False
        win4 = True
        next_point = self.board.next_diagonal(move, 1, 1)
        while self.board.is_point_valid(next_point):
            valid4 = True
            if self.board.loc[next_point[0]][next_point[1]] != Game.character[self.turn]:
                win4 = False
                break
            next_point = self.board.next_diagonal(next_point, 1, 1)

        # bottom-left
        next_point = self.board.next_diagonal(move, 1, -1)
        while self.board.is_point_valid(next_point):
            valid4 = True
            if self.board.loc[next_point[0]][next_point[1]] != Game.character[self.turn]:
                win4 = False
                break
            next_point = self.board.next_diagonal(next_point, 1, -1)

        win4 = win4 and valid4

        return win1 or win2 or win3 or win4


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
            game.start()
            

            self.run()

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
            exit(0)

        else:
            self.message = 'Invalid input! Try again\n'
            self.run()


menu = Menu()
menu.run()
