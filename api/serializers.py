from .models import Person, Contract
from rest_framework import serializers

class PersonSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Person
		fields = ('name', 'email', 'uuid')

class ContractSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Contract
		fields = ('uuid', 'data', 'location', 'owner', 'verifiers', 'status')