import argparse


def create_parser(project, file_path=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', nargs='?', default=project)
    parser.add_argument('-f', '--file', nargs='?', default=file_path)
    return parser
