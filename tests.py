#!/bin/python3
import os
from glob import glob

from dreamwork import parser, testhelpers
from dreamwork import document
from dreamwork import tangler



os.chdir(os.path.dirname(os.path.abspath(__file__)))
inputfiles = glob(os.path.join("tests","inputs","*"))

for filename in inputfiles:
    print("="*40)
    print("Parsing",filename)

    parser_obj = parser.MultipassParser()
    parser_obj.visitor = testhelpers.ReducingVisitor(parser_obj)
    stmts = parser_obj.parse_file(filename)
    for stmt in stmts:
        print(repr(stmt))


for filename in inputfiles:
    print("="*40)
    print("Creating a document using", filename)
    doc = document.Document(parser.MultipassParser)

    doc.append_from_file(filename)

    for chunk in doc.chunks:
        print(repr(chunk))

    for name, pieces in doc.definitions.items():
        print("Definition", name)
        for piece in pieces:
            print("\t",piece)

    t = tangler.Tangler('/dev/null')
    t.tangle(doc)