from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request, format=None):
        return Response(data_list, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Maneja las solicitudes POST para crear un nuevo elemento.
        """
        data = request.data # request.data maneja automáticamente el parsing de JSON/form-data

        # Validar que los campos 'name' y 'email' estén presentes
        if 'name' not in data or 'email' not in data:
            return Response(
                {"error": "Los campos 'name' y 'email' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si los campos son válidos:
        # 1. Generar un identificador único
        data['id'] = str(uuid.uuid4())
        # 2. Asignar 'is_active' a True
        data['is_active'] = True
        # 3. Agregar el nuevo dato a la lista
        data_list.append(data)

        # 4. Retornar una respuesta con código HTTP 201 y los datos guardados
        return Response(
            {"message": "Elemento creado con éxito", "data": data},
            status=status.HTTP_201_CREATED
        )
class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def get(self, request, item_id, format=None):
        """
        Maneja solicitudes GET para un elemento específico por ID.
        """
        item = next((item for item in data_list if item['id'] == item_id), None)
        if item:
            return Response(item, status=status.HTTP_200_OK)
        return Response(
            {"error": f"Elemento con ID {item_id} no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, item_id, format=None):
        """
        Maneja solicitudes PUT para reemplazar completamente un elemento.
        """
        data = request.data
        # Validar que los campos 'name', 'email', 'is_active' estén presentes
        if 'name' not in data or 'email' not in data or 'is_active' not in data:
             return Response(
                {"error": "Los campos 'name', 'email', y 'is_active' son obligatorios para PUT."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el índice del elemento
        found_index = -1
        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                found_index = i
                break

        if found_index != -1:
            # Crear un nuevo diccionario para el elemento, manteniendo el ID original
            # y agregando los nuevos datos
            updated_item = {
                'id': item_id, # Aseguramos que el ID no cambie
                'name': data.get('name'),
                'email': data.get('email'),
                'is_active': data.get('is_active')
            }
            data_list[found_index] = updated_item
            return Response(
                {"message": f"Elemento con ID {item_id} actualizado completamente.", "data": updated_item},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": f"Elemento con ID {item_id} no encontrado para actualizar."},
            status=status.HTTP_404_NOT_FOUND
        )

    def patch(self, request, item_id, format=None):
        """
        Maneja solicitudes PATCH para actualizar parcialmente un elemento.
        """
        data = request.data
        found_item = None
        found_index = -1

        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                found_item = item
                found_index = i
                break

        if found_item:
            # Actualiza solo los campos presentes en la solicitud
            for key, value in data.items():
                found_item[key] = value

            data_list[found_index] = found_item # Reemplazar el ítem actualizado
            return Response(
                {"message": f"Elemento con ID {item_id} actualizado parcialmente.", "data": found_item},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": f"Elemento con ID {item_id} no encontrado para actualizar parcialmente."},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, item_id, format=None):
        """
        Maneja solicitudes DELETE para eliminar lógicamente un elemento (marcar como inactivo).
        """
        found_item = None
        found_index = -1

        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                found_item = item
                found_index = i
                break

        if found_item:
            # Eliminación lógica: marcar como inactivo
            found_item['is_active'] = False
            data_list[found_index] = found_item # Actualizar la lista con el ítem modificado
            return Response(
                {"message": f"Elemento con ID {item_id} eliminado lógicamente (inactivado).", "data": found_item},
                status=status.HTTP_200_OK # O 204 No Content si no se devuelve nada
            )
        return Response(
            {"error": f"Elemento con ID {item_id} no encontrado para eliminar."},
            status=status.HTTP_404_NOT_FOUND
        )
