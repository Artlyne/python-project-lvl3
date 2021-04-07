import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description='web-page loader')
    parser.add_argument('url')
    parser.add_argument('--output', default=os.getcwd(),
                        help='specify path to save')
    return parser
