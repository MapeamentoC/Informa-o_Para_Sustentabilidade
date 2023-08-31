import json
import pandas as pd
import glob
dikt = {}
name_list = []
for file in glob.glob('./*.json'):

    name = file.replace('.\\', '').replace('.json', '')
    name_list.append(name+'_unicas')
    with open(file, 'r', encoding='utf8') as infile:
        json_data = [json.loads(linha) for linha in infile]
    new_df = pd.concat([pd.DataFrame(pd.json_normalize(x))
                        for x in json_data], ignore_index=True)

    dikt[name] = new_df

name_list.append('repetidas')

dikt['repetidas'] = pd.DataFrame()
dikt['sustentabilidade_unicas'] = pd.DataFrame()
dikt['sustentavel_unicas'] = pd.DataFrame()
dikt['sustentaveis_unicas'] = pd.DataFrame()

for i in dikt['sustentabilidade'].index:
    resultado_suvel = dikt['sustentavel']['Título'][dikt['sustentavel']
                                                     ['Título'] == dikt['sustentabilidade']['Título'].loc[i]]
    resultado_suveis = dikt['sustentaveis']['Título'][dikt['sustentaveis']
                                                       ['Título'] == dikt['sustentabilidade']['Título'].loc[i]]
    if len(resultado_suvel) > 0 or len(resultado_suveis):
        dikt['repetidas'] = pd.concat(
            [dikt['repetidas'], dikt['sustentabilidade'].loc[i]], axis=1, ignore_index=True)
    else:
        dikt['sustentabilidade_unicas'] = pd.concat(
            [dikt['sustentabilidade_unicas'], dikt['sustentabilidade'].loc[i]], axis=1, ignore_index=True)

dikt['sustentabilidade_unicas'] = dikt['sustentabilidade_unicas'].transpose()

for i in dikt['sustentavel'].index:
    resultado_sudade = dikt['sustentabilidade']['Título'][dikt['sustentabilidade']
                                                           ['Título'] == dikt['sustentavel']['Título'].loc[i]]
    resultado_suveis = dikt['sustentaveis']['Título'][dikt['sustentaveis']
                                                       ['Título'] == dikt['sustentavel']['Título'].loc[i]]
    if len(resultado_sudade) > 0 or len(resultado_suveis):
        dikt['repetidas'] = pd.concat(
            [dikt['repetidas'], dikt['sustentavel'].loc[i]], axis=1, ignore_index=True)
    else:
        dikt['sustentavel_unicas'] = pd.concat(
            [dikt['sustentavel_unicas'], dikt['sustentavel'].loc[i]], axis=1, ignore_index=True)

dikt['sustentavel_unicas'] = dikt['sustentavel_unicas'].transpose()

for i in dikt['sustentaveis'].index:
    resultado_sudade = dikt['sustentabilidade']['Título'][dikt['sustentabilidade']
                                                           ['Título'] == dikt['sustentaveis']['Título'].loc[i]]
    resultado_suvel = dikt['sustentavel']['Título'][dikt['sustentavel']
                                                     ['Título'] == dikt['sustentaveis']['Título'].loc[i]]
    if len(resultado_sudade) > 0 or len(resultado_suveis):
        dikt['repetidas'] = pd.concat(
            [dikt['repetidas'], dikt['sustentaveis'].loc[i]], axis=1, ignore_index=True)
    else:
        dikt['sustentaveis_unicas'] = pd.concat(
            [dikt['sustentaveis_unicas'], dikt['sustentaveis'].loc[i]], axis=1, ignore_index=True)

dikt['sustentaveis_unicas'] = dikt['sustentaveis_unicas'].transpose()
dikt['repetidas'] = dikt['repetidas'].transpose()
dikt['repetidas'] = dikt['repetidas'].drop_duplicates()

for item in name_list:
    with open('./'+item+'.json', 'w', encoding='utf8') as outfile:
        saida = []
        for i in dikt[item].index:
            out_dikt = {'Título': dikt[item]['Título'].loc[i],
                        'Texto': dikt[item]['Texto'].loc[i],
                        'Autor': dikt[item]['Autor'].loc[i],
                        'Data': dikt[item]['Data'].loc[i]}
            json.dump(out_dikt, outfile)
            outfile.write('\n')
