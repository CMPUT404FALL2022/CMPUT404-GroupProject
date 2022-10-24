from rest_framework import serializers
from SocialDistribution.authors.models import single_author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = single_author
        fields = '__all__'