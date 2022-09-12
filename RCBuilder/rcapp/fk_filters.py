from django import template
from .models import ResultsChain, Target, Resource, Activity, Output, OutputIndicator, OutputPlanFact, OutputMethod, Outcome, OutcomeIndicator, OutcomePlanFact, OutcomeMethod, Impact, ImpactIndicator, ImpactPlanFact

register = template.Library()

@register.filter
def with_ref_to_output(output_submodels, current_output_ref):
    return output_submodels.objects.filter(output_ref=current_output_ref)