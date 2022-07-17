from argparse import ArgumentParser
import codecs
import sys

from eqthy.parser import Parser


def main(args):
    argparser = ArgumentParser()

    argparser.add_argument('input_files', nargs='+', metavar='FILENAME', type=str,
        help='Source files containing the scenario descriptions'
    )

    options = argparser.parse_args(args)

    text = ''
    for filename in options.input_files:
        with codecs.open(filename, 'r', encoding='UTF-8') as f:
            text += f.read()

    p = Parser(text, filename)
    ast = p.program()
    # if options.dump_ast:
    print(ast)

