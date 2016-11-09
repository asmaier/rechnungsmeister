# rechnungsmeister
This tool is a simple GUI written in python 2.7 that allows to create an invoice from a latex template.

## Prerequisite
The tool needs LaTeX (pdflatex) and python 2.7 with jinja2 installed.
### Mac OS X
I recommend to use [homebrew](http://brew.sh/):
    
    $ brew install python
    $ brew cask install mactex
    $ pip install jinja2
    
### Windows
I recommend to use [chocolatey](https://chocolatey.org/):

    C:\> choco install python2
    C:\> choco install miktex
    C:\> pip install jinja2
    
### Linux
On most Linux distribution Python is already preinstalled and available. To install LaTeX on e.g. Ubuntu do

    $ sudo apt-get install texlive
    $ pip install jinja2
    
## Configuration
Before first use you should edit the file `rechnung.ini`, enter your data and save the file:

    [biller]
    name_long=Prokurist Josef K.
    name=Josef K.
    street=Straße 12a
    city=12345 Stadt
    phone=+1\,234\,5678910
    email=josefk@bank.ab
    vat_number=AB123456789
    [bank]
    name=ABC Bank
    code=123\,456\,78
    account=123\,231\,312
    bic=ABCDEFGHIJK
    iban=AB12\,1234\,2341\,3412\,4123\,12

## Usage
To start the program type on your commandline
    
    python rechnungsmeister.py
    
This will open up a small GUI allowing you to enter the 
customers data and price and quantity of the items you want to charge for.
After entering your data click on `Erstelle Rechnung` and the tool will generate
a file `rechnung.pdf` using `pdflatex` in the background. Open the file with 
some pdfviewer. If it is ok, you can stop the Rechnungsmeister by clicking 
on `Schliessen`.

## Customization
The tool comes with a default LaTeX template `rechnung_template.tex`. To change 
the generated PDF simply edit this LaTeX template.

    
