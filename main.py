from turtle import tilt, title
from flask import *
import csv
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Rediction vers la page "games"
@app.route('/')
def index():
    return redirect(url_for('games'))

# Affiche l'ensemble des jeux avec leurs informations
@app.route("/games", methods=['GET'])
def games():

    # Récupération de l'url et de ses données
    url = "https://api.geekdo.com/xmlapi/collection/megtrinity"
    response = requests.get(url)

    # Vérification de la requête 
    if response.status_code == 200: 
        # Analyse du contenu XML 
        root = ET.fromstring(response.content) 
        data = []

        # Parcours des éléments XML et extraction des données 
        for item in root.findall('item'): 
            id = item.get('objectid')
            title = item.find('name').text
        
            lst_published_year = item.find('yearpublished').text
            thumbnail = item.find('thumbnail').text

            stats = item.find('stats')
            minplayers = stats.get('minplayers')
            maxplayers = stats.get('maxplayers')
            if minplayers == maxplayers:
                players = maxplayers
            else: 
                players = f'{minplayers}-{maxplayers}'

            minplaytime = stats.get('minplaytime')
            maxplaytime = stats.get('maxplaytime')
            if minplaytime == maxplaytime:
                playtime = f'{maxplaytime}min'
            else: 
                playtime = f'{minplaytime}-{maxplaytime}min'

            data.append({
                'id' : id, 
                "title" : title, 
                "lst_published_year" : lst_published_year, 
                "thumbnail" : thumbnail,
                "players" : players, 
                "playtime" : playtime
            })

        # ouverture en écriture d'un fichier csv
        with open('LudothequeIsBack/boardGames.csv', 'w', newline='') as file:
            # on déclare un objet writer 
            writer = csv.writer(file, delimiter=';')
            #écrire une ligne dans le fichier:
            writer.writerow(['boardgamecategory', 'description YEAR', 'boardgameexpansion', 'id', 'title', 'img', 'players', 'playtime'])
    
            # quelques lignes:
            for i in data:
                writer.writerow(i)

    else: 
        print('Erreur lors de la récupération des données:', response.status_code)

    return jsonify(data)


# Affiche un seul jeu avec ses informations
@app.route("/games/<int:id>", methods=['GET'])
def one_game(id):
    
    # Récupération de l'url et de ses données
    url = f"https://api.geekdo.com/xmlapi/boardgame/{id}"
    response = requests.get(url)

    # Vérification de la requête
    if response.status_code == 200: 
        # Analyse du contenu XML 
        root = ET.fromstring(response.content) 
        data = []

        # Parcours des éléments XML et extraction des données  
        for boardgame in root.findall('boardgame'):
            id = boardgame.get('objectid')
            description = boardgame.find('description').text
        
            expansions = [] 
            for boardgameexpansion in boardgame.findall('boardgameexpansion'): 
                expansions.append(boardgameexpansion.text)

            categories = [] 
            for boardgamecategory in boardgame.findall('boardgamecategory'): 
                categories.append(boardgamecategory.text)

            id = boardgame.get('objectid')
            title = boardgame.find('name').text

            img = boardgame.find('image').text
            minplayers = boardgame.find('minplayers').text
            maxplayers = boardgame.find('maxplayers').text
            if minplayers == maxplayers:
                players = maxplayers
            else: 
                players = f'{minplayers}-{maxplayers}'

            playingtime = boardgame.find('playingtime').text

            data.append({
                    'categories': ", ".join(categories), 
                    'description': description, 
                    'expansion': ", ".join(expansions), 
                    'id': id, 
                    'title': title, 
                    'img': img, 
                    'players': players, 
                    'playingtime': playingtime
                })
                 
        # ouverture en écriture d'un fichier csv
        with open('LudothequeIsBack/boardgame.csv', 'w', newline='') as file:
            # on déclare un objet writer 
            writer = csv.writer(file, delimiter=';')
            #écrire une ligne dans le fichier:
            writer.writerow(['categories', 'description', 'expansions', 'id', 'title', 'players', 'img', 'playingtime'])

            # quelques lignes:
            for i in data:
                writer.writerow(i)
    else: 
        print('Erreur lors de la récupération des données:', response.status_code)

    return jsonify(data)


if __name__=='__main__':
    app.run(port=5000, debug=True)