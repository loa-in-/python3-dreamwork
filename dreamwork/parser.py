#!/bin/python3
from functools import partial

import arpeggio
from arpeggio import ParserPython

from . import grammar
from . import document

class AParser:        
    def parse_file(self, filename):
        self.text = open(filename,'r').read()
        return self.wholetext_parse(self.text)
        
    def parse_text(self, text):
        self.text = text
        return self.wholetext_parse(self.text)

    def wholetext_parse(self, text):
        stmts, raw = [], text
        while raw:
            stmt, raw = self.parse(raw)
            stmts.append(stmt)

        return stmts





class MultipassParser(AParser):
    def __init__(self):
        self.stmtparser = ParserPython(grammar.statement, skipws=False, debug=False)
        self.textparser = ParserPython(grammar.freetext,  skipws=False, debug=False)
        self.visitor = document.TreeVisitor(self)

    def parse(self, text):
        parsers = [(self.stmtparser, self.__statement_transform, lambda parse_tree, parse_result: parse_tree.position_end),
                   (self.textparser, self.__free_text_transform, lambda parse_tree, parse_result: parse_result["length"])]
        
        try:
            parse_tree = self.stmtparser.parse(text)
            node = self.__statement_transform(parse_tree)
            node_length = parse_tree.position_end
            return node, text[node_length:]

        except arpeggio.NoMatch:
            pass

        
        try:
            parse_tree = self.textparser.parse(text)
            if parse_tree is None:
                return {
                    'type': 'skip',
                    'text': text
                }, None

            text_node = self.__free_text_transform(parse_tree)
            text_length = text_node["length"]
            return text_node, text[text_length:]
    
        except arpeggio.NoMatch:
            pass

        return {
            'type': 'text',
            'length': len(text),
            'text': text
        }, None

    def __statement_transform(self, parse_tree):
        
        return arpeggio.visit_parse_tree(parse_tree, self.visitor)

    def __free_text_transform(self, parse_tree):
        raw = str(parse_tree)
        node = dict(type="text", kind="text")

        node["text"] = raw
        node["length"] = len(raw)

        return node


    

