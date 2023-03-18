from argparse import ArgumentParser
import codecs
import sys

from eqthy.parser import Parser
from eqthy.verifier import Verifier


def extract_from_markdown(text):
    new_lines = []
    for line in text.split("\n"):
        if line.startswith("    "):
            new_lines.append(line[4:])
    return "\n".join(new_lines)


def main(args):
    argparser = ArgumentParser()

    argparser.add_argument(
        'input_files', nargs='+', metavar='FILENAME', type=str,
        help='Source files containing the scenario descriptions'
    )

    argparser.add_argument(
        "--bare",
        action="store_true",
        help="Treat the input as bare Eqthy that is not embedded in Markdown"
    )
    argparser.add_argument(
        "--dump-ast",
        action="store_true",
        help="Just show the AST and stop"
    )
    argparser.add_argument(
        "--traceback",
        action="store_true",
        help="When an error occurs, display a full Python traceback."
    )
    argparser.add_argument(
        "--verbose",
        action="store_true",
        help="Tell the user about every little thing"
    )
    argparser.add_argument(
        "--version", action="version", version="%(prog)s 0.2"
    )

    options = argparser.parse_args(args)

    try:
        context = {}
        for filename in options.input_files:
            with codecs.open(filename, 'r', encoding='UTF-8') as f:
                text = f.read()

            if not options.bare:
                text = extract_from_markdown(text)

            p = Parser(text, filename)
            ast = p.document()
            if options.dump_ast:
                print(ast)
                sys.exit(0)

            verifier = Verifier(ast, verbose=options.verbose, context=context)
            new_context = verifier.verify()
            context.update(new_context)
    except Exception as e:
        print('*** {}: {}'.format(e.__class__.__name__, e))
        if options.traceback:
            raise
        sys.exit(1)
