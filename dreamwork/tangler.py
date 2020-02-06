from collections import deque
import os.path

class Tangler:
    def __init__(self, path_prefix=None):
        super().__init__()
        self.__prefix = path_prefix
    
    def resolve_path(self, path):
        if self.__prefix:
            path = os.path.join(self.__prefix, path)
        return os.path.abspath(path)

    def tangle(self, document):
        defined_files = filter(lambda s: s.startswith('file:'), document.definitions.keys())
        for definition_name in defined_files:
            filename = definition_name[definition_name.index(':')+1: ]
            
            file_text = document.resolve_text_by_defname(definition_name)
            
            self.write_assembly(file_text, filename)

    def write_assembly(self, text, filename):
        print("-="*30)
        print("Writing to file", self.resolve_path(filename))
        print(text)
        print("-="*30)
        print()
            
                    
                
                    
            


    