import arpeggio

from . import parser

class Document:
    def __init__(self, parserklass):
        super().__init__()
        self.__parser = parserklass()
        
        self.chunks = []

    def append_from_file(self, filename):
        self.add_nodes(self.__parser.parse_file(filename))
        
    def add_nodes(self, nodes):
        self.chunks.extend(nodes)
        
        # filter
        # rebuild
        

class ATreeVisitor(arpeggio.PTNodeVisitor):
    def __init__(self, parser, defaults=True, **kwargs):
        super().__init__(defaults=defaults, **kwargs)
        self.parser = parser

class TreeVisitor(ATreeVisitor):
    def visit_block_statement(self, node, children):
        props = dict(type="definiton")
        for child_props in children:
            if not isinstance(child_props, dict): continue
            props.update(child_props)
        return props

    def visit_ref_statement(self, node, children):
        props = dict(type="reference")
        props.update(children[0])
        return props
    
    def visit_block_start(self, node, children):
        return {
            "name": str(children.identifier[0]),
            'modifier': str(node[-1])
        }

    def visit_block_freeform(self, node, children):
        return {
            "kind": "freeform"
        }

    def visit_block_freeform_interior(self, node, children):
        return {
            "interior": str(node)
        }

    def visit_block_tabular(self, node, children):
        return {
            "kind":"tabular"
        }

    def visit_block_interior(self, node, children):
        return {
            "interior": self.parser.parse(str(node))
        }


    def visit_ref_insert_middle(self, node, children):
        identifier = children.identifier[0]
        return {"name": identifier, "kind": str(node[0])}

    
    def visit_identifier(self, node, children):
        return str(node).strip()

