from xml.etree.ElementTree import TreeBuilder
import keyboard
import random
import sys
import time

moves = {
    0 : lambda a, b : (a, b - 1),
    1 : lambda a, b : (a + 1, b),
    2 : lambda a, b : (a, b + 1),
    3 : lambda a, b : (a - 1, b)
    }

dirs = {
    'w' : 0,
    'd' : 1,
    's' : 2,
    'a' : 3
    }


class board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.lines = [ [' ']* (width + 2) for i in range((height + 2))]
        self.snek = snake(self)
        self.snack = (random.randrange(1, width - 1), random.randrange(1, height - 1))

        for x in range(len(self.lines)):
            self.lines[x][0] = '*'
            self.lines[x][-1] = '*'
            print('\n')
        self.lines[0] = '*' * (width + 2)
        self.lines[-1] = '*' * (width + 2)


    def clear(self):
        self.lines = [ [' ']* (self.width + 2) for i in range((self.height + 2))]
        for x in range(len(self.lines)):
            self.lines[x][0] = '*'
            self.lines[x][-1] = '*'

        self.lines[0] = '*' * (self.width + 2)
        self.lines[-1] = '*' * (self.width + 2)

    def getTile(self, x, y):
        return self.lines[y + 1][x + 1]

    def setTile(self, x, y, val):
        self.lines[y + 1][x + 1] = val

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def printBoard(self, clear = False):
        self.clear()

        for x in range(0, self.height + 2):
            sys.stdout.write('\x1b[1A') 

        for i in self.snek.getBody():
            x, y = i
            self.setTile(x, y, '▇')

        self.setTile(self.snack[0], self.snack[1], '◦')

        
        
        for y in self.lines:
            line = ''
            for x in y:
                line = line + x
            print(line)

    def setSnek(self, Snake):
        self.snek = Snake

    def getSnek(self):
        return self.snek

    def newSnack(self):
        x, y = random.randrange(1, self.width - 1), random.randrange(1, self.height - 1)
        while True:
            if (x,y) in self.snek.getBody():
                x, y = random.randrange(1, self.width - 1), random.randrange(1, self.height - 1)
                continue
            break
        self.snack = (x, y)

    def getSnack(self):
        return self.snack

class snake:
    def __init__(self, Board):
        self.Board = Board
        self.body = []
        self.direction = ''
        x = random.randrange(1, Board.getWidth() - 1)
        y = random.randrange(1, Board.getHeight() - 1)
        self.body.append((x,y))

        self.running = True


    def move(self, dir = 4):
        pos = self.head()
        if dir == 4:
            dir = self.direction
        self.direction = dir
        newpos = moves[dir](pos[0], pos[1])

        if newpos[0] == -1 or newpos[0] == (self.Board.getWidth() + 1) or newpos[1] == -1 or newpos[1] == (self.Board.getHeight() + 1):
            self.running = False

        self.body.append(newpos)

        if newpos == self.Board.getSnack():
            self.Board.newSnack()
        else:
            del self.body[0]

    def length(self):
        return len(self.body)

    def d(self):
        return self.direction

    def head(self):
        return self.body[-1]
    
    def getBody(self):
        return self.body

    def isRunning(self):
        return self.running


# game = board(20,10)

# game.printBoard()

# snek = snake(game)

# print(snek.getBody())

#         width           height
# t = [ [0]*4 for i in range(3)]w


def main():
    w, h = 15, 15
    game = board(w, h)
    s = 4
    game.printBoard()
    # snek = snake(game)
    while True:
        if keyboard.is_pressed('w'):
            s = 0
            break
        if keyboard.is_pressed('a'):
            s = 3
            break
        if keyboard.is_pressed('s'):
            s = 2
            break
        if keyboard.is_pressed('d'):
            s = 1
            break






    while game.getSnek().isRunning():
        if s != 4:
            game.getSnek().move(s)
            game.printBoard()
            s = 4
            continue

        t = round(time.time(), 1)
        skip = False
        while True:
            if round(time.time(), 1) == t + 1:
                m = game.getSnek().d()
                skip = True
                break
            if keyboard.is_pressed('w'):
                m = 0
                break
            if keyboard.is_pressed('a'):
                m = 3
                break
            if keyboard.is_pressed('s'):
                m = 2
                break
            if keyboard.is_pressed('d'):
                m = 1
                break
        if not skip:
            time.sleep((t + 1) - time.time())

        game.getSnek().move(m)
        game.printBoard()


        
    print('Game over')


main()
