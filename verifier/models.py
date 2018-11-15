from django.db import models
import uuid

# Create your models here.
class Verifier(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	def __str__(self):
		return self.name

class Verifier_Address(models.Model):
	verifier = models.ForeignKey(Verifier, on_delete=models.CASCADE)
	address = models.CharField(max_length=1000)