from django.test import TestCase

# Create your tests here.
from actors.models import Breeder, Actor
from breeds.models import Breed
from dogs.models import Dog
from provinces.models import Province
from django.contrib.auth.models import User
from datetime import datetime, date, time


class DogTestCase(TestCase):

    def setUp(self):
        #Tipos de género
        MALE = 'Macho'
        #FEMALE = 'Hembra'
        # Raza
        #breed = Breed.objects.create(name='Raza1')

        # Cuenta de usuario
        #userAccount = User.objects.create_user('usuario1', 'jesosa94@gmail.com', 'contraseña1')

        # Provincia
        #province = Province.objects.create(name='Sevilla')

        # Criador


        #breeder = Breeder.objects.create(phone='954000000', photo=None, centerName='Nombre del centro',
       #                                  postalCode='410000', province=province.pk, address='Calle 123',
        #                                 opening='12:43:10', closing='12:43:10', cif='G00000123', userAccount=userAccount,
         #                                people=0, private=False, notes='Notas sobre el horario')

        # Perro

       # dog1 = Dog.objects.create(name='Perro1', age=2, gender=MALE, descendant='Descendencia para el perro 1',
        #                          details='Detalles para el perro 1', photo='uploads/default-dog.png',
         #                         awards='Premios para el perro 1',
          #                        breeder=breeder, breed=breed)
