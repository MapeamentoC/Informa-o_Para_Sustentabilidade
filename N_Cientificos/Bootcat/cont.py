import re
import ftfy
import nltk
import json

def organiza_texo(texto):
 
    texto = texto.replace(' - \n', '')
    texto = texto.replace('\t', ' ')
    texto = texto.replace(' -\n', '')
    texto = texto.replace('-\n', '')
    texto = texto.replace('.\n', '.⁜')
    texto = texto.replace('?\n', '?⁜')
    texto = texto.replace('!\n', '!⁜')
    texto = texto.replace('\n', ' ')
    texto = texto.replace('.⁜', '.\n')
    texto = texto.replace('?⁜', '?\n')
    texto = texto.replace('!⁜', '!\n')
    texto = texto.replace('\n', ' ')
    padrao = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    texto = re.sub(padrao, ' ', texto)
    texto = texto.replace('\t', ' ')
    texto = texto.replace('\r', ' ')
    while '__' in texto:
        texto = texto.replace('__', ' ')
    while '  ' in texto:
        texto = texto.replace('  ', ' ')
    return texto


nltk.download('punkt')

def tokenize_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

with open('./Bootcat-corpus-final-sujo.txt', 'r', encoding='utf8') as infile:
    texto = infile.read()
    texto =ftfy.ftfy(texto)
    texto = organiza_texo(texto)
    sent = tokenize_sentences(texto)
    with open('./bootcat.json', 'w', encoding='utf8') as outfile:
        out_text = ''
        for sentenca in sent:
            out_text += sentenca+'\n'
        dikt = {'Título' : 'Bootcat', 'Texto' : out_text}
        json.dump(dikt, outfile)