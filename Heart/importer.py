import os,json

def modules():
    r=[]
    for dos in os.listdir(r'H\Apps'):
        if 'importer.json' in os.listdir(r'H\Apps\\'+dos):
            r.append(r'H\Apps\\'+dos)

    return r

def commands():
    mod = modules()
    r = {
        'import_link':[],
        'import_line':[],
        'image':[],
        'FILES':[]
    }
    for module in mod:
        with open(module+'\\importer.json','r',encoding='utf8') as f:
            content = json.load(f)
            for k in r.keys():
                r[k].append(content[k])

    return r
