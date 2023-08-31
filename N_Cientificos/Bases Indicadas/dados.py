import os
import PyPDF2
import re


def ler_pdf(path):
    text = ''
    with open(path, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        for page in reader.pages:
            text += page.extract_text()

    return text


def organiza_texo(texto):

    padrao = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    texto = re.sub(padrao, ' ', texto)
    texto = texto.replace('\t', ' ')
    while '..' in texto:
        texto = texto.replace('..', ' ')
    while '__' in texto:
        texto = texto.replace('__', ' ')
    while '  ' in texto:
        texto = texto.replace('  ', ' ')

    return texto


for root, dirs, files in os.walk('./PDFs'):
    for file in files:
        if '.pdf' in file:
            file_path = os.path.join(root, file)
            print(file_path)
            out_path = file_path.replace('.pdf', '.txt')
            try:
                texto = ler_pdf(file_path)
                texto = organiza_texo(texto)
            except:
                texto = ''
            with open(out_path, 'w', encoding='utf8') as outfile:
                outfile.write(texto)
            print('foi\n')
