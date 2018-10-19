from django.shortcuts import render
from .models import Person, Contract, Verifier_Contract
from rest_framework import viewsets
from .serializers import PersonSerializer, ContractSerializer, Verifier_ContractSerializer
# Create your views here.

class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonSerializer

class ContractViewSet(viewsets.ModelViewSet):
	queryset = Contract.objects.all()
	serializer_class = ContractSerializer

class VerifierContractViewSet(viewsets.ModelViewSet):
	queryset = Verifier_Contract.objects.all()
	serializer_class = Verifier_ContractSerializer