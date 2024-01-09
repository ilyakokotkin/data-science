from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .services import CSVReader, ShapiroWilkTest
import pandas as pd

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            uploaded_file = file_serializer.validated_data['file']
            csv_data = CSVReader.read_csv(uploaded_file)
            test_result = ShapiroWilkTest.perform_test(csv_data)

            return Response(test_result, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
