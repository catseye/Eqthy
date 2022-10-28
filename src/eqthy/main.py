from argparse import ArgumentParser
import codecs
import sys

from eqthy.parser import Parser
from eqthy.verifier import Verifier


def main(args):
    argparser = ArgumentParser()

    argparser.add_argument(
        'input_files', nargs='+', metavar='FILENAME', type=str,
        help='Source files containing the scenario descriptions'
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

    options = argparser.parse_args(args)

    text = ''
    for filename in options.input_files:
        with codecs.open(filename, 'r', encoding='UTF-8') as f:
            text += f.read() + '\n'

    p = Parser(text, filename)
    ast = p.document()
    if options.dump_ast:
        print(ast)
        sys.exit(0)

    verifier = Verifier(ast, verbose=options.verbose)
    try:
        verifier.verify()
    except Exception as e:
        print('*** {}: {}'.format(e.__class__.__name__, e))
        if options.traceback:
            raise
        sys.exit(1)
