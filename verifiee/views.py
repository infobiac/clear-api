from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Verifiee, Verifiee_Address
from api.models import VerifieePendingContractForm, VerifierPendingContractForm, PendingContract
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
	if request.method == "POST":
		form = VerifieePendingContractForm(request.POST)
		print(form)
		print(form.is_valid())
		if form.is_valid():
			form.save()
		return HttpResponseRedirect("/verifiee/home")

	form = VerifieePendingContractForm()
	pendings = PendingContract.objects.filter(status=False)
	c = {"form":form, "pendings":pendings}
	return render(request, "verifiee_home.html", c)

def register_address(request):
	if request.method == "POST":
		verif = Verifiee.objects.get(pk=request.POST["usr"])
		v = Verifiee_Address(verifiee=verif, address=request.POST["addr"])
		v.save()
		return HttpResponse("Complete")
	verifiees = Verifiee.objects.all()
	return render(request, "register_verifiee.html", {"vs":verifiees})


@csrf_exempt
def name_from_uuid(request):
	addr = request.POST["addr"]
	try:
		verif_addr = Verifiee_Address.objects.get(address=addr)
		usr = Verifiee.objects.get(uuid=verif_addr.verifiee.uuid)
		ret = {"uuid":usr.uuid, "name": usr.name}
		return JsonResponse(ret)
	except:
		return HttpResponseRedirect("../register")