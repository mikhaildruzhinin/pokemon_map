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
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = show_map(request, pokemon_entities)

    pokemon_data = {
        'title_ru': pokemon.name,
        'title_en': pokemon.name_en,
        'title_jp': pokemon.name_jp,
        'img_url': pokemon.image.url,
        'description': pokemon.description,   
    }
    
    if pokemon.previous_evolution is not None:
        previous_evolution = {
            'title_ru': pokemon.previous_evolution.name,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': pokemon.previous_evolution.image.url,
        }
        pokemon_data['previous_evolution'] = previous_evolution
    try:
        next_evolution = {
            'title_ru': pokemon.next_pokemons.all()[0].name,
            'pokemon_id': pokemon.next_pokemons.all()[0].id,
            'img_url': pokemon.next_pokemons.all()[0].image.url,
        }
        pokemon_data['next_evolution'] = next_evolution
    except IndexError:
        pass

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_data})

def show_map(request, pokemon_entities):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        img_url = pokemon_entity.pokemon.image.url
        img_url = request.build_absolute_uri(location=img_url)
        add_pokemon(
            folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
            pokemon_entity.pokemon.name, img_url)
    return folium_map

