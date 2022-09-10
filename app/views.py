from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from meta_craft_be import settings

# Create your views here.


@api_view(["GET"])
def index(request):
    return_data = {"success": True, "status": 200, "message": "Successful"}
    return Response(return_data)
