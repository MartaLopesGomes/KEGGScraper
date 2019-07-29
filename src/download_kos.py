# -*- coding: utf-8 -*-
"""

"""

import argparse
import sys
import logging
import os
from urllib.request import urlopen
import aux
from MultipleRequests import MultipleRequests

# from keggscraper import __version__

__author__ = "MartaLopesGomes"
__copyright__ = "MartaLopesGomes"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Create a database with all the KO (KEGG Orthology) sequences associated with the give ID/s "
                    "(KEGG pathway ID, KEGG Rections IDs, EC numers or KEGG orthology IDs)")
    group = parser.add_mutually_exclusive_group(required=True)
    group2 = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "--version",
        action="version"# ,
        # version="KEGGScraper {ver}".format(ver=__version__))
    )
    parser.add_argument(
        "-o",
        dest="output_dir",
        required=True,
        help="Output directory to store the database."
    )
    parser.add_argument(
        "-s",
        dest="size",
        help="Size - defines the number of requests that are made to the KEGG database at the same time. DEFAULT: 5",
        type=int
    )
    group.add_argument(
        "-m",
        dest="map",
        help="KEGG pathway ID",
    )
    group.add_argument(
        "-r",
        dest="reactions",
        help="Path to txt file containing KEGG reaction IDs (one per each line)",
    )
    group.add_argument(
        "-e",
        dest="ec_numbers",
        help="Path to txt file containing EC numbers (one per each line)",
    )
    group.add_argument(
        "-k",
        dest="kos",
        help="Path to txt file containing KEGG Orthology IDs (one per each line)",
    )
    group2.add_argument(
        "-p",
        dest="protein",
        help="Use this option if you want to download amino acid sequences. (DEFAULT)",
    )
    group2.add_argument(
        "-g",
        dest="gene",
        help="Use this option if you want to download nucleotide sequences.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    if not loglevel:
        loglevel = logging.INFO
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    args = parse_args(args)
    setup_logging(args.loglevel)

    if args.size:
        size = args.size
    else:
        size = 5

    if args.map:
        _logger.info('Searching for KEGG Orthology IDs associated to {}'.format(args.map))
        _logger.debug('Getting url...')
        url = aux.get_orthology_ids_url_from_map(args.map)
        _logger.debug('Making the request - {}'.format(url))
        response = urlopen(url)
        _logger.debug('Parsing IDs from the returned page...')
        kos = aux.get_ids(response)
        if kos is not None:
            kos_to_download = kos
        else:
            kos_to_download = []

    elif args.reactions:
        _logger.info('Searching for KEGG Orthology IDs associated to the given reaction IDs')
        if not os.path.isfile(args.reactions):
            _logger.error('REACTION IDs FILE - {} does not exist.'.format(args.reactions))
            return -1
        _logger.debug('Parsing input file to get Reaction IDs...')
        reactions = aux.parser_ids(args.reactions)
        urls = []
        _logger.debug('Calculating urls for each Reaction ID...')
        for reac in reactions:
            _logger.debug(reac)
            urls.append(aux.get_orthology_url_from_rn(reac))
        _logger.debug('Making the multiple requests...')
        r_requests = MultipleRequests(urls, size)
        responses = r_requests.async()
        kos_to_download = []
        _logger.debug('Parsing IDs from the returned pages...')
        for res in responses:
            _logger.debug(res)
            kos = aux.get_ids(res)
            if kos is not None:
                kos_to_download.extend(kos)


    elif args.ec_numbers:
        _logger.info('Searching for KEGG Orthology IDs associated to the given EC numbers')
        if not os.path.isfile(args.ec_numbers):
            _logger.error('EC NUMBERS - {} does not exist.'.format(args.ec_numbers))
            return -1
        _logger.debug('Parsing input file to get EC numbers...')
        ec_numbers = aux.parser_ids(args.ec_numbers)
        urls = []
        for ec in ec_numbers:
            _logger.debug(ec)
            urls.append(aux.get_orthology_url_from_ec(ec))
        _logger.debug('Making the multiple requests...')
        ec_requests = MultipleRequests(urls, size)
        responses = ec_requests.async()
        kos_to_download = []
        _logger.debug('Parsing IDs from the returned pages...')
        for res in responses:
            _logger.debug(res)
            kos = aux.get_ids(res)
            if kos is not None:
                kos_to_download.extend(kos)

    elif args.kos:
        _logger.info('Parsing input file to get KEGG Orthology IDs...')
        if not os.path.isfile(args.kos):
            _logger.error('KO IDs FILE - {} does not exist.'.format(args.kos))
            return -1
        kos_to_download = aux.parser_ids(args.kos)

    if len(kos_to_download) < 1:
        _logger.warning('No KEGG Orthology IDs found.')
        return -1

    _logger.info('KEGG Orthology IDs to download:')
    _logger.info('\t'.join(kos_to_download))

    total = 0

    _logger.info('Searching for the genes annotated to each KO...')
    urls = []
    multiple = {}
    _logger.debug('Calculating urls...')
    for ko in kos_to_download:
        urls.append(aux.get_gene_ids_url(ko))
    _logger.debug('Making the multiple requests...')
    test = MultipleRequests(urls, size)
    results = test.async()
    _logger.debug('Parsing IDs from the returned pages...')
    for res in results:
        gene_ids = aux.get_ids(res)
        ko_name = res.url.split(':')[-1]
        _logger.debug(ko_name)
        _logger.debug(res)
        if gene_ids is not None:
            multiple[ko_name] = gene_ids
            total += len(gene_ids)
    _logger.info('Total number of genes to download:')
    _logger.info(total)

    _logger.info('Requesting fasta sequences for each gene and writing fasta files...')
    for ko in multiple:
        fasta_urls = []
        _logger.info(ko)
        _logger.debug('Calculating urls for each sequence/gene ID...')
        for g_id in multiple[ko]:
            _logger.debug(g_id)
            if args.gene:
                fasta_urls.append(aux.get_fasta_url(g_id))
            else:
                fasta_urls.append(aux.get_fastaProt_url(g_id))
        _logger.debug('Making the multiple requests...')
        fasta_requests = MultipleRequests(fasta_urls, size)
        responses = fasta_requests.async()
        _logger.info('Writing sequences on fasta file...')
        with open(os.path.join(args.output_dir, ko + '.fa'), 'w') as f:
            for seq in responses:
                text = aux.get_fastaProt(seq)
                if text is not None:
                    f.write(text)
                    seq.close()
    return 0


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
