import requests
import json

def get_soc_ress_dict():
    url = "http://base.socialvalue.ru/api/api.php"

    querystring = {"gettagslist":""}

    response = requests.request("GET", url, params=querystring)

    ldd = json.loads(response.text)
    soc_ress = ldd['Социальные результаты']
    return soc_ress

def get_soc_ress():
    soc_ress = get_soc_ress_dict()

    soc_ress_check = [soc_ress[ld] for ld in soc_ress]
    return soc_ress_check

def get_soc_res_id_by_text(text):
    soc_ress = get_soc_ress_dict()
    for soc_res in soc_ress:
        if soc_ress[soc_res] == text:
            return soc_res
    return -1

def get_instr_by_soc_res_id(id):
    if id == -1:
        return []
    url = "http://base.socialvalue.ru/api/api.php"

    querystring = {"tags":str(id)}

    response = requests.request("GET", url, params=querystring)

    instruments_json = json.loads(response.text)
    instr_dict = instruments_json["success"]
    return [instr_dict[idn]["title"] for idn in instr_dict]