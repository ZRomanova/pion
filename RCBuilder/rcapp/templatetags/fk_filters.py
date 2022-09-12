from django import template
from rcapp.models import ResultsChain, Target, Resource, Activity, Output, OutputIndicator, Outcome, OutcomeIndicator, Impact, ImpactIndicator, CompanyData, CompanyDataUserConnector

register = template.Library()

@register.filter
def with_ref_to_output(output_submodels, current_output_ref):
    return output_submodels.filter(output_ref=current_output_ref)

@register.filter
def with_ref_to_outcome(outcome_submodels, current_outcome_ref):
    return outcome_submodels.filter(outcome_ref=current_outcome_ref)

@register.filter
def with_ref_to_impact(impact_submodels, current_impact_ref):
    return impact_submodels.filter(impact_ref=current_impact_ref)

@register.filter
def with_ref_to_output_indicator(output_indicator_submodels, current_output_indicator_ref):
    return output_indicator_submodels.filter(output_indicator_ref=current_output_indicator_ref)

@register.filter
def with_ref_to_outcome_indicator(outcome_indicator_submodels, current_outcome_indicator_ref):
    return outcome_indicator_submodels.filter(outcome_indicator_ref=current_outcome_indicator_ref)

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def with_ref_to_company(rc, company_ref):
    return rc.filter(company_data_ref=company_ref)