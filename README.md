# Python IR (Information Retrieval) system

<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

A basic command line application that fetches a json catalog of products from S3,
ingests the product data, and creates an IR system. 
For the sake of keeping this test short it is fine to store all your data into memory, you do not need to use any kind of database. You can choose the indexing method and the way you prepare the data for it. The purpose of indexing is for the user to be able to search the dataset in real-time as on a search engine.

### Prerequisites

- [Python 3.7](https://www.python.org/downloads/release/python-370/)

Note:

On Windows to run the Makefile you need [cygwin](http://www.cygwin.com/).

### Usage

```bash
git clone 
```

```bash
# install pipenv
# set up virtualenv
# install dependecies

make install
```

To start the CLI

```bash
make run
```

### Info

- settings can be found in [config.ini](config.ini)
- unbound cache for analyzers
- results top to bottom decreasing, by default 3 displayed
- basic queries eg.: `.[field_name] [random search query]`, `.help` 

### Demo

![CLI demo gif](https://media.giphy.com/media/eejOqa4U82yydiMbeV/giphy.gif)

___

[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://blog.peterl.io)
