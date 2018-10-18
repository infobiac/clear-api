from django.db import models
import uuid

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



class Contract(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	data = models.TextField()
	location = models.URLField(default=None, blank=True, null=True)
	owner = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="whom")
	verifiers = models.ManyToManyField(Person, related_name="verifier")
	POSSIBLE_STATUSES = (
		('COMPLETE', 'Complete'),
		('PENDING', 'Pending'),
		('ERROR','Error')
		)
	status = models.CharField(max_length=10, choices=POSSIBLE_STATUSES)

	def __unicode__(self):
		return str(uuid)


# class Verifier_Contract(models.Model):
# 	verifier = models.ForeignKey(Person, on_delete=models.PROTECT)
# 	contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
# 	verified = models.BooleanField(blank=True, null=True)

# 	def __unicode__(self):
		return str(verifier)