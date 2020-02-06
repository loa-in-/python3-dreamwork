class Workspace:
    pass

class WorkspaceEntity:
    pass

class BackingStore(WorkspaceEntity):
    pass

class ReadOnlyBackingStore(BackingStore):
    pass

class ReadWriteBackingStore(BackingStore):
    pass

class FilesystemBackingStore(BackingStore):
    pass



class Document(WorkspaceEntity):
    pass

class DocElement(WorkspaceEntity):
    """DocElement
        All objects that are of this class, have at least
    weave-semantics and tangle-semantics implemented."""
    pass

class BlockChunk(DocElement):
    pass

class Reference(DocElement):
    pass

class Text(DocElement):
    pass

class Identifier(DocElement):
    pass

"""
INPUT:
source file + includes + referenced files (how?) =

MODEL:
= document =
= blocks + references + styles + headers + paragraphs + comments +
+ ...chapters, TOC, listings, 

OUTPUT DOCUMENTATION:
= html / markdown / plaintext formatted files (multiple? how?) =
= possibly interactive unraveling of references and inserts and includes,
  and whatnot =
= documentation in the same order and spirit of the way it was written
  in the lit source file =

OUTPUT SOURCE CODE:
= anything, written to sandbox directory? , whitespace-perfectly defined
by the author in a predictable, flexible way.

"""