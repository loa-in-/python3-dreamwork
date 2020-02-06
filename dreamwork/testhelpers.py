import arpeggio

from . import document

class ReducingVisitor(document.ATreeVisitor):
    def visit_identifier(self, node, children):
        return str(node).strip()

    def visit_block_statement(self, node, children):
        props = dict()
        for child_props in children:
            if not isinstance(child_props, dict): continue
            props.update(child_props)
        return "Block "+str(props)

    def visit_block_start(self, node, children):
        return {
            "name": str(children.identifier[0]),
            'mode': str(node[-1])
        }

    def visit_block_freeform(self, node, children):
        return {
            "type": "freeform"
        }

    def visit_block_freeform_interior(self, node, children):
        return {
            "interior": str(node)
        }

    def visit_block_tabular(self, node, children):
        return {
            "type":"tabular"
        }

    def visit_block_interior(self, node, children):
        return {
            "interior": self.parser.parse(str(node))
        }

    def visit_ref_statement(self, node, children):
        return "Reference {}".format(str(children[0]))

    def visit_ref_insert_middle(self, node, children):
        identifier = children.identifier[0]
        return "name {} type {}".format(identifier, str(node[0]))