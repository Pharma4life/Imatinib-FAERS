from data_collection import collect_data
import numpy as np
import pandas as pd
import pycountry_convert

def rename_seriousnessdeath(df):
    #create a visually more aesthetic column with yes and no instead of 1 and 0
    if 'seriousnessdeath' in df.columns:
        try:
            df['seriousnessdeath'] = df['seriousnessdeath'].apply(lambda x: 'Yes' if x== '1' else 'No')
            return df
        except KeyError:
            df['seriousnessdeath'] = 'No'
            return df
    else:
        return df

def rename_seriousnesshospitalization(df):
    #create a visually more aesthetic column with yes and no instead of 1 and 0
    try:
        df['seriousnesshospitalization'] = df['seriousnesshospitalization'].apply(lambda x: 'Yes' if x == '1' else 'No')
        return df
    except KeyError:
        df['seriousnesshospitalization'] = 'No'
        return df

def rename_reactionoutcome(df):
    #maps over the reactionoutcome column and changes the numbers into a string that indicates better the outcome of the reaction
    outcomes = {
        '1' : 'Recovered',
    '2' :  'Recovering',
    '3' :  'Not recovered',
    '4' :  'Recovered with sequelae',
    '5' :  'Fatal',
    '6' :  'Unknown'
    }
    try:
        df['reactionoutcome'] = df['reactionoutcome'].map(outcomes)
        return df
    except KeyError:
        df['reactionoutcome'] = 'Unknown'
        return df

def rename_serious(df):
    #create a visually more aesthetic column with yes and no instead of 1 and 0
    try:
        df['serious'] = df['serious'].apply(lambda x: 'Yes' if x== '1' else 'No')
        return df
    except KeyError:
        df['serious'] = 'No'
        return df


def set_qualification(df):
    #maps over the qualification column and changes the numbers into strings that describe better the qualification
    qualifications = {
        '1' : 'Physician',
    '2' : 'Pharmacist',
    '3': 'Other health professional',
    '4': 'Lawyer',
    '5' : 'Consumer or non - health professional',
    }

    df['qualification'] = df.qualification.map(qualifications)
    return df

def set_patientsex(df):
    #changes the sex into males and females
    patientsex = {'0': 'Unknown',

     '1': 'Male',

     '2': 'Female'
     }

    df['patientsex'] = df['patientsex'].map(patientsex)
    return df

def set_drugcharacterization(df):
    #maps over the drugcharacterization column and changes the values into strings that describe better the characterization of the drug
    if 'drugcharacterization' in df.columns:
        ch = {'1': 'Suspect',

        '2' : 'Concomitant',

        '3' : 'Interacting',

        }
        df['drugcharacterization'] = df['drugcharacterization'].map(ch)
    return df

def set_countryname(df):
    #use of pycountry_convert library to change the values to the country name
    if 'primarysourcecountry' in df.columns:
        for i in range(len(df['primarysourcecountry'])):
            try:
                df['primarysourcecountry'].iloc[i] = pycountry_convert.country_alpha2_to_country_name(df['primarysourcecountry'].iloc[i])
            except:
                pass
    return df

def rename_other(df):
    df['other_reactions'] = df['other_reactions'].apply(lambda x: str(x).replace("'", ' ')[1:-1].strip())
    df['other_products'] = df['other_products'].apply(lambda x: str(x).replace("'", ' ')[1:-1].strip())
    df['other_apis'] = df['other_apis'].apply(lambda x: str(x).replace("'", ' ')[1:-1].strip())
    df['other_products'] = df['other_products'].apply(lambda x: str(x).replace(' /00018101/', ' '))
    df['other_reactions'] = df['other_reactions'].apply(lambda x: str(x).replace(' /00018101/', ' '))
    return df

def receive_year(df):
    #create column with values that indicate the year the ISCR has been received by the FDA
    df['receive_year'] = df['receivedate'].apply(lambda x: str(x)[:4])
    return df

def set_patient_age(df):
    #formats the age column using the patientageunit
    set_age = {
        800.0: 10,

        801.0: 1,

        802.0: 12,

        803.0: 0.0208333333333333,

        804.0: 0.0027397260273973,

        805.0: 0.000114155251141552,
    }

    df['patientonsetage'] = df['patientonsetageunit'].map(set_age) * df['patientonsetage'] // 1
    df = df.drop('patientonsetageunit', axis = 1)
    return df

def get_reccurent_number_ar(df, adverse_reactions):
    #create new column with number of reccurent adverse reactions> an ICSR may have multiple PTs
    df['reccurent_ar'] = df['other_reactions'].apply(lambda x: len(set(x.split(',')).intersection(adverse_reactions)))
    return df

def get_number_all_ar(df):
    #column that counts all the adverse reactions of the ICSR
    df['no_adverse_reactions'] = df['other_reactions'].apply(lambda x: len(x.split(',')))
    return df

def get_number_all_medication(df):
    #column that counts the number of medications taken by the patient
    df['no_medications_taken'] = df['other_apis'].apply(lambda x: len(x.split(',')))
    return df

def manipulate_data(json_data, adverse_reactions):
    #formats and creates the final df
    df = pd.DataFrame.from_dict(json_data)
    df = rename_seriousnesshospitalization(df)
    df = rename_seriousnessdeath(df)
    df = rename_serious(df)
    df = set_qualification(df)
    df = set_drugcharacterization(df)
    df = set_countryname(df)
    df = set_patientsex(df)
    df = rename_reactionoutcome(df)
    df = rename_other(df)
    df = receive_year(df)
    df = set_patient_age(df)
    df = get_reccurent_number_ar(df, adverse_reactions)
    df = get_number_all_ar(df)
    df = get_number_all_medication(df)
    return df