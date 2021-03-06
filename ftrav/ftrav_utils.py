"""
Tool for traversing a directory and reporting information related to all files
"""
import os  # path and directory info
from datetime import datetime  # timestamp conversion
import xml.etree.ElementTree as ET  # xml generation
import xml.dom.minidom  # pretty xml printing
import json  # json outputting
import copy  # dictionary deepcopy
import hashlib

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

    @staticmethod
    def json_encode(directory):

        return {'Directory': {'name': directory.path, 'content': directory.content}}


class File:
    """
    File object - contains information related to file on system
    Tracked Properties:
    * Size
    * Last Modified Time
    * Last Accessed Time
    * Last File Permission Change Time
    """

    def __init__(self, path, hash_fxn=None):
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

        # hash function (if provided)
        if hash_fxn is not None:
            # read file
            with open(self.path, 'rb') as file:
                content = file.read()
            hasher = hashlib.new(hash_fxn)
            hasher.update(content)
            self.stats['{}-hash'.format(hash_fxn)] = hasher.hexdigest()

        # last modification date
        self.stats['modified'] = datetime.fromtimestamp(stats[8]).strftime(
            '%A, %m/%d/%Y, %I:%M:%S %p')


    # Static dictionary for size units
    UNITS = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}

    @staticmethod
    def json_encode(file):
        """
        Method for encoding the File object in JSON
        :param file: File obj
        :return: JSON encoding
        """
        stats = copy.deepcopy(file.stats)
        stats['name'] = file.name
        return {'File': stats}


class FileParser:
    """
    Class for traversing directories for file information
    """

    def __init__(self, start_dir, hash_type=None):
        """
        Constructor
        :param start_dir: directory to begin traversal from
        :param hash_type: hashing type - must be supported (see HASH FXNS)
        """
        self.start_dir = os.path.abspath(start_dir)
        self.hash_type = hash_type
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
                new_dir = Directory(os.path.abspath(item_path))
                parent_dir.append(new_dir)
                self.__traverse_dir(item_path, new_dir)
            elif os.path.isfile(item_path):
                parent_dir.append(File(item_path, hash_fxn=self.hash_type))

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

    def write_xml(self, output_file):
        """
        Write XML tree to file
        :param output_file: name of output file
        :return: None
        """
        # Build XML tree
        root = self.__xml_traverse(self.files)

        # Prettify XML string
        output = xml.dom.minidom.parseString(ET.tostring(root))
        output = output.toprettyxml()

        # Write to file
        with open(output_file, 'w') as file:
            file.write(output)

    def write_json(self, output_file):
        """
        Write Directory information to JSON
        :param output_file: name of output file
        :return:
        """
        with open(output_file, 'w') as file:
            json.dump(self.files, file, indent=1, default=encode)


def encode(item):
    """
    Calls correct json encoding function
    :param item: File or Directory object
    :return: appropriate encoding of object
    """
    if isinstance(item, File):
        return File.json_encode(item)
    else:
        return Directory.json_encode(item)
