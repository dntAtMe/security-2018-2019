from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Payment(models.Model):
	title = models.CharField(max_length=100)
	content = models.CharField(max_length=500)
	value = models.FloatField()
	date_created = models.DateTimeField(default = timezone.now)
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	account = models.PositiveIntegerField(default=0)
	confirmed = models.BooleanField()

	def __str__(self):
		return self.title


	def clean(self):
		if str(self.value)[::-1].find('.') > 2 or self.value <= 0:
			raise ValidationError({'value': ['Not valid money value']})

		if len(str(self.account)) != 8:
			raise ValidationError({'account': ['Not valid account format ! Account number is 8 digit length.']})
