from data_collection import collect_data
from data_manipulation import manipulate_data
import pandas as pd


def main():
    #main function that takes the PTs -> adverse reactions of interes, the date and the active ingredient name = imatinib
    adverse_reactions = [
        'Acute kidney injury', 'Acute phosphate nephropathy', 'Anuria', 'Azothemia', 'Continuous haemodiafiltration', 'Dialysis',
        'Foetal renal impairment', 'Haemodialysis', 'Haemofiltration', 'Neonatal anuria', 'Nephropathy toxic', 'Oliguria',
        'Peritoneal dialysis', 'Prerenal failure', 'Renal failure', 'Renal failure neonatal', 'Renal impairment', 'Renal impairment neonatal', 'Subacute kidney injury'
    ]
    date = '20150101'
    api = 'IMATINIB'

    main_df = pd.DataFrame()
    for adverse_reaction in adverse_reactions:
        print('trying -> ' + adverse_reaction)
        json_data = collect_data(adverse_reaction, date, api)
        if json_data != None:
            data = manipulate_data(json_data, adverse_reactions)
            main_df = pd.concat([main_df, data], ignore_index=True)
            print('--------' + adverse_reaction + '-----------')
    main_df = main_df.drop_duplicates(subset=['safetyreportid'], ignore_index=True)
    main_df.to_excel('data.xlsx')




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/