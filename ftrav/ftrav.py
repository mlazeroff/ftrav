#! /usr/bin/env python3

import argparse  # argument parsing
import os        # path calls
from ftrav import ftrav_utils as ft


def directory_check(path):
    """
    Check if passed path is a directory
    :param path: complete path to the directory
    :return: path if directory is valid, error if not
    """
    if not os.path.isdir(path):
        raise NotADirectoryError('\"{}\" is not a directory'.format(path))

    return path


def file_type_check(file_name):
    """
    Check if output file is of XML or JSON type
    :param file_name: file name
    :return: xml/json if valid, error if not
    """
    if '.' not in file_name:
        raise TypeError('\"{}\" - file type not given. Must be .xml or .json'.format(file_name))

    # check extension
    file_type = os.path.split(file_name)[1].split('.')[-1]
    if file_type != 'xml' and file_type != 'json':
        raise TypeError('\"{}\" is not of .xml or .json type'.format(file_name))

    return file_type


def main():
    # parse arguments <directory> <hash_type> <report_name>
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=directory_check)
    parser.add_argument('--hash', choices=ft.HASH_FXNS)
    parser.add_argument('report_name', type=str)
    args = parser.parse_args()

    # traverse directory
    if 'hash' in args:
        files = ft.FileParser(args.directory, hash_type=args.hash)
    else:
        files = ft.FileParser(args.directory)
    files.traverse()

    # output data based on file type
    file_type = file_type_check(args.report_name)
    if file_type == 'xml':
        files.write_xml(args.report_name)
    elif file_type == 'json':
        files.write_json(args.report_name)


if __name__ == '__main__':
    main()