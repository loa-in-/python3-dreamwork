#!/bin/python3
import arpeggio
from arpeggio import ParserPython

from dreamwork import parser

filename = r'/home/rne/LiterateProgramming/repos/arpeggiolib-dreamwork/turingtest.txt'

parser = parser.MultipassParser()
stmts = parser.parse_file(filename)
for stmt in stmts:
    print(repr(stmt))
