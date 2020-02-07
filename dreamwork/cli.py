#!/bin/python3
import argparse

import os

parser = argparse.ArgumentParser('dreamwork', 
    description=""" Turns the world of comments and documentation on it's
very head! Approach your requirements first, then worry about code. Keep
your config files in the same source code.""")

parser.add_argument('--output-to', '-o', dest='output_prefix', help="all created files will be relative to this")
parser.add_argument('--weave-to', '-wo', dest='weave_output_prefix', help="all documentation files will have this prefixed to path")
parser.add_argument('--tangle-to', '-to', dest='tangle_output_prefix', help="all generated output files will have this prefixed to path")

parser.add_argument('--output-jail', '-O', dest='output_jail', action='store_true', help="files can be opened only below current path")
parser.add_argument('--weave-jail', '-W', dest='weave_jail', action='store_true', help="files can be opened only below current path")
parser.add_argument('--tangle-jail', '-J', dest='tangle_jail', action='store_true', help="files can be opened only below current path")

parser.add_argument('--set', '-s', nargs=2, metavar='NAME VAL', action='append', dest='options')

parser.add_argument('--search-also', '-l', action='append', dest='search_path')



from . import weaver, tangler, document, parser

if __name__ == "__main__":
    options, args = parser.parse_args()
    if not args:
        raise IndexError("No file specified")

    if not all(map(os.path.exists, args)):
        for filename in args:
            if not os.path.exists(filename):
                print("Path",filename,"cannot be reached.")
        os.exit(1)
    
    for filename in args:
        print("Working on> ",filename)
        doc = document.Document(parser.MultipassParser)
        doc.append_from_file(filename)

        tangle_prefix = os.path.join(options.output_prefix, options.tangle_output_prefix)
        weave_prefix = os.path.join(options.output_prefix, options.weave_output_prefix)

        print("Weaving documentation/requirements/specs...")
        w = weaver.Weaver(weave_prefix)
        w.weave(doc)

        print("Tangling piecewise output code/config files...")
        t = tangler.Tangler(tangle_prefix)
        t.tangle(doc)

        print("All done!")

        

