from flask import Flask
from flask import render_template
from flask import request, escape, redirect
from flask_caching import Cache
import pandas as pd
import numpy as np
import imdb

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
page_data = {}
page_data['search_results'] = ""
page_data['pt_table'] = ""
page_data['pt_list'] = ""



@app.route("/reset")
def reset():
    page_data['search_results'] = ""
    page_data['pt_table'] = ""
    page_data['pt_list'] = ""

    return redirect("/")
@app.route("/license")
def license():
    return render_template('license.html', title='Patient Table Generator')


@app.route("/")
def index():

    user_keyword = str(escape(request.args.get("keywords", "")))
    if user_keyword:
        page_data['search_results'] = search_imdb(user_keyword)

    selected_IMDB = str(escape(request.args.get("ID", "")))
    if selected_IMDB:
        df_characters = generate_patient_table(selected_IMDB)
        character_table_html = table_to_html(df_characters)
        page_data['pt_table'] = character_table_html
        page_data['pt_list'] = pt_entries(df_characters)
    return render_template('home.html',
                           search_results=page_data['search_results'],
                           pt_table=page_data['pt_table'],
                           pt_list=page_data['pt_list'],
                           title='Patient Table Generator')

def search_imdb(keywords):
    ia = imdb.IMDb()
    results = ia.search_movie(keywords)
    search_results = []
    for each in results:
        try:
            search_results.append({'imdb_id' : each.movieID, 'title' : str(each), 'year' : str(each['year'])})
        except KeyError:
            continue
    return search_results

def generate_patient_table(movie_ID):
    ia = imdb.IMDb()
    movie = ia.get_movie(movie_ID)
    actor = movie['cast']
    i = 0
    character_names = []
    for each in actor:
        character_names.append(str(each.currentRole))
        i += 1
        if i == 20:
            break
    with open('data/dob.txt', 'r') as a:
        DOB_list = a.read().splitlines()
    Gender_list = []
    with open('data/gender.txt', 'r') as a:
        genders = a.read().splitlines()
        list_length = 0
        while list_length < 20:
            for each in genders:
                Gender_list.append(each)
                list_length = len(Gender_list)
                if list_length == 20:
                    break
    with open('data/hcn.txt', 'r') as a:
        HCN_list = a.read().splitlines()
    with open('data/phone_number.txt', 'r') as a:
        phone_number_list = a.read().splitlines()
    with open('data/address.txt', 'r', encoding='utf-8') as a:
        Address_list = a.read().splitlines()
    with open('data/allergies.txt', 'r') as a:
        allergies_list = a.read().splitlines()

    alphabet = 'ABCDEFGHIJKLMNOPQRSTWXYZ'
    length = len(alphabet)
    i = 0
    index_alpha = []
    while length > i:
        index_alpha.append(alphabet[i])
        i += 1
    df = pd.DataFrame(
        {
            "Patient ID": pd.Series(index_alpha),
            "Name of Patient": pd.Series(character_names),
            "Date of Birth": pd.Series(DOB_list),
            "Gender": pd.Series(Gender_list),
            "HCN": pd.Series(HCN_list),
            "Phone": pd.Series(phone_number_list),
            "Address": pd.Series(Address_list),
            "Allergies": pd.Series(allergies_list)
        }
    )
    df.set_index("Patient ID", inplace=True)
    df_filtered = df.dropna(how='all').fillna('')
    return df_filtered

def table_to_html(df):
    html_result = df.to_html()
    return html_result

def pt_entries(df):
    df_list = df.values.tolist()
    df_index = df.index.values.tolist()
    a = 0
    for each in df_index:
        df_list[a].insert(0, each)
        a += 1
    return df_list

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)