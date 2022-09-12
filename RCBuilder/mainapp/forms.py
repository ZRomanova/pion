from django.forms import ModelForm
from .models import Subscription, MainForm

class SubscriptionForms(ModelForm):
	class Meta:
		model = Subscription
		fields = '__all__'

class MainFormForms(ModelForm):
	class Meta:
		model = MainForm
		fields = '__all__'
