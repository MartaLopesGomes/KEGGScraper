===========
KEGGScraper
===========

Description
===========

Python Tool to request information in bulk from KEGG (Kyoto Encyclopedia of Genes and Genomes) database.

Installation 
============

Use the package manager pip to install virtualenv.

```bash
pip install virtualenv
```

Create a virtual environment to use with this tool.

```bash
virtualenv venv_KEGGScraper
```

Activate the virtualenvironment.

```bash
soure venv_KEGGScraper/bin/activate
```

Then move to the folder where the file setup.py from the KEGGScraper tool is located.

```bash
cd /path/to/KEGGSCraper
```

Run the command:

```bash
python setup.py install 
```

The tool should be ready to use.

Usage
=====

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
