from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', null=False, blank=False)
    image = models.ImageField(verbose_name='Изображение', null=False, blank=False)
    description = models.TextField(max_length=500, default="", verbose_name='Описание', null=False, blank=True)
    name_en = models.CharField(max_length=200, default="", verbose_name='Название (англ.)', null=False, blank=True)
    name_jp = models.CharField(max_length=200, default="", verbose_name='Название (яп.)', null=False, blank=True)
    previous_evolution = models.ForeignKey('self', related_name = 'next_pokemons', verbose_name='Предыдущая эволюция',
                                            on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='pokemon_entities', verbose_name='Покемон', on_delete=models.PROTECT, null=False, blank=False)
    latitude = models.FloatField(verbose_name='Широта', null=False, blank=False)
    longitude = models.FloatField(verbose_name='Долгота', null=False, blank=False)
    appeared_at = models.DateTimeField(verbose_name='Появился в', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет в', null=True, blank=True)
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)