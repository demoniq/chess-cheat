#!/usr/bin/python

# Chess PGN notation converter v.0.1
# Converts short PGN notation to long PGN and FEN
#
# This file is part of the python-chess library.
# Copyright (C) 2015 Paulius Dapkus <pauliusdapkus@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# USAGE:
#        need to pass the (short PGN file), (RAM quantity) and (thread nr)
#        Example: [ ./PGNtoFEN.py short_pgn_file 512 4]
# OOUTPUT:
#        script generates two notation dumps (long PGN and FEN)

import chess
import re
import sys
import os
import subprocess, time

notationFile = sys.argv[1]
RAMQuan = sys.argv[2]
threadNr = sys.argv[3]
engDepth = sys.argv[4]
print "Using notation file: "+notationFile
print "Using RAM :"+RAMQuan
print "Using threads :"+threadNr
print "Using depth :"+engDepth

dump_baseDir = "notationDump/"
if not os.path.exists(dump_baseDir):
    os.makedirs(dump_baseDir)

l_PGN_filename = "long_PGN.dump"
FEN_filename = "FEN.dump"
l_PGN_dump = open(dump_baseDir + l_PGN_filename,'w')
FEN_dump = open(dump_baseDir + FEN_filename,'w')

board = chess.Bitboard()

def insert_newline(string, index):
    return string[:index] + '\n' + string[index:]

#with open(sys.argv[1], "r") as ins:
with open(notationFile, "r") as ins:
    array = []
    for line in ins:
        array.append(line)

str = ""
strF = ""
for x in range(0, array.__len__()):
    str = array[x].split(".")[1] # Removing characters before "."

    first = re.search("\d", str) # Search for digit

    print str.__len__()
    if str.__len__() > 4:
        if str[4] == "O" and True is not str[1].isdigit():
            if str[3].isdigit():
                if first:
                    if str[first.start()+1] == "+":
                        strF = insert_newline(str, first.start()+2) # inserting "\n" after "+" (this is for cheks)
                    else:
                        strF = insert_newline(str, first.start()+1) # inserting "\n" after digit
            else:
                strF = insert_newline(str, 5) # inserting "\n" after digit
        elif str[2] == "O":
            strF = insert_newline(str, 2)
        else:
            if first:
                if str[first.start()+1] == "+":
                    strF = insert_newline(str, first.start()+2) # inserting "\n" after "+" (this is for cheks)
                else:
                    strF = insert_newline(str, first.start()+1) # inserting "\n" after digit
        l_PGN_dump.write(strF)
    else:

        if False is not str[1].isdigit() and False is not str[3].isdigit():
            strF = insert_newline(str, 2)
        else:
            l_PGN_dump.write(str)

        l_PGN_dump.write(strF)



l_PGN_dump.close()
with open(dump_baseDir + l_PGN_filename, "r") as ia:
    for li in ia:
        #print li.strip()
        if li != '\n':
            board.push_san(li.strip())


# Generated FEN
print "\033[93m * Translated short PGN to long PGN and FEN notation\033[0m"
print "\033[93m * All translations exists in [notationDump] dir\033[0m"
print '\033[92m'+board.fen()+'\033[0m'
FEN_dump.write(board.fen()+"\n")




##############################################################################
# StockFish
engine = subprocess.Popen(
    'stockfish',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

def put(command):
    print('\nyou:\n\t'+command)
    engine.stdin.write(command+'\n')

def get():
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    engine.stdin.write('isready\n')
    print('\nengine:')
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
         #  print "readyOK"
            break
        if text !='':
            print('\t'+text)



get()
put('position fen '+board.fen())
get()
put('setoption name Hash value '+RAMQuan)
get()
put('setoption name Threads value '+threadNr)
#get()
#put('go depth 20')
get()
put('go infinite')
time.sleep(int(engDepth)) # sleeping some time (engine depth)
get()
put('stop')
get()
put('quit')

#position fen r3k2r/2p2ppp/p1pbbn2/3pB3/3P4/2N2P2/PPP1N1PP/R3K2R b KQkq - 0 12
