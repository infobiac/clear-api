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
		for verifier in contract.verify.all():
			if verifier.verified: trues += 1
			else: falses += 1
		go = trues > falses
		
		for verify in contract.verify.all():
			if verify.verified == go:
				if verify.verifier in fin: fin[verify.verifier] += 1
				else: fin[verify.verifier] = 1
	heap = []
	print(fin)
	heapq.heapify(heap)
	for key, value in fin.items():
		heapq.heappush(heap, (-1 * value, key))
	ret = [(i[1], i[0]*-1)for i in heapq.nsmallest(10, heap)]
	c = {'top_list':ret}
	return render(request, "score.html", c)