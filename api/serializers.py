from .models import Person, Contract, Verifier_Contract
from rest_framework import serializers

class PersonSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Person
		fields = ('name', 'email', 'uuid')

class Verifier_ContractSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Verifier_Contract
		fields = ("verifier", "contract", "verified")

class ContractSerializer(serializers.HyperlinkedModelSerializer):
	verify = Verifier_ContractSerializer(many=True, read_only=True)
	class Meta:
		model = Contract
		fields = ('uuid', 'data', 'location', 'owner', 'verify', 'status')