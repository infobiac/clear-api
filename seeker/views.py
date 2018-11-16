from django.shortcuts import render
from .models import Seeker, Seeker_Address
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def home(request):
	return render(request,"seeker_home.html", {})


def register_address(request):
	if request.method == "POST":
		seeker = Seeker.objects.get(pk=request.POST["usr"])
		v = Seeker_Address(seeker=seeker, address=request.POST["addr"])
		v.save()
		return HttpResponse("Complete")
	seekers = Seeker.objects.all()
	return render(request, "register_verifiee.html", {"vs":seekers})


def scanning_page(request):
	return render(request, "seeker_scan.html", {})


@csrf_exempt
def name_from_uuid(request):
	addr = request.POST["addr"]
	print(addr)
	try:
		s_addr = Seeker_Address.objects.get(address=addr)
		usr = Seeker.objects.get(uuid=s_addr.seeker.uuid)
		ret = {"uuid":usr.uuid, "name": usr.name, "addr":addr}
		print(ret)
		return JsonResponse(ret)
	except:
		return HttpResponseRedirect("../register")