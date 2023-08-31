import glob
import json
import re

def organiza_texo(texto):
    referencias = ['Bibliografia\n', 'Referências bibliográficas\n',
                   'Bibliografia consultada\n', 'Referências consultadas\n',
                   'Fontes consultadas\n', 'Referências bibliográficas consultadas\n']
    
    for item in referencias:
        if texto.find(item) != -1:
            texto = texto[:texto.find(item)]
            break   
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

cont_vazios = 0
cont_n_enc = 0
cont_quebrado = 0
cont_nc = 0
cont = 0
dicionarios_validos = []
todos_dicionarios = []
tokens = 0

for file in glob.glob('C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\Oasis\\*.json'):
    with open(file, 'r', encoding='utf8') as infile:
        print(file+'\n')
        for linha in infile:
            valid = 0
            linha = linha.replace('\n', ' ')
            dkt = json.loads(linha)
            todos_dicionarios.append(dkt)
            cont = cont+1
            if dkt['Texto'] == 'Não Capturado':
                cont_nc += 1
                valid += 1
            if dkt['Texto'] == '':
                cont_vazios += 1
                valid += 1
            if dkt['Texto'] == 'Página não encontrada':
                cont_n_enc += 1
                valid += 1
            if dkt['Texto'] == 'Url quebrado, 400 ou 401, ou 403' or dkt['Texto'] == '405 Not Allowed' or dkt['Texto'] == 'Url quebrado':
                cont_quebrado += 1
                valid += 1
            if valid == 0:
                dkt['Texto'] = organiza_texo(dkt['Texto'])
                tokens += len(dkt['Texto'].split(' '))
                dicionarios_validos.append(dkt)
            
file_cont = 1
file_name = 'validos_'
saida = 'C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\Oasis\\Final_geral\\'

k = 0
for item in dicionarios_validos:
    with open(saida+file_name+str(file_cont)+'.json', 'a', encoding='utf8') as outfile:
        if k > 500:
            file_cont += 1
            outfile.close()
            outfile = open(saida+file_name+str(file_cont)+'.json', 'a', encoding='utf8')
            k = 0
        json.dump(item, outfile)
        outfile.write('\n')
        k += 1




