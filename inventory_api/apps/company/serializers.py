from rest_framework import serializers
from .models import Company

class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)

class CompanyDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    address = AddressSerializer()

class CompanyCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    company_data = CompanyDataSerializer()

    class Meta:
        model = Company
        fields = ["name", "company_data"]

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

class CompanyCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_key"]

class CompanyRetrieveResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "status", "company_data", "created_at"]
        read_only_fields = fields

class CompanyUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    company_data = CompanyDataSerializer()

    class Meta:
        model = Company
        fields = ["name", "status", "company_data"]
        read_only_fields = ["company_key"]
    
    def update(self, instance, validated_data):
        
        if "name" in validated_data:
            instance.name = validated_data["name"]

        if "company_data" in validated_data:
            instance.company_data = validated_data["company_data"]

        instance.save(update_fields=list(validated_data.keys()))
        
        return instance