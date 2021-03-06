import os
from Robos import stateRobot
from googleapiclient.discovery import build
import urllib.request

os.chdir(r'C:\Users\Marcos\Documents\Bots\Imagens ')


async def downloadImage(imgURL, name):

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    local = name + '.jpg'
    urllib.request.urlretrieve(imgURL, local)


async def downloadAllImages(content):
    arrayImages = []
    for i in range(len(content["Informations"])):
        image = content["Informations"][i]["urlImages"]
        for imgURL in range(len(image)):
            try:
                if image[imgURL] not in arrayImages:
                    await downloadImage(imgURL=image[imgURL],
                                        name=str(len(arrayImages)))
                    arrayImages.append(image[imgURL])
                    break
                print('Imagem ja baixada', end='|')
                raise NameError()

            except NameError:
                print('erro ao baixar')
                pass

    return arrayImages


def seachImagesFromCustomSeach(query):
    import json
    with open(r'C:\Users\Marcos\Documents\Credenciais\credenciais.json') as json_file:
        dados = json.load(json_file)
        key_id = dados["Google_ID"]
        cse_id = dados["CSE_ID"]

    service = build(serviceName="customsearch", version='v1', developerKey=key_id).cse()
    #res = service.list(q=query, cx=cse_id, num=2, searchType='image', imgSize='xlarge').execute()
    res = service.list(q=query, cx=cse_id, num = 3 ,imgSize='LARGE', searchType='image', imgType='photo').execute()
    arrayImages = []
    for i in range(len(res['items'])):
        arrayImages.append(res['items'][i]['link'])
    return arrayImages


def fechtImagesForAllSentenes(content):
    for i in range(len(content['Informations'])):
        if len(content["Informations"][i]['keywords']) != 0:
            query = content["Informations"][i]['Sentence'] + ' ' + content["Informations"][i]['keywords'][0]['text']
        else:
            query = content["Informations"][i]['Sentence']
        resusts = seachImagesFromCustomSeach(query=query)
        content["Informations"][i]['urlImages'] = resusts

    return content


async def ActivateImageBoot():
    content = stateRobot.load()

    fechtImagesForAllSentenes(content=content)
    await downloadAllImages(content=content)

    os.chdir(r'C:\Users\Marcos\Documents\Bots')
    stateRobot.save(content=content)
