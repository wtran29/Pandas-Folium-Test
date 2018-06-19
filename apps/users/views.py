from django.shortcuts import render, HttpResponse, redirect
import json
from difflib import SequenceMatcher, get_close_matches
import folium
import pandas as pd
# Create your views here.

mapOBJ = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Mapbox Bright")
fgv = folium.FeatureGroup(name="Volcanoes in US")

volcanoList = pd.read_csv("c://users//wtran//desktop//projects//django//test_app//apps//users//Volcanoes_USA.csv")
lat = list(volcanoList["LAT"])
lon = list(volcanoList["LON"])
coord = zip(lat, lon)
elev = list(volcanoList["ELEV"])
name = list(volcanoList["NAME"])


def color_change(e):
    if e < 1000:
        return "green"
    elif 1000 <= e < 3000:
        return "orange"
    else:
        return "red"


for coordinates, elevation, volname in zip(coord, elev, name):
    content = "<p style='font-family: Arial; font-size: 18px;'>{}</p><p style='font-family: Arial'>Elevation: {} MASL</p>".format(str(volname), str(elevation))
    iframe = folium.IFrame(content, width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=coordinates, popup=folium.Popup(iframe), radius=6,
                                      fill_color=color_change(elevation), fill=True, color='grey', fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('apps/users/world.json', 'r', encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                             else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

mapOBJ.add_child(fgp)
mapOBJ.add_child(fgv)
mapOBJ.add_child(folium.LayerControl())

mapOBJ.save("apps/users/templates/users/Map1.html")
data = json.load(open("apps/users/data.json"))


def index(request):
    return render(request, "users/index.html")


def translate(request):
    if request.method == 'POST':
        word = request.POST['word'].lower()
        try:
            close_match = get_close_matches(word, data.keys())[0]
        except IndexError:
            error = 'error'
            invalid = "Unknown word. Try again."
            return render(request, "users/index.html", {'word': error, 'invalid': invalid, 'match': error})
        if word in data:
            output = data[word]
            return render(request, "users/index.html", {'word': word, 'data': output, 'match': close_match})
        elif word.title() in data:
            output = data[word.title()]
            return render(request, "users/index.html", {'word': word.title(), 'data': output, 'match': word.title()})
        elif word.upper() in data:
            output = data[word.upper()]
            return render(request, "users/index.html", {'word': word.upper(), 'data': output, 'match': word.upper()})
        else:
            if len(get_close_matches(word, data.keys())) > 0:
                message = "Did you mean {} instead?".format(close_match)
                print(type(message) == str)
            else:
                message = "Could not find word! Try again"
            return render(request, "users/index.html", {'word': word, 'message': message, 'match': close_match})


def yes(request):
    if request.method == 'POST':
        reword = request.POST['word'].lower()
        word = get_close_matches(reword, data.keys())[0]
        output = data[word]
        print(type(data[word]))
        return render(request, "users/index.html", {'word': word, 'data': output, 'match': word})
    else:
        print("This is not a post??", request.method)


def no(request):
    if request.method == 'POST':
        error = "error"
        invalid = "Could not find word! Try again"
        print(type(invalid))
        return render(request, "users/index.html", {'word': error, 'invalid': invalid, 'match': error})
    else:
        print("This isn't a post??", request.method)
