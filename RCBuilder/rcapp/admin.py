from django.contrib import admin
from .models import ResultsChain, CompanyData, CompanyDataUserConnector, PageComment, Target, Resource, Activity, Output, OutputIndicator, Outcome, OutcomeIndicator, Impact, ImpactIndicator, TargetsListGroup, TargetsListItem, OutputIndicatorPF, OutcomeIndicatorPF, LibraryPage, UserRequest, HelpParagraph, BenchmarkingParametersQuery
# Register your models here.

admin.site.register(ResultsChain)

admin.site.register(Target)
admin.site.register(Resource)
admin.site.register(Activity)

admin.site.register(Output)
admin.site.register(OutputIndicator)
admin.site.register(OutputIndicatorPF)

admin.site.register(Outcome)
admin.site.register(OutcomeIndicator)
admin.site.register(OutcomeIndicatorPF)

admin.site.register(Impact)
admin.site.register(ImpactIndicator)

admin.site.register(TargetsListGroup)
admin.site.register(TargetsListItem)

admin.site.register(PageComment)
admin.site.register(CompanyData)
admin.site.register(CompanyDataUserConnector)

admin.site.register(LibraryPage)

class UserRequestAdmin(admin.ModelAdmin):
    exclude = ('password', 'password_repeat')

admin.site.register(UserRequest, UserRequestAdmin)

admin.site.register(HelpParagraph)

admin.site.register(BenchmarkingParametersQuery)