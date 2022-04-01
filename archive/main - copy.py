from flask import Flask
from flask import request, escape
import pandas as pd
import numpy as np
import imdb

app = Flask(__name__)

@app.route("/")
def index():
    user_keyword = str(escape(request.args.get("keywords", "")))
    if user_keyword:
        output = search_imdb(user_keyword)
    else:
        output = ""
    selected_IMDB = str(escape(request.args.get("ID", "")))
    if selected_IMDB:
        pt_table = generate_patient_table(selected_IMDB)
    else:
        pt_table = ""
    return ("""<h1><a href='https://patient-name-generator.ue.r.appspot.com/'>Patient Table Generator</h1></a>
    <h2>Step 1: IMDB Search </h2>
    <form action="" method="get">
                <input type="text" name="keywords">
                <input type="submit" value="Search">
              </form>
    
    """
            + output
            + """
       <h2>Step 2: Enter IMDB ID to Generate Patient Table</h2>
       <form action="" method="get">
                   <input type="text" name="ID">
                   <input type="submit" value="Generate">
                 </form>"""
            + pt_table
)

def search_imdb(keywords):
    ia = imdb.IMDb()
    print('Search for title:')
    results = ia.search_movie(keywords)
    print(results)
    movie_id = []
    movie_title = []
    movie_year = []
    for each in results:
        try:
            movie_id.append(each.movieID)
            movie_title.append(str(each))
            movie_year.append(str(each['year']))
        except KeyError:
            continue
    print(movie_id)
    print(movie_title)
    print(movie_year)
    df = pd.DataFrame({
        "IMDB ID": pd.Series(movie_id),
        "Title": pd.Series(movie_title),
        "Year": pd.Series(movie_year)
    })
    df_filtered = df.dropna(how='all').fillna('')
    return df_filtered.to_html()
def generate_patient_table(movie_ID):
    ia = imdb.IMDb()
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

    # print(Gender_list)

    HCN_list = []
    with open('../data/hcn.txt', 'r') as a:
        HCN_list = a.read().splitlines()

    phone_number_list = []
    with open('../data/phone_number.txt', 'r') as a:
        phone_number_list = a.read().splitlines()

    Address_list = []
    with open('../data/address.txt', 'r', encoding='utf-8') as a:
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
    print(df)
    df_filtered = df.dropna(how='all').fillna('')
    print(df_filtered)

    html_result = df_filtered.to_html()

    df_list = df_filtered.values.tolist()
    print(df_list)
    df_index = df_filtered.index.values.tolist()
    print(df_index)
    a = 0
    for each in df_index:
        df_list[a].insert(0, each)
        a += 1
    print(df_list)

    for each in df_list:
        print(each[0])
        pt_id = each[0]
        pt_name = each[1]
        pt_dob = each[2]
        pt_gender = each[3]
        pt_HCN = str(each[4])
        pt_phone = each[5]
        pt_address = each[6]
        pt_allergies = each[7]
        print(pt_allergies)
        id = "<b>Patient ID: " + pt_id + "<br></b>"
        name = "Name: " + pt_name + "<br>"
        dob = "Date of Birth: " + pt_dob + "<br>"
        gender = "Gender: " + pt_gender + "<br>"
        hcn = "HCN: " + pt_HCN + "<br>"
        phone = "Phone: " + pt_phone + "<br>"
        address = "Address: " + pt_address + "<br>"
        allergies = "Allergies: " + pt_allergies + "<br>"
        html_entry = "<hr>" + id + name + dob + gender + hcn + phone + address + allergies + "<hr>"
        html_result = html_result + html_entry

    return html_result

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)