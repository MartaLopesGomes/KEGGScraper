===========
KEGGScraper
===========

Description
===========

Python Tool to request information in bulk from KEGG (Kyoto Encyclopedia of Genes and Genomes) database.

Usage

1. Download all the files

2. On the shell, create a python virtual environment

3. In the directory where the file setup.py is located run:

python setup.py install

4. After that the tool is ready to use.

Available commands:

download_kos - Download all the sequences from each desired KO (KEGG Orthology) group to a fasta file.

The input can be:

- KEGG pathway map ID

- List of KO IDs

- List of KEGG Reaction IDs

- List of EC (Enzyme commission) numbers

Note: The format of the input lists must be a txt file with only one ID per line.


Note
====

This project has been set up using PyScaffold 3.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
