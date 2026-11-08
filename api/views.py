from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from api.models import FundoImobiliario
from api.serializers import FundoImobiliarioSerializer


class FundoImobiliarioListCreateAPIView(APIView):
    """
    Listar todos os fundos imobiliários ou cadastrar um novo fundo.
    """
    def get(self, request):
        fundos = FundoImobiliario.objects.all()
        serializer = FundoImobiliarioSerializer(fundos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FundoImobiliarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FundoImobiliarioDetailAPIView(APIView):
    """
    Detalhar, atualizar ou remover um fundo imobiliário específico.
    """
    def get_object(self, pk):
        try:
            return FundoImobiliario.objects.get(pk=pk)
        except FundoImobiliario.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        fundo = self.get_object(pk)
        serializer = FundoImobiliarioSerializer(fundo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        fundo = self.get_object(pk)
        serializer = FundoImobiliarioSerializer(fundo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        fundo = self.get_object(pk)
        fundo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
