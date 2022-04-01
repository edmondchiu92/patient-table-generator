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
    if i == 20:
        break
print(character_names)

DOB_list = []
with open('../data/dob.txt', 'r') as a:
    DOB_list = a.read().splitlines()
Gender_list = []
with open('../data/gender.txt', 'r') as a:
    genders = a.read().splitlines()
    list_length = 0
    while list_length < 20:
        print(genders)
        for each in genders:
            Gender_list.append(each)
            print(Gender_list)
            list_length = len(Gender_list)
            print(list_length)
            if list_length == 20:
                break

#print(Gender_list)

HCN_list = []
with open('../data/hcn.txt', 'r') as a:
    HCN_list = a.read().splitlines()

phone_number_list = []
with open('../data/phone_number.txt', 'r') as a:
    phone_number_list = a.read().splitlines()

Address_list = []
with open('../data/address.txt', 'r') as a:
    Address_list = a.read().splitlines()

allergies_list = []
with open('../data/allergies.txt', 'r') as a:
    allergies_list = a.read().splitlines()


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

with open ('../patient_names.html', 'w') as a:
    a.write(df_filtered.to_html())

webbrowser.open('../patient_names.html')
