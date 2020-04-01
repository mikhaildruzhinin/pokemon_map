import folium
import json

from django.http import HttpResponseNotFound
from django.http import HttpRequest
from django.shortcuts import render

from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = show_map(request, pokemon_entities)

    pokemons_on_page = []
    for pokemon_id, pokemon in enumerate(pokemons):
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.name,
            'img_url': pokemon.image.url,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })

def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(pk=pokemon_id)
    pokemon_entities = PokemonEntity.objects.filter(Pokemon=pokemon)

    folium_map = show_map(request, pokemon_entities)

    pokemon_data = {}
    previous_evolution = {}
    next_evolution = {}
    pokemon_data['title_ru'] = pokemon.name
    pokemon_data['title_en'] = pokemon.name_en
    pokemon_data['title_jp'] = pokemon.name_jp
    pokemon_data['img_url'] = pokemon.image.url
    pokemon_data['description'] = pokemon.description
    if pokemon.previous_evolution is not None:
        pokemon_data['previous_evolution'] = previous_evolution
        previous_evolution['title_ru'] = pokemon.previous_evolution.name
        previous_evolution['pokemon_id'] = pokemon.previous_evolution.id
        previous_evolution['img_url'] = pokemon.previous_evolution.image.url
    try:
        pokemon_data['next_evolution'] = next_evolution
        next_evolution['title_ru'] = pokemon.next.all()[0].name
        next_evolution['pokemon_id'] = pokemon.next.all()[0].id
        next_evolution['img_url'] = pokemon.next.all()[0].image.url
    except IndexError:
        pass

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_data})

def show_map(request, pokemon_entities):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        img_url = pokemon_entity.Pokemon.image.url
        img_url = request.build_absolute_uri(location=img_url)
        add_pokemon(
            folium_map, pokemon_entity.Latitude, pokemon_entity.Longitude,
            pokemon_entity.Pokemon.name, img_url)
    return folium_map

