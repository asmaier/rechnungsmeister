#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import subprocess
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

from ConfigParser import SafeConfigParser

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        Label(frame, text="Invoice", font="-weight bold").grid(row=0, columnspan=2)
        self.invoice_date = self.make_entry2(frame, 1, "Date:", default="04.11.2017")
        self.invoice_number = self.make_entry2(frame, 2, "Number:", default="TT/1333")

        Label(frame, text="Customer", font="-weight bold").grid(row=3, columnspan=2)
        self.customer_title = self.make_entry2(frame, 4, "Title:", default="geehrter Herr")
        self.customer_first_name = self.make_entry2(frame, 5, "First name:", default="Franz")
        self.customer_last_name = self.make_entry2(frame, 6, "Last name", default="Kafka")
        self.customer_street = self.make_entry2(frame, 7, "Street:", default="No-Name-Straße 2a")
        self.customer_city = self.make_entry2(frame, 8, "City:", default="12345 Prag")

        Label(frame, text="Item", font="-weight bold").grid(row=9, columnspan=2)
        self.item_long = self.make_entry2(frame, 10, "Item (long):", default="die schriftliche Übersetzung mit der Auftragsnummer 12345")
        self.item = self.make_entry2(frame, 11, "Item:", default="Übersetzung, 70 Cent pro Zeile")
        self.quantity = self.make_entry2(frame, 12, "Quantity:", default="100")
        self.price = self.make_entry2(frame, 13, "Price:", default="0,70")

        self.quit = Button(frame, text="QUIT", font="-weight bold", command=frame.quit)
        self.quit.grid(row=14, column=0)
        self.generate = Button(frame, text="Generate Invoice", font="-weight bold", command=self.generate_invoice)
        self.generate.grid(row=14, column=1, sticky=E)

        self.parser = SafeConfigParser()
        self.parser.read("invoice.ini")

    def make_entry(self, parent, caption, width=None, default=None, **options):
        fm = Frame(parent)
        Label(fm, text=caption, width=10).pack(side=LEFT)
        entry = Entry(fm, **options)
        if width:
            entry.config(width=width)
        if default:
            entry.insert(0, default)
        entry.pack(side=LEFT)
        fm.pack(side=TOP, anchor=W, fill=X, expand=YES)
        return entry

    def make_entry2(self, parent, row, label, default=None):
        Label(parent, text=label).grid(row=row, column=0, sticky=W)
        entry = Entry(parent)
        if default:
            entry.insert(0, default)
        entry.config(width=64)
        entry.grid(row=row, column=1)
        return entry

    def generate_invoice(self):
        template = latex_jinja_env.get_template('invoice_template.tex')

        variables = {
            "biller_name_long" : self.parser.get("biller","name_long"),
            "biller_name" : self.parser.get("biller","name"),
            "biller_street" : self.parser.get("biller","street"),
            "biller_city" : self.parser.get("biller","city"),
            "biller_phone" : self.parser.get("biller","phone"),
            "biller_email" : self.parser.get("biller","email"),
            "biller_vat" : self.parser.get("biller","vat_number"),
            "bank_name" : self.parser.get("bank","name"),
            "bank_code" : self.parser.get("bank","code"),
            "bank_account" : self.parser.get("bank","account"),
            "bank_iban" : self.parser.get("bank","iban"),
            "bank_bic" : self.parser.get("bank","bic"),
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
        proc = subprocess.Popen(["pdflatex", "invoice.tex"])
        proc.communicate()

root = Tk()

app = App(root)

root.mainloop()
root.destroy()


