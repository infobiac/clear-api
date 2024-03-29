from django.shortcuts import render
from .models import Person, Contract, Verifier_Contract
from rest_framework import viewsets
from .serializers import PersonSerializer, ContractSerializer, Verifier_ContractSerializer
from django.http import HttpResponse
import heapq
import random
import networkx as nx
import pickle
from django.views.decorators.csrf import csrf_exempt
# from vython import *
from random import randint

UUID_not_name = True
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

def landing(request):
	return render(request,"landing.html")


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
	heapq.heapify(heap)
	for key, value in fin.items():
		heapq.heappush(heap, (-1 * value, random.random(), key))
	ret = [(i[2], i[0]*-1)for i in heapq.nsmallest(10, heap)]
	c = {'top_list':ret}
	return render(request, "score.html", c)

def get_graph():
	print("activating")
	contracts = Contract.objects.all()
	users = Person.objects.all()
	G = nx.Graph()
	for user in users:
		G.add_node(user.uuid)
	for contract in contracts:
		trues = []
		falses = []
		for verify in contract.verify.all():
			if verify.verified:
				trues.append(verify.verifier)
			else: 
				falses.append(verify.verifier)
		for v in trues:
			for w in trues:
				G.add_edge(v.uuid, w.uuid)
		for v in falses:
			for w in falses:
				G.add_edge(v.uuid, w.uuid)
	return G


def prscore(request):
	try:
		graph = pickle.load(open("graph.p", "rb"))
	except:
		graph = get_graph()
		pickle.dump(graph, open("graph.p", "wb"))
	print(graph)
	pr = nx.pagerank(graph)
	print(pr)

	fin = sorted([(val, key if UUID_not_name else Person.objects.get(uuid=key).name) for key, val in pr.items()], reverse = True)
	print(fin)
	num_to_display = 100
	resp = "<h2> Page Rank Based Scoring: top {}</h2>".format(num_to_display)
	count = 1
	for i in fin[0:num_to_display]:
		resp = "{} <p>{}. {}: {}</p>".format(resp, count, Person.objects.get(uuid=i[1]).name, i[0])
		count += 1

	return HttpResponse(resp)

# def get_contract(request):

# class Safe:    
#     value = public(wei_value()) #Value of the item
#     seller = public(address())
#     buyer = public(address())
#     unlocked = public(bool())
#     val = public(uint256())
#     #@constant
#     #def unlocked() -> bool: #Is a refund possible for the seller?
#     #    return (self.balance == self.value*2)

#     @public
#     @payable
#     def __init__():
#         assert (msg.value % 2) == 0
#         self.value = msg.value / 2  #The seller initializes the contract by
#             #posting a safety deposit of 2*value of the item up for sale.
#         self.seller = msg.sender
#         self.unlocked = True

#     @public
#     def abort():
#         assert self.unlocked #Is the contract still refundable?
#         assert msg.sender == self.seller #Only the seller can refund
#             # his deposit before any buyer purchases the item.
#         selfdestruct(self.seller) #Refunds the seller and deletes the contract.

#     @public
#     @payable
#     def purchase():
#         assert self.unlocked #Is the contract still open (is the item still up for sale)?
#         assert msg.value == (2 * self.value) #Is the deposit the correct value?
#         self.buyer = msg.sender
#         self.unlocked = False

#     @public
#     def received():
#         assert not self.unlocked #Is the item already purchased and pending confirmation
#             # from the buyer?
#         assert msg.sender == self.buyer
#         send(self.buyer, self.value) #Return the buyer's deposit (=value) to the buyer.
#         selfdestruct(self.seller) #Return the seller's deposit (=2*value)
#             # and the purchase price (=value) to the seller.
# @csrf_exempt
# def create_new_contract(request):
# 	if request.method == "GET":
# 		return render(request, "create.html", {})
# 	elif request.method == "POST":
# 		test = deploy(transpile(Safe))
# 		print(test["transactionHash"].hex())
# 		return HttpResponse("Contract complete. Transaction ID: {}".format(test["transactionHash"].hex()))
# 	return HttpResponse("unsupported method")

# def metatest(request):
# 	return render(request, "metatest.html", {})
