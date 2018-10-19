from django.shortcuts import render
from .models import Person, Contract, Verifier_Contract
from rest_framework import viewsets
from .serializers import PersonSerializer, ContractSerializer, Verifier_ContractSerializer
from django.http import HttpResponse
import heapq
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


def score(request):
	contracts = Contract.objects.all()
	fin = {}
	for contract in contracts:
		trues = 0
		falses = 0
		print(contract)
		for verifier in contract.verify.all():
			if verifier.verified: trues += 1
			else: falses += 1
		go = trues > falses
		for verify in contract.verify.all():
			if verify.verified == go:
				if verify.verifier in fin: fin[verify.verifier] += 1
	heap = []
	print(fin)
	heapq.heapify(heap)
	for key, value in fin.items():
		heapq.push(heap, (-1 * value, key))
	print(heap)
	fin = []
	while heap:
		temp = heapq.pop(fin)
		fin.append((temp[1], -1 * temp[0]))
	print(fin)
	c = {'l':fin}
	return render(request, "score.html", c)