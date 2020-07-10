from django.http import HttpResponse
import requests
import json 
from django.template import Template, Context
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.shortcuts import render
import graphene

# reference : https://www.youtube.com/watch?v=2TseIMieHPQ used to create the search bar

"""url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={location(id:"+str(1)+"){id name type dimension residents{id name}created}}"
response = requests.get(url).json()['data']['location']

print(response)"""

"{locations(page:1){results{idnametypedimensioncreated}}}"

### API CONSULTING FUNCTIONS #######
def search_all_episodes():
    lista_episodios = []
    for i in range(1,3):
        url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={episodes(page:" + str(i) + "){results{id name air_date episode}}}"
        response = requests.get(url).json()['data']['episodes']['results']
        for e in response:
            id_ = e["id"]
            name = e["name"]
            air_date = e["air_date"]
            codigo = e["episode"]
            dicc = {"code" : codigo, "date" : air_date, "name": name, "id": id_}
            lista_episodios.append(dicc)

    # for episode in json_body["results"]:
    #     id_ = episode["id"]
    #     name = episode["name"]
    #     air_date = episode["air_date"]
    #     codigo = episode["episode"]

    #     dicc = {"code" : codigo, "date" : air_date, "name" : name, "id": id_}
    #     #lista_episodios.append(Episodio(name,air_date,codigo))
    #     lista_episodios.append(dicc)
    # for aux in range(21,32):
    #     num_ = str(aux)
    #     url = 'https://integracion-rick-morty-api.herokuapp.com/api/episode/' + num_
    #     req = requests.get(url)
    #     json_body = req.json()
    #     id_ = json_body["id"]
    #     name = json_body["name"]
    #     air_date = json_body["air_date"]
    #     codigo = json_body["episode"]
    #     dicc = {"code" : codigo, "date" : air_date, "name": name, "id": id_}
    #     lista_episodios.append(dicc)
    return lista_episodios

    ##################################### Locations ##########################################
def search_all_locations():
    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={locations{info{pages}}}"
    all_locations = requests.get(url).json()['data']['locations']['info']['pages']
    counter = 1
    lista_locations = []
    while counter <= all_locations:
        url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={locations(page:"+str(counter)+"){results{id name}}}"
        response = requests.get(url).json()['data']['locations']['results']
        for place in response:
            id_ = place["id"]
            name = place["name"]
            dicc = {"name" : name, "id": id_}
            lista_locations.append(dicc)
        counter += 1
    return lista_locations

    ##################################### Characters ##########################################
def search_all_characters():
    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={characters{info{pages}}}"
    all_characters = requests.get(url).json()['data']['characters']['info']['pages']
    lista_characters = []
    counter = 1
    while counter <= all_characters:
        url_ = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={characters(page:"+str(counter)+"){results{id name}}}"
        response = requests.get(url_).json()['data']['characters']['results']
        for charac in response:
            id_ = charac["id"]
            name = charac["name"]
            dicc = {"name" : name, "id": id_}
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

    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={episode(id:"+str(id)+"){id name episode air_date created characters{id name}}}"
    response = requests.get(url).json()['data']
    episode_r = response['episode']
    name = episode_r["name"]
    air_date = episode_r["air_date"]
    episode = episode_r["episode"]
    characters = episode_r["characters"]
    # detalles_personajes = []
    # for carac in characters:
    #     print(carac, "carac")
    #     dicc_aux = {'name': carac['name'], 'id': carac['id']}
    #     detalles_personajes.append(dicc_aux)
    chapter = {"episode_name" : name, "air_date" : air_date, "episode": episode, "characters" :characters}
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

    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={character(id:" + str(id) + "){name status species type gender origin{name dimension id}location{name id}image episode{id name}created}}"
    json_body = requests.get(url).json()['data']['character']
    dicc = {"name":json_body["name"], "status":json_body["status"], "species": json_body["species"], "type": json_body["type"],
     "gender": json_body["gender"], "image":json_body["image"]}
    print("--------------", dicc)
    json_ubication = json_body["location"]
    dic_location = {"name":json_ubication["name"], 'id':json_ubication['id']}
    dicc["location"] = dic_location

    json_location = json_body["origin"]
    dic_ = {"name":json_location["name"], 'id':json_location['id']}
    dicc["origin"] = dic_

    episodes_names = []
    for episode_ in json_body["episode"]:
        dic_aux = {}
        dic_aux["name"] = episode_["name"]
        dic_aux["id"] = episode_["id"]
        episodes_names.append(dic_aux)
    # controlling unknown type
    if dicc["type"] == "":
        dicc["type"] = "not specified"
    dicc["episode"] = episodes_names
    print(dicc, "--------------")
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
        
    url = "https://integracion-rick-morty-api.herokuapp.com/graphql/?query={location(id:"+str(id)+"){id name type dimension residents{id name}created}}"
    response = requests.get(url).json()['data']['location']
    dicc = {"name":response["name"], "type": response["type"], "dimension": response["dimension"]}
    residents_names = []
    # no tiene url
    for resident_ in response["residents"]:
        dic_aux = {}
        dic_aux["name"] = resident_["name"]
        dic_aux["id"] = resident_["id"]
        residents_names.append(dic_aux)
    dicc["residents"] = residents_names
    return render(request, "location.html", dicc)