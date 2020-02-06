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
        self.textparser = ParserPython(grammar.freetext,  skipws=False, debug=False)
        self.stmtparser = ParserPython(grammar.statement, skipws=False, debug=False)
        self.visitor = document.TreeVisitor(self)

    def parse(self, text):
        parsers = [(self.stmtparser, self.__statement_transform, lambda parse_tree, parse_result: parse_tree.position_end),
                   (self.textparser, self.__free_text_transform, lambda parse_tree, parse_result: parse_result["length"])]
        for parser, transform_func, length_func in parsers:
            try:
                parse_tree = parser.parse(text)
                result = transform_func(parse_tree)
                return result, text[length_func(parse_tree, result):]
            except arpeggio.NoMatch:
                continue
        
        return text, None

    def __statement_transform(self, parse_tree):
        return arpeggio.visit_parse_tree(parse_tree, self.visitor)

    def __free_text_transform(self, parse_tree):
        raw = str(parse_tree)
        node = dict(type="text", kind="text")

        if raw.startswith("\n"):
            count = len(raw) - len(raw.lstrip("\n"))
            node["kind"] = "vertical_space"
            node["length"] = count
            node["text"] = raw[:count]
            return node
        
        node["kind"] = "paragraph"
        node["text"] = raw
        index = raw.find("\n")
        if (index > 0):
            node["text"] = raw[:index]
        node["length"] = len(node["text"])

        return node


    

