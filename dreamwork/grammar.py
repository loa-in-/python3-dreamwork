from functools import partial
import re

from arpeggio import ZeroOrMore, EOF, And
from arpeggio import RegExMatch as _
from arpeggio import StrMatch as literal



__ = partial(_, multiline=True, re_flags=re.DOTALL+re.MULTILINE)




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



def block_statement(): return (block_start, [
        (block_freeform, block_freeform_interior, block_freeform_end),
        (block_tabular, block_interior, block_end)
    ])

def ref_statement(): return (ref_insert_start, ref_insert_middle, ref_insert_end) 

def statement(): return [block_statement, ref_statement]


def until_block_maybe(): return __(r'.*?(?=>)'), And(literal('>'))

def freetext(): return until_block_maybe