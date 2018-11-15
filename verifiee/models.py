from django.db import models
import uuid

class Verifiee(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	def __str__(self):
		return self.name

class Verifiee_Address(models.Model):
	verifiee = models.ForeignKey(Verifiee, on_delete=models.CASCADE)
	address = models.CharField(max_length=1000)