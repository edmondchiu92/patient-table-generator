from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import webbrowser
import imdb

ia = imdb.IMDb()
print('Search for title:')
query_keywords = input() or 'mad men'
results = ia.search_movie(query_keywords)
i = 0 
for each in results:
    try:
        print(str(i) + ' ' + each.movieID + ' ' + str(each)+ ' ' + str(each['year']))
        i+=1
    except KeyError:
        continue

movie_ID = results[int(input())].movieID

movie = ia.get_movie(movie_ID)
print(movie)
actor = movie['cast']
i = 0
character_names = []
for each in actor:
    print(each.currentRole)
    character_names.append(str(each.currentRole))
    i += 1
    if i == 11:
        break
print(character_names)

middle_names = ['James','Robert','John']

DOB_list = ['1972-11-13','1932-08-29','1948-04-09','1957-05-22', '2012-02-27', '1932-03-21', '2017-05-25', '1955-05-07']

Gender_list = ['Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male']

HCN_list = ['5648 524 122', 'GELR 1932 0829', 'A23467898 (Canadian Forces)', '728 754 165']

phone_number_list = ['905-232-8044', '613-150-4570', '780-189-9840', '905-893-5481', '905-295-4812', '587-859-8910', '780-449-7815','306-895-4562']

Address_list = ['820 Heritage Hills Blvd, Mississauga, L5R 1Y0, ON', '1251 Avenue Sandford Fleming., Gatineau, G1A 0A9, QC', '100 Albert Ave. , Saint John, E3V 2B0, NB', '6845 Heritage Court, Moncton, E1A 1Y0, NB', '482 Heritage Hills Blvd, Mississauga, L5R 1Y0, ON', '36 Kensington Road NW, Calgary, T2N 3P3, AB', '101 Jasper Ave. , Edmonton, T5J 2B0, AB', '78 Zone St, Saskatoon, SK S0K 0Y0']

allergies_list = ['no allergies specified','no allergies specified','ciprofloxacin (Severe), bees (Mild)', 'minocycline (moderate)']
alphabet = 'ABCDEFGHIJKLMNOPQRSTWXYZ'
length = len(alphabet)
i = 0
index_alpha = []
while length > i:
    index_alpha.append(alphabet[i])
    i += 1
print(index_alpha)
df = pd.DataFrame(
    {
        "Patient ID": pd.Series(index_alpha),
        "Name of Patient":pd.Series(character_names),
        "Middle Name":pd.Series(middle_names),
        "Date of Birth":pd.Series(DOB_list),
        "Gender":pd.Series(Gender_list),
        "HCN": pd.Series(HCN_list),
        "Phone": pd.Series(phone_number_list),
        "Address": pd.Series(Address_list),
        "Allergies": pd.Series(allergies_list)
        }
    )
df.set_index("Patient ID", inplace= True)
print(df)
df_filtered = df.dropna(how='all').fillna('')
print(df_filtered)

with open ('patient_names.html', 'w') as a:
    a.write(df_filtered.to_html())

webbrowser.open('patient_names.html')
