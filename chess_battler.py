import pexpect
import re
move_log = open('move_log.txt','w')

"""
This module uses the pexpect library to simulate a chess mach between two 
instances of gnuchess and records the game in a log file named move_log.txt, 
which is created in the current directory. 
"""


class Player:
    
    """
    This class spawns an instance of gnuchess and plays as color color against the 
    computer. It also creates a logfile of this players moves in the file named 
    log_file_name.txt. 

    engine -- gnuchess (maybe will change when other engines are added)
    color -- the player's color
    log_file_name -- the player's log file location
    """

    def __init__(self, engine = 'gnuchess', color, log_file_name):
        self.engine = engine
        self.game = pexpect.spawn(str(engine))
        self.color = str(color)
        self.logfile = open(str(log_file_name) + str(color) + '.txt', 'w+')
        self.game.logfile = self.logfile
        self.log_name = str(log_file_name) + str(color) + '.txt'
    last_move = ' '
    has_drawn = False
    has_turn = True
        

    def start(self): 
    """ stars the game """
        if self.color == 'White':
            pass
        else:
            self.game.sendline('go')
            
            self.has_turn = False

    def make_move(self,move):
    """ makes the move specified by input move in chess notation. """
        self.game.sendline(str(move))

    def is_winner(self):
    """ checks to see if the game is over and who won. """
        if self.last_move[-1] == '#' or self.has_drawn:
            return True
        else: 
            return False 

def do_next_move(just_moved, is_moving):
    """
    This method takes the move that is_moving needs to make from just_moved's
    log file then makes it and records it in the log file. 
    """
    just_moved.game.expect('My move is')
    temp_file = open(just_moved.log_name, 'r')
    temp_log_list = reversed(list(temp_file))
    log_string = ''.join(list(temp_log_list))
    if "{draw}" in log_string:
        just_moved.has_drawn = True
        is_moving.has_drawn = True
    start_index = log_string.find("My move")
    end_index = log_string.find("\r", start_index)
    move = log_string[start_index:end_index].split(': ')[1]
    is_moving.game.sendline(move)
    is_moving.last_move = move

""" the rest of this module simulates the game and prints the winner. """

white_player = Player('gnuchess','White','w')
black_player = Player('gnuchess','Black','b')


black_player.start()

while not white_player.is_winner() and not black_player.is_winner():
    if white_player.has_turn:
        do_next_move(black_player,white_player)
        move_log.write("W:" + white_player.last_move + "\n")
        white_player.has_turn = False
        black_player.has_turn = True
    elif black_player.has_turn:
        do_next_move(white_player,black_player)
        move_log.write("B:" + black_player.last_move + "\n")
        white_player.has_turn = True
        black_player.has_turn = False

if white_player.is_winner:
    print "White wins!"
elif black_player.is_winner:
    print "Black wins!"
else:
    print "It's a draw!"


    



         
    



