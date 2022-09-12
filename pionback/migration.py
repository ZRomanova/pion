import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pionback.settings')

import django
django.setup()


# -*- coding: utf8 -*-
import json, urllib.parse
import requests
from public.views import *


def get_soc_ress_dict():
    url = "https://base.socialvalue.ru/api/api.php"

    querystring = {"gettagslist":""}

    response = requests.request("GET", url, params=querystring, verify=False)

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
    url = "https://base.socialvalue.ru/api/api.php"

    querystring = {"tags":str(id)}

    response = requests.request("GET", url, params=querystring, verify=False)

    instruments_json = json.loads(response.text)
    if "success" in instruments_json:
        instr_dict = instruments_json["success"]
        return [{"name":instr_dict[idn]["title"], "url": instr_dict[idn]["url"]} for idn in instr_dict]
    else:
        return []

names = ['Повышение уровня удовлетворения базовых потребностей ребенка', 'Повышение социальных компетенций детей и коммуникативных навыков', 'Развитие знаний у детей в рамках образовательных программ', 'Развитие когнитивных умений детей', 'Развитие навыков самообслуживания у детей', 'Повышение уровня адаптированности ребенка', 'Повышение уровня самостоятельности ребенка/молодого взрослого', 'Развитие жизненных навыков ребенка/молодого взрослого', 'Снижение риска утраты родительского попечения', 'Улучшение эмоционального состояния ребенка', 'Улучшение материально-экономического положения семьи', 'Развитие родительских компетенций', 'Улучшение в детско-родительских отношениях', 'Развитие у родителей навыков взаимодействия с ребенком', 'Улучшение эмоционального состояния ребенка', 'Улучшение климата в семье', 'Изменение установок специалистов сферы детства', 'Развитие профессиональных компетенций специалистов сферы детства', 'Развитие компетенций волонтёров и наставников', 'Повышение эффективности волонтерских программ']
res = []
for name in names:
    id = get_soc_res_id_by_text(name)
    res.append([name, get_instr_by_soc_res_id(id)])

    for result in res:
        outcome, created = Outcome.objects.get_or_create(name=result[0])      
        methods = outcome.method_refs.all()
        for method in result[1]:
            if len(methods.filter(name=method['name'])) == 0:
                obj, created = OutcomeMethod.objects.get_or_create(name=method['name'], url=method['url'])
                outcome.method_refs.add(obj)