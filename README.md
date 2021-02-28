
Setup
===
virtualenv venv
source venv/bin/activate


Gutenberg project is good for training sets:

Twenty thousand leagues under the sea, Jules Verne:
http://www.gutenberg.org/ebooks/164

Trump tweets:
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi%3A10.7910%2FDVN%2FKJEBIL
Use texts/data.py to process this into a raw text file format.
Requires ndjson in venv.
When training with this data, use option to process new lines as a term character.