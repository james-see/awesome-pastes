"""Confirm pastebins.json equals README.md using md_to_json."""
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
from contextlib import contextmanager
import json
import logging
import markdown_to_json
from markdown_to_json.vendor.docopt import docopt
from markdown_to_json.vendor import CommonMark
import sys
import filecmp


def get_markdown_ast(markdown_file):
    try:
        f = open(markdown_file, 'r')
        return CommonMark.DocParser().parse(f.read())
    except:
        logging.error("Error: Can't open {0} for reading".format(
            markdown_file))
        sys.exit(1)
    finally:
        f.close()


@contextmanager
def writable_io_or_stdout(filename):
    if filename is None:
        yield sys.stdout
        return
    else:
        try:
            f = open(filename, 'w')
            yield f
            f.close()
        except:
            logging.error("Error: Can't open {0} for writing".format(
                filename))
            sys.exit(1)


def jsonify_markdown(markdown_file, outfile, indent):
    nester = CMarkASTNester()
    renderer = Renderer()
    with writable_io_or_stdout(outfile) as f:
        ast = get_markdown_ast(markdown_file)
        nested = nester.nest(ast)
        rendered = renderer.stringify_dict(nested)
        json.dump(rendered, f, indent=indent)
        f.write("\n")
    return 0


def main():
    jsonify_markdown("README.md", "test_pastebins.json", 2)
    print(f"Test and json equal?: {filecmp.cmp('pastebins.json', 'test_pastebins.json')}")


if __name__ == "__main__":
    main()
