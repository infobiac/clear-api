from django.db import models
import uuid
from verifier.models import Verifier
from verifiee.models import Verifiee
import verifiee.models
from django.forms import ModelForm
from django import forms
# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



class Contract(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	data = models.TextField()
	location = models.URLField(default=None, blank=True, null=True)
	owner = models.ForeignKey(Person, on_delete=models.PROTECT)
	#verifiers = models.ManyToManyField(Person)
	POSSIBLE_STATUSES = (
		('COMPLETE', 'Complete'),
		('PENDING', 'Pending'),
		('ERROR','Error')
		)
	status = models.CharField(max_length=10, choices=POSSIBLE_STATUSES)

	def __unicode__(self):
		return str(uuid)


class Verifier_Contract(models.Model):
	verifier = models.ForeignKey(Person, on_delete=models.PROTECT)
	contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name="verify")
	verified = models.BooleanField(blank=True, null=True)

	def __unicode__(self):
		return str()

class PendingContract(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	status = models.BooleanField(blank=True, null=True, default=False)
	linking_data = models.TextField()
	accepted = models.BooleanField(blank=True, null=True)
	VERIFICATION_TYPES = (
		('DEGREE', 'Education'),
		('SSN', 'Social Security Number'),
		('CREDIT','Credit Score'),
		('ADDRESS','Address'),
		('BIRTHDAY','Birthday'),
		)
	verification_type = models.CharField(max_length=8, choices=VERIFICATION_TYPES)
	verifier = models.ForeignKey(Verifier, on_delete=models.CASCADE)
	verifiee = models.ForeignKey(Verifiee, on_delete=models.CASCADE, blank=False, default="")
	address = models.CharField(max_length=10000)

class VerifieePendingContractForm(ModelForm):
	class Meta:
		model = PendingContract
		fields = ["linking_data", "verification_type", "verifier", "verifiee"]
		widgets = {
			"linking_data": forms.Textarea(attrs={"class":"form-control"}),
			"verification_type": forms.Select(attrs={"class":"form-control"}),
			"verifier": forms.Select(attrs={"class":"form-control"}),
			"verifiee": forms.HiddenInput(attrs={"class": "form-control"}),
		}

class VerifierPendingContractForm(ModelForm):
	class Meta:
		model = PendingContract
		fields = ["verifiee", "linking_data", "verification_type"]
		widgets = {
			"linking_data": forms.Textarea(attrs={"class":"form-control", "disabled":"disabled"}),
			"verification_type": forms.Select(attrs={"class":"form-control", "disabled":"disabled"}),
			"verifier": forms.HiddenInput(attrs={"class":"form-control", "disabled":"disabled"}),
			"verifiee": forms.Select(attrs={"class": "form-control", "disabled":"disabled"}),
			# "accepted": forms.NullBooleanSelect(attrs={"class":"form-control", "disabled":"disabled"})
		}

