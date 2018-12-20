# FTrav - FileTraverse
Utility for traversing and indexing directory contents
## Overview
FTrav tracks indexes, tracks metadata, and can hash all files from a starting directory and outputs the data in XML/JSON format.

## Getting Started
### Prerequisites
* Python 3.*
### Installing
Installing via pip and git
```angular2html
pip install git+https://github.com/mlazeroff/ftrav
```

## Using the Tool
Usage: ftrav <starting_directory> <output.xml/.json>
* starting_directory - directory to begin traversal from
* output - output file name (must be .xml or .json) . Extension determines output format
* Optional: 
    * --hash <hash_type> 
        * Hash all files
        * see -h for all supported hash types
```angular2html
>>> ftrav ~/Documents sample.xml
```
Can use --hash argument to include hash information
```angular2html
>>> ftrav ~/Documents sample.json --hash sha256
```

## Author
* **Matthew Lazeroff**
## License
Licensed under GNU GPLv3