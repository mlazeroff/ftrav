# FTrav - FileTraverse
Utility for traversing and indexing directory contents
## Overview
FTrav tracks indexes, metadata, and can hash all files from a starting directory and outputs the data in XML/JSON format.

Useful for indexing directories and keeping track of file changes. 

Note: Hashing alters last access date in metadata

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

## Example Usage
Example File Structure
```angular2html
D:/sample/
    sample1.txt
    sample2.txt
    subsample/
        subsample2.txt
```
```angular2html
>>> ftrav D:/sample sample.xml
>>> cat sample.xml
<?xml version="1.0" ?>
<Directory name="D:\sample">
	<File name="sample1.txt">
		<size>7 Bytes</size>
		<modified>Wednesday, 12/19/2018, 10:31:13 PM</modified>
	</File>
	<File name="sample2.txt">
		<size>11 Bytes</size>
		<modified>Wednesday, 12/19/2018, 10:31:13 PM</modified>
	</File>
	<Directory name="D:\sample\subsample">
		<File name="subsample2.txt">
			<size>14 Bytes</size>
			<modified>Wednesday, 12/19/2018, 10:31:14 PM</modified>
		</File>
	</Directory>
</Directory>
```


Can use --hash argument to include hash information for each file
```angular2html
>>> ftrav D:/sample sample.xml --hash sha256
>>> cat sample.xml
<?xml version="1.0" ?>
<Directory name="D:\sample">
	<File name="sample1.txt">
		<size>7 Bytes</size>
		<sha256-hash>e85130791f31db1699f61a5e7ae7b5e85e70399414f38476091896214771cd17</sha256-hash>
		<modified>Wednesday, 12/19/2018, 10:31:13 PM</modified>
	</File>
	<File name="sample2.txt">
		<size>11 Bytes</size>
		<sha256-hash>36d4fa357ff83bfffc4c6593ad3a4cc134c9cf092683ec15795cc757ae337a4c</sha256-hash>
		<modified>Wednesday, 12/19/2018, 10:31:13 PM</modified>
	</File>
	<Directory name="D:\sample\subsample">
		<File name="subsample2.txt">
			<size>14 Bytes</size>
			<sha256-hash>d6ca706d643f2804f857d0cead9ce95ea7f1952197ac9d171006cd4d91af714d</sha256-hash>
			<modified>Wednesday, 12/19/2018, 10:31:14 PM</modified>
		</File>
	</Directory>
</Directory>
```

## Author
* **Matthew Lazeroff**
## License
Licensed under GNU GPLv3