import glob
import pandas as pd
import json


def get_all_elements(dictionary_set, key):
    elements = []
    num_dictionaries = len(dictionary_set)
    max_elements = max(len(dictionary.get(key, []))
                       for dictionary in dictionary_set)

    for i in range(max_elements):
        for j in range(num_dictionaries):
            dictionary = dictionary_set[j]
            dictionary_elements = dictionary.get(key, [])
            if i < len(dictionary_elements):
                elements.append(dictionary_elements[i])

    return elements


dict = {}

for infile in glob.glob('C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\Oasis\\*.csv'):

    data = pd.read_csv(infile)

    for i in range(len(data.index)):
        pointer = data['URL do documento'][i].find('/', 8)
        url_base = data['URL do documento'][i][0:pointer]
        if url_base not in dict:
            dict[url_base] = {}
        if data['URL do documento'][i] not in dict[url_base]:
            dict[url_base][data['Título']
                           [i]] = data['URL do documento'][i]

sum = 0
for item in dict:
    dict[item]['tamanho'] = len(dict[item])
    if len(dict[item]) < 30:
        sum += len(dict[item])

print(sum)

list_dict = [{'links': list(dict[item].values()), 'titulos': list(
    dict[item].keys())} for item in dict if dict[item]['tamanho'] < 30]

for item in list_dict:
    item['links'].pop()
    item['titulos'].pop()

links_to_download = get_all_elements(list_dict, 'links')
titulos_to_download = get_all_elements(list_dict, 'titulos')

with open('C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\Oasis\\lista_final.json', 'w', encoding='utf8') as outfile:
    for i in range(len(links_to_download)):
        json.dump({'titulo': titulos_to_download[i],
                   'link': links_to_download[i]}, outfile)
        outfile.write('\n')


with open('C:\\Users\\isc_j\\OneDrive\\Documentos\\Py Projects\\Artigo_Lana\\Oasis\\lista_final.json', 'r', encoding='utf8') as infile:
    for linha in infile:
        dict_base = json.loads(linha)
        break
