from collections import deque

class MarkdownWeaver:
    def render(self, document):
        self.doc_stack = stack = deque()
        stack.append(document)



    def subrender(self, subdocument):



