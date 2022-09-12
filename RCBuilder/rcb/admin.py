from django.contrib import admin
from .models import Description, Contact, SocialNetworkLink, Document, Page, TargetsHyperlink

# Register your models here.
admin.site.register(Description)
admin.site.register(Contact)
admin.site.register(SocialNetworkLink)
#admin.site.register(MyModel2)

admin.site.register(Document)
admin.site.register(Page)

admin.site.register(TargetsHyperlink)