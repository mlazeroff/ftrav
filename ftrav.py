"""
Tool for traversing a directory and reporting information related to all files
"""
import argparse  # argument parsing
import logging   # logging
import sys
import os        # path and directory info
import xml.etree.ElementTree as ET  # xml generation
import xml.dom.minidom  # pretty xml printing


# supported hash functions
HASH_FXNS = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
FTRAV_VERSION = '0.1d'


class FileParser():
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

        # starting dir for xml
        self.root = ''

    def traverse(self):
        """
        Begins traversal of file directories from starting directory
        """
        self.__travel_dir(self.start_dir, '')

    def __travel_dir(self, path, parent_dir):
        """
        Traverse the passed directory for files
        :param path: complete path of the directory
        :param parent_dir: Element of parent directory
        :return: None
        """
        # create new directory entry
        new_dir = ET.Element('Directory')
        new_dir.set('name', path)

        # append to last directory
        if self.root == '':
            self.root = new_dir
        else:
            parent_dir.append(new_dir)

        # write contents of directory
        for item in os.listdir(path):
            if os.path.isfile('{}/{}'.format(path, item)):
                self.__writeFile(item, new_dir)
            elif os.path.isdir('{}/{}'.format(path, item)):
                self.__travel_dir('{}\\{}'.format(path, item), new_dir)

    def __writeFile(self, file_name, parent_dir):
        """
        Creates a new file element in the XML
        :param file_name: file name
        :param parent_dir: Element of parent directory
        :return: None
        """
        new_file = ET.Element('File')
        new_file.set('name', file_name)
        parent_dir.append(new_file)

    def writeXml(self):
        """
        Write XML tree to file
        :return: None
        """
        output = xml.dom.minidom.parseString(ET.tostring(self.root))
        output = output.toprettyxml()
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


if __name__ == '__main__':
    main()