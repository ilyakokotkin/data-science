from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ['file']
