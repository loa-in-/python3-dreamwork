import textwrap

class BaseRenderer:
    def __init__(self, weaver, document):
        super().__init__()
        self.weaver = weaver
        self.document = document

        self.started = False

    def weave_node(self, node, type, text):
        if not self.started:
            self.begin()
            self.started = True

        method = getattr(self, 'weave_'+type)
        return method(node, text)

    def weave_text(self, node, text):
        pass

    def weave_reference(self, node, text):
        pass

    def weave_definition(self, node, text):
        pass

    def write(self, text):
        self.weaver.write_to_active(text)

    def begin(self):
        pass

    def finish(self):
        self.weaver.flush_buffers()

PARAGRAPH_SEPARATOR = "\n\n"

class Renderer(BaseRenderer):
    def __init__(self, weaver, document):
        super().__init__(weaver, document)
        self.wrapper = textwrap.TextWrapper(80, '>   ')
        self.paragraphs = []
        self.paragraph = ""

    def start_paragraph(self):
        if self.paragraph:
            self.end_paragraph()
        self.write("\n")

    def end_paragraph(self):
        if not self.paragraph:
            return
        self.write(self.wrapper.fill(self.paragraph))
        self.write('\n\n')
        self.paragraphs.append(self.paragraph)
        self.paragraph = ""

    def begin(self):
        self.start_paragraph()

    def finish(self):
        return super().finish()
        self.end_paragraph()

    def weave_text(self, node, text):
        self.paragraph += text
        while PARAGRAPH_SEPARATOR in self.paragraph:
            paragraph, another = self.paragraph.split(PARAGRAPH_SEPARATOR, 1)
            self.paragraph = paragraph
            self.end_paragraph()
            self.paragraph = another


    def weave_reference(self, node, text):
        indented = node.get('kind') is 'indented'

        if indented:
            self.end_paragraph()

            self.wrapper.width = 50
            lines = self.wrapper.fill(text).splitlines()
            self.wrapper.width = 80
            for line in lines:
                self.write(line.center(80) + "\n")
            
            self.start_paragraph()
        
        else:
            self.weave_text(None, '|'+text+'|')



    def weave_definition(self, node, text):
        self.end_paragraph()
        self.write(("*" * 60).center(80)+"\n")
        self.write("       Definition of "+node.get('name')+"\n")
        self.write(("-" * 60).center(80)+"\n")
        self.write(text + "\n")        

        self.write(("*" * 60).center(80)+"\n")
        self.start_paragraph()
