
class BaseRenderer:
    def __init__(self, weaver, document):
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


