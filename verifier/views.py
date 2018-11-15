from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Verifier, Verifier_Address
from api.models import VerifieePendingContractForm, VerifierPendingContractForm, PendingContract
from django.views.decorators.csrf import csrf_exempt


def home(request):
	if request.method == "POST":
		form = VerifierPendingContractForm(request.POST)
		print(form)
		print(form.is_valid())
		if form.is_valid():
			form.save()
		return HttpResponseRedirect("/verifier/home")
	pendings = PendingContract.objects.filter(status=False)
	completes = PendingContract.objects.filter(status=True)
	forms = []
	for pending in pendings:
		form = VerifierPendingContractForm(instance=pending)
		forms.append((pending.uuid, form))
	c = {"forms":forms, "pendings":pendings, "completes":completes}
	return render(request, "verifier_home.html", c)



def register_address(request):
	if request.method == "POST":
		verif = Verifier.objects.get(pk=request.POST["usr"])
		v = Verifier_Address(verifier=verif, address=request.POST["addr"])
		v.save()
		return HttpResponse("Complete")
	verifiers = Verifier.objects.all()
	return render(request, "register_verifiee.html", {"vs":verifiers})

@csrf_exempt
def name_from_uuid(request):
	addr = request.POST["addr"]
	try:
		verif_addr = Verifier_Address.objects.get(address=addr)
		usr = Verifier.objects.get(uuid=verif_addr.verifier.uuid)
		ret = {"uuid":usr.uuid, "name": usr.name}
		return JsonResponse(ret)
	except:
		return HttpResponse("""No verifier under your current metamask wallet! 
			Either register it, or select the right wallet and refresh""")


def accept(request):
	uuid = request.GET["id"]
	contract = PendingContract.objects.get(uuid=uuid)
	contract.status = True
	contract.accepted = True
	contract.save()
	return HttpResponseRedirect("/verifier/home")

def deny(request):
	uuid = request.GET["id"]
	contract = PendingContract.objects.get(uuid=uuid)
	contract.status = True
	contract.accepted = False
	contract.save()
	return HttpResponseRedirect("/verifier/home")