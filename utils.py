import json
import requests
import main


def link2(id, token):
    id = id[1:]
    params = {
        "token": token
    }
    response = requests.post('https://api.clashofclans.com/v1/players/%23' + id + '/verifytoken',
                             data=json.dumps(params), headers=main.headers)
    user_json = response.json()
    if user_json['status'] == 'ok':
        return True
    else:
        return False


def get_heroes(json):
    num = len(json['heroes'])

    heroes = ''
    for x in range(num):
        if json['heroes'][x]['name'] == 'Barbarian King':
            heroes += "<:BK:822687680915308586> " + str(json['heroes'][x]['level'])
        elif json['heroes'][x]['name'] == 'Archer Queen':
            heroes += " <:AQ:822687698413289512> " + str(json['heroes'][x]['level'])
        elif json['heroes'][x]['name'] == 'Grand Warden':
            heroes += " <:GW:822687710509531156> " + str(json['heroes'][x]['level'])
        elif json['heroes'][x]['name'] == 'Royal Champion':
            heroes += " <:RC:822687723848073227> " + str(json['heroes'][x]['level'])

    return heroes


def check_bm(json):
    num = len(json['heroes'])
    bm = ''
    for x in range(num):
        if json['heroes'][x]['name'] == 'Battle Machine':
            bm = "<:bm:862948965129519134>" + '\t' + str(json['heroes'][x]['level'])
            break
    return bm


def get_dono(clan_json, num):
    data = json.loads(json.dumps(clan_json))
    dono = list(range(0, len(data['items'])))
    final = ""
    for i in range(len(dono)):
        max = i
        for j in range(i + 1, len(dono)):
            if data['items'][dono[max]]['donations'] < data['items'][dono[j]]['donations']:
                max = j
        dono[i], dono[max] = dono[max], dono[i]
    for i in dono[:num]:
        final += "\n" + str(data['items'][i]["donations"])

    return final


def get_rank(num):
    string = ""
    for i in range(num):
        string += "\n" + str(i + 1)
    return string


def get_eachmember(clan_json, num):
    data = json.loads(json.dumps(clan_json))
    dono = list(range(0, len(data['items'])))
    final = ""
    for i in range(len(dono)):
        max = i
        for j in range(i + 1, len(dono)):
            if data['items'][dono[max]]['donations'] < data['items'][dono[j]]['donations']:
                max = j
        dono[i], dono[max] = dono[max], dono[i]
    for i in dono[:num]:
        final += "\n" + str(data['items'][i]["name"])
    return final


def get_rec(clan_json, num):
    data = json.loads(json.dumps(clan_json))
    dono = list(range(0, len(data['items'])))
    final = ""
    for i in range(len(dono)):
        max = i
        for j in range(i + 1, len(dono)):
            if data['items'][dono[max]]['donations'] < data['items'][dono[j]]['donations']:
                max = j
        dono[i], dono[max] = dono[max], dono[i]
    for i in dono[:num]:
        final += "\n" + str(data['items'][i]["donationsReceived"])
    return final


def get_bhall_emoji(json):
    if json['builderHallLevel'] == 1:
        bhall = "<:b1:862937487093530645>"
    elif json['builderHallLevel'] == 2:
        bhall = "<:b2:862937487251996673>"
    elif json['builderHallLevel'] == 3:
        bhall = "<:b3:862937487760293889>"
    elif json['builderHallLevel'] == 4:
        bhall = "<:b4:862937487931736074>"
    elif json['builderHallLevel'] == 5:
        bhall = "<:b5:862937487734865931>"
    elif json['builderHallLevel'] == 6:
        bhall = "<:b6:862937488308699157>"
    elif json['builderHallLevel'] == 7:
        bhall = "<:b7:862937488633102386>"
    elif json['builderHallLevel'] == 8:
        bhall = "<:b8:862937488624320563>"
    else:
        bhall = "<:b9:862937488717119488>"
    return bhall


def get_thall_emoji(json):
    if json['townHallLevel'] == 1:
        thall = "<:Town_Hall1:819094243242672159>"
    elif json['townHallLevel'] == 2:
        thall = "<:Town_Hall2:819094243444260874>"
    elif json['townHallLevel'] == 3:
        thall = "<:Town_Hall3:819094245549015060>"
    elif json['townHallLevel'] == 4:
        thall = "<:Town_Hall4:819094245402869781>"
    elif json['townHallLevel'] == 5:
        thall = "<:Town_Hall5:819094245671043112>"
    elif json['townHallLevel'] == 6:
        thall = "<:Town_Hall6:819094246769295370>"
    elif json['townHallLevel'] == 7:
        thall = "<:Town_Hall7:819094247365017600>"
    elif json['townHallLevel'] == 8:
        thall = "<:Town_Hall8:819094247260028948>"
    elif json['townHallLevel'] == 9:
        thall = "<:Town_Hall9:819094247583383552>"
    elif json['townHallLevel'] == 10:
        thall = "<:Town_Hall10:819094228000309248>"
    elif json['townHallLevel'] == 11:
        thall = "<:Town_Hall11:819094231087841310>"
    elif json['townHallLevel'] == 12:
        thall = "<:Town_Hall12:819094241660764200>"
    elif json['townHallLevel'] == 13:
        thall = "<:Town_Hall13:819094243536273461>"
    else:
        thall = "<:Town_Hall14:833756232375468032>"
    return thall