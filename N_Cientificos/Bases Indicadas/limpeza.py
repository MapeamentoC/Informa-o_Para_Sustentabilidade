import re
import ftfy
import nltk
import os
import fasttext

model = fasttext.load_model('./lid.176.ftz')

nltk.download('punkt')

def reonhece_lingua(sentenca):
    result = model.predict(sentenca, k=1)
    if result[0][0] == '__label__pt':
        validador  = True
    else:
        validador =  False
    
    return validador
     

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


def tokenize_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

def verificar_e_criar_diretorios(caminho):
    """
    Verifica se uma sequência de diretórios existe e, caso contrário, cria-os.
    
    Argumentos:
    caminho -- sequência de diretórios a ser verificada/criada
    
    Retorno:
    True se os diretórios já existirem ou forem criados com sucesso,
    False em caso de falha na criação dos diretórios
    """
    try:
        # Verifica se o caminho já existe como diretório
        if os.path.isdir(caminho):
            return True
        
        # Tenta criar os diretórios recursivamente
        os.makedirs(caminho)
        return True
    except OSError as e:
        print(f"Erro ao criar os diretórios: {e}")
        return False

for root, dirs, files in os.walk('./PDFs'):
    for file in files:
        if '.txt' in file:
            file_path = os.path.join(root, file)
            print(file_path)
            out_path = file_path.replace('./PDFs', './Limpos')
            out_path = out_path.replace(file, '')
            verificar_e_criar_diretorios(out_path)
            out_path = out_path+file

            with open(file_path, 'r', encoding='utf8') as infile:
                texto = infile.read()
                texto = ftfy.ftfy(texto)
                texto = organiza_texo(texto)
                sent = tokenize_sentences(texto)

                with open(out_path, 'w', encoding='utf8') as outfile:
                    for sentenca in sent:
                        is_pt = reonhece_lingua(sentenca)
                        if len(sentenca) > 30 and is_pt == True:
                            outfile.write(sentenca)
                            outfile.write('\n')