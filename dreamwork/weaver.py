from collections import defaultdict
import os.path
import sys

from . import renderers


class Weaver:
    def __init__(self, path_prefix=None):
        self.__prefix = path_prefix

        self.settings = dict()

        self.renderer_module = renderers.plain
        self.rendererinst = None
        self.active_file = 'stdout.txt'

        self.buffers = defaultdict(list)

    def resolve_path(self, path):
        if self.__prefix:
            path = os.path.join(self.__prefix, path)
        return os.path.abspath(path)


    def enter(self, document):
        self.document = document
        #document.keystore_stack.append(self)

    def exit(self, document):
        #document.keystore_stack.remove(self)
        self.flush_buffers()
        self.document = None

    def weave(self, document):
        self.enter(document)
        
        for node in document.chunks:
            type = node.get('type')
            name = document.nodes_view(*node.get('name', '')).render()
            namespace = name.split(':',1)[0] if ':' in name else 'document'
            shortname = name.split(':',1)[1] if ':' in name else name

            text = document.nodes_view(node).render()

            if type == 'definition' and namespace == 'output':
                self.configure(document, shortname, text, namespace)
                print("setting",shortname,"to",text)
                continue

            if type in ('text', 'definition', 'reference'):
                self.renderer(document).weave_node(node, type, text)
                continue

        self.renderer(document).finish()
        self.exit(document)

    def configure(self, document, name, value, namespace='document'):
        if namespace == 'output':
            self.set_option(name, value)
        else:
            document.replace_definition(name, value)

    def getvalue(self, document, name, namespace='document'):
        if namespace == 'output':
            return self.get_option(name, value)
        else:
            return document.defintion_view_reordered(name).render()


    def get_option(self, name, value=None):
        return self.settings.get(name, value)
    
    def set_option(self, name, value):
        print("setting option",name,"to",value)
        self.settings[name] = value
        
        if name == 'chapterfile':
            print ("Changing files!!!")
            self.flush_buffers()
            self.active_file = value
        
        if name is 'renderer':
            pass #TODO





    def write_to_active(self, text):
        self.buffers[self.active_file].append(text)

    def flush_buffers(self):
        for filename in self.buffers:
            path = self.resolve_path(filename)
        
        text = "".join(self.buffers[filename])

        print("-="*30)
        print("Writing to file", path)
        print(text)
        print("-="*30)
        print()

        try:
            os.makedirs(os.path.dirname(path))
        except:
            pass
        
        with open(path, 'w') as outfile:
            outfile.write(str(text))

    def renderer(self, document):
        if self.rendererinst is None:
            self.rendererinst = self.renderer_module.Renderer(self, document)
        return self.rendererinst

            
                                
            
            

                   
                