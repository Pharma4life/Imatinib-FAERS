import requests
import time

def dissect_data(results, api, adverse_reaction):
    fields_of_interes = [
    "safetyreportid", "primarysourcecountry", "serious", "seriousnesshospitalization","receivedate", #general data
    'qualification', #primary source
    'patientonsetage', 'patientonsetageunit', 'patientsex', #patient data
    'drugcharacterization', #drug data
    'seriousnessdeath'
    ]
    final_data = []
    for dicts in results:
        row = {}
        for k, v in dicts.items():
            if k in fields_of_interes:
               row[k]=v
            if isinstance(v, dict):
                for k1,v1 in v.items():
                    if k1 in fields_of_interes:
                        row[k1] = v1
                    elif k1 == 'reaction':
                        reactions = []
                        for reactionmeddrapt in v1:
                            #add adverse reactions and reaction outcome
                            reactions.append(reactionmeddrapt['reactionmeddrapt'])
                            try:
                                row['reactionoutcome'] = reactionmeddrapt['reactionoutcome']
                            except:
                                continue
                        row['other_reactions'] = reactions

                    elif k1 == 'drug':
                        other_products = []
                        other_apis = []
                        for element in v1:
                            if 'activesubstance' in element.keys() and api in element['activesubstance']['activesubstancename']:
                                row['medicinalproduct'] = element['medicinalproduct'].replace('.', ' ') #adds the product name
                                for k2,v2 in element.items():
                                    if k2 in fields_of_interes:
                                        row[k2]=v2.capitalize()
                            else:
                                try:
                                    other_apis.append(element['activesubstance']['activesubstancename'].replace('.', ' '))
                                except KeyError:
                                    pass
                                other_products.append(element['medicinalproduct'].replace('.', ' '))
                        row['other_products'] = list(set(other_products))
                        row['other_apis'] = list(set(other_apis))
        row['main_adverse_reaction'] = adverse_reaction.capitalize()
        final_data.append(row)


    return final_data

def collect_data(adverse_reaction, date, api):
    #collects data twith the specific url that consists of 3 parameters> the active ingredient, the adverse reaction and the date that the FDA received the ICSR
    url = f'https://api.fda.gov/drug/event.json?search=patient.drug.activesubstance.activesubstancename:{api}+AND+patient.reaction.reactionmeddrapt:{adverse_reaction}+AND+receivedate:[{date}+TO+20221231]&limit=1000'
    print(url)
    try:
        data = requests.get(url).json()
        results = data['results']
        time.sleep(5)
        return dissect_data(results, api, adverse_reaction)
    except KeyError:
        return None

