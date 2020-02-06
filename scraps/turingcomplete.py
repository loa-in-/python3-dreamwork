#!/bin/python2

import arpeggio
from arpeggio import ParserPython
from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, And, Not, UnorderedGroup, Sequence
from arpeggio import RegExMatch as _
from arpeggio import StrMatch as literal

from functools import partial
import re

__ = partial(_, multiline=True, re_flags=re.DOTALL+re.MULTILINE)

def until_block_maybe(): return __(r'.*?(?=>)'), And(literal('>'))
def skip_to_end_of_file(): return __(r'.+'), And(EOF)
def identifier(): return _(r'[\w\s]+')
def ws(): return _(r'\s*')
def anyws(): return __(r'[\s\r\n]*')

def block_start(): return literal('>->'), identifier, literal('<'), [literal('+'), literal('-')]
def block_tabular():  return literal('<'), ws
def block_interior(): return __('.+?(?=<<<)')
def block_end(): return literal('<<<')

def block_freeform(): return literal('{'), ZeroOrMore((ws,literal('<-{'))), 
def block_freeform_interior(): return __(r'.+?(?=}[\s\r\n]*<<<)')
def block_freeform_end(): return literal('}'), anyws, block_end

def ref_insert_start(): return literal('>'), And([literal('['), literal('{')])
def ref_insert_middle(): return [(literal('['), identifier, literal(']')),
                                    (literal('{'), identifier, literal('}'))], And(literal('<'))
def ref_insert_end(): return literal('<')

def grammar(): return OneOrMore(
            (Optional(until_block_maybe),
                [
                    (block_start, [(block_freeform, block_freeform_interior, block_freeform_end),
                                   (block_tabular, block_interior, block_end)])
                ,
                    (ref_insert_start, ref_insert_middle, ref_insert_end)
                ],
             anyws)
        )

parser = ParserPython(grammar(), skipws=False, debug=False)
text = open(r'/home/rne/LiterateProgramming/repos/arpeggiolib-dreamwork/turingtest.txt','r').read()
tree = parser.parse(text)

print(type(tree))

print("Tree spans {} top level nodes".format(len(tree)))
for branch in tree[:]:
    print(branch)
    print("="*40)
