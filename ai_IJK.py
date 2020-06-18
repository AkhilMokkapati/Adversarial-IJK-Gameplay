#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Authors: PLEASE ENTER YOUR NAMES AND USER ID'S HERE

Based on skeleton code by Abhilash Kuhikar, October 2019
"""

from logic_IJK import Game_IJK
import copy
import random
import math

# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game
#
# This function should analyze the current state of the game and determine the
# best move for the current player. It should then call "yield" on that move.


def fun(k):
    return math.ceil(math.log2(pow(2, k + 1) + pow(2, 2 * k)))


def heuristic(initial_player, board):
    board_T = copy.deepcopy(board)
    board_TT = list(map(list, zip(*board_T)))
    upper = sum([pow(2, fun(ord(char) - ord("@"))) for row in board for char in row if char.isupper()])
    lower = sum([pow(2, fun(ord(char) - ord("`"))) for row in board for char in row if char.islower()])

    upper_add = sum([pow(4, fun(ord(row[x].upper()) - ord("@"))) for row in board for x in range(len(row) - 1) if
                     row[x] == row[x + 1] and row[x] != ' ' and row[x].isupper()])
    lower_add = sum([pow(4, fun(ord(row[x].upper()) - ord("@"))) for row in board for x in range(len(row) - 1) if
                     row[x] == row[x + 1] and row[x] != ' ' and row[x].islower()])

    upper_add_T = sum([pow(4, fun(ord(row[x].upper()) - ord("@"))) for row in board_TT for x in range(len(row) - 1) if
                       row[x] == row[x + 1] and row[x] != ' ' and row[x].isupper()])
    lower_add_T = sum([pow(4, fun(ord(row[x].upper()) - ord("@"))) for row in board_TT for x in range(len(row) - 1) if
                       row[x] == row[x + 1] and row[x] != ' ' and row[x].islower()])

    if initial_player == 1:
        return upper + upper_add - lower - lower_add + upper_add_T - lower_add_T
    else:
        return -1 * (upper + upper_add - lower - lower_add + upper_add_T - lower_add_T)

# def heuristic(board, dete_flag):
#     if dete_flag:
#         upper = sum([abs(ord(char)-ord("K")) for row in board for char in row if char.isupper()])
#         lower = sum([abs(ord(char)-ord("k")) for row in board for char in row if char.islower()])
#         empty_tiles = sum([1 for row in board for char in row if char == ' '])
#         # evaluation_score = (mins - maxs)* empty_tiles
#         evaluation_score = ((upper - lower)*empty_tiles)
#     else:
#         upper = sum([abs(ord(char) - ord("K")) for row in board for char in row if char.isupper()])
#         lower = sum([abs(ord(char) - ord("k")) for row in board for char in row if char.islower()])
#         empty_tiles = sum([1 for row in board for char in row if char == ' '])
#         evaluation_score = -((upper - lower) * empty_tiles)
#     return evaluation_score


def minmax(depth, game, alpha, beta, initialPlayer):
    max_values = []
    min_values = []

    if depth >= 6:
        return heuristic(initialPlayer, game.getGame())

    if getCurrentPlayer(game)*initialPlayer == 1:
        moves = ['U', 'D', 'L', 'R']
        for move in moves:
            successor = copy.deepcopy(game)
            successor.makeMove(move)
            score = minmax(depth + 1, successor, alpha, beta, initialPlayer)
            max_values.append(score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return max(max_values)

    else:
        moves = ['U', 'D', 'L', 'R']
        for move in moves:
            successor = copy.deepcopy(game)
            successor.makeMove(move)
            score = minmax(depth + 1, successor, alpha, beta, initialPlayer)
            min_values.append(score)
            beta = min(beta, score)
            if alpha >= beta:
                break
        return min(min_values)


def getBestMove(game, initialPlayer):
    max_score = float('-inf')
    final_move = ""

    moves = ['U', 'D', 'L', 'R']
    for move in moves:
        if initialPlayer == 1:
            successor = Game_IJK(game.getGame(), "+", game.getDeterministic())
            successor.makeMove(move)
            score = minmax(1, successor, float('-inf'), float('inf'), initialPlayer)
            if score > max_score:
                max_score = score
                final_move = move
        else:
            successor = Game_IJK(game.getGame(), "-", game.getDeterministic())
            successor.makeMove(move)
            score = minmax(1, successor, float('-inf'), float('inf'), initialPlayer)
            if score > max_score:
                max_score = score
                final_move = move
    return final_move


def calculateNumberOfEmptyTiles(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ' ':
                count = count + 1
    return count


def minmax_nondet(depth, game, alpha, beta, initialPlayer):
    max_values = []
    min_values = [float('inf')]
    avg_values = []

    if depth >= 3:
        return heuristic(initialPlayer, game.getGame())

    if depth % 2 == 1:
        # Chance node
        moves = ['U', 'D', 'L', 'R']
        for move in moves:
            successor = copy.deepcopy(game)
            successor.makeMove(move)
            emptyTiles = calculateNumberOfEmptyTiles(successor.getGame())
            # The new variable is still not added here
            score = minmax_nondet(depth + 1, successor, alpha, beta, initialPlayer)
            if emptyTiles != 0:
                avg_values.append(score/emptyTiles)
        return sum(avg_values)
    elif getCurrentPlayer(game)*initialPlayer != 1:
        # Max node
        board = game.getGame()
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == ' ':
                    successor = copy.deepcopy(game)
                    successor.add_piece((i, j))
                    score = minmax_nondet(depth + 1, successor, alpha, beta, initialPlayer)
                    max_values.append(score)
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
        return max(max_values)
    else:
        # Min node
        board = game.getGame()
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == ' ':
                    successor = copy.deepcopy(game)
                    successor.add_piece((i, j))
                    score = minmax_nondet(depth + 1, successor, alpha, beta, initialPlayer)
                    min_values.append(score)
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
        return min(min_values)


def getBestMoveForNonDet(game, initialPlayer):
    max_score = float('-inf')
    final_move = ""

    moves = ['U', 'D', 'L', 'R']
    for move in moves:
        if initialPlayer == 1:
            successor = Game_IJK_Own(game.getGame(), "+", game.getDeterministic())
            successor.makeMove(move)
            score = minmax_nondet(1, successor, float('-inf'), float('inf'), initialPlayer)
            if score > max_score:
                max_score = score
                final_move = move
        else:
            successor = Game_IJK_Own(game.getGame(), "-", game.getDeterministic())
            successor.makeMove(move)
            score = minmax_nondet(1, successor, float('-inf'), float('inf'), initialPlayer)
            if score > max_score:
                max_score = score
                final_move = move
    return final_move


def next_move(game: Game_IJK)-> None:

    '''board: list of list of strings -> current state of the game
       current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''

    deterministic = game.getDeterministic()
    initialPlayer = getCurrentPlayer(game)

    if deterministic:
        return getBestMove(game, initialPlayer)
    else:
        return getBestMoveForNonDet(game, initialPlayer)


def getCurrentPlayer(game):
    return +1 if (game.getCurrentPlayer() == '+') else -1


class Game_IJK_Own:
    def __init__(self, game, currentPlayer, deterministic):
        self.__game = game
        self.__current_player = +1 if currentPlayer == '+' else -1
        self.__previous_game = self.__game
        self.__new_piece_loc = (0, 0)
        self.__deterministic = deterministic

    def __switch(self):
        self.__current_player = -self.__current_player

    def isGameFull(self):
        for i in range(len(self.__game)):
            for j in range(len(self.__game[0])):
                if self.__game[i][j] == ' ':
                    return False
        return True

    def __game_state(self, mat):
        highest = {'+': 'A', '-': 'a'}

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if (mat[i][j]).isupper():
                    highest['+'] = chr(max(ord(mat[i][j]), ord(highest['+'])))
                if (mat[i][j]).islower():
                    highest['-'] = chr(max(ord(mat[i][j]), ord(highest['-'])))

        if highest['+'] == 'K' or highest['-'] == 'k' or self.isGameFull():
            if highest['+'].lower() != highest['-']:
                return highest['+'] if highest['+'].lower() > highest['-'] else highest['-']
            return 'Tie'

        return 0

    def __reverse(self, mat):
        new = []
        for i in range(len(mat)):
            new.append([])
            for j in range(len(mat[0])):
                new[i].append(mat[i][len(mat[0]) - j - 1])
        return new

    def __transpose(self, mat):
        new = []
        for i in range(len(mat[0])):
            new.append([])
            for j in range(len(mat)):
                new[i].append(mat[j][i])
        return new

    def __cover_up(self, mat):
        new = [[' ' for _ in range(len(self.__game))] for _ in range(len(self.__game))]

        done = False
        for i in range(len(self.__game)):
            count = 0
            for j in range(len(self.__game)):
                if mat[i][j] != ' ':
                    new[i][count] = mat[i][j]
                    if j != count:
                        done = True
                    count += 1
        return (new, done)

    def __merge(self, mat):
        global current_player

        done = False
        for i in range(len(self.__game)):
            for j in range(len(self.__game) - 1):
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != ' ':
                    mat[i][j] = chr(ord(mat[i][j]) + 1)
                    mat[i][j + 1] = ' '
                    done = True
                elif mat[i][j].upper() == mat[i][j + 1].upper() and mat[i][j] != ' ':
                    mat[i][j] = chr(ord(mat[i][j]) + 1)
                    mat[i][j] = mat[i][j].upper() if self.__current_player > 0 else mat[i][j].lower()
                    mat[i][j + 1] = ' '
                    done = True
        return (mat, done)

    def __up(self, game):
        # print("up")
        # return matrix after shifting up
        game = self.__transpose(game)
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__transpose(game)
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __down(self, game):
        # print("down")
        game = self.__reverse(self.__transpose(game))
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__transpose(self.__reverse(game))
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __left(self, game):
        # print("left")
        # return matrix after shifting left
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __right(self, game):
        # print("right")
        # return matrix after shifting right
        game = self.__reverse(game)
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__reverse(game)
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __skip(self):
        x, y = self.__new_piece_loc
        self.__game[x][y] = self.__game[x][y].swapcase()

    '''
    Expose this method to client to print the current state of the board
    '''

    def printGame(self):
        str_game = [['______' for _ in range(len(self.__game))] for _ in range(len(self.__game))]

        for i in range(len(self.__game)):
            for j in range(len(self.__game)):
                str_game[i][j] = "_" + self.__game[i][j] + "_"

        for i in range(len(self.__game)):
            print("|".join(str_game[i]))
        print("\n")

    def add_piece(self, r):
        self.__game[r[0]][r[1]] = 'A' if self.__current_player > 0 else 'a'
        self.__new_piece_loc = r

    def makeMove(self, move):
        self.__previous_game = self.__game
        if move == 'L':
            self.__left(self.__game)
        if move == 'R':
            self.__right(self.__game)
        if move == 'D':
            self.__down(self.__game)
        if move == 'U':
            self.__up(self.__game)

        '''
        Switch player after the move is done
        '''
        self.__switch()
        # self.__add_piece()

        return copy.deepcopy(self)

    def getDeterministic(self):
        return self.__deterministic

    def getGame(self):
        return copy.deepcopy(self.__game)

    '''player who will make the next move'''

    def getCurrentPlayer(self):
        return '+' if self.__current_player > 0 else '-'

    ''' '+' : '+' has won
       '-1' : '-' has won
       '' : Game is still on
    '''

    def state(self):
        return self.__game_state(self.__game)

