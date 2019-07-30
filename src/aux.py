# -*- coding: utf-8 -*-
"""

"""

from bs4 import BeautifulSoup as bs


def parser_ids(file):
    res = []
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        kID = line.strip()
        if len(kID) > 0:
            res.append(kID)
    return res


def get_orthology_ids_url_from_map(pathway_id):
    URL = 'http://www.genome.jp'
    FUN = '/dbget-bin/get_linkdb?-t+orthology+path:'
    return URL + FUN + pathway_id


def get_gene_ids_url(orthology_id):
    URL = 'http://www.genome.jp'
    FUN = '/dbget-bin/get_linkdb?-t+genes+ko:'
    return URL + FUN + orthology_id


def get_orthology_url_from_ec(ec):
    URL = 'https://www.genome.jp'
    FUN = '/dbget-bin/get_linkdb?-t+orthology+ec:'  # ec:1.3.1.25'
    return URL + FUN + ec


def get_orthology_url_from_rn(rn):
    URL = 'https://www.genome.jp'
    FUN = '/dbget-bin/get_linkdb?-t+orthology+rn:'
    return URL + FUN + rn


def get_ids(response):
    try:
        html = response.text
        b = bs(html, features="html.parser")
        links = b.find_all('a')
        valid_link = lambda x: 'www_bget' in x.get('href')
        links = filter(valid_link, links)
        lista = [link.text for link in links]
        return lista
    except AttributeError:
        html = response.read()
        b = bs(html, features="html.parser")
        links = b.find_all('a')
        valid_link = lambda x: 'www_bget' in x.get('href')
        links = filter(valid_link, links)
        lista = [link.text for link in links]
        return lista
    else:
        return None


def get_fastaProt_url(prot_id):
    URL = 'http://www.genome.jp'
    FUN = '/dbget-bin/www_bget?-f+-n+a+'
    return URL + FUN + prot_id

def get_fasta_url(gene_id):
    URL = 'http://www.genome.jp'
    FUN = '/dbget-bin/www_bget?-f+-n+n+'
    return URL + FUN + gene_id

def get_fastaProt(response):
    try:
        html = bs(response.text, features="html.parser")
        return html.pre.text
    except:
        return None
