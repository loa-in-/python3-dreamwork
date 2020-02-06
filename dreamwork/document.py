import arpeggio

from . import parser
from . import documentview

from collections import defaultdict, deque

class Document:
    def __init__(self, parserklass):
        super().__init__()
        self.__parserklass = parserklass
        self.__parser = parserklass()
        self.paragraphs = []
        self.chunks = []
        self.rawtext = []
        self.definitions = defaultdict(list)


    def append_from_file(self, filename):
        nodes = self.__parser.parse_file(filename)
        self.add_nodes(nodes)
        self.rawtext.append(self.__parser.text)

    def append_source(self, text):
        nodes = self.__parser.parse_text(text)
        self.add_nodes(nodes)
        self.rawtext.append(text)
        
    def add_nodes(self, nodes):
        from collections import deque
        paragraph_stack = deque()

        def end_paragraph():
            if paragraph_stack:
                paragraph_node = dict(type='paragraph',
                    contents=list(paragraph_stack),
                    length=sum(map(lambda node: node['length'], paragraph_stack))
                )
                
                self.chunks.extend(paragraph_stack)
                self.paragraphs.append(paragraph_node)
                
                paragraph_stack.clear()

        for node in nodes:

            if node['type'] not in ('reference', 'text'):
                end_paragraph()
            else:
                paragraph_stack.append(node)

            if node['type'] not in ('reference', 'definition'):
                continue

            parsable_fields = ['name']
            if node['type'] == 'definition':
                parsable_fields.append('text')
            
            parsable_fields_contents = [
                node.get(field_name) for field_name in parsable_fields]

            for field_name, contents in zip(parsable_fields, parsable_fields_contents):
                subnodes = self.__parser.wholetext_parse(contents)
                print("\nFrom:\n\t",contents,"\ngot:\n\t", subnodes)
                
                if subnodes and subnodes[-1] is None:
                    subnodes = subnodes[:-1]

                node[field_name] = subnodes

                if len(subnodes) == 1 and subnodes[0]['type'] == 'text':
                    node[field_name] = subnodes[-1].get('text')

            if node['type'] == 'definition':
                self.chunks.append(node)
                self.definitions[node.get('name')].append(node)
        
        end_paragraph()

    def resolve_reference_text(self, node, parent_indent=0):
        name = node.get('name')
        node['text'] = self.resolve_text_by_defname(name, parent_indent)
        return node['text']
        
    def resolve_text_by_defname(self, name, parent_indent=0):
        pieces = self.definitions[name]

        if not pieces:
            raise NameError('Definition',name,'does not exist')

        assembly = deque()
        for definition in pieces:
            text_pieces = []
            contents = definition.get('text')

            if isinstance(contents, str):
                text_pieces.append(contents)
            else:
                for subnode in contents:
                    type = subnode.get('type')
                    if type == 'reference':
                        self.resolve_reference_text(subnode, parent_indent)
                    text = subnode.get('text')
                    text_pieces.append(text)
            
            kind = definition.get('kind')
            token = (kind, text_pieces)
            
            mod_left, mod_right = modifiers = map(lambda s: bool(s.strip('-')), definition.get('modifiers'))
            if not any(modifiers):
                mod_right = True
            
            if mod_left:
                assembly.appendleft(token)
            if mod_right:
                assembly.append(token)

        alltext = ""
        for kind, pieces in assembly:
            tokentext = "".join(pieces)
            if kind is 'freeform':
                alltext += tokentext
            elif kind is 'tabular':
                indent_spaces = len(alltext)
                last_break = alltext.rfind('\n')
                if last_break>=0:
                    indent_spaces -= last_break
                
                indent_spaces += alltext.count('\t',-indent_spaces) * 4
                indent_spaces += parent_indent

                print("Detected", indent_spaces, "spaces")
                indent = " "*indent_spaces
                lines = tokentext.splitlines(True)
                if lines[-1].endswith('\n'):
                    lines.append(indent)
                alltext += indent.join(lines)
        
        return alltext
        
        
        
        

class ATreeVisitor(arpeggio.PTNodeVisitor):
    def __init__(self, parser, defaults=True, **kwargs):
        super().__init__(defaults=defaults, **kwargs)
        self.parser = parser

class TreeVisitor(ATreeVisitor):
    def visit_block_statement(self, node, children):
        props = dict(type="definition", length=node.position_end)
        for child_props in children:
            try:
                props.update(child_props)
            except TypeError:
                continue
            except ValueError:
                continue
        
        return props

    def visit_ref_statement(self, node, children):
        props = dict(type="reference", length=node.position_end)
        props.update(children.ref_insert_middle[0])
        return props

    def visit_rem_statement(self, node, children):
        props = dict(type="comment", length=node.position_end)
        props.update(children.rem_insert_middle[0])
        return props

    def visit_block_start(self, node, children):
        return {
            "name": str(children.identifier[0]),
            'modifiers': [str(node[0])[1], str(node[-1])[-1]]
        }

    def visit_block_freeform(self, node, children):
        return {
            "kind": "freeform"
        }

    def visit_block_freeform_interior(self, node, children):
        return {
            "text": str(node)
        }

    def visit_block_tabular(self, node, children):
        return {
            "kind":"tabular"
        }

    def visit_block_interior(self, node, children):
        return {
            "text": str(node)
        }


    def visit_ref_insert_middle(self, node, children):
        identifier = children.identifier[0]
        return {"name": identifier, "kind": str(node[0])}

    def visit_rem_insert_middle(self, node, children):
        return {"text": str(node)}

    
    def visit_identifier(self, node, children):
        return str(node).strip()

