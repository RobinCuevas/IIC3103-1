from django.http import HttpResponse
import requests
import json 
from django.template import Template, Context
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.shortcuts import render

# reference : https://www.youtube.com/watch?v=2TseIMieHPQ used to create the search bar

### API CONSULTING FUNCTIONS #######
def search_all_episodes():
    r = requests.get('https://rickandmortyapi.com/api/episode/')
    json_body = r.json()
    lista_episodios = []

    for episode in json_body["results"]:
        id_ = episode["id"]
        name = episode["name"]
        air_date = episode["air_date"]
        codigo = episode["episode"]

        dicc = {"code" : codigo, "date" : air_date, "name" : name, "id": id_}
        #lista_episodios.append(Episodio(name,air_date,codigo))
        lista_episodios.append(dicc)
    for aux in range(21,32):
        num_ = str(aux)
        url = 'https://rickandmortyapi.com/api/episode/' + num_
        req = requests.get(url)
        json_body = req.json()
        id_ = json_body["id"]
        name = json_body["name"]
        air_date = json_body["air_date"]
        codigo = json_body["episode"]
        dicc = {"code" : codigo, "date" : air_date, "name": name, "id": id_}
        lista_episodios.append(dicc)
    return lista_episodios

    ##################################### Locations ##########################################
def search_all_locations():
    rl = requests.get('https://rickandmortyapi.com/api/location/')
    json_body = rl.json()
    lista_locations = []
    all_locations = json_body["info"]["pages"]
    counter = 1
    while counter <= all_locations:
        rl = requests.get("https://rickandmortyapi.com/api/location/?page=" + str(counter))
        json_body2 = rl.json()
        for place in json_body2["results"]:
            id_ = place["id"]
            name = place["name"]
            dicc = {"name" : name, "id": id_}
            #lista_episodios.append(Episodio(name,air_date,codigo))
            lista_locations.append(dicc)
        counter += 1
    return lista_locations

    ##################################### Characters ##########################################
def search_all_characters():
    rc = requests.get('https://rickandmortyapi.com/api/character/')
    json_body = rc.json()
    lista_characters = []
    all_characters = json_body["info"]["pages"]
    counter = 1
    while counter <= all_characters:
        rl = requests.get("https://rickandmortyapi.com/api/character/?page=" + str(counter))
        json_body2 = rl.json()
        for charac in json_body2["results"]:
            id_ = charac["id"]
            name = charac["name"]
            dicc = {"name" : name, "id": id_}
            #lista_episodios.append(Episodio(name,air_date,codigo))
            lista_characters.append(dicc)
        counter += 1
    return lista_characters
### API CONSULTING FUNCTIONS #######

#### VIEWS ###########
def vista_principal(request):
    lista_episodios = search_all_episodes()
    order = request.GET.get("search")
    if order:
        lista_characters = search_all_characters()
        lista_locations = search_all_locations()
        order = str(order).lower()
        episodes_results = [chap for chap in lista_episodios if order in chap["name"].lower()]
        characters_results = [charac for charac in lista_characters if order in charac["name"].lower()]
        location_results = [loc for loc in lista_locations if order in loc["name"].lower()]
        return render(request, "show_results.html", {"episodes_results":episodes_results,
        "characters_results":characters_results,"location_results":location_results})
    #else:
        #here has to be the "normal" code
    #doc_externo = get_template("miplantilla.html")
    #documento = doc_externo.render({"lista_epis": lista_episodios})
    return render(request, "home.html", {"lista_epis": lista_episodios})

def episodio_selec(request, id):
    order = request.GET.get("search")
    if order:
        lista_episodios = search_all_episodes()
        lista_characters = search_all_characters()
        lista_locations = search_all_locations()
        order = str(order).lower()
        episodes_results = [chap for chap in lista_episodios if order in chap["name"].lower()]
        characters_results = [charac for charac in lista_characters if order in charac["name"].lower()]
        location_results = [loc for loc in lista_locations if order in loc["name"].lower()]
        return render(request, "show_results.html", {"episodes_results":episodes_results,
        "characters_results":characters_results,"location_results":location_results})

    r = requests.get('https://rickandmortyapi.com/api/episode/' + id)
    json_body = r.json()
    name = json_body["name"]
    air_date = json_body["air_date"]
    episode = json_body["episode"]
    characters = json_body["characters"]
    detalles_personajes = []
    for urll in characters:
        c = requests.get(urll)
        json_ = c.json()
        detalles_personajes.append(json_)

    chapter = {"episode_name" : name, "air_date" : air_date, "episode": episode, "characters" : detalles_personajes }
    return render(request, "chapter.html",chapter)

def specific_character(request, id):
    order = request.GET.get("search")
    if order:
        lista_episodios = search_all_episodes()
        lista_characters = search_all_characters()
        lista_locations = search_all_locations()
        order = str(order).lower()
        episodes_results = [chap for chap in lista_episodios if order in chap["name"].lower()]
        characters_results = [charac for charac in lista_characters if order in charac["name"].lower()]
        location_results = [loc for loc in lista_locations if order in loc["name"].lower()]
        return render(request, "show_results.html", {"episodes_results":episodes_results,
        "characters_results":characters_results,"location_results":location_results})

    r = requests.get('https://rickandmortyapi.com/api/character/' + id)
    json_body = r.json()
    dicc = {"name":json_body["name"], "status":json_body["status"], "species": json_body["species"], "type": json_body["type"],
     "gender": json_body["gender"], "origin" : json_body["origin"], "image":json_body["image"]}
    json_ubication = json_body["location"]
    dic_location = {"name":json_ubication["name"]}
    url_location = json_ubication["url"]
    rq = requests.get(url_location)
    json_loc = rq.json()
    id_location = json_loc["id"]
    dic_location["id"] = id_location
    print(dic_location)
    dicc["location"] = dic_location
    episodes_names = []
    for episode_url in json_body["episode"]:
        rr = requests.get(episode_url)
        json_ = rr.json()
        dic_aux = {}
        dic_aux["name"] = json_["name"]
        dic_aux["id"] = json_["id"]
        episodes_names.append(dic_aux)

    # controlling unknown type
    if dicc["type"] == "":
        dicc["type"] = "not specified"
    dicc["episode"] = episodes_names
    return render(request, "character.html", dicc)

def location(request, id):
    order = request.GET.get("search")
    if order:
        lista_episodios = search_all_episodes()
        lista_characters = search_all_characters()
        lista_locations = search_all_locations()
        order = str(order).lower()
        episodes_results = [chap for chap in lista_episodios if order in chap["name"].lower()]
        characters_results = [charac for charac in lista_characters if order in charac["name"].lower()]
        location_results = [loc for loc in lista_locations if order in loc["name"].lower()]
        return render(request, "show_results.html", {"episodes_results":episodes_results,
        "characters_results":characters_results,"location_results":location_results})
        
    r = requests.get('https://rickandmortyapi.com/api/location/' + id)
    json_body = r.json()
    dicc = {"name":json_body["name"], "type": json_body["type"], "dimension": json_body["dimension"]}
    residents_names = []
    for resident_url in json_body["residents"]:
        rr = requests.get(resident_url)
        json_ = rr.json()
        dic_aux = {}
        dic_aux["name"] = json_["name"]
        dic_aux["id"] = json_["id"]
        residents_names.append(dic_aux)
    dicc["residents"] = residents_names
    return render(request, "location.html", dicc)

