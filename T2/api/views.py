from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import HamburguesaSerializer, IngredienteSerializer
from .models import Hamburguesa,Ingrediente

class HamburguesaViewSet(APIView):

    def get(self, request):
        hamburguesas = Hamburguesa.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = HamburguesaSerializer(hamburguesas, context = serializer_context, many = True)
        return Response (serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = HamburguesaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def get_extra_actions(cls):
        return []

class HamburguesaDetails(APIView):

    def get_object(self, id):
        try:
            return Hamburguesa.objects.get(id=id)
        except Hamburguesa.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# 400 id invalido y 404 hamb inexistente
    def get(self,request, id):
        hamburguesa = self.get_object(id)
        serializer_context = {
            'request': request,
        }
        serializer = HamburguesaSerializer(hamburguesa, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,id):
        hamburguesa = self.get_object(id)
        serializer = HamburguesaSerializer(hamburguesa)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        hamburguesa = self.get_object(id)
        serializer = HamburguesaSerializer(hamburguesa, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        hamburguesa = self.get_object(id)
        hamburguesa.delete()
        return Response(status=status.HTTP_200_OK)

class IngredienteViewSet(APIView):

    def get(self, request):
        ingredientes = Ingrediente.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = IngredienteSerializer(ingredientes, context=serializer_context,  many = True)
        return Response (serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IngredienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
    @classmethod
    def get_extra_actions(cls):
        return []


class IngredienteDetails(APIView):

    def get_object(self, id):
        try:
            return Ingrediente.objects.get(id=id)

        except Ingrediente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# falta el 404, ingrediente no existe y 400 id invalido
    def get(self,request, id):
        ingrediente = self.get_object(id)
        serializer_context = {
            'request': request,
        }
        serializer = IngredienteSerializer(ingrediente, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

# falta 404 y 409 ingrediente no se puede borrar, está presente en una hamburguesa
    def delete(self,request,id):
        ingrediente = self.get_object(id)
        ingrediente.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


class HamburguesaIngrediente(APIView):
    def get_hamburguesa_object(self,id):
        try:
            return Hamburguesa.objects.get(id=id)
        except Hamburguesa.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get_ingrediente_object(self,id):
        try:
            return Ingrediente.objects.get(id=id)
        except Ingrediente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id, ide):
        hamburguesa = self.get_hamburguesa_object(id)
        ingrediente = self.get_ingrediente_object(id=ide)
        ##OJO CON ESTO
        hamburguesa.ingredientes.add(ingrediente)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self,request,id, ide):
        hamburguesa = self.get_hamburguesa_object(id)
        ingrediente = self.get_ingrediente_object(ide)
        #OJO aca deberia ir un try y except para saber si está el ingrediente
        try:
            hamburguesa.ingredientes.remove(ingrediente)
            return Response(status=status.HTTP_200_OK)
        except Ingrediente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)