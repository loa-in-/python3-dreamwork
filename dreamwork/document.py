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

        #self.keystore_stack = deque() #for future use
        #self.keystore_stack.append(self.definitions)

        self.view_stack = deque()


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
                
                if subnodes and subnodes[-1] is None:
                    subnodes = subnodes[:-1]

                node[field_name] = subnodes

                if len(subnodes) == 1 and subnodes[0]['type'] == 'text':
                    node[field_name] = subnodes[-1].get('text')

            if node['type'] == 'definition':
                self.chunks.append(node)
                self.definitions[node.get('name')].append(node)
        
        end_paragraph()

    def resolve_reference(self, node):
        name = node.get('name')
        assert node.get('type') is 'reference'
        
        kind = node.get('kind')

        view = documentview.IndentationPreservingView(self) if kind is 'indented' \
            else documentview.DeferredView(self)
        view.extend(self.ordered_definitions(name))
        return view

    def defintion_view(self, definition_name):
        return self.nodes_view(*self.definitions[definition_name])

    def defintion_view_reordered(self, definition_name):
        return self.nodes_view(*self.ordered_definitions(name))
        
        
    def nodes_view(self, *nodes):
        view = documentview.DeferredView(self)
        view.extend([self.resolve_reference(node) if not isinstance(node, str) and node.get('type') == 'reference' else node for node in nodes])
        return view

    def ordered_definitions(self, name):
        assembly = deque()
        for definition_piece in self.definitions[name]:
            
            mod_left, mod_right = modifiers = map(lambda m: bool(m.strip('-')), definition_piece.get('modifiers'))
            
            if not any(modifiers):
            #    mod_right = True
                assembly.clear()
                assembly.append(definition_piece)
            
            if mod_left:
                assembly.appendleft(definition_piece)
            if mod_right:
                assembly.append(definition_piece)
            
        
        return list(assembly)

    def replace_definition(self, name, value):
        self.definitions


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
        props['kind'] = {
            '{': 'freeform',
            '[': 'indented'
        }.get(props.get('kind'))
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

