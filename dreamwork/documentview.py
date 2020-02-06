
TAB_SIZE = 4

class DeferredView(list):
    def __init__(self, document):
        self.document = document

    def enter(self):
        self.document.view_stack.append(self)

    def exit(self):
        assert self.document.view_stack.pop() is self

    def current_depth(self):
        return len(self.document.view_stack)

    def render(self):
        self.enter()

        self.rendered_text = ""
        for piece in self:
            self.render_piece(piece)

        self.exit()
        return self.rendered_text

    def __str__(self):
        return self.render()

    def render_piece(self, piece):
        if isinstance(piece, str):
            self.rendered_text += piece
        elif isinstance(piece, dict) and 'text' in piece.keys():
            text = piece.get('text')
            if isinstance(text, str):
                self.rendered_text += text
            if isinstance(text, list):
                self.rendered_text += self.document.nodes_view(*text).render()
        elif isinstance(piece, DeferredView):
            self.rendered_text += piece.render()

        

class IndentationPreservingView(DeferredView):
    def __init__(self, document):
        super().__init__(document)

    def total_stack_indent_spaces(self):
        spaces = 0

        self.exit()
        for view in self.document.view_stack:
            viewtext = view.rendered_text
            current_pos = len(viewtext)
            line_start = viewtext.rfind('\n')+1
            tab_count = viewtext.count('\t', line_start)
            spaces += current_pos - line_start + tab_count * TAB_SIZE
        self.enter()

        return spaces

    def current_indent_spaces(self):
        viewtext = self.rendered_text
        current_pos = len(viewtext)
        line_start = viewtext.rfind('\n')+1
        tab_count = viewtext.count('\t', line_start)
        spaces = current_pos - line_start + tab_count * TAB_SIZE
        return spaces


    def render_piece(self, piece):
        
        previous_length = len(self.rendered_text)
        
        super().render_piece(piece)

        indent_level = self.total_stack_indent_spaces() + self.current_indent_spaces()
        spaces = " "*indent_level

        lines = self.rendered_text[previous_length:].splitlines()
        
        self.rendered_text = self.rendered_text[:previous_length] + \
                            ("\n" + spaces).join(lines) + "\n" + spaces

    def exit(self):
        return super().exit()
        indent_level = self.total_stack_indent_spaces() + self.current_indent_spaces()
        self.rendered_text = self.rendered_text[:-indent_level]

        
    
