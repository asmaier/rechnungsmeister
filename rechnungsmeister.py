#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# see http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
import os
import jinja2
latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)
template = latex_jinja_env.get_template('invoice_template.tex')

variables = {
    "invoice_number":"TT/1333",
    "invoice_date":"04.11.2017",
    "customer_title":"geehrter Herr",
    "customer_first_name":"Franz",
    "customer_last_name":"Kafka",
    "customer_street":"No-Name-Str. 2",
    "customer_city":"64560 Prag",
    "item_long": "die schriftliche Übersetzung mit der Auftragsnummer 89898",
    "item":"Übersetzung, 70 Cent pro Zeile",
    "quantity":"100",
    "price": "0,70"
}

with open("invoice.tex", "w") as out_file:
    output = template.render(variables)

    # jinja returns unicode - so `output` needs to be encoded to a bytestring
    # before writing it to a file
    out_file.write(output)
