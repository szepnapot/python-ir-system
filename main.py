#!/usr/bin/env python3
import gzip
import json
import os
import shutil
from pprint import pprint
from configparser import ConfigParser

import whoosh
from whoosh import index
from whoosh.fields import Schema, TEXT
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser, MultifieldParser
import requests


config = ConfigParser()
config.read("config.ini")
FILE_URL = config.get("general", "data_file_url")
FILEPATH = config.get("general", "local_data_path")
INDEX_DIR = config.get("general", "index_directory")
STEMMING_CACHESIZE = config.getint("general", "cachesize")

FIRST_RUN = False
DEFAULT_LIMIT = 3
SHOW_STATS = True
CLI_USAGE = """
IR (Information Retrieval) system
Peter Lodri@szepnapot - 2019.02.13 - v0.1
-----------------------------------------
basic usage:
[search query]
~~~~~~~~~~~~~~~~
query operators:
- search query,  filter only for field
.[field] [query] 
~~~~~~~~~~~~~~~~
- limit number of results, default 3        
[query] .limit [max number of items to display]
~~~~~~~~~~~~~~~~
- toggle show stats, default On
.show_stats
~~~~~~~~~~~~~~~~
- quit the application
.exit
~~~~~~~~~~~~~~~~
- print usage info
.help
-----------------------------------------
Examples:
.title jeans limit 10
furniture
lewis limit 1
.merchant lewis
-----------------------------------------
"""


def unzip(archive, target):
    with gzip.open(archive, "rb") as f_in:
        with open(target, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(archive)


def fetch_and_save_data():
    r = requests.get(FILE_URL, stream=True)
    filename = FILE_URL.split("/")[-1]
    with open(filename, "wb") as fd:
        for chunk in r.iter_content(1024):
            fd.write(chunk)
    unzip(filename, FILEPATH)


analyzer = StemmingAnalyzer(cachesize=-1)
schema = Schema(
    description=TEXT(analyzer=analyzer),
    title=TEXT(analyzer=analyzer),
    merchant=TEXT(analyzer=analyzer),
)

if not os.path.exists(INDEX_DIR):
    FIRST_RUN = True
    os.mkdir(INDEX_DIR)

if not os.path.exists(FILEPATH):
    fetch_and_save_data()

with open(FILEPATH) as f:
    data = json.load(f)

try:
    ix = index.open_dir(INDEX_DIR)
except whoosh.index.EmptyIndexError:
    ix = index.create_in(INDEX_DIR, schema)

if FIRST_RUN:
    writer = ix.writer()
    for product in data:
        writer.add_document(
            description=product["description"],
            title=product["title"],
            merchant=product["merchant"],
        )
    writer.commit()

fields = ["description", "title", "merchant"]

parsers = {
    "default": MultifieldParser(fields, schema=ix.schema),
    "description": QueryParser("description", schema=ix.schema),
    "title": QueryParser("title", schema=ix.schema),
    "merchant": QueryParser("merchant", schema=ix.schema),
}

parser = parsers["default"]


def parse_limit(inp):
    if ".limit" not in inp:
        return inp, None
    tokens = inp.strip().split(".limit ")
    _query = tokens[0].strip()
    limit = int(tokens[1])
    return _query, limit


def is_exit_request(inp):
    if inp.strip() == ".exit":
        return True
    return False


def is_help_request(inp):
    return inp.strip() == ".help"


def is_toggle_stats_request(inp):
    return inp.strip() == ".show_stats"


while True:
    user_input = input(">>").strip()
    query = user_input
    if is_exit_request(query):
        print("Bye")
        break
    if is_help_request(query):
        print(CLI_USAGE)
        continue
    if is_toggle_stats_request(query):
        SHOW_STATS = False if SHOW_STATS else True
        print("show_stats: {}".format("ON" if SHOW_STATS else "OFF"))
        continue
    with ix.searcher() as searcher:
        if user_input.startswith("."):
            input_tokens = user_input.split()
            query_filter = input_tokens[0][1:]
            if query_filter not in fields:
                query = user_input
            else:
                query = " ".join(input_tokens[1:])
                parser = parsers[query_filter]

        query, user_limit = parse_limit(query)
        q = parser.parse(query)
        results = searcher.search(q, limit=user_limit if user_limit else DEFAULT_LIMIT)
        for hit in results.items():
            pprint(data[hit[0]])
        if SHOW_STATS:
            pprint({"runtime": results.runtime, "results": results.estimated_length()})
        # set back to default
        parser = parsers["default"]
