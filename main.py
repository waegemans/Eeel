import numpy as np
from colorama import Fore, Style
BOARD_SIZE = 9



class Game:
    def __init__(self):
        self.turn = 0
        self.player_position = np.zeros((2,BOARD_SIZE,BOARD_SIZE))

        self.player1_position[0,BOARD_SIZE//2] = 1
        self.player2_position[BOARD_SIZE-1,BOARD_SIZE//2] = 1

        self.walls_hoz = np.zeros((BOARD_SIZE-1,BOARD_SIZE))
        self.walls_vez = np.zeros((BOARD_SIZE,BOARD_SIZE-1))

        self.walls_remaining = np.ones(2)*10

    @property
    def player1_position(self):
        return self.player_position[0]

    @property
    def player2_position(self):
        return self.player_position[1]

    @player1_position.setter
    def player1_position(self,value):
        self.player_position[0] = value

    @player2_position.setter
    def player2_position(self,value):
        self.player_position[1] = value

    def at_edge(self,i,j):
        pass

    def at_position(self,i,j):
        retval = ''
        if self.player1_position[i,j]:
            return '1'
        if self.player2_position[i,j]:
            return '2'
        return ' '

    def print(self):
        outstring_lines = []
        for i in range(BOARD_SIZE):
            outstring_lines.append(
            list(' '+u' \u2551 '.join([str(self.at_position(i,j)) for j in range(BOARD_SIZE)]))
            )
            if i != BOARD_SIZE-1:
                outstring_lines.append(list(u'\u2550'*(3*BOARD_SIZE+BOARD_SIZE-1)))
                for j in range(3,len(outstring_lines[i]),4):
                    outstring_lines[-1][j] = ' '# u'\u256c'
        for i,hoz_line in enumerate(self.walls_hoz):
            for j, wall_hoz in enumerate(hoz_line):
                if (wall_hoz):
                    outstring_lines[i*2+1][j*4] = Fore.RED + outstring_lines[i*2+1][j*4]
                    outstring_lines[i*2+1][j*4+2] += Style.RESET_ALL
        for i,vez_line in enumerate(self.walls_vez):
            for j, wall_vez in enumerate(vez_line):
                if (wall_vez):
                    outstring_lines[i*2][j*4+3] = Fore.RED + outstring_lines[i*2][j*4+3] + Style.RESET_ALL

        outstring_lines = [[' '] + [f' {i} {i}' for i in range(BOARD_SIZE-1)]] + outstring_lines
        for i in range(BOARD_SIZE-1):
            outstring_lines[i*2+1][0] = chr(ord('a')+i) + outstring_lines[i*2+1][0]
            outstring_lines[i*2+2][0] = chr(ord('A')+i) + outstring_lines[i*2+2][0]

        outstring_lines[-1][0] = ' '+ outstring_lines[-1][0]
        print('\n'.join(map(lambda x: ''.join(x), outstring_lines)))
        print('Player1: ' + '|'*int(self.walls_remaining[0]))
        print('Player2: ' + '|'*int(self.walls_remaining[1]))
        print(f'Player{self.turn+1} ist am Zug')
    def next_player(self):
        self.turn +=1
        self.turn %=2

    def move(self, d, axis):
        self.player_position[self.turn] = np.roll(self.player_position[self.turn], d, axis)

    def move_up(self):
        self.move(-1,0)
    def move_down(self):
        self.move(1,0)

    def move_left(self):
        self.move(-1,1)
    def move_right(self):
        self.move(1,1)

    def place_wall(self,string):
        column,row = string
        x = ord(column.lower()) - ord('a')
        y = int(row)

        if column.islower():
            self.walls_vez[x:x+2,y] = 1
        else:
            self.walls_hoz[x,y:y+2] = 1

        self.walls_remaining[self.turn] -= 1

def game_loop():
    g = Game()
    while 1:
        g.print()
        a = input()
        if len(a) == 2:
            g.place_wall(a)
        if a == 'w':
            g.move_up()
        if a == 's':
            g.move_down()
        if a == 'a':
            g.move_left()
        if a == 'd':
            g.move_right()
        g.next_player()
        if a == 'r':
            g = Game()
        if a == 'q':
            break

def main():
    game_loop()

if __name__ == '__main__':
    main()
