import argparse
import os
from dotenv import load_dotenv

load_dotenv()


def create_parser(file_path=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', nargs='?',
                        default=os.getenv('GOOGLE_PROJECK_ID'))
    parser.add_argument('-f', '--file', nargs='?', default=file_path)
    return parser
