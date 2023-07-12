import argparse

def parsers():
    parser = argparse.ArgumentParser(
        usage='python gester --show-cam'
    )
    parser.add_argument(
        '--show-cam',
        action='store_true',
        help='Toggle to show camera.'
    )

    return parser.parse_args()