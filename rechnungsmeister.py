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

from Tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        Label(frame, text="Invoice").pack()
        self.invoice_date = self.make_entry(frame, "date", default="04.11.2017")
        self.invoice_number = self.make_entry(frame, "number", default="TT/1333")
        Label(frame, text="Customer").pack()
        self.customer_title = self.make_entry(frame, "title", default="geehrter Herr")
        self.customer_first_name = self.make_entry(frame, "first name", default="Franz")
        self.customer_last_name = self.make_entry(frame, "last name", default="Kafka")
        self.customer_street = self.make_entry(frame, "street", default="No-Name-Straße 2a")
        self.customer_city = self.make_entry(frame, "city", default="12345 Prag")
        Label(frame, text="Item").pack()
        self.item_long = self.make_entry(frame, "item_long", default="die schriftliche Übersetzung mit der Auftragsnummer 89898")
        self.item = self.make_entry(frame, "item", default="Übersetzung, 70 Cent pro Zeile")
        self.quantity = self.make_entry(frame, "quantity", default="100")
        self.price = self.make_entry(frame, "price", default="0,70")

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Generate Invoice", command=self.generate_invoice)
        self.hi_there.pack(side=RIGHT)

        frame.pack(fill=BOTH, expand=YES)

    def make_entry(self, parent, caption, width=None, default=None, **options):
        fm = Frame(parent)
        Label(fm, text=caption).pack(side=LEFT)
        entry = Entry(fm, **options)
        if width:
            entry.config(width=width)
        if default:
            entry.insert(0, default)
        entry.pack(side=LEFT)
        fm.pack()
        return entry

    def generate_invoice(self):
        template = latex_jinja_env.get_template('invoice_template.tex')

        variables = {
            "invoice_number" : self.invoice_number.get(),
            "invoice_date" : self.invoice_date.get(),
            "customer_title" : self.customer_title.get(),
            "customer_first_name" : self.customer_first_name.get(),
            "customer_last_name" : self.customer_last_name.get(),
            "customer_street" : self.customer_street.get(),
            "customer_city" : self.customer_city.get(),
            "item_long" : self.item_long.get(),
            "item" : self.item.get(),
            "quantity" : self.quantity.get(),
            "price" : self.price.get()
        }

        with open("invoice.tex", "w") as out_file:
            output = template.render(variables)

            # jinja returns unicode - so `output` needs to be encoded to a bytestring
            # before writing it to a file
            out_file.write(output)
            print "Created file invoice.tex."

root = Tk()

app = App(root)

root.mainloop()
root.destroy()


