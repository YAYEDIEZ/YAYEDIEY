from rest_framework import serializers
from .models import Randonnee, Point, Photo

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'
        read_only_fields = ('id', 'timestamp')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ('id', 'timestamp')

class RandonneeSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Randonnee
        fields = '__all__'
        read_only_fields = ('id', 'date_debut', 'distance')

    def create(self, validated_data):
        return Randonnee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.titre = validated_data.get('titre', instance.titre)
        instance.description = validated_data.get('description', instance.description)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.save()
        return instance
