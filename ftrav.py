"""
Tool for traversing a directory and reporting information related to all files
"""
import argparse  # argument parsing
import logging  # logging
import sys
import os  # path and directory info
from datetime import datetime
import xml.etree.ElementTree as ET  # xml generation
import xml.dom.minidom  # pretty xml printing

# supported hash functions
HASH_FXNS = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
FTRAV_VERSION = '0.1d'


class Directory:
    """
    Directory object - contains the information of the files in the directory
    """

    def __init__(self, path):
        """
        Constructor
        :param path: complete path of the directory
        """
        try:
            if os.path.isdir(path):
                self.path = path
            else:
                raise NotADirectoryError("\"{}\" is not a directory".format(path))
        except NotADirectoryError:
            raise
        self.content = []

    def append(self, item):
        self.content.append(item)


class File:
    """
    File object - contains information related to file on system
    """

    def __init__(self, path):
        """
        Constructor
        :param path: complete path to the file - error if not a file
        """
        # check if path is a file
        try:
            if os.path.isfile(path):
                self.path = path
                self.name = os.path.split(self.path)[1]
            else:
                raise FileNotFoundError('\"{}\" is not a file'.format(path))
        except FileNotFoundError:
            raise

        # Get Stats
        self.stats = dict()
        stats = os.stat(self.path)
        # size of the file
        size = stats[6]
        # convert to largest unit size
        units = 0
        while size >= 1024:
            size /= 1024
            units += 1
        self.stats['size'] = '{} {}'.format(round(size), self.UNITS[units])
        # last access date
        self.stats['accessed'] = datetime.fromtimestamp(stats[7]).strftime(
            '%A, %m/%d/%Y, %I:%M:%S %p')
        # last modification date
        self.stats['modified'] = datetime.fromtimestamp(stats[8]).strftime(
            '%A, %m/%d/%Y, %I:%M:%S %p')
        # last file permissions change
        self.stats['change'] = datetime.fromtimestamp(stats[9]).strftime(
            '%A, %m/%d/%Y, %I:%M:%S %p')

    # Static dictionary for size units
    UNITS = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}


class FileParser:
    """
    Class for traversing directories for file information
    """

    def __init__(self, start_dir, hash_type, output_name):
        """
        Constructor
        :param start_dir: directory to begin traversal from
        :param hash_type: hashing type - must be supported (see HASH FXNS)
        :param output_name: output file name
        """
        self.start_dir = start_dir
        self.hash_type = hash_type
        self.output_file = output_name
        self.files = Directory(self.start_dir)

    def traverse(self):
        self.__traverse_dir(self.start_dir, self.files)

    def __traverse_dir(self, path, parent_dir):
        """
        Traverse the directory for files
        :param path: complete path to directory
        :param parent_dir: parent directory object
        :return: None
        """
        files = os.listdir(path)
        for item in files:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                new_dir = Directory(item_path)
                parent_dir.append(new_dir)
                self.__traverse_dir(item_path, new_dir)
            elif os.path.isfile(item_path):
                parent_dir.append(File(item_path))

    def __xml_traverse(self, directory, parent_dir=None):
        """
        Builds an XML tree from Directory contents
        :param directory: initial Directory
        :param parent_dir: Parent Directory if not the root Directory
        :return: Root Element of the XML Tree
        """
        # Create new directory entry
        new_dir = ET.Element('Directory')
        new_dir.set('name', directory.path)

        # Add to existing directory if not the first
        if parent_dir is not None:
            parent_dir.append(new_dir)

        # Iterate and add items from current directories content
        for item in directory.content:
            # if file
            if isinstance(item, File):
                # create file entry
                new_file = ET.Element('File')
                new_file.set('name', item.name)
                # add sub-entries for each attribute
                for attribute, val in item.stats.items():
                    sub_item = ET.SubElement(new_file, attribute)
                    sub_item.text = val
                new_dir.append(new_file)
            # if directory
            else:
                # iterate through sub-directory
                self.__xml_traverse(item, parent_dir=new_dir)

        # Root Element of XML sub-tree
        return new_dir

    def write_xml(self):
        """
        Write XML tree to file
        :return: None
        """
        # Build XML tree
        root = self.__xml_traverse(self.files)

        # Prettify XML string
        output = xml.dom.minidom.parseString(ET.tostring(root))
        output = output.toprettyxml()

        # Write to file
        with open(self.output_file, 'w') as file:
            file.write(output)


def main():
    # enable logging
    logging.basicConfig(filename='ftrav.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')
    logging.info("ftrav Version: {} - Starting new scan".format(FTRAV_VERSION))
    logging.info("System: {}".format(sys.platform))
    logging.info("Version: {}".format(sys.version))

    # parse arguments <directory> <hash_type> <report_name>
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str)
    parser.add_argument('hash_type', choices=HASH_FXNS)
    parser.add_argument('report_name', type=str)
    args = parser.parse_args()

    files = FileParser(args.directory, args.hash_type, args.report_name)
    files.traverse()
    files.write_xml()


if __name__ == '__main__':
    main()
