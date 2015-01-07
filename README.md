# phladdress

A high-performance address standardizer for the City of Philadelphia

## Overview

Got dirty addresses? Let phladdress solve your parsing and standardizing needs. This is a lightweight Python module capable of standardizing street addresses, intersections, and post office boxes.

## Example

    from phladdress import Parser

    parser = Parser()
    comps = parser.parse('1234 MARKET STREET FIRST FLOOR')

    print comps['full_address']  # 1234 MARKET ST FL 1

## Installation

    pip install https://rbrtmrtn@bitbucket.org/rbrtmrtn/phladdress.git