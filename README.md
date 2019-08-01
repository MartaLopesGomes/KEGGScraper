KEGGScraper
===========

Description
===========

Python Tool to request information in bulk from KEGG (Kyoto Encyclopedia of Genes and Genomes) database.

Installation
============

Python 3 is required.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install virtualenv.

```bash
pip install virtualenv
```

Create a virtual environment to use with this tool.

```bash
virtualenv venv_KEGGScraper
```

Activate the virtual environment.

```bash
source venv_KEGGScraper/bin/activate
```

Install dependencies

```bash
pip install grequests
pip install bs4
```

Then move to the folder where the file setup.py from the KEGGScraper tool is located.

```bash
cd /path/to/KEGGScraper
```

Run the command:

```bash
python setup.py install
```

The tool should be ready to use.

Usage
=====

## download_kos

Download all the sequences from each desired KO (KEGG Orthology) group to a fasta file.

The input can be:

- KEGG pathway map ID

- List of KO IDs

- List of KEGG Reaction IDs

- List of EC (Enzyme commission) numbers

Note: The format of the input lists must be a txt file with only one ID per line.


Run the command with the help option to see the usage and all the available options.

```bash
download_kos -h
```

To test if the tool is working you can use the files contained in the examples folder.

Using the tool to download all the sequences from the KO associated with the pathway with the ID map:

```bash
download_kos -o /path/to/output/folder/ -m map map00362
```

Using the tool to download all the sequences from the KO's listed in the file examples/kos.txt:

```bash
download_kos -o /path/to/output/folder/ -k /path/to/KEGGScraper/examples/kos.txt
```

Using the tool to download all the sequences from the KO's associated with the listed reactions in the file examples/reactions.txt:

```bash
download_kos -o /path/to/output/folder/ -r /path/to/KEGGScraper/examples/reactions.txt
```

Using the tool to download all the sequences from the KO's associated with the listed enzymes in the file examples/ecs.txt:

```bash
download_kos -o /path/to/output/folder/ -e /path/to/KEGGScraper/examples/ecs.txt
```

Note: Running this commands may take some time and memory space.


Output
======
In the output folder you will find one fasta file for each selected KO.
If you use one of the -e or -r options you will have another file, associations.txt, which indicates which kos where selected for download for each reaction/EC number.


Note
====

This project has been set up using PyScaffold 3.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
