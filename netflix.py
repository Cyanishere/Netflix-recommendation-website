
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly_express as px
import seaborn as sns
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request

def create_4train(x):
    return x['Genre'] + ' ' + x['Tags'] + ' ' +x['Actors']+' '+ x['Viewrating']

def find_recommendations(title,cosine_sim2):
  title = title.lower().replace(' ','')
  values = cosine_sim2[title].sort_values(ascending=False)[1:51]
  return values.index.str.title().tolist()

data = pd.read_csv('~/Downloads/NetflixDataset.csv',encoding='latin-1',index_col='Title')
data.index = data.index.str.title().str.lower().str.replace(' ','')
data = data[~data.index.duplicated()]

data.rename(columns={'View Rating':'Viewrating'},inplace=True)

new_features = ['Genre', 'Tags', 'Actors', 'Viewrating']
selected_data = data[new_features]
for new_feature in new_features:
  data.loc[:,new_features] = data.loc[:,new_features].apply(lambda x:x.str.replace(' ',''))
  data[new_feature] = data[new_feature].str.lower()

Language = data.Languages.str.get_dummies(',')
Lang = Language.columns.str.strip().values.tolist()
Lang = set(Lang)

Titles = set(data.index.to_list())

data['Genre'] = data['Genre'].fillna('').astype(str)
data['Tags'] = data['Tags'].fillna('').astype(str)
data['Actors'] = data['Actors'].fillna('').astype(str)
data['Viewrating'] = data['Viewrating'].fillna('').astype(str)
score_med = data['IMDb Score'].median()
data['IMDb Score'] = data['IMDb Score'].apply(lambda x:score_med if math.isnan(x) or x==0 else x)

selected_data['Train_fea'] = data.apply(create_4train, axis = 1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(selected_data['Train_fea'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim,columns=data.index,index=data.index)

df = pd.DataFrame()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html', languages = Lang, titles = Titles) 

@app.route('/about',methods=['POST'])
def getvalue():
    global df
    movienames = request.form.getlist('titles')
    languages = request.form.getlist('languages')
    for moviename in movienames:
        get_recommendations(moviename,cosine_sim2)
        for language in languages:
            df = pd.concat([result[result['Languages'].str.count(language) > 0], df], ignore_index=True)
    df.drop_duplicates(keep = 'first', inplace = True)
    df.sort_values(by = 'IMDb Score', ascending = False, inplace = True)
    images = df['Image'].tolist()
    titles = df['Title'].tolist()
    return render_template('result.html',  titles =  titles, images = images)

@app.route('/moviepage/<name>')
def movie_details(name):
    global df
    details_list = df[df['Title'] == name].to_numpy().tolist()
    return render_template('moviepage.html', details = details_list[0])


if __name__ == '__main__':
    app.run(debug=True)
