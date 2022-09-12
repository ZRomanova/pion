# _*_ coding: utf-8
from django.shortcuts import render, redirect, render_to_response
from django.views import generic
from django import forms
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, View
from .models import ResultsChain, PageComment, Target, Resource, Activity, Output, OutputIndicator, Outcome, OutcomeIndicator, Impact, ImpactIndicator, ResultsChainUserConnector, OutcomeIndicatorMethod, OutputIndicatorMethod, CompanyDataUserConnector, CompanyData, CompanyDataUserConnector, OutputIndicatorPF, OutcomeIndicatorPF, LibraryPage, UserRequest, HelpParagraph, BenchmarkingParametersQuery
from rcb.models import Contact, SocialNetworkLink, TargetsHyperlink
from django.contrib.auth.mixins import LoginRequiredMixin
import reportlab
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .forms import RCForm, PageCommentForm, TargetForm, ResourceForm, ActivityForm, OutputForm, OutcomeForm, ImpactForm, OutputIndicatorForm, OutcomeIndicatorForm, ImpactIndicatorForm, CompanyDataForm, TARGET_CHOISES, UserRequestCreateForm, OutputActivitiesForm, OutputSelectForm
from reportlab.lib.pagesizes import A4, landscape, cm, A3
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from django.views.generic.edit import FormMixin
from django.template.response import TemplateResponse
from django.forms.utils import ErrorList
from sys import stderr
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q
from functools import reduce
import re
from django.core.mail import send_mail
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from django.http import Http404
import json, urllib.parse
import requests

def get_soc_ress_dict():
    url = "http://base.socialvalue.ru/api/api.php"

    querystring = {"gettagslist":""}

    response = requests.request("GET", url, params=querystring)

    ldd = json.loads(response.text)
    soc_ress = ldd['Социальные результаты']
    return soc_ress

def get_soc_ress():
    soc_ress = get_soc_ress_dict()

    soc_ress_check = [soc_ress[ld] for ld in soc_ress]
    return soc_ress_check

def get_soc_res_id_by_text(text):
    soc_ress = get_soc_ress_dict()
    for soc_res in soc_ress:
        if soc_ress[soc_res] == text:
            return soc_res
    return -1

def get_instr_by_soc_res_id(id):
    if id == -1:
        return []
    url = "http://base.socialvalue.ru/api/api.php"

    querystring = {"tags":str(id)}

    response = requests.request("GET", url, params=querystring)

    instruments_json = json.loads(response.text)
    print(instruments_json)
    instr_dict = instruments_json["success"]
    return [instr_dict[idn]["title"] for idn in instr_dict]

def get_value_or_none(dictionary, key):
    try:
        return dictionary[key]
    except:
        return None

def update_last_seen(request):
    if request.user.is_authenticated:
        user_requests = UserRequest.objects.filter(username=request.user.username)
        if len(user_requests) > 0:
            user_request = user_requests[0]
            user_request.last_seen = datetime.datetime.now()
            user_request.save()


admins_list = ['priakni', 'rozinolga', 'tester1', 'validate', 'evdoa']

# Main Viewers
class RCsListView(LoginRequiredMixin, ListView):
    template_name = 'rcapp/rclistview.html'
    context_object_name = 'rcapp_archive'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(RCsListView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['allRCs'] = False
        orgs = CompanyDataUserConnector.objects.filter(user_ref=self.request.user)
        if len(orgs) != 0:
            context['organization_name'] = str(orgs[0].company_data_ref)
        user = self.request.user
        if user.username in admins_list:
            context['rcapp_archive_all'] = ResultsChain.objects.order_by('-pk')
            companies_displayed = []
            for rc in context['rcapp_archive_all']:
                if rc.company_data_ref is not None:
                    companies_displayed.append(rc.company_data_ref)
            companies_displayed = set(companies_displayed)
            all_companies = set(CompanyData.objects.all())
            companies_not_displayed = all_companies - companies_displayed
            context['companies_not_displayed'] = list(companies_not_displayed)


        return context
    def get_queryset(self):
        users_connectors = ResultsChainUserConnector.objects.filter(user_ref = self.request.user)
        users_rcs = [connector.rc_ref.pk for connector in users_connectors]
        return ResultsChain.objects.filter(Q(user=self.request.user) | Q(pk__in=users_rcs)).distinct().order_by('-formation_date')
    def get(self, request, *args, **kwargs):
        return super(ListView, self).get(self, request, *args, **kwargs)

frequency_texts = ["", "год", "полгода", "3 раза", "квартал", "5", "6", "7", "8", "9", "10", "11", "месяц"]

class RCView(generic.DetailView):
    template_name = 'rcapp/rcview.html'
    model = ResultsChain
    # form_class = PageCommentForm
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(RCView, self).get_context_data(**kwargs)
        context['delete_link'] = "edit/" + self.kwargs['pk'] + "/delete"
        context['is_authenticated'] = self.request.user.is_authenticated
        if self.request.user.is_authenticated:
            context['is_my'] = self.request.user == context['object'].user or (self.request.user.username in admins_list) or self.request.user.pk == 15
            connectors = ResultsChainUserConnector.objects.filter(user_ref = self.request.user).filter(rc_ref = context['object']).count()
            if connectors > 0:
                context['is_my'] = True
        else:
            context['is_my'] = False
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['target'] = Target.objects.filter(rc_ref = context['object'])
        context['resource'] = Resource.objects.filter(rc_ref = context['object'])
        context['activity'] = Activity.objects.filter(rc_ref = context['object'])
        if context['object'].company_data_ref and context['object'].company_data_ref is not None:
            context['organization'] = CompanyData.objects.get(pk = context['object'].company_data_ref.pk)
        outputs = Output.objects.filter(rc_ref = context['object'])
        outputs_table = []
        outputs_table.append(['Результат', 'Показатель', 'План/Факт', 'Частота сбора', 'Метод 1', 'Метод 2', 'Метод 3'])
        current_line = 1
        for output in outputs:
            outputs_table.append([])
            output_line = current_line
            outputs_table[output_line].append(output.value if output.value != "custom" else output.custom_value)
            outputs_indicators = OutputIndicator.objects.filter(rc_ref = context['object']).filter(output_ref = output)
            for output_indicator in outputs_indicators:
                if current_line > output_line:
                    outputs_table.append([])
                    outputs_table[current_line].append(output.value if output.value != "custom" else output.custom_value)
                outputs_table[current_line].append(('<i class="fa fa-paperclip" aria-hidden="true"></i> ' if output_indicator.source_file or output_indicator.method_file else '') + (output_indicator.value if output_indicator.value != "custom" else output_indicator.custom_value))
                outputs_table[current_line].append(str(output_indicator.plan if output_indicator.plan is not None and output_indicator.plan.strip() != "" else "–") + "/" + str(output_indicator.fact if output_indicator.fact is not None and output_indicator.fact.strip() != "" else "–"))
                outputs_table[current_line].append(frequency_texts[output_indicator.frequency if output_indicator.frequency is not None else 0])
                outputs_table[current_line].append(output_indicator.method if output_indicator.method != "custom" else output_indicator.custom_method)
                outputs_table[current_line].append(output_indicator.method2 if output_indicator.method2 != "custom" else output_indicator.custom_method2)
                outputs_table[current_line].append(output_indicator.method3 if output_indicator.method3 != "custom" else output_indicator.custom_method3)
                current_line += 1
            if len(outputs_indicators) == 0:
                outputs_table[current_line].append("")
                outputs_table[current_line].append("")
                outputs_table[current_line].append("")
                current_line += 1
            
        context['outputs_table'] = outputs_table
        
        outcomes = Outcome.objects.filter(rc_ref = context['object'])
        outcomes_table = []
        outcomes_table.append(['Результат', 'Показатель', 'План/Факт', 'Период', 'Метод'])
        current_line = 1
        for outcome in outcomes:
            outcomes_table.append([])
            outcome_line = current_line
            outcomes_table[outcome_line].append(outcome.value if outcome.value != "custom" else outcome.custom_value)
            outcomes_indicators = OutcomeIndicator.objects.filter(rc_ref = context['object']).filter(outcome_ref = outcome)
            for outcome_indicator in outcomes_indicators:
                if current_line > outcome_line:
                    outcomes_table.append([])
                    outcomes_table[current_line].append(outcome.value if outcome.value != "custom" else outcome.custom_value)
                outcomes_table[current_line].append(('<i class="fa fa-paperclip" aria-hidden="true"></i> ' if outcome_indicator.source_file or outcome_indicator.method_file else '') + (outcome_indicator.value if outcome_indicator.value != "custom" else outcome_indicator.custom_value))
                outcomes_table[current_line].append(str(outcome_indicator.plan if outcome_indicator.plan is not None and outcome_indicator.plan.strip() != "" else "–") + "/" + str(outcome_indicator.fact if outcome_indicator.fact is not None and outcome_indicator.fact.strip() != "" else "–"))
                outcomes_table[current_line].append(frequency_texts[outcome_indicator.frequency if outcome_indicator.frequency is not None else 0])
                outcomes_table[current_line].append(outcome_indicator.method if outcome_indicator.method != "custom" else outcome_indicator.custom_method)
                current_line += 1
            if len(outcomes_indicators) == 0:
                outcomes_table[current_line].append("")
                outcomes_table[current_line].append("")
                outcomes_table[current_line].append("")
                current_line += 1
        context['outcomes_table'] = outcomes_table
        
        impacts = Impact.objects.filter(rc_ref = context['object'])
        impacts_table = []
        impacts_table.append(['Результат', 'Показатель', 'План/Факт', 'Период'])
        current_line = 1
        for impact in impacts:
            impacts_table.append([])
            impact_line = current_line
            impacts_table[impact_line].append(impact.value if impact.value != "custom" else impact.custom_value)
            impacts_indicators = ImpactIndicator.objects.filter(rc_ref = context['object']).filter(impact_ref = impact)
            for impact_indicator in impacts_indicators:
                if current_line > impact_line:
                    impacts_table.append([])
                    impacts_table[current_line].append(impact.value if impact.value != "custom" else impact.custom_value)
                impacts_table[current_line].append(('<i class="fa fa-paperclip" aria-hidden="true"></i> ' if impact_indicator.source_file else '') + (impact_indicator.value if impact_indicator.value != "custom" else impact_indicator.custom_value))
                impacts_table[current_line].append(str(impact_indicator.plan if impact_indicator.plan is not None and impact_indicator.plan.strip() != "" else "–") + "/" + str(impact_indicator.fact if impact_indicator.fact is not None and impact_indicator.fact.strip() != "" else "–"))
                impacts_table[current_line].append(frequency_texts[impact_indicator.frequency if impact_indicator.frequency is not None else 0])
                current_line += 1
            if len(impacts_indicators) == 0:
                impacts_table[current_line].append("")
                impacts_table[current_line].append("")
                impacts_table[current_line].append("")
                current_line += 1
        context['impacts_table'] = impacts_table
        return context

class RCDelete(generic.DeleteView):
    model = ResultsChain
    template_name = 'rcapp/common_delete_form.html'
    success_url = "/portal/"

# RC
class RCCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/rccreate.html'
    form_class = RCForm
    model = ResultsChain
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(RCCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        company_connectors = CompanyDataUserConnector.objects.filter(user_ref=self.request.user)
        company_pks = [company_connector.company_data_ref.pk for company_connector in company_connectors]
        is_admin = (self.request.user.username in admins_list) or (self.request.user.pk == 15)
        if not is_admin:
            context['form'].fields["company_data_ref"].queryset = CompanyData.objects.filter(pk__in=company_pks)
        helper_data = HelpParagraph.objects.filter(special_name="rc_before")
        with_help = get_value_or_none(self.request.GET, 'with_help')
        if with_help is not None and with_help.lower() == "true":
            context['display_helpers'] = True
            with_help = True
        else:
            with_help = False
        # with_help can be used later to pass different helpers
        if len(helper_data) != 0:
            full_content = helper_data[0].full_content
            if full_content:
                context['helper_before'] = full_content
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.website == 'http://':
            self.object.website = ''
        self.object.user = self.request.user
        self.object.save()
        with_help = get_value_or_none(self.request.GET, 'with_help')
        if with_help is not None and with_help.lower() == "true":
            with_help = True
        else:
            with_help = False
        if with_help:
            return redirect(self.object.get_edit_url() + "?with_help=true")
        else:
            return redirect(self.object.get_edit_url())
    def get_initial(self):
        # call super if needed
        return {'website': 'http://'}

class RCEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/rcedit.html'
    model = ResultsChain
    form_class    = RCForm
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(RCEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['target'] = Target.objects.filter(rc_ref = context['object'])
        context['resource'] = Resource.objects.filter(rc_ref = context['object'])
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['activity'] = Activity.objects.filter(rc_ref = context['object'])
        context['output'] = Output.objects.filter(rc_ref = context['object'])
        context['output_indicator'] = OutputIndicator.objects.filter(rc_ref = context['object'])
        context['output_indicator_methods'] = OutputIndicatorMethod.objects.filter(output_indicator_ref__in=[ind.pk for ind in context['output_indicator']])
        context['outcome'] = Outcome.objects.filter(rc_ref = context['object'])
        context['outcome_indicator'] = OutcomeIndicator.objects.filter(rc_ref = context['object'])
        context['outcome_indicator_methods'] = OutcomeIndicatorMethod.objects.filter(outcome_indicator_ref__in=[ind.pk for ind in context['outcome_indicator']])
        context['impact'] = Impact.objects.filter(rc_ref = context['object'])
        context['impact_indicator'] = ImpactIndicator.objects.filter(rc_ref = context['object'])
        context['users'] = User.objects.exclude(pk = self.request.user.pk).exclude(pk = context['object'].user.pk)
        company_connectors = CompanyDataUserConnector.objects.filter(user_ref=self.request.user)
        company_pks = [company_connector.company_data_ref.pk for company_connector in company_connectors]
        is_admin = (self.request.user.username in admins_list) or (self.request.user.pk == 15)
        if not is_admin:
            context['form'].fields["company_data_ref"].queryset = CompanyData.objects.filter(pk__in=company_pks)
        with_help = get_value_or_none(self.request.GET, 'with_help')
        if with_help is not None and with_help.lower() == "true":
            context['display_helpers'] = True
            with_help = True
        else:
            with_help = False
        helper_paragraphs = HelpParagraph.objects.order_by('order')
        # with_help can be used later to pass different helpers
        helper_data = HelpParagraph.objects.filter(special_name="rc_before")
        if len(helper_data) != 0:
            full_content = helper_data[0].full_content
            if full_content:
                context['helper_before'] = full_content
                context['helper_before_x'] = [i for i, j in enumerate(helper_paragraphs) if j.pk == helper_data[0].pk][0]
        target_data = HelpParagraph.objects.filter(special_name="target")
        if len(target_data) != 0:
            full_content = target_data[0].full_content
            if full_content:
                context['target_before'] = full_content
                context['target_before_x'] = [i for i, j in enumerate(helper_paragraphs) if j.pk == target_data[0].pk][0]
        resources_data = HelpParagraph.objects.filter(special_name="resources")
        if len(resources_data) != 0:
            full_content = resources_data[0].full_content
            if full_content:
                context['resource_before'] = full_content
                context['resource_before_x'] = [i for i, j in enumerate(helper_paragraphs) if j.pk == resources_data[0].pk][0]
        activity_before = HelpParagraph.objects.filter(special_name="activity")
        if len(activity_before) != 0:
            full_content = activity_before[0].full_content
            if full_content:
                context['activity_before'] = full_content
                context['activity_before_x'] = [i for i, j in enumerate(helper_paragraphs) if j.pk == activity_before[0].pk][0]
        outputs_before = HelpParagraph.objects.filter(special_name="output")
        if len(outputs_before) != 0:
            full_content = outputs_before[0].full_content
            if full_content:
                context['outputs_before'] = full_content
                context['outputs_before_x'] = [i for i, j in enumerate(helper_paragraphs) if j.pk == outputs_before[0].pk][0]
        outcome_before = HelpParagraph.objects.filter(special_name="outcome")
        if len(outcome_before) != 0:
            full_content = outcome_before[0].full_content
            if full_content:
                context['outcome_before'] = full_content
                context['outcome_before_x'] = [i for i, j in enumerate(helper_paragraphs) if j.pk == outcome_before[0].pk][0]
        impact_before = HelpParagraph.objects.filter(special_name="impact")
        if len(impact_before) != 0:
            full_content = impact_before[0].full_content
            if full_content:
                context['impact_before'] = full_content
                context['impact_before_x'] = [i for i, j in enumerate(helper_paragraphs) if j.pk == impact_before[0].pk][0]
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        #return redirect("/portal/" + str(context[object].pk))
        self.object = form.save(commit=False)
        if self.object.website == 'http://':
            self.object.website = ''
        self.object.save()
        return redirect(self.object.get_absolute_url())

# Target
class TargetCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = TargetForm
    model = Target
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(TargetCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['step'] = 0
        targets = TARGET_CHOISES + (('custom', 'Введите свой вариант'),)
        context['form'].fields['value'].widget.choices = targets
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#targets-table")

class TargetDelete(generic.DeleteView):
    model = Target
    template_name = 'rcapp/common_delete_form.html'
    # success_url = "/portal/"
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

class TargetEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = TargetForm
    model = Target
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(TargetEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        company_ref = context['results_chain'].company_data_ref
        if company_ref is not None:
            other_rcs = ResultsChain.objects.filter(company_data_ref = company_ref.pk)
            other_tgts = Target.objects.filter(rc_ref__in = [other_rc.pk for other_rc in other_rcs]).filter(value="custom")
        else:
            other_tgts = []
        custom_targets = ()
        for other_tgt in other_tgts:
            custom_targets += ((other_tgt.custom_value, other_tgt.custom_value),)
        custom_targets = ('Ранее созданные целевые группы', custom_targets)
        targets = TARGET_CHOISES
        targets += ((custom_targets),)
        targets += (('custom', 'Введите свой вариант'),)
        context['form'].fields['value'].widget.choices = targets
        context['step'] = 0
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#targets-table")

# Resource
class ResourceCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = ResourceForm
    model = Resource
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ResourceCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['step'] = 1
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#resources-table")

class ResourceDelete(generic.DeleteView):
    model = Resource
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

class ResourceEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = ResourceForm
    model = Resource
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ResourceEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['step'] = 1
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#resources-table")

# Activity
class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = ActivityForm
    model = Activity
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ActivityCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["target_refs"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 2
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#activities-table")

class ActivityDelete(generic.DeleteView):
    model = Activity
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

class ActivityEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = ActivityForm
    model = Activity
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ActivityEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["target_refs"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 2
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#activities-table")

# Output
class OutputCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = OutputForm
    model = Output
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutputCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["target_ref"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 3
        context['is_output'] = True
        context['form'].fields["activity_refs"].queryset = Activity.objects.filter(rc_ref=self.kwargs['rc'])
        # Get activities here
        # activities = Activity.objects.filter(rc_ref=context['results_chain'].pk)
        # activities_choises = [[None, 'Выберите из списка']]
        # for activity in activities:
        #     activities_choises.append([str(activity.pk), activity.value])
        # context['activities_choises'] = activities_choises
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        other_outputs = Output.objects.filter(rc_ref = self.object.rc_ref.pk).order_by('-order')
        if len(other_outputs) > 0:
            self.object.order = other_outputs[0].order + 100
        else:
            self.object.order = 0
        # if self.request.POST.get('activity_ref') != None and self.request.POST.get('activity_ref') != '' and self.request.POST.get('activity_ref') != 'None':
        #     self.object.activity_ref = Activity.objects.get(pk=self.request.POST.get('activity_ref'))
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
            form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outputs-table")

class OutputDelete(generic.DeleteView):
    model = Output
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

class OutputEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = OutputForm
    model = Output
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutputEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['step'] = 3
        context['is_output'] = True
        context['form'].fields["activity_refs"].queryset = Activity.objects.filter(rc_ref=self.kwargs['rc'])
        # 
        activities = Activity.objects.filter(rc_ref=self.kwargs['rc'])
        outputs = Output.objects.filter(activity_refs__in = activities)
        output_names = []
        for output in outputs:
            output_name = output.value
            if output_name == "custom":
                output_name = output.custom_value
            if output_name is None or output_name == "":
                continue
            output_names.append((output_name, output_name))
        output_names.append(('custom', 'Введите свой вариант'))
        choices=tuple(output_names)
        context['form'].fields["value"].widget = forms.Select(choices=choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        # Get activities here
        # activities = Activity.objects.filter(rc_ref=context['results_chain'].pk)
        # activities_choises = [[None, 'Выберите из списка']]
        # for activity in activities:
        #     activities_choises.append([str(activity.pk), activity.value])
        # context['activities_choises'] = activities_choises
        # if Output.objects.get(pk = self.kwargs['pk']).activity_ref != None:
        #     context['selected_pk'] = str(Output.objects.get(pk = self.kwargs['pk']).activity_ref.pk)
        # context['selected_ay'] = str(Output.objects.get(pk = self.kwargs['pk']).activity_ref)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        # if self.request.POST.get('activity_ref') != None and self.request.POST.get('activity_ref') != '' and self.request.POST.get('activity_ref') != 'None':
        #     self.object.activity_ref = Activity.objects.get(pk=self.request.POST.get('activity_ref'))
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
            form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outputs-table")

# Outcome
class OutcomeCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = OutcomeForm
    model = Outcome
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutcomeCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        
        # context['form'].fields["target_ref"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        context['form'].fields["output_refs"].queryset = Output.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 4
        context['is_outcome'] = True
        # outputs = Output.objects.filter(rc_ref=context['results_chain'].pk)
        # outputs_choises = [[None, 'Выберите из списка']]
        # for output in outputs:
        #     outputs_choises.append([str(output.pk), output.value if output.value != "custom" else output.custom_value])
        # context['outputs_choises'] = outputs_choises
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        other_outcomes = Outcome.objects.filter(rc_ref = self.object.rc_ref.pk).order_by('-order')
        if len(other_outcomes) > 0:
            self.object.order = other_outcomes[0].order + 100
        # if self.request.POST.get('output_ref') != None and self.request.POST.get('output_ref') != '' and self.request.POST.get('output_ref') != 'None':
        #     self.object.output_ref = Output.objects.get(pk=self.request.POST.get('output_ref'))
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
            form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outcomes-table")

class OutcomeDelete(generic.DeleteView):
    model = Outcome
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

class OutcomeEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = OutcomeForm
    model = Outcome
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutcomeEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["output_refs"].queryset = Output.objects.filter(rc_ref=self.kwargs['rc'])
        # context['form'].fields["target_ref"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        # context['form'].fields["output_ref"].queryset = Output.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 4
        context['is_outcome'] = True
        # outputs = Output.objects.filter(rc_ref=context['results_chain'].pk)
        # outputs_choises = [[None, 'Выберите из списка']]
        # for output in outputs:
        #     outputs_choises.append([str(output.pk), output.value if output.value != "custom" else output.custom_value])
        # context['outputs_choises'] = outputs_choises
        # if Outcome.objects.get(pk = self.kwargs['pk']).output_ref != None:
        #     context['selected_pk'] = str(Outcome.objects.get(pk = self.kwargs['pk']).output_ref.pk)
        # context['selected_ay'] = str(Outcome.objects.get(pk = self.kwargs['pk']).output_ref)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        # if self.request.POST.get('output_ref') != None and self.request.POST.get('output_ref') != '' and self.request.POST.get('output_ref') != 'None':
        #     self.object.output_ref = Output.objects.get(pk=self.request.POST.get('output_ref'))
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
            form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outcomes-table")

# Impact
class ImpactCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = ImpactForm
    model = Impact
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ImpactCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["target_ref"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        context['form'].fields["outcome_refs"].queryset = Outcome.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 5
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        other_impacts = Impact.objects.filter(rc_ref = self.object.rc_ref.pk).order_by('-order')
        if len(other_impacts) > 0:
            self.object.order = other_impacts[0].order + 100
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
            form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#impacts-table")

class ImpactDelete(generic.DeleteView):
    model = Impact
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

class ImpactEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = ImpactForm
    model = Impact
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ImpactEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["target_ref"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        context['form'].fields["outcome_refs"].queryset = Outcome.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 5
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
            form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#impacts-table")

# Indicators create
class OutputIndicatorCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = OutputIndicatorForm
    model = OutputIndicator
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutputIndicatorCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['parent_entity'] = Output.objects.get(pk=self.kwargs['parent'])
        context['parent_entity_name'] = context['parent_entity']._meta.verbose_name.title()
        context['step'] = 3
        context['show_methods'] = True
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        self.object.output_ref = Output.objects.get(pk=self.kwargs['parent'])
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
            OutputIndicatorPF.objects.create(plan=self.object.plan, fact=self.object.fact, year=self.object.year, output_indicator_ref=self.object)
            methods_names = self.request.POST.getlist('methods')
            for method in methods_names:
                if method is not None and method.strip() != '':
                    OutputIndicatorMethod.objects.create(value=method, output_indicator_ref=self.object)
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outputs-table")

class OutputIndicatorDelete(generic.DeleteView):
    model = OutputIndicator
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

OUTCOME_INDICATORS = [['Результат', 'Наименование показателя'], ['Повышение уровня готовности женщин к материнству', 'Число женщин, у которых повысился уровень готовности к материнству'], ['Увеличение доли (или числа) детей, воспитываемых в кровных семьях / Сокращение случаев изъятий', 'Доля детей, воспитывающихся в кровных семьях (от числа заявленных намерений отказа от новорожденных детей в роддомах на период реализации проекта) '], ['Сокращение доли (числа) детей, изъятых из кровных семей', 'Число детей, в отношении которых снижен риск отказа', 'число детей, изъятых из кровных семей', '- рождённых детей у беременных женщин в ТЖС и воспитывающихся в кровной семье ', '- детей из числа семей в ТЖС, возвращённых в кровную семью', 'Количество детей в возрасте от 0 до 5 лет, временно размещенных в доме ребенка, возвращенных в кровную семью', 'доля / число предотвращенных случаев изъятия детей из кровных семей', 'Число (доля) детей, сохраненных в кровных семьях'], ['Повышение уровня поддержки кровных семей со стороны окружения (родственники, друзья, школы, детские сады, соседи и пр.)', 'увеличение уровня поддержки со стороны различных групп окружения'], ['Улучшение отношений кровных семей со своим социальным окружением', 'Доля семей, улучшивших (отмечающих улучшение) в отношениях со своим социальным окружением'], ['Увеличение численности профессиональных замещающих семей', 'Число подготовленных замещающих родителей', 'Число семей, прошедших подготовку И принявших на воспитание детей'], ['Изменение (сокращение) доли (числа) случаев возврата детей из приемных семей', 'доля (или число) случаев возврата детей из замещающих семей на контрольные периоды', 'Число детей, возвращенных в детские учреждения из сопровождаемых замещающих семей'], ['Повышение уровня поддержки приемных семей со стороны окружения (родственники, друзья, школы, детские сады, соседи и пр.)', 'увеличение уровня поддержки со стороны различных групп – соседей, родственников, друзей, коллег и пр. '], ['Улучшение отношений приемных семей со своим социальным окружением', 'Доля семей, отмечающих улучшение в отношениях со своим социальным окружением'], ['Улучшение социального, материального, экономического положения семей / родителей', 'Число женщин в ТЖС, воспитывающих детей, улучшивших своё социальное положение ', 'Количество семей, у которых улучшилось материально-экономическое положение  '], ['Сокращение доли (числа) семей, находящихся в СОП', 'Динамика снижения риска, %'], ['Повышение доступности профессиональных услуг для семей и детей', 'число семей / детей, которые получили новые услуги ', 'число организаций / специалистов, оказывающих профессиональные услуги по различным категориям ЦГ на число жителей / численность ЦГ за учетные периоды'], ['Улучшение детско-родительских отношений ', 'Число детей, отмечающих улучшения в отношениях с родителями', 'число (доля) семей, в которых наблюдается улучшение детско-родительских отношений'], ['Улучшение психологического климата в семье', 'Число / доля сопровождаемых семей, у которых наблюдается улучшение психологического климата в семье ', 'Число / доля семей, отметивших улучшение коммуникативных навыков внутри семьи'], ['Улучшение эмоционального состояния членов семьи (родителя / ребенка)', 'Доля семей, отметивших улучшение эмоционального состояния внутри семьи'], ['Повышение уровня педагогических (родительских) компетенций', 'Число / доля семей, у которых наблюдается развитие родительских компетенций ', 'Количество родителей, ответственно исполняющих родительские функции '], ['Улучшение коммуникативных навыков родителей в отношении ребенка', 'Доля семей, отмечающих улучшение коммуникативных навыков с ребенком'], ['увеличение числа детей, воспитываемых на СФУ', 'доля / число детей, устроенных на семейные формы устройства', 'Число детей, принятых на воспитание в семьи '], ['Сокращение количества нарушений прав детей', 'Количество детей / случаев, в отношении которых предотвращено нарушение прав '], ['Снижение угрозы жизни и здоровью ребенка в ситуациях жестокого обращения в семье ', 'Количество детей, в отношении которых оперативно предотвращена угроза жизни и здоровью в ситуациях жестокого обращения в семье '], ['Повышение уровня базовых потребностей детей', 'Количество детей, у которых повысился уровень удовлетворения базовых потребностей'], ['Улучшение физического состояния детей', 'доля / число детей, у которых изменились установки в отношении здорового образа жизни ', 'доля / число детей, у которых снизилась заболеваемость '], ['Изменение установок (поведения) детей в отношении здорового образа жизни ', 'Число детей, уделяющих внимание собственному здоровью'], ['Улучшение психологического состояния детей', 'Доля детей, повысивших психологический уровень развития'], ['Снижение уровня агрессии у детей', 'Число детей, у которых снижен уровень агрессии '], ['Повышение уровня развития и навыков у детей', 'доля / число детей, у которых улучшились показатели успеваемости ', 'доля / число детей, у которых улучшился уровень моторики и пр. ', 'доля/ число детей, у которых наблюдается развитие речи', 'доля / число детей, у которых улучшились социальные навыки ', 'доля/ число детей, у которых улучшились когнитивные способности', 'число случаев задержек в развитии детей на контрольные периоды'], ['Улучшение успеваемости детей', 'доля / число детей, у которых улучшились показатели успеваемости '], ['Развитие речи у детей', 'Доля детей, у которых наблюдается развитие речи'], ['Улучшение когнитивных способностей детей', 'Доля детей, у которых наблюдается развитие когнитивных способностей'], ['Улучшение эмоционального состояния детей', 'Доля семей, отметивших улучшение эмоционального состояния ребенка'], ['Улучшение коммуникативных навыков детей ', 'Число / доля детей улучшивших коммуникативные навыки'], ['Эмоциональное развитие детей', 'Число детей, повысивших свое эмоциональное развитие'], ['Улучшение уровня социальных навыков у детей', 'Число детей, конструктивно взаимодействующих с ровесниками, друзьями  ', 'Число детей, конструктивно взаимодействующих со взрослыми: родителями, учителями, близкими', 'Число / доля детей, повысивших социальные навыки'], ['Повышение уровня готовности детей к самостоятельной жизни в обществе', 'доля / число детей, у которых улучшились показатели готовности / адаптации к жизни в обществе ', 'доля / число детей, у которых повысился уровень владения социальными навыками ', 'доля / число детей, у которых улучшилось психическое состояние ', 'Число детей, справляющихся с трудностями, согласно своему возрасту ', 'Число детей, умеющих восстанавливать силы / отдыхать', 'Число детей, проявляющих желание жить и развиваться '], ['Расширение участия детей в позитивной, социально одобряемой деятельности ', 'Число детей, уделяющих время социально одобряемым  хобби и увлечениям'], ['Повышение уровня адаптации детей к школе ', 'Количество детей, у которых сформированы навыки поведения в школе'], ['Увеличение числа детей с ОВЗ, посещающих общеобразовательные школы', 'Доля детей с ОВЗ, адаптировавшихся к обучению в школе, %'], ['Развитие санитарно-гигиенических навыков у детей', 'Доля детей, у которых наблюдается развитие санитарно-гигиенических навыков, %'], ['Повышение информированности (осведомленности) целевых групп по вопросу…', 'Число информационных кампаний, реализованных в рамках программы', 'Число сообщений в СМИ, инициированных в рамках программы ', 'Число публичных мероприятий, организованных или поддержанных в рамках проекта, на которых представлен и распространен опыт организации / Программы', 'Уровень информированности, осведомленности стейкхолдеров о проблеме'], ['Повышение уровня информированности (осведомленности) стейкхолдеров  о программе', 'Уровень информированности, осведомленности стейкхолдеров о программе на контрольные периоды'], ['Повышение уровня удовлетворенности стейкхолдеров', 'Уровень удовлетворенности стейкхолдеров ', 'Уровень удовлетворенности благополучателей ', 'число / доля семей / детей, обращающихся по рекомендации на отчетные периоды', 'число/доля семей, отказавшихся от получения услуг в процессе их оказания на отчетные периоды', 'Динамика сложившихся за год новых партнерств'], ['Развитие компетенций и навыков специалистов', 'Число подготовленных специалистов, применяющих полученные знания и навыки', 'число/доля специалистов, у которых повысился уровень компетенций / навыков '], ['Повышение доступности профессиональных знаний для специалистов', 'Число изданных информационных (методических) материалов', 'Чило (или тираж) распространенных печатных информационно-методических материалов для профессионалов.', 'Число просветительских/обучающих мероприятий для специалистов'], ['Изменение установок специалистов', 'Число специалистов, изменивших свои установки при работе с ЦГ']]

class OutcomeIndicatorCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = OutcomeIndicatorForm
    model = OutcomeIndicator
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutcomeIndicatorCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        outcome = Outcome.objects.get(pk=self.kwargs['parent'])
        context['parent_entity'] = outcome
        context['parent_entity_name'] = context['parent_entity']._meta.verbose_name.title()
        context['step'] = 4
        context['show_methods'] = True
        resulting_choices_html = '<option value="">Выберите</option>'
        for line in OUTCOME_INDICATORS:
            if context['parent_entity'].value.lower().strip() == line[0].lower().strip():
                for ind in line[1:]:
                    resulting_choices_html += '<option value="'+ ind +'">'+ind+'</option>'
                break
        resulting_choices_html += '<option value="custom" style="display: none;">Введите свой вариант</option>'
        context['resulting_choices_html'] = resulting_choices_html
        outcome_name = (outcome.value if outcome.value != "custom" else outcome.custom_value)
        outcome_id = get_soc_res_id_by_text(outcome_name)
        get_methods_list = get_instr_by_soc_res_id(outcome_id)

        methods_choices_names = []
        for methods_name in get_methods_list:
            if methods_name is None or methods_name == "":
                continue
            methods_choices_names.append((methods_name, methods_name))
        methods_choices_names.append(('custom', 'Введите свой вариант'))
        methods_choices=tuple(methods_choices_names)

        context['form'].fields["method"].widget  = forms.Select(choices=methods_choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        context['form'].fields["method2"].widget = forms.Select(choices=methods_choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        context['form'].fields["method3"].widget = forms.Select(choices=methods_choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        # if self.object.custom_value != None and self.object.custom_value != "":
        #     self.object.value = "custom"
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        self.object.outcome_ref = Outcome.objects.get(pk=self.kwargs['parent'])
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
            OutcomeIndicatorPF.objects.create(plan=self.object.plan, fact=self.object.fact, year=self.object.year, outcome_indicator_ref=self.object)
            methods_names = self.request.POST.getlist('methods')
            for method in methods_names:
                if method is not None and method.strip() != '':
                    OutcomeIndicatorMethod.objects.create(value=method, outcome_indicator_ref=self.object)
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outcomes-table")

class OutcomeIndicatorDelete(generic.DeleteView):
    model = OutcomeIndicator
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

class ImpactIndicatorCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = ImpactIndicatorForm
    model = ImpactIndicator
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ImpactIndicatorCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['parent_entity'] = Impact.objects.get(pk=self.kwargs['parent'])
        context['parent_entity_name'] = context['parent_entity']._meta.verbose_name.title()
        context['step'] = 5
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        self.object.impact_ref = Impact.objects.get(pk=self.kwargs['parent'])
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#impacts-table")

class ImpactIndicatorDelete(generic.DeleteView):
    model = ImpactIndicator
    template_name = 'rcapp/common_delete_form.html'
    def get_success_url(self):
        return "/portal/edit/" + str(self.object.rc_ref.pk)

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)
# Indicator editors
class OutputIndicatorEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = OutputIndicatorForm
    model = OutputIndicator
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutputIndicatorEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['parent_entity'] = Output.objects.get(pk=self.kwargs['parent'])
        context['parent_entity_name'] = context['parent_entity']._meta.verbose_name.title()
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['step'] = 3
        context['show_methods'] = True
        context['methods'] = OutputIndicatorMethod.objects.filter(output_indicator_ref=self.object.pk)
        context['pfs'] = OutputIndicatorPF.objects.filter(output_indicator_ref=self.object.pk)
        period_names = []
        if self.object.frequency is not None and self.object.recieve_date is not None:
            freq = self.object.frequency
            start_date = self.object.recieve_date
            ctr = 0
            while ctr < freq:
                cur_date = add_months(start_date, (int(12.0/freq) * ctr))
                period_names.append(cur_date.strftime('%d.%m.%Y'))
                ctr += 1
        context['period_names'] = period_names
                
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
            pfs = OutputIndicatorPF.objects.filter(year=self.object.year).filter(output_indicator_ref=self.object.pk)
            if len(pfs) == 0:
                OutputIndicatorPF.objects.create(plan=self.object.plan, fact=self.object.fact, year=self.object.year, output_indicator_ref=self.object)
            else:
                pfs[0].plan = self.object.plan
                pfs[0].fact = self.object.fact
                pfs[0].save()                
            methods_names = self.request.POST.getlist('methods')
            OutputIndicatorMethod.objects.filter(output_indicator_ref=self.object.pk).delete()
            for method in methods_names:
                if method is not None and method.strip() != '':
                    OutputIndicatorMethod.objects.create(value=method, output_indicator_ref=self.object)
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outputs-table")

class OutcomeIndicatorEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = OutcomeIndicatorForm
    model = OutcomeIndicator
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(OutcomeIndicatorEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        outcome = Outcome.objects.get(pk=self.kwargs['parent'])
        context['parent_entity'] = outcome
        context['parent_entity_name'] = context['parent_entity']._meta.verbose_name.title()
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['step'] = 4
        context['show_methods'] = True
        context['methods'] = OutcomeIndicatorMethod.objects.filter(outcome_indicator_ref=self.object.pk)
        context['pfs'] = OutcomeIndicatorPF.objects.filter(outcome_indicator_ref=self.object.pk)
        resulting_choices_html = '<option value="">Выберите</option>'
        for line in OUTCOME_INDICATORS:
            if context['parent_entity'].value.lower().strip() == line[0].lower().strip():
                for ind in line[1:]:
                    resulting_choices_html += '<option value="'+ ind +'">'+ind+'</option>'
                break
        resulting_choices_html += '<option value="custom" style="display: none;">Введите свой вариант</option>'
        context['resulting_choices_html'] = resulting_choices_html
        context['selected_passed'] = OutcomeIndicator.objects.get(pk=self.kwargs['pk']).value
        
        outcome_name = (outcome.value if outcome.value != "custom" else outcome.custom_value)
        outcome_id = get_soc_res_id_by_text(outcome_name)
        get_methods_list = get_instr_by_soc_res_id(outcome_id)
        
        methods_choices_names = []
        for methods_name in get_methods_list:
            if methods_name is None or methods_name == "":
                continue
            methods_choices_names.append((methods_name, methods_name))
        methods_choices_names.append(('custom', 'Введите свой вариант'))
        methods_choices=tuple(methods_choices_names)

        context['form'].fields["method"].widget  = forms.Select(choices=methods_choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        context['form'].fields["method2"].widget = forms.Select(choices=methods_choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        context['form'].fields["method3"].widget = forms.Select(choices=methods_choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
            pfs = OutcomeIndicatorPF.objects.filter(year=self.object.year).filter(outcome_indicator_ref=self.object.pk)
            if len(pfs) == 0:
                OutcomeIndicatorPF.objects.create(plan=self.object.plan, fact=self.object.fact, year=self.object.year, outcome_indicator_ref=self.object)
            else:
                pfs[0].plan = self.object.plan
                pfs[0].fact = self.object.fact
                pfs[0].save()    
            methods_names = self.request.POST.getlist('methods')
            OutcomeIndicatorMethod.objects.filter(outcome_indicator_ref=self.object.pk).delete()
            for method in methods_names:
                if method is not None and method.strip() != '':
                    OutcomeIndicatorMethod.objects.create(value=method, outcome_indicator_ref=self.object)
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outcomes-table")

class ImpactIndicatorEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = ImpactIndicatorForm
    model = ImpactIndicator
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ImpactIndicatorEditView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['parent_entity'] = Impact.objects.get(pk=self.kwargs['parent'])
        context['parent_entity_name'] = context['parent_entity']._meta.verbose_name.title()
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['step'] = 5
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#impacts-table")

class PageCommentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = PageCommentForm
    model = PageComment
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(PageCommentCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.page_url = self.kwargs['prev']
        self.object.save()
        return redirect("/portal/" + str(self.kwargs['prev']))

class RCPdfView(generic.TemplateView):
    template_name = 'rcapp/iframe_view.html'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(RCPdfView, self).get_context_data(**kwargs)
        context['rc'] = self.kwargs['rc']
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

def get_pdf_view(request, rc):
    # Getting data
    lines_numbers = []

    targets_list = Target.objects.filter(rc_ref = rc)
    lines_numbers.append(len(targets_list))

    resources_lines = 0
    resources_lists_dictionary = {}
    for grp in ('Материальные', 'Финансовые', 'Организационные', 'Информационные', 'Человеческие', 'Другое'):
        resourses_list = Resource.objects.filter(rc_ref = rc).filter(subtitle = grp)
        resources_lists_dictionary[grp] = resourses_list
        if len(resourses_list) > 0:
            resources_lines += 1
    lines_numbers.append(resources_lines)
    
    activities_list = Activity.objects.filter(rc_ref = rc)
    lines_numbers.append(len(activities_list))

    outputs_list = Output.objects.filter(rc_ref = rc)
    lines_numbers.append(len(outputs_list))

    outcomes_list = Outcome.objects.filter(rc_ref = rc)
    lines_numbers.append(len(outcomes_list))

    impacts_list = Impact.objects.filter(rc_ref = rc)
    lines_numbers.append(len(impacts_list))

    output_indicators_list = OutputIndicator.objects.filter(rc_ref = rc)
    outcome_indicators_list = OutcomeIndicator.objects.filter(rc_ref = rc)
    impact_indicators_list = ImpactIndicator.objects.filter(rc_ref = rc)

    # End of getting data

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pion_program.pdf"'

    width, height = landscape(A4)
    def coord(x, y, unit=1):
        x, y = x * unit, y * unit
        return x, y
    
    MyFontObject = ttfonts.TTFont('ArialRU', 'https://pion.org.ru/static/fonts/arial-2.ttf')
    pdfmetrics.registerFont(MyFontObject)

    styles = getSampleStyleSheet()

    headerStyle = styles["Normal"]
    headerStyle.alignment = TA_CENTER # TA_JUSTIFY
    headerStyle.fontName = "ArialRU"
    headerStyle.fontSize = 11
    
    mainStyle = styles["Normal"]
    mainStyle.alignment = TA_LEFT# TA_JUSTIFY
    mainStyle.fontName = "ArialRU"
    mainStyle.fontSize = 6

    # Setting headers

    targets_header = Paragraph(u'''Целевые группы''', headerStyle)
    resourses_header = Paragraph(u'''Ресурсы''', headerStyle)
    activities_header = Paragraph(u'''Деятельность''', headerStyle)
    outputs_header = Paragraph(u'''Непосредственные результаты''', headerStyle)
    outcomes_header = Paragraph(u'''Социальные результаты''', headerStyle)
    impacts_header = Paragraph(u'''Социальные эффекты''', headerStyle)

    # End of setting headers

    # Setting cells

    # targets
    target_cells = []

    for trg in targets_list:
        strtouse = u''''''
        strtouse += u'''<ul>'''
        if trg.value == "custom":
            strtouse += u'''<br /><li>''' + str(trg.custom_value) + u'''</li><br />'''
        else:
            strtouse += u'''<br /><li>''' + str(trg.value) + u'''</li><br />'''
        strtouse += u'''</ul>'''
        target_cells.append(Paragraph(strtouse, mainStyle))

    # resources
    resource_cells = []
    for grp in ('Материальные', 'Финансовые', 'Организационные', 'Информационные', 'Человеческие', 'Другое'):
        strtouse = u''''''
        strtouse += u'''<ul>'''
        resourses_list = Resource.objects.filter(rc_ref = rc).filter(subtitle = grp)
        if len(resourses_list) == 0:
            continue
        if resourses_list:
            strtouse += u'''<br /><li>''' + grp + u''': </li><br />'''
        for rcs in resourses_list:
            if rcs.value == "custom":
                strtouse += u'''<br /><li>''' + str(rcs.custom_value) + u'''</li>'''
            else:
                strtouse += u'''<br /><li>''' + str(rcs.value) + u'''</li>'''
        strtouse += u'''</ul>'''

        resource_cells.append(Paragraph(strtouse, mainStyle))

    # activities
    activity_cells = []
    for act in activities_list:
        strtouse = u''''''
        strtouse += u'''<ul>'''
        strtouse += u'''<br /><li>''' + str(act.value) + u'''</li><br />'''
        strtouse += u'''</ul>'''

        activity_cells.append(Paragraph(strtouse, mainStyle))

    # outputs
    output_cells = []
    for opt in outputs_list:
        strtouse = u''''''
        strtouse += u'''<ul>'''
        if opt.value == "custom":
            strtouse += u'''<br /><li>''' + str(opt.custom_value) + u'''</li><br />'''
        else:
            strtouse += u'''<br /><li>''' + str(opt.value) + u'''</li><br />'''
        # for ind in output_indicators_list.filter(output_ref = opt):
        #     if ind.value == "custom":
        #         strtouse += u''' - показатель: ''' + str(ind.custom_value)
        #     else:
        #         strtouse += u''' - показатель: ''' + str(ind.value)
            
        #     # if True:# ind.plan_to_file:
        #     #     strtouse += u'''<br/>план:''' + str(ind.plan)
        #     # if True:# ind.fact_to_file:
        #     #     strtouse += u'''<br/>факт:''' + str(ind.fact)
        #     strtouse += u'''<br/>'''
        strtouse += u'''</ul>'''

        output_cells.append(Paragraph(strtouse, mainStyle))

    # outcomes
    outcome_cells = []
    for ocm in outcomes_list:
        strtouse = u''''''
        strtouse += u'''<ul>'''
        if ocm.value == "custom":
            strtouse += u'''<br /><li>''' + str(ocm.custom_value) + u'''</li><br />'''
        else:
            strtouse += u'''<br /><li>''' + str(ocm.value) + u'''</li><br />'''
        # for ind in outcome_indicators_list.filter(outcome_ref = ocm):
        #     if ind.value == "custom":
        #         strtouse += u''' - показатель: ''' + str(ind.custom_value)
        #     else:
        #         strtouse += u''' - показатель: ''' + str(ind.value)
            
        #     # if True:# ind.plan_to_file:
        #     #     strtouse += u'''<br/>план:''' + str(ind.plan)
        #     # if True:# ind.fact_to_file:
        #     #     strtouse += u'''<br/>факт:''' + str(ind.fact)
        #     strtouse += u'''<br/>'''
        strtouse += u'''</ul>'''

        outcome_cells.append(Paragraph(strtouse, mainStyle))

    # impacts
    impact_cells = []
    for imp in impacts_list:
        strtouse = u''''''
        strtouse += u'''<ul>'''
        if imp.value == "custom":
            strtouse += u'''<br /><li>''' + str(imp.custom_value) + u'''</li><br />'''
        else:
            strtouse += u'''<br /><li>''' + str(imp.value) + u'''</li><br />'''
        # for ind in impact_indicators_list.filter(impact_ref = imp):
        #     if ind.value == "custom":
        #         strtouse += u''' - показатель: ''' + str(ind.custom_value)
        #     else:
        #         strtouse += u''' - показатель: ''' + str(ind.value)
            
        #     # if True:# ind.plan_to_file:
        #     #     strtouse += u'''<br/>план:''' + str(ind.plan)
        #     # if True:# ind.fact_to_file:
        #     #     strtouse += u'''<br/>факт:''' + str(ind.fact)
        #     strtouse += u'''<br/>'''
        strtouse += u'''</ul>'''

        impact_cells.append(Paragraph(strtouse, mainStyle))
    
    empty = Paragraph(u'''''', mainStyle)

    # End of setting cells

    # Setting datas

    targets_data = [[targets_header]]
    resources_data = [[resourses_header]]
    activities_data = [[activities_header]]
    outputs_data = [[outputs_header]]
    outcomes_data = [[outcomes_header]]
    impacts_data = [[impacts_header]]

    for target_cell in target_cells:
        targets_data.append([target_cell])

    for resource_cell in resource_cells:
        resources_data.append([resource_cell])

    for activity_cell in activity_cells:
        activities_data.append([activity_cell])

    for output_cell in output_cells:
        outputs_data.append([output_cell])

    for outcome_cell in outcome_cells:
        outcomes_data.append([outcome_cell])

    for impact_cell in impact_cells:
        impacts_data.append([impact_cell])

    # End of setting datas

    empty_cols = 5 + 2

    # Setting tables

    targets_table = Table(targets_data, colWidths=[
        (width-empty_cols*10)/6], rowHeights=[((height*(0.4/3))-20)] + [((height*(2.0/3))-20)/len(target_cells) for target_cell in target_cells])

    resources_table = Table(resources_data, colWidths=[
        (width-empty_cols*10)/6], rowHeights=[((height*(0.4/3))-20)] + [((height*(2.0/3))-20)/len(resource_cells) for resource_cell in resource_cells])

    activities_table = Table(activities_data, colWidths=[
        (width-empty_cols*10)/6], rowHeights=[((height*(0.4/3))-20)] + [((height*(2.0/3))-20)/len(activity_cells) for activity_cell in activity_cells])

    outputs_table = Table(outputs_data, colWidths=[
        (width-empty_cols*10)/6], rowHeights=[((height*(0.4/3))-20)] + [((height*(2.0/3))-20)/len(output_cells) for output_cell in output_cells])

    outcomes_table = Table(outcomes_data, colWidths=[
        (width-empty_cols*10)/6], rowHeights=[((height*(0.4/3))-20)] + [((height*(2.0/3))-20)/len(outcome_cells) for outcome_cell in outcome_cells])

    impacts_table = Table(impacts_data, colWidths=[
        (width-empty_cols*10)/6], rowHeights=[((height*(0.4/3))-20)] + [((height*(2.0/3))-20)/len(impact_cells) for impact_cell in impact_cells])

    # End of setting tables

    # Setting styles for tables

    lightgreen = colors.CMYKColor(0.38, 0, 0.24, 0.04)
    lightorange = colors.CMYKColor(0.11, 0.27, 0, 0.01)
                    
    targets_table.setStyle(TableStyle([
                    ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lavenderblush),
                    ('LINEBELOW', (0,0), (-1,0), 10, colors.white),
                    ]))
                
    resources_table.setStyle(TableStyle([
                    ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lemonchiffon),
                    ('LINEBELOW', (0,0), (-1,0), 10, colors.white),
                    ]))
                
    activities_table.setStyle(TableStyle([
                    ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                    ('LINEBELOW', (0,0), (-1,0), 10, colors.white),
                    ]))
                
    outputs_table.setStyle(TableStyle([
                    ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightcoral),
                    ('LINEBELOW', (0,0), (-1,0), 10, colors.white),
                    ]))
                
    outcomes_table.setStyle(TableStyle([
                    ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                    ('BACKGROUND', (0, 0), (0, -1), lightgreen),
                    ('LINEBELOW', (0,0), (-1,0), 10, colors.white),
                    ]))
                
    impacts_table.setStyle(TableStyle([
                    ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                    ('BACKGROUND', (0, 0), (0, -1), lightorange),
                    ('LINEBELOW', (0,0), (-1,0), 10, colors.white),
                    ]))

    # End of setting styles for tables

    # Perform drawing

    c = canvas.Canvas(response)

    c.setFont("ArialRU",18)

    c.setPageSize(landscape(A4))

    targets_table.wrapOn(c, width, height)
    targets_table.drawOn(c, *coord(10, 10))

    resources_table.wrapOn(c, width, height)
    resources_table.drawOn(c, *coord(((width-empty_cols*10)/6)+10*2, 10))

    activities_table.wrapOn(c, width, height)
    activities_table.drawOn(c, *coord(((width-empty_cols*10)/6)*2+10*3, 10))

    outputs_table.wrapOn(c, width, height)
    outputs_table.drawOn(c, *coord(((width-empty_cols*10)/6)*3+10*4, 10))

    outcomes_table.wrapOn(c, width, height)
    outcomes_table.drawOn(c, *coord(((width-empty_cols*10)/6)*4+10*5, 10))

    impacts_table.wrapOn(c, width, height)
    impacts_table.drawOn(c, *coord(((width-empty_cols*10)/6)*5+10*6, 10))

    this_rc = ResultsChain.objects.get(pk=rc)


    c.drawString(10, height-35, "Название программы: " + str(this_rc.name))
    c.drawString(10, height-35-18-10, "Организация: " + str(this_rc.organization))

    from reportlab.lib.utils import ImageReader
    logo = ImageReader('https://pion.org.ru/static/img/logo-mini.png')

    c.drawImage(logo, width - 234, height-50, mask='auto')

    c.linkURL('https://pion.org.ru', (width - 244, height-50, width-10, height-10), relative=1)

    c.showPage()

    # End of perform drawing


    # # Here goes second page
    # secondHeaderStyle = styles["Normal"]
    # secondHeaderStyle.alignment = TA_CENTER # TA_JUSTIFY
    # secondHeaderStyle.fontName = "ArialRU"
    # secondHeaderStyle.fontSize = 16
    
    # secondMainStyle = styles["Normal"]
    # secondMainStyle.alignment = TA_LEFT# TA_JUSTIFY
    # secondMainStyle.fontName = "ArialRU"
    # secondMainStyle.fontSize = 13

    # outputs_header = Paragraph(u'''Непосредственные результаты''', secondHeaderStyle)
    # outcomes_header = Paragraph(u'''Социальные результаты''', secondHeaderStyle)

    # strtouse = u''''''
    # strtouse += u'''<ul>'''
    # for opt in outputs_list:
    #     if opt.value == "custom":
    #         strtouse += u'''<br /><li>''' + str(opt.custom_value) + u'''</li><br />'''
    #     else:
    #         strtouse += u'''<br /><li>''' + str(opt.value) + u'''</li><br />'''
    #     if opt.comm is not None and opt.comm != "":
    #         strtouse += u'''<br /><li>Комментарий: ''' + str(opt.comm) + u'''</li><br />'''
    #     for ind in output_indicators_list.filter(output_ref = opt):
    #         strtouse += u''' - метод сбора данных: ''' + str(ind.custom_method) + u'''<br />'''
    # strtouse += u'''</ul>'''

    # output_methods = Paragraph(strtouse, secondMainStyle)

    # strtouse = u''''''
    # strtouse += u'''<ul>'''
    # for ocm in outcomes_list:
    #     if ocm.value == "custom":
    #         strtouse += u'''<br /><li>''' + str(ocm.custom_value) + u'''</li><br />'''
    #     else:
    #         strtouse += u'''<br /><li>''' + str(ocm.value) + u'''</li><br />'''
    #     if ocm.comm is not None and ocm.comm != "":
    #         strtouse += u'''<br /><li>Комментарий: ''' + str(ocm.comm) + u'''</li><br />'''
    #     for ind in outcome_indicators_list.filter(outcome_ref = ocm):
    #         strtouse += u''' - метод сбора данных: ''' + str(ind.custom_method) + u'''<br />'''
    # strtouse += u'''</ul>'''

    # outcome_methods = Paragraph(strtouse, secondMainStyle)

    # empty = Paragraph(u'''''', secondMainStyle)

    # data= [[outputs_header, empty, outcomes_header],
    #     [output_methods, empty, outcome_methods],
    #     ]
    # empty_cols = 1 + 2 #2 are left and right sides

    # table = Table(data, colWidths=[
    #     (width-empty_cols*10)/2, 
    #     10, 
    #     (width-empty_cols*10)/2], rowHeights=[((height*(0.4/3))-20), ((height*(2.0/3))-20)])

    # table.setStyle(TableStyle([
    #                     ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
    #                     ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    #                     ('BOX', (0,0), (-1,-1), 0.25, colors.white),
    #                     # ('BACKGROUND', (0, 0), (0, -1), colors.lavenderblush),
    #                     # ('BACKGROUND', (2, 0), (2, -1), colors.lemonchiffon),
    #                     # ('BACKGROUND', (4, 0), (4, -1), colors.lightblue),
    #                     ('BOX', (0, 0), (0, -1), 1, colors.lightcoral),
    #                     ('BOX', (2, 0), (2, -1), 1, lightgreen),
    #                     # ('BACKGROUND', (10, 0), (10, -1), lightorange),
    #                     ]))

    # #c = canvas.Canvas("a.pdf", pagesize=A4)

    # # c = canvas.Canvas(response)

    # c.setFont("ArialRU",18)

    # # c.setPageSize(landscape(A4))
    # table.wrapOn(c, width, height)
    # table.drawOn(c, *coord(10, 10))

    # this_rc = ResultsChain.objects.get(pk=rc)


    # c.drawString(10, height-35, "Название программы: " + str(this_rc.name))
    # c.drawString(10, height-35-18-10, "Организация: " + str(this_rc.organization))

    # from reportlab.lib.utils import ImageReader
    # logo = ImageReader('https://pion.org.ru/static/img/logo-mini.png')

    # c.drawImage(logo, width - 234, height-50, mask='auto')

    # c.linkURL('https://pion.org.ru', (width - 244, height-50, width-10, height-10), relative=1)
    # # Uncomment to create second page
    # c.showPage()

    c.save()
    return response

from io import BytesIO
import xlsxwriter
 
FREQUENCY_DICT = {None: 'Не указано', 1:'1 раз в год', 2:'1 раз в полгода', 4:'1 раз в квартал', 12: '1 раз в месяц'}

def WriteIndicatorsToExcel(rc):
    col_widths = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
    xlsx_output = BytesIO()
    workbook = xlsxwriter.Workbook(xlsx_output)
 
    worksheet = workbook.add_worksheet('ResultsChain')
    
    header = workbook.add_format({
        'bg_color': '#788002',
        'color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    title = workbook.add_format({
        'bg_color': 'white',
        'color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'border': 1
    })
    # Add data here
    # Headers
    worksheet.set_row(0, 40)
    
    result_title = u'Результат'
    indicator_title = u'Показатель'
    method_title = u'Метод сбора'
    frequency_title = u'Регулярность сбора'
    owner_title = u'Ответственный за сбор'
    reports_title = u'В каких отчетах используется'
    
    worksheet.write(0, 0, result_title, header)
    worksheet.write(0, 1, indicator_title, header)
    worksheet.write(0, 2, method_title, header)
    worksheet.write(0, 3, frequency_title, header)
    worksheet.write(0, 4, owner_title, header)
    worksheet.write(0, 5, reports_title, header)
    
    if len(result_title) > col_widths[0]:
        col_widths[0] = len(result_title)
        
    if len(indicator_title) > col_widths[1]:
        col_widths[1] = len(indicator_title)
        
    if len(method_title) > col_widths[2]:
        col_widths[2] = len(method_title)
        
    if len(frequency_title) > col_widths[3]:
        col_widths[3] = len(frequency_title)
        
    if len(owner_title) > col_widths[4]:
        col_widths[4] = len(owner_title)
        
    if len(reports_title) > col_widths[5]:
        col_widths[5] = len(reports_title)
    
    current_row = 1
    
    output_title = u'Показатели непосредственных результатов'
    
    worksheet.merge_range('A'+ str(current_row + 1) +':F' + str(current_row + 1), output_title, title)
    worksheet.set_row(current_row, 40)
    current_row += 1
    
    outputs = Output.objects.filter(rc_ref = rc)
    output_indicators = OutputIndicator.objects.filter(rc_ref = rc).order_by('output_ref')
    
    for output in outputs:
        current_output_indicators = [output_indicator for output_indicator in output_indicators if output_indicator.output_ref == output]
        current_output_indicators_length = len(current_output_indicators)
        worksheet.merge_range('A'+ str(current_row + 1) +':A'+ str(current_row + current_output_indicators_length), output.value if output.value != "custom" else output.custom_value, title)
        
        if len(output.value if output.value != "custom" else output.custom_value) > col_widths[0]:
            col_widths[0] = len(output.value if output.value != "custom" else output.custom_value)
        # delete when filled right columns
        # current_row += current_output_indicators_length
        
        # Вынести номера в кнстанты
        for output_indicator in current_output_indicators:
            worksheet.write(current_row, 1, output_indicator.value if output_indicator.value != "custom" else output_indicator.custom_value, title)
            worksheet.write(current_row, 2, output_indicator.method if output_indicator.method != "custom" else output_indicator.custom_method, title)
            worksheet.write(current_row, 3, FREQUENCY_DICT[output_indicator.frequency], title)
            worksheet.write(current_row, 4, output_indicator.owner, title)
            worksheet.write(current_row, 5, output_indicator.reports, title)
            
            if len(output_indicator.value if output_indicator.value != "custom" else output_indicator.custom_value) > col_widths[1]:
                col_widths[1] = len(output_indicator.value if output_indicator.value != "custom" else output_indicator.custom_value)
                
            if len(output_indicator.method if output_indicator.method != "custom" else output_indicator.custom_method) > col_widths[2]:
                col_widths[2] = len(output_indicator.method if output_indicator.method != "custom" else output_indicator.custom_method)
                
            if len(FREQUENCY_DICT[output_indicator.frequency]) > col_widths[3]:
                col_widths[3] = len(FREQUENCY_DICT[output_indicator.frequency])
                
            if len(output_indicator.owner) > col_widths[4]:
                col_widths[4] = len(output_indicator.owner)
                
            if len(output_indicator.reports) > col_widths[5]:
                col_widths[5] = len(output_indicator.reports)
            #HEREHERE
            #Other columns
            current_row += 1
        
    
    outcome_title = u'Показатели социальных результатов'
    
    worksheet.merge_range('A'+ str(current_row + 1) +':F' + str(current_row + 1), outcome_title, title)
    worksheet.set_row(current_row, 40)
    current_row += 1
    
    outcomes = Outcome.objects.filter(rc_ref = rc)
    outcome_indicators = OutcomeIndicator.objects.filter(rc_ref = rc).order_by('outcome_ref')
    
    for outcome in outcomes:
        current_outcome_indicators = [outcome_indicator for outcome_indicator in outcome_indicators if outcome_indicator.outcome_ref == outcome]
        current_outcome_indicators_length = len(current_outcome_indicators)
        worksheet.merge_range('A'+ str(current_row + 1) +':A'+ str(current_row + current_outcome_indicators_length), outcome.value if outcome.value != "custom" else outcome.custom_value, title)
        
        if len(outcome.value if outcome.value != "custom" else outcome.custom_value) > col_widths[0]:
            col_widths[0] = len(outcome.value if outcome.value != "custom" else outcome.custom_value)
        
        # delete when filled right columns
        # current_row += current_outcome_indicators_length
        
        # Вынести номера в кнстанты
        for outcome_indicator in current_outcome_indicators:
            worksheet.write(current_row, 1, outcome_indicator.value if outcome_indicator.value != "custom" else outcome_indicator.custom_value, title)
            worksheet.write(current_row, 2, outcome_indicator.method if outcome_indicator.method != "custom" else outcome_indicator.custom_method, title)
            worksheet.write(current_row, 3, FREQUENCY_DICT[outcome_indicator.frequency], title)
            worksheet.write(current_row, 4, outcome_indicator.owner, title)
            worksheet.write(current_row, 5, outcome_indicator.reports, title)
            
            if len(outcome_indicator.value if outcome_indicator.value != "custom" else outcome_indicator.custom_value) > col_widths[1]:
                col_widths[1] = len(outcome_indicator.value if outcome_indicator.value != "custom" else outcome_indicator.custom_value)
                
            if len(outcome_indicator.method if outcome_indicator.method != "custom" else outcome_indicator.custom_method) > col_widths[2]:
                col_widths[2] = len(outcome_indicator.method if outcome_indicator.method != "custom" else outcome_indicator.custom_method)
                
            if len(FREQUENCY_DICT[outcome_indicator.frequency]) > col_widths[3]:
                col_widths[3] = len(FREQUENCY_DICT[outcome_indicator.frequency])
                
            if len(outcome_indicator.owner) > col_widths[4]:
                col_widths[4] = len(outcome_indicator.owner)
                
            if len(outcome_indicator.reports) > col_widths[5]:
                col_widths[5] = len(outcome_indicator.reports)
            
            #HEREHERE
            #Other columns
            current_row += 1
    
    impact_title = u'Показатели социальных эффектов'
    
    worksheet.merge_range('A'+ str(current_row + 1) +':F' + str(current_row + 1), impact_title, title)
    worksheet.set_row(current_row, 40)
    current_row += 1
    
    impacts = Impact.objects.filter(rc_ref = rc)
    impact_indicators = ImpactIndicator.objects.filter(rc_ref = rc).order_by('impact_ref')
    
    for impact in impacts:
        current_impact_indicators = [impact_indicator for impact_indicator in impact_indicators if impact_indicator.impact_ref == impact]
        current_impact_indicators_length = len(current_impact_indicators)
        if current_impact_indicators_length == 0:
            continue
        if current_impact_indicators_length > 1:
            worksheet.merge_range('A'+ str(current_row + 1) +':A'+ str(current_row + current_impact_indicators_length), impact.value if impact.value != "custom" else impact.custom_value, title)
        else:
            worksheet.write(current_row, 0, impact.value if impact.value != "custom" else impact.custom_value, title)
        if len(impact.value if impact.value != "custom" else impact.custom_value) > col_widths[0]:
            col_widths[0] = len(impact.value if impact.value != "custom" else impact.custom_value)
        
        # delete when filled right columns
        # current_row += current_impact_indicators_length
        
        # Вынести номера в кнстанты
        for impact_indicator in current_impact_indicators:
            worksheet.write(current_row, 1, impact_indicator.value if impact_indicator.value != "custom" else impact_indicator.custom_value, title)
            worksheet.write(current_row, 2, u'', title)
            worksheet.write(current_row, 3, FREQUENCY_DICT[impact_indicator.frequency], title)
            worksheet.write(current_row, 4, impact_indicator.owner, title)
            worksheet.write(current_row, 5, impact_indicator.reports, title)
            
            if len(impact_indicator.value if impact_indicator.value != "custom" else impact_indicator.custom_value) > col_widths[1]:
                col_widths[1] = len(impact_indicator.value if impact_indicator.value != "custom" else impact_indicator.custom_value)
                
            if len(FREQUENCY_DICT[impact_indicator.frequency]) > col_widths[3]:
                col_widths[3] = len(FREQUENCY_DICT[impact_indicator.frequency])
                
            if len(impact_indicator.owner) > col_widths[4]:
                col_widths[4] = len(impact_indicator.owner)
                
            if len(impact_indicator.reports) > col_widths[5]:
                col_widths[5] = len(impact_indicator.reports)
            
            #HEREHERE
            #Other columns
            current_row += 1
    
    worksheet.set_column('A:A', col_widths[0])
    worksheet.set_column('B:B', col_widths[1])
    worksheet.set_column('C:C', col_widths[2])
    worksheet.set_column('D:D', col_widths[3])
    worksheet.set_column('E:E', col_widths[4])
    worksheet.set_column('F:F', col_widths[5])
    
    # End headers
    # Finish data here
    workbook.close()
    xlsx_data = xlsx_output.getvalue()
    
    return xlsx_data



def lcm(a, b):
    if a > b:
        greater = a
    else:
        greater = b

    while True:
        if greater % a == 0 and greater % b == 0:
            lcm = greater
            break
        greater += 1

    return lcm

def get_lcm_for(your_list):
    return reduce(lambda x, y: lcm(x, y), your_list)
    
def get_col_letter(numb):
    a_letter = ord('A')
    return chr(int(a_letter) + int(numb))

def WriteIndicatorValuesToExcel(rc, opts, ocms, imps, year, plan_p, periods_p, fact_p, deviation_p, meth_p, source_p):
    year = int(year)
    
    output_indicators = OutputIndicator.objects.filter(rc_ref = rc).order_by('output_ref') if opts else []
    for output_indicator in output_indicators:
        if year != 0:
            pfs = OutputIndicatorPF.objects.filter(output_indicator_ref=output_indicator.pk).filter(year=year)
            if len(pfs) != 0:
                output_indicator.plan = pfs[0].plan
                output_indicator.fact = pfs[0].fact
            else:
                output_indicator.plan = ""
                output_indicator.fact = ""
    outcome_indicators = OutcomeIndicator.objects.filter(rc_ref = rc).order_by('outcome_ref') if ocms else []
    for outcome_indicator in outcome_indicators:
        if year != 0:
            pfs = OutcomeIndicatorPF.objects.filter(outcome_indicator_ref=outcome_indicator.pk).filter(year=year)
            if len(pfs) != 0:
                outcome_indicator.plan = pfs[0].plan
                outcome_indicator.fact = pfs[0].fact
            else:
                outcome_indicator.plan = ""
                outcome_indicator.fact = ""
    impact_indicators = ImpactIndicator.objects.filter(rc_ref = rc).order_by('impact_ref') if imps else []
    
    max_columns = 0
    
    for output_indicator in output_indicators:
        if periods_p:
            if output_indicator.frequency is None:
                output_indicator.frequency = 0
            elif output_indicator.frequency != 0 and output_indicator.frequency > max_columns:
                max_columns = int(lcm(output_indicator.frequency, max_columns if max_columns != 0 else 1))
    
    for outcome_indicator in outcome_indicators:
        if periods_p:
            if outcome_indicator.frequency is None:
                outcome_indicator.frequency = 0
            elif outcome_indicator.frequency != 0 and outcome_indicator.frequency > max_columns:
                max_columns = int(lcm(outcome_indicator.frequency, max_columns if max_columns != 0 else 1))
            
    for impact_indicator in impact_indicators:
        if periods_p:    
            if impact_indicator.frequency is None:
                impact_indicator.frequency = 0
            elif impact_indicator.frequency != 0 and impact_indicator.frequency > max_columns:
                max_columns = int(lcm(impact_indicator.frequency, max_columns if max_columns != 0 else 1))
    
    col_widths = []
    
    ind_value_width = 0
    
    columns_total = max_columns + 7
    
    if not plan_p:
        columns_total -= 1
    if not fact_p:
        columns_total -= 1
    if not deviation_p:
        columns_total -= 1
    if not meth_p:
        columns_total -= 1
    if not source_p:
        columns_total -= 1
    # , plan, periods, fact, deviation, meth, source
    
    counter = 0
    
    while counter < columns_total:
        col_widths.append(0)
        counter += 1
    
    xlsx_output = BytesIO()
    workbook = xlsxwriter.Workbook(xlsx_output)
 
    worksheet = workbook.add_worksheet('ResultsChain')
    
    header = workbook.add_format({
        'bg_color': '#788002',
        'color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    title = workbook.add_format({
        'bg_color': 'white',
        'color': 'black',
        'align': 'left',
        'valign': 'vcenter',
        'border': 1
    })
    
    # Data here
    
    current_row = 0
    
    # !!!!!!!!!!!!!!!!!!!!Start importing data!!!!!!!!!!!!!!!!
    indicators = list(output_indicators) + list(outcome_indicators) + list(impact_indicators)
    indicators = sorted(indicators, key=lambda ind: -ind.frequency)
    
    current_frequency = -1
    
    for indicator in indicators:
        if indicator.frequency != current_frequency:
            current_frequency = indicator.frequency
            current_col = 0
            # Показатель топ
            worksheet.write(int(current_row), int(current_col), u'Показатель', header)
            if len(u'Показатель') > col_widths[int(current_col)]:
                col_widths[int(current_col)] = len(u'Показатель')
            if plan_p:
                current_col += 1
                # План топ
                worksheet.write(int(current_row), int(current_col), u'План', header)
                if len(u'План') > col_widths[int(current_col)]:
                    col_widths[int(current_col)] = len(u'План')
            if periods_p:
                counter = 1
                # Периоды топ
                while counter <= current_frequency:
                    current_col += 1
                    if int(current_col) != int(current_col + (max_columns/current_frequency) - 1):
                        worksheet.merge_range(int(current_row), int(current_col), int(current_row), int(current_col + (max_columns/current_frequency) - 1), u'Период ' + str(counter), header)
                    else:
                        worksheet.write(int(current_row), int(current_col), u'Период ' + str(counter), header)
                    if len(u'Период ' + str(counter))/((max_columns/current_frequency)) > ind_value_width:
                        ind_value_width = len(u'Период ' + str(counter))/((max_columns/current_frequency))
                    current_col += (max_columns/current_frequency) - 1
                    counter += 1
                if current_frequency == 0 and max_columns != 0:
                    current_col += 1
                    if max_columns == 1:
                        worksheet.write(int(current_row), int(current_col), u'', header)
                    else:
                        worksheet.merge_range(int(current_row), int(current_col), int(current_row), int(current_col + max_columns - 1), u'', header)
                    current_col += max_columns - 1
            if fact_p:
                current_col += 1
                # Факт топ
                worksheet.write(int(current_row), int(current_col), u'Факт', header)
                if len(u'Факт') > col_widths[int(current_col)]:
                    col_widths[int(current_col)] = len(u'Факт')
            if deviation_p:
                current_col += 1
                # Отклонение топ
                worksheet.write(int(current_row), int(current_col), u'Отклонение', header)
                if len(u'Отклонение') > col_widths[int(current_col)]:
                    col_widths[int(current_col)] = len(u'Отклонение')
            if meth_p:
                current_col += 1
                # Методика сбора данных
                worksheet.write(int(current_row), int(current_col), u'Методика сбора данных', header)
                if len(u'Методика сбора данных') > col_widths[int(current_col)]:
                    col_widths[int(current_col)] = len(u'Методика сбора данных')
            if source_p:
                current_col += 1
                # Источник данных
                worksheet.write(int(current_row), int(current_col), u'Источник данных', header)
                if len(u'Источник данных') > col_widths[int(current_col)]:
                    col_widths[int(current_col)] = len(u'Источник данных')
            current_row += 1
        #data here
        current_col = 0
        # Показатель
        worksheet.write(int(current_row), int(current_col), indicator.value if indicator.value != "custom" else indicator.custom_value, title)
        if len(indicator.value if indicator.value != "custom" else indicator.custom_value) > col_widths[int(current_col)]:
            col_widths[int(current_col)] = len(indicator.value if indicator.value != "custom" else indicator.custom_value)
        if plan_p:
            current_col += 1
            # План
            worksheet.write(int(current_row), int(current_col), indicator.plan, title)
            if len(indicator.plan) > col_widths[int(current_col)]:
                col_widths[int(current_col)] = len(indicator.plan)
        if periods_p:
            counter = 0
            # Периоды
            ind_values = indicator.values.split(',')
            while counter < current_frequency and counter < len(ind_values):
                current_col += 1
                if int(current_col) != int(current_col + (max_columns/current_frequency) - 1):
                    worksheet.merge_range(int(current_row), int(current_col), int(current_row), int(current_col + (max_columns/current_frequency) - 1), ind_values[counter], title)
                else:
                    worksheet.write(int(current_row), int(current_col), ind_values[counter], title)
                if len(ind_values[counter])/((max_columns/current_frequency)) > ind_value_width:
                    ind_value_width = len(ind_values[counter])/((max_columns/current_frequency))
                current_col += (max_columns/current_frequency) - 1
                counter += 1
            if current_frequency == 0 and max_columns != 0:
                current_col += 1
                if max_columns == 1:
                    worksheet.write(int(current_row), int(current_col), u'', title)
                else:
                    worksheet.merge_range(int(current_row), int(current_col), int(current_row), int(current_col + max_columns - 1), u'', title)
                current_col += max_columns - 1
        if fact_p:
            current_col += 1
            # Факт
            worksheet.write(int(current_row), int(current_col), indicator.fact, title)
            if len(indicator.fact) > col_widths[int(current_col)]:
                col_widths[int(current_col)] = len(indicator.fact)
        if deviation_p:
            current_col += 1
            # Отклонение
            try:
                fact = int(indicator.fact)
                plan = int(indicator.plan)
                deviation = str(fact-plan)
            except:
                deviation = u"0"
            worksheet.write(int(current_row), int(current_col), deviation, title)
            if len(deviation) > col_widths[int(current_col)]:
                col_widths[int(current_col)] = len(deviation)
        if meth_p:
            current_col += 1
            # Методика сбора данных
            if indicator.methodic == None:
                indicator.methodic = ""
            worksheet.write(int(current_row), int(current_col), indicator.methodic, title)
            if len(indicator.methodic) > col_widths[int(current_col)]:
                col_widths[int(current_col)] = len(indicator.methodic)
        if source_p:
            current_col += 1
            # Источник данных
            if indicator.data_source == None:
                indicator.data_source = ""
            worksheet.write(int(current_row), int(current_col), indicator.data_source, title)
            if len(indicator.data_source) > col_widths[int(current_col)]:
                col_widths[int(current_col)] = len(indicator.data_source)
        current_row += 1
    
    counter = 2
    while counter < 2 + max_columns:
        col_widths[counter] = ind_value_width
        counter += 1
    
    counter = 0
    while counter < columns_total:
        worksheet.set_column(counter, counter, col_widths[counter])
        counter += 1
    
    # End data here
    
    workbook.close()
    xlsx_data = xlsx_output.getvalue()
    
    return xlsx_data

def get_indicator_monitoring_form_xlsx_file(request, rc):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ResultsChain.xlsx'
    xlsx_data = WriteIndicatorsToExcel(rc)
    response.write(xlsx_data)
    return response
    
def get_indicator_values_monitoring_form_xlsx_file(request, rc):
    opts = request.GET.get("opts", "true").lower() == "true"
    ocms = request.GET.get("ocms", "true").lower() == "true"
    imps = request.GET.get("imps", "true").lower() == "true"
    plan = request.GET.get("plan", "true").lower() == "true"
    periods = request.GET.get("periods", "true").lower() == "true"
    fact = request.GET.get("fact", "true").lower() == "true"
    deviation = request.GET.get("deviation", "true").lower() == "true"
    meth = request.GET.get("meth", "true").lower() == "true"
    source = request.GET.get("source", "true").lower() == "true"
    year = request.GET.get("year", "0")
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ResultsChain.xlsx'
    xlsx_data = WriteIndicatorValuesToExcel(rc, opts, ocms, imps, year, plan, periods, fact, deviation, meth, source)
    response.write(xlsx_data)
    return response

class VisualizationView(TemplateView):
    template_name = 'rcapp/visualization_view.html'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(VisualizationView, self).get_context_data(**kwargs)
        return context
        

class DuplicateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        rc = ResultsChain.objects.get(pk=self.kwargs['pk'])
        rc.pk = None
        rc.user = self.request.user
        rc.save()
        old_rc = ResultsChain.objects.get(pk=self.kwargs['pk'])
        
        targets = Target.objects.filter(rc_ref = old_rc)
        for target in targets:
            target.pk = None
            target.rc_ref = rc
            target.save()
        resources = Resource.objects.filter(rc_ref = old_rc)
        for resource in resources:
            resource.pk = None
            resource.rc_ref = rc
            resource.save()
        
        activities = Activity.objects.filter(rc_ref = old_rc)
        for activity in activities:
            outputs = Output.objects.filter(rc_ref = old_rc).filter(activity_refs=activity)
            activity.pk = None
            activity.rc_ref = rc
            activity.save()
            for output in outputs:
                output_indicators = OutputIndicator.objects.filter(rc_ref = old_rc).filter(output_ref=output)
                output.pk = None
                output.activity_ref = activity
                output.rc_ref = rc
                output.save()
                for output_indicator in output_indicators:
                    output_indicator.pk = None
                    output_indicator.output_ref = output
                    output_indicator.rc_ref = rc
                    output_indicator.save()
        
        outcomes = Outcome.objects.filter(rc_ref = old_rc)
        for outcome in outcomes:
            outcome_indicators = OutcomeIndicator.objects.filter(rc_ref = old_rc).filter(outcome_ref=outcome)
            outcome.pk=None
            outcome.rc_ref = rc
            outcome.save()
            for outcome_indicator in outcome_indicators:
                outcome_indicator.pk = None
                outcome_indicator.rc_ref = rc
                outcome_indicator.outcome_ref = outcome
                outcome_indicator.save()
        
        impacts = Impact.objects.filter(rc_ref = old_rc)
        for impact in impacts:
            impact_indicators = ImpactIndicator.objects.filter(rc_ref = old_rc).filter(impact_ref=impact)
            impact.pk = None
            impact.rc_ref = rc
            impact.save()
            for impact_indicator in impact_indicators:
                impact_indicator.pk = None
                impact_indicator.rc_ref = rc
                impact_indicator.impact_ref = impact
                impact_indicator.save()
        return redirect(rc.get_edit_url())
        
class AssignView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        rc = ResultsChain.objects.get(pk=self.kwargs['pk'])
        userpk = get_value_or_none(self.request.POST, 'userpk')
        if userpk is None:
            raise Exception("Error at assigning")
        user = User.objects.get(pk=userpk)
        connectors = ResultsChainUserConnector.objects.filter(user_ref = user).filter(rc_ref = rc).count()
        if connectors > 0:
            return redirect(rc.get_edit_url())
        ResultsChainUserConnector.objects.create(rc_ref = rc, user_ref = user)
        return redirect(rc.get_edit_url())
        
class ArchiveView(ListView):
    template_name = 'rcapp/rclistview.html'
    context_object_name = 'rcapp_archive'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ArchiveView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['allRCs'] = True
        return context
    def get_queryset(self):
        return ResultsChain.objects.order_by('-formation_date')
    
class DownloadView(generic.DetailView):
    template_name = 'rcapp/rc_download_page.html'
    model = ResultsChain
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(DownloadView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    
class CompanyView(generic.DetailView):
    template_name = 'rcapp/company_view.html'
    model = CompanyData
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(CompanyView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['is_my'] = context['object'].company_owner.pk == self.request.user.pk
        context['rcs'] = ResultsChain.objects.filter(company_data_ref = context['object'].pk)
        connectors = CompanyDataUserConnector.objects.filter(company_data_ref=context['object'].pk)
        context['people'] = User.objects.filter(pk__in = [connector.user_ref.pk for connector in connectors])
        context['users'] = User.objects.all()
        return context
    
class CompanyEdit(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = CompanyDataForm
    model = CompanyData
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(CompanyEdit, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    
class CompanyCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = CompanyDataForm
    model = CompanyData
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(CompanyCreate, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.company_owner = self.request.user
        self.object.save()
        CompanyDataUserConnector.objects.create(user_ref=self.request.user, company_data_ref = self.object)
        return redirect(self.object.get_absolute_url())
    
class Companies(LoginRequiredMixin, generic.ListView):
    template_name = 'rcapp/companies_list_view.html'
    context_object_name = 'companies_archive'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(Companies, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    def get_queryset(self):
        connectors = CompanyDataUserConnector.objects.filter(user_ref = self.request.user)
        users_rcs = [connector.company_data_ref.pk for connector in connectors]
        return CompanyData.objects.filter(pk__in=users_rcs).distinct()
    
class AddUserToCompany(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        rc = CompanyData.objects.get(pk=self.kwargs['pk'])
        user = get_value_or_none(self.request.POST, 'userpk')
        CompanyDataUserConnector.objects.create(user_ref = User.objects.get(pk=user), company_data_ref = rc)
        return redirect(rc.get_absolute_url())
    
class ViewTotalDataNew(generic.TemplateView):
    template_name = 'rcapp/special_list_view_r.html'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewTotalDataNew, self).get_context_data(**kwargs)
        companies = CompanyData.objects.all()
        context['rchs'] = ResultsChain.objects.exclude(company_data_ref__isnull = True)
        context['companies'] = companies
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class ViewTotalData(generic.TemplateView):
    template_name = 'rcapp/special_list_view.html'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewTotalData, self).get_context_data(**kwargs)
        companies = CompanyData.objects.filter(display_in_list = True)
        context['rchs'] = ResultsChain.objects.exclude(company_data_ref__isnull = True)
        context['companies'] = companies
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    
class LibraryPageData(generic.DetailView):
    template_name = "main/custom_page.html"
    model = LibraryPage
 
 # Class to store the result of the search   
class SearchResult:
    def __init__(self, header_text, info_text, url):
          self.header_text = header_text
          self.info_text = info_text
          self.url = url
          self.counter = 1
    def __str__(self):
        return self.header_text
    def __hash__(self):
        return hash(self.url)
    def __eq__(self, other):
        return self.url == other.url

class SearchView(generic.TemplateView):
    template_name = 'rcapp/search_page.html'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        search_in_library = True
        context = super(SearchView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        search_line = get_value_or_none(self.request.GET, 'search')
        search_results = []
        if search_line is not None:
            words = re.split(' |; |, |\*|\n',str(search_line))
            for word in words:
                if len(word) > 5:
                    word = word[:-2]
                # Поиск по странице
                results = list(LibraryPage.objects.filter(name__icontains=word))
                results += list(LibraryPage.objects.filter(content__icontains=word))
                for result in results:
                    search_result = SearchResult(result.name, "Страница библиотека", result.get_absolute_url())
                    if search_result in search_results:
                        index = search_results.index(search_result)
                        search_results[index].counter += 1
                    else:
                        search_results.append(search_result)
                # Поиск по социальным результатам
                results = list(Outcome.objects.filter(value__icontains=word))
                results += list(Outcome.objects.filter(custom_value__icontains=word))
                for result in results:
                    chain = ResultsChain.objects.get(pk=result.rc_ref.pk)
                    search_result = SearchResult(chain.name, "Цепочка \""+ chain.name +"\", Социальный результат \"" + (result.value if result.value != "custom" else result.custom_value) +"\"", (chain.get_absolute_url() + "/#outcomes-table"))
                    if search_result in search_results:
                        index = search_results.index(search_result)
                        search_results[index].counter += 1
                    else:
                        search_results.append(search_result)
                # Поиск по показателям социальных результатов
                results = list(OutcomeIndicator.objects.filter(value__icontains=word))
                results += list(OutcomeIndicator.objects.filter(custom_value__icontains=word))
                results += list(OutcomeIndicator.objects.filter(method__icontains=word))
                results += list(OutcomeIndicator.objects.filter(custom_method__icontains=word))
                for result in results:
                    outcome = Outcome.objects.get(pk=result.outcome_ref.pk)
                    chain = ResultsChain.objects.get(pk=result.rc_ref.pk)
                    search_result = SearchResult(chain.name, "Цепочка \""+ chain.name +"\", Социальный результат \"" + (outcome.value if outcome.value != "custom" else outcome.custom_value) +"\", Показатель \""+ (result.value if result.value != "custom" else result.custom_value) +"\"", (chain.get_absolute_url() + "/#outcomes-table"))
                    if search_result in search_results:
                        index = search_results.index(search_result)
                        search_results[index].counter += 1
                    else:
                        search_results.append(search_result)
        search_results = list(set(search_results))
        search_results.sort(key=lambda x: -x.counter)
        context['search_results'] = search_results
        return context
    

# UserRequest
class UserRequestCreateView(generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class    = UserRequestCreateForm
    model = UserRequest
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(UserRequestCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['entity_name'] = 'Регистрация'
        context['display_user_agreement'] = True
        context['registration_form'] = True
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)

        recaptcha_response = get_value_or_none(self.request.POST, 'g-recaptcha-response')
        data = {
            'secret': '6Ld_G9kUAAAAAPFeGuVUVgqCALvsQozDw8CD0Gzw',
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''

        if result['success']:
            if self.object.email == "malvina.doorbell.cherkesova@mail.ru":
                raise Http404("Превышено количество запросов!")
            self.object.username = self.object.username.lower()
            users = User.objects.filter(username=self.object.username)
            if len(users) != 0:
                return redirect("/portal/user_exists")
            user_requests = UserRequest.objects.filter(username=self.object.username).filter(created=False)
            if len(user_requests) != 0:
                return redirect("/portal/user_in_progress")
            send_mail('Заявка на создание нового пользователя', 'Заявка на создание нового пользователя поступила\nАдминистрация запроса: https://pion.org.ru/portal/user_requests_list', 'mail@pion.org.ru', ['priakni@gmail.com', 'info@ep.org.ru'], fail_silently=True)
            send_mail('Заявка на сервисе pion.org.ru', 'Ваша заявка на регистрацию принята. Мы свяжемся с вами!', 'mail@pion.org.ru', [self.object.email], fail_silently=True)
            self.object.save()
            return redirect("/portal/registration_success")
        else:
            raise Http404("Не пройдена проверка!")
    
class ViewHelperPage(generic.TemplateView):
    template_name = "rcapp/helper_page.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        helper_paragraphs = HelpParagraph.objects.order_by('order')
        page_number = get_value_or_none(self.request.GET, 'page')
        if page_number is None:
            page_number = 0
        else:
            page_number = int(page_number)
        context['pages_number'] = int(len(helper_paragraphs))
        if page_number > 0:
            context["prev_page_link"] = "/portal/helper?page=" + str(page_number - 1)
        if page_number < context["pages_number"] - 1:
            context["next_page_link"] = "/portal/helper?page=" + str(page_number + 1)
        helper_paragraphs = helper_paragraphs[page_number:page_number+1]
        context['helper_paragraphs'] = helper_paragraphs
        context['all_helper_paragraphs'] = HelpParagraph.objects.order_by('order')
        return context

class CalendarDay:
    def __init__(self, day_number):
        self.day_number = day_number
        self.message = None
        self.filled_value = False
        self.passed = False
    def __str__(self):
        return self.day_number
    
def add_to_calendar(year_calendar, date, data_to_add, filled_value):
      month = year_calendar[date.month - 1]
      for week in month:
          for day in week:
              if day.day_number == date.day:
                  day.message = data_to_add
                  day.filled_value = filled_value
                  day.passed = date < datetime.date.today()
                  return

class CalendarView(generic.TemplateView):
    template_name = "rcapp/calendar.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        now = datetime.datetime.now()
        year = now.year
        year_calendar = []
        for month in range(0, 12):
            year_calendar.append(calendar.monthcalendar(year, month + 1))
        class_year_calendar = []
        for month in year_calendar:
            new_month = []
            for week in month:
                new_week = []
                for day in week:
                    new_day = CalendarDay(day)
                    new_week.append(new_day)
                new_month.append(new_week)
            class_year_calendar.append(new_month)
        rc = self.kwargs['pk']
        output_indicators = OutputIndicator.objects.filter(rc_ref=rc)
        outcome_indicators = OutcomeIndicator.objects.filter(rc_ref=rc)
        impact_indicators = ImpactIndicator.objects.filter(rc_ref=rc)
        indicators = list(output_indicators) + list(outcome_indicators) + list(impact_indicators)
        for indicator in indicators:
            indicator_date = indicator.recieve_date
            indicator_frequency = indicator.frequency
            if indicator_date is not None:
                inds_index = 0
                if indicator.values.strip() != "":
                    ind_values = indicator.values.strip().split(',')
                    # del
                    context["ind_values"] = ind_values
                else:
                    ind_values = []
                if indicator_date.year == year:
                    add_to_calendar(class_year_calendar, indicator_date, (indicator.value if indicator.value != "custom" else indicator.custom_value), len(ind_values) > inds_index and ind_values[inds_index] != "")
                if indicator_frequency is not None and indicator_frequency != 0:
                    while True:
                        indicator_date = indicator_date + relativedelta(months=(int(12/indicator_frequency)))
                        if indicator_date.year == year:
                            add_to_calendar(class_year_calendar, indicator_date, (indicator.value if indicator.value != "custom" else indicator.custom_value), len(ind_values) > inds_index and ind_values[inds_index] != "")
                        if indicator_date.year > year:
                            break
                        inds_index += 1
        context["calendar"] = class_year_calendar
        context["rc"] = rc
        context["months"] = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        return context

# New helper

class ViewNewRCHelperPage(generic.TemplateView):
    template_name = "main/helpers/rc.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewRCHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class ViewNewTargetsHelperPage(generic.TemplateView):
    template_name = "main/helpers/targets.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewTargetsHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['hyperlinks'] = TargetsHyperlink.objects.all()
        return context

class ViewNewResourcesHelperPage(generic.TemplateView):
    template_name = "main/helpers/resources.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewResourcesHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class ViewNewActivitiesHelperPage(generic.TemplateView):
    template_name = "main/helpers/activities.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewActivitiesHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class ViewNewOutputsHelperPage(generic.TemplateView):
    template_name = "main/helpers/outputs.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewOutputsHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class ViewNewOutcomesHelperPage(generic.TemplateView):
    template_name = "main/helpers/outcomes.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewOutcomesHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class ViewNewImpactsHelperPage(generic.TemplateView):
    template_name = "main/helpers/impacts.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewImpactsHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class ViewNewAdditionalHelperPage(generic.TemplateView):
    template_name = "main/helpers/additional.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(ViewNewAdditionalHelperPage, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
        
class UserRequestsListView(generic.ListView):
    template_name = "rcapp/user_requests_list.html"
    context_object_name = 'requests'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(UserRequestsListView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    def get_queryset(self):
        return UserRequest.objects.filter(created=False).order_by('-pk')

class UserRequestsMonitorView(generic.ListView):
    template_name = "rcapp/user_requests_monitor.html"
    context_object_name = 'requests'
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(UserRequestsMonitorView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    def get_queryset(self):
        return UserRequest.objects.order_by('-pk')
        
class UserRequestView(generic.DetailView):
    template_name = "rcapp/user_request_view.html"
    model = UserRequest
    def post(self, request, *args, **kwargs):
        submit = get_value_or_none(self.request.POST, 'submit')
        if submit == "1":
            ur = UserRequest.objects.get(pk=self.kwargs['pk'])
            User.objects.create_user(username=ur.username, email=ur.email, password=ur.password)
            ur.created = True
            ur.submission_date = datetime.datetime.now()
            ur.save()
            if ur.wanna_be_shown:
                ur.create_company()
            send_mail('Заявка на сервисе pion.org.ru', 'Ваша заявка принята! Вы можете войти с использованием ваших логина и пароля по адресу https://pion.org.ru', 'mail@pion.org.ru', [ur.email], fail_silently=True)
        return redirect("/portal/user_requests_list")
        
class UserRequestViewDecline(generic.DetailView):
    template_name = "rcapp/user_request_view.html"
    model = UserRequest
    def post(self, request, *args, **kwargs):
        ur = UserRequest.objects.get(pk=self.kwargs['pk'])
        ur.created = True
        ur.save()
        return redirect("/portal/user_requests_list")
        
class RegistrationSuccess(generic.TemplateView):
    template_name = "rcapp/registration_success.html"

class UserExists(generic.TemplateView):
    template_name = "rcapp/user_exists.html"

class UserInProgress(generic.TemplateView):
    template_name = "rcapp/user_in_progress.html"

class CreateCompanyData(generic.View):
    def get(self, request, *args, **kwargs):
        pk = get_value_or_none(self.request.GET, 'pk')
        if pk is None:
            return redirect("/portal/user_requests_monitor")
        user_requests = UserRequest.objects.filter(pk=pk)
        if len(user_requests) == 0:
            return redirect("/portal/user_requests_monitor")
        user_request = user_requests[0]
        user_request.create_company()
        return redirect("/portal/user_requests_monitor")
class RemoveCompanyData(generic.View):
    def get(self, request, *args, **kwargs):
        pk = get_value_or_none(self.request.GET, 'pk')
        if pk is None:
            return redirect("/portal/user_requests_monitor")
        user_requests = UserRequest.objects.filter(pk=int(pk))
        if len(user_requests) == 0:
            return redirect("/portal/user_requests_monitor")
        user_request = user_requests[0]
        user_request.remove_company()
        return redirect("/portal/user_requests_monitor")

class IndicatorsLibraryView(generic.TemplateView):
    template_name = "rcapp/library.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(IndicatorsLibraryView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['page_title'] = 'Библиотека показателей'
        content = get_value_or_none(self.request.GET, 'content')
        resulting_list = []
        if content == "outputindicators":
            context["is_output"] = True
            output_indicators = OutputIndicator.objects.filter(value="custom").order_by('-pk')
            for output_indicator in output_indicators:
                output_indicator.is_output = True
                output_indicator.is_outcome = False
                output_indicator.is_impact = False
                resulting_list.append(output_indicator)
        elif content == "outcomeindicators":
            context["is_outcome"] = True
            outcome_indicators = OutcomeIndicator.objects.filter(value="custom").order_by('-pk')
            for outcome_indicator in outcome_indicators:
                outcome_indicator.is_output = False
                outcome_indicator.is_outcome = True
                outcome_indicator.is_impact = False
                resulting_list.append(outcome_indicator)
        elif content == "impactindicators":
            context["is_impact"] = True
            impact_indicators = ImpactIndicator.objects.filter(value="custom").order_by('-pk')
            for impact_indicator in impact_indicators:
                impact_indicator.is_output = False
                impact_indicator.is_outcome = False
                impact_indicator.is_impact = True
                resulting_list.append(impact_indicator)
        else:
            context["is_all"] = True
            output_indicators = OutputIndicator.objects.filter(value="custom").order_by('-pk')
            for output_indicator in output_indicators:
                output_indicator.is_output = True
                output_indicator.is_outcome = False
                output_indicator.is_impact = False
                resulting_list.append(output_indicator)
            outcome_indicators = OutcomeIndicator.objects.filter(value="custom").order_by('-pk')
            for outcome_indicator in outcome_indicators:
                outcome_indicator.is_output = False
                outcome_indicator.is_outcome = True
                outcome_indicator.is_impact = False
                resulting_list.append(outcome_indicator)
            impact_indicators = ImpactIndicator.objects.filter(value="custom").order_by('-pk')
            for impact_indicator in impact_indicators:
                impact_indicator.is_output = False
                impact_indicator.is_outcome = False
                impact_indicator.is_impact = True
                resulting_list.append(impact_indicator)
        # get all the indicators here
        context['indicators'] = resulting_list
        return context

class BenchmarkingParameter:
    name = ""
    def __init__(self):
        self.name = ""
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

def containsBenchmarkingParameter(benchmarkingParameterList, elem):
    for el in benchmarkingParameterList:
        if el.name == elem.name:
            return True
    return False

def deduplicateBenchmarkingParametersList(first_list):
    new_list = []
    for elem in first_list:
        if not containsBenchmarkingParameter(new_list, elem):
            new_list.append(elem)
    return new_list


class BenchmarkingParametersView(generic.TemplateView):
    template_name = "rcapp/benchmarking_parameters.html"
    def get(self, request, *args, **kwargs):
        # Getting query parameters
        selected_targets_names = get_value_or_none(self.request.GET, 'selected_targets_names')
        selected_outcomes_names = get_value_or_none(self.request.GET, 'selected_outcomes_names')
        selected_impacts_names = get_value_or_none(self.request.GET, 'selected_impacts_names')
        selected_outcomeIndicators_names = get_value_or_none(self.request.GET, 'selected_outcomeIndicators_names')
        selected_impactIndicators_names = get_value_or_none(self.request.GET, 'selected_impactIndicators_names')
        
        # Checking query 
        if ((selected_targets_names is None or selected_targets_names.strip() == "")
            and (selected_outcomes_names is None or selected_outcomes_names.strip() == "")
            and (selected_impacts_names is None or selected_impacts_names.strip() == "")
            and (selected_outcomeIndicators_names is None or selected_outcomeIndicators_names.strip() == "")
            and (selected_impactIndicators_names is None or selected_impactIndicators_names.strip() == "")):
            if self.request.user.is_authenticated:
                queries = BenchmarkingParametersQuery.objects.filter(user_ref=self.request.user)
                if len(queries) > 0:
                    query = queries[0]
                    query_string = str(query)
                    BenchmarkingParametersQuery.objects.filter(user_ref=self.request.user).delete()
                    return redirect(query_string)
        return super(BenchmarkingParametersView, self).get(self, request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(BenchmarkingParametersView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['page_title'] = 'Бенчмаркинг'

        # Getting query parameters
        selected_targets_names = get_value_or_none(self.request.GET, 'selected_targets_names')
        selected_outcomes_names = get_value_or_none(self.request.GET, 'selected_outcomes_names')
        selected_impacts_names = get_value_or_none(self.request.GET, 'selected_impacts_names')
        selected_outcomeIndicators_names = get_value_or_none(self.request.GET, 'selected_outcomeIndicators_names')
        selected_impactIndicators_names = get_value_or_none(self.request.GET, 'selected_impactIndicators_names')
        
        # Unurl
        if selected_targets_names:
            selected_targets_names = urllib.parse.unquote_plus(selected_targets_names)
        if selected_outcomes_names:
            selected_outcomes_names = urllib.parse.unquote_plus(selected_outcomes_names)
        if selected_impacts_names:
            selected_impacts_names = urllib.parse.unquote_plus(selected_impacts_names)
        if selected_outcomeIndicators_names:
            selected_outcomeIndicators_names = urllib.parse.unquote_plus(selected_outcomeIndicators_names)
        if selected_impactIndicators_names:
            selected_impactIndicators_names = urllib.parse.unquote_plus(selected_impactIndicators_names)
        # Unjson
        if selected_targets_names:
            selected_targets_names = json.loads(selected_targets_names)
        if selected_outcomes_names:
            selected_outcomes_names = json.loads(selected_outcomes_names)
        if selected_impacts_names:
            selected_impacts_names = json.loads(selected_impacts_names)
        if selected_outcomeIndicators_names:
            selected_outcomeIndicators_names = json.loads(selected_outcomeIndicators_names)
        if selected_impactIndicators_names:
            selected_impactIndicators_names = json.loads(selected_impactIndicators_names)

        if selected_targets_names:
            context["selected_targets_names"] = selected_targets_names
        if selected_outcomes_names:
            context["selected_outcomes_names"] = selected_outcomes_names
        if selected_impacts_names:
            context["selected_impacts_names"] = selected_impacts_names
        if selected_outcomeIndicators_names:
            context["selected_outcomeIndicators_names"] = selected_outcomeIndicators_names
        if selected_impactIndicators_names:
            context["selected_impactIndicators_names"] = selected_impactIndicators_names
        # Targets names
        targets = Target.objects.all()
        targets_names = []
        for target in targets:
            if target.value != "custom":
                targets_names.append(BenchmarkingParameter(target.value))
            else:
                targets_names.append(BenchmarkingParameter(target.custom_value))
        targets_names = deduplicateBenchmarkingParametersList(targets_names)
        targets_names = sorted(targets_names, key=lambda property: str(property).lower())
        context['targets_names'] = targets_names

        # Outcomes names
        outcomes = Outcome.objects.all()
        outcomes_names = []
        for outcome in outcomes:
            if outcome.value != "custom":
                outcomes_names.append(BenchmarkingParameter(outcome.value))
            else:
                outcomes_names.append(BenchmarkingParameter(outcome.custom_value))
        outcomes_names = deduplicateBenchmarkingParametersList(outcomes_names)
        outcomes_names = sorted(outcomes_names, key=lambda property: str(property).lower())
        # Filtering system
        for outcome_name in outcomes_names:
            # targets_names = []
            outcomes = Outcome.objects.filter(Q(value = outcome_name) | Q(custom_value = outcome_name))
            # for outcome in outcomes:
            #     outputs = outcome.output_refs.all()
            #     for output in outputs:
            #         activities = output.activity_refs.all()
            #         for activity in activities:
            #             targets = activity.target_refs.all()
            #             targets_names += [str(target) for target in targets]
            outcomes_rcs = [outcomes_elem.rc_ref for outcomes_elem in outcomes]
            targets = Target.objects.filter(rc_ref__in=outcomes_rcs)
            targets_names = [str(target) for target in targets]
            targets_names = list(set(targets_names))
            outcome_name.targets_names = targets_names
        # Filtering system end
        context['outcomes_names'] = outcomes_names

        # Impacts names
        impacts = Impact.objects.all()
        impacts_names = []
        for impact in impacts:
            if impact.value != "custom":
                impacts_names.append(BenchmarkingParameter(impact.value))
            else:
                impacts_names.append(BenchmarkingParameter(impact.custom_value))
        impacts_names = deduplicateBenchmarkingParametersList(impacts_names)
        impacts_names = sorted(impacts_names, key=lambda property: str(property).lower())
        # Filtering system
        for impact_name in impacts_names:
            # outcomes_names = []
            impacts = Impact.objects.filter(Q(value = impact_name) | Q(custom_value = impact_name))
            # for impact in impacts:
            #     outcomes = impact.outcome_refs.all()
            #     outcomes_names += [str(outcome) for outcome in outcomes]
            impacts_rcs = [impacts_elem.rc_ref for impacts_elem in impacts]
            outcomes = Outcome.objects.filter(rc_ref__in=impacts_rcs)
            outcomes_names = [str(outcome) for outcome in outcomes]
            outcomes_names = list(set(outcomes_names))
            impact_name.outcomes_names = outcomes_names
        # Filtering system end
        context['impacts_names'] = impacts_names

        # OutcomeIndicators names
        outcomeIndicators = OutcomeIndicator.objects.all()
        outcomeIndicators_names = []
        for outcomeIndicator in outcomeIndicators:
            if outcomeIndicator.value != "custom":
                outcomeIndicators_names.append(BenchmarkingParameter(outcomeIndicator.value))
            else:
                outcomeIndicators_names.append(BenchmarkingParameter(outcomeIndicator.custom_value))
        outcomeIndicators_names = deduplicateBenchmarkingParametersList(outcomeIndicators_names)
        outcomeIndicators_names = sorted(outcomeIndicators_names, key=lambda property: str(property).lower())
        for outcomeIndicator_name in outcomeIndicators_names:
            outcomes_names = []
            outcomeIndicators = OutcomeIndicator.objects.filter(Q(value = outcomeIndicator_name) | Q(custom_value = outcomeIndicator_name))
            for outcomeIndicator in outcomeIndicators:
                outcome = outcomeIndicator.outcome_ref
                outcomes_names.append(str(outcome))
            outcomes_names = list(set(outcomes_names))
            outcomeIndicator_name.outcomes_names = outcomes_names
        context['outcomeIndicators_names'] = outcomeIndicators_names

        # ImpactIndicators names
        impactIndicators = ImpactIndicator.objects.all()
        impactIndicators_names = []
        for impactIndicator in impactIndicators:
            if impactIndicator.value != "custom":
                impactIndicators_names.append(BenchmarkingParameter(impactIndicator.value))
            else:
                impactIndicators_names.append(BenchmarkingParameter(impactIndicator.custom_value))
        impactIndicators_names = deduplicateBenchmarkingParametersList(impactIndicators_names)
        impactIndicators_names = sorted(impactIndicators_names, key=lambda property: str(property).lower())
        for impactIndicator_name in impactIndicators_names:
            impacts_names = []
            impactIndicators = ImpactIndicator.objects.filter(Q(value = impactIndicator_name) | Q(custom_value = impactIndicator_name))
            for impactIndicator in impactIndicators:
                impact = impactIndicator.impact_ref
                impacts_names.append(str(impact))
            impacts_names = list(set(impacts_names))
            impactIndicator_name.impacts_names = impacts_names
        context['impactIndicators_names'] = impactIndicators_names

        return context
        
    def post(self, request, *args, **kwargs):
        selected_targets_names = get_value_or_none(self.request.POST, 'selected_targets_names')
        selected_outcomes_names = get_value_or_none(self.request.POST, 'selected_outcomes_names')
        selected_impacts_names = get_value_or_none(self.request.POST, 'selected_impacts_names')
        selected_outcomeIndicators_names = get_value_or_none(self.request.POST, 'selected_outcomeIndicators_names')
        selected_impactIndicators_names = get_value_or_none(self.request.POST, 'selected_impactIndicators_names')
        return redirect("/portal/benchmarking_results?"
            +"selected_targets_names=" + urllib.parse.quote_plus(selected_targets_names)
            +"&selected_outcomes_names=" + urllib.parse.quote_plus(selected_outcomes_names)
            +"&selected_impacts_names=" + urllib.parse.quote_plus(selected_impacts_names)
            +"&selected_outcomeIndicators_names=" + urllib.parse.quote_plus(selected_outcomeIndicators_names)
            +"&selected_impactIndicators_names=" + urllib.parse.quote_plus(selected_impactIndicators_names)
        )

class BenchmarkingResultsView(generic.TemplateView):
    template_name = "rcapp/benchmarking_results.html"
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(BenchmarkingResultsView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['page_title'] = 'Бенчмаркинг'
        # Getting values from url
        selected_targets_names = get_value_or_none(self.request.GET, 'selected_targets_names')
        selected_outcomes_names = get_value_or_none(self.request.GET, 'selected_outcomes_names')
        selected_impacts_names = get_value_or_none(self.request.GET, 'selected_impacts_names')
        selected_outcomeIndicators_names = get_value_or_none(self.request.GET, 'selected_outcomeIndicators_names')
        selected_impactIndicators_names = get_value_or_none(self.request.GET, 'selected_impactIndicators_names')

        params_string = "/portal/benchmarking_parameters?"
        params_string += "selected_targets_names=" + urllib.parse.quote_plus(selected_targets_names)
        params_string += "&selected_outcomes_names=" + urllib.parse.quote_plus(selected_outcomes_names)
        params_string += "&selected_impacts_names=" + urllib.parse.quote_plus(selected_impacts_names)
        params_string += "&selected_outcomeIndicators_names=" + urllib.parse.quote_plus(selected_outcomeIndicators_names)
        params_string += "&selected_impactIndicators_names=" + urllib.parse.quote_plus(selected_impactIndicators_names)
        context["params_string"] = params_string
        # Save to BenchmarkingParametersQuery
        if self.request.user.is_authenticated:
            BenchmarkingParametersQuery.objects.filter(user_ref = self.request.user).delete()
            BenchmarkingParametersQuery.objects.create(user_ref = self.request.user, query = params_string)

        # Unurl
        selected_targets_names = urllib.parse.unquote_plus(selected_targets_names)
        selected_outcomes_names = urllib.parse.unquote_plus(selected_outcomes_names)
        selected_impacts_names = urllib.parse.unquote_plus(selected_impacts_names)
        selected_outcomeIndicators_names = urllib.parse.unquote_plus(selected_outcomeIndicators_names)
        selected_impactIndicators_names = urllib.parse.unquote_plus(selected_impactIndicators_names)
        # Unjson
        selected_targets_names = json.loads(selected_targets_names)
        selected_outcomes_names = json.loads(selected_outcomes_names)
        selected_impacts_names = json.loads(selected_impacts_names)
        selected_outcomeIndicators_names = json.loads(selected_outcomeIndicators_names)
        selected_impactIndicators_names = json.loads(selected_impactIndicators_names)
        # Find Objects
        rcs_list = []

        selected_targets = []
        if selected_targets_names and len(selected_targets_names) > 0:
            selected_targets = Target.objects.filter(Q(value__in=selected_targets_names) | Q(custom_value__in=selected_targets_names))
            rcs_list += [selected_target.rc_ref for selected_target in selected_targets]
            
        selected_outcomes = []
        if selected_outcomes_names and len(selected_outcomes_names) > 0:
            selected_outcomes = Outcome.objects.filter(Q(value__in=selected_outcomes_names) | Q(custom_value__in=selected_outcomes_names))
            rcs_list += [selected_outcome.rc_ref for selected_outcome in selected_outcomes]
            
        selected_impacts = []
        if selected_impacts_names and len(selected_impacts_names) > 0:
            selected_impacts = Impact.objects.filter(Q(value__in=selected_impacts_names) | Q(custom_value__in=selected_impacts_names))
            rcs_list += [selected_impact.rc_ref for selected_impact in selected_impacts]
            
        selected_outcomeIndicators = []
        if selected_outcomeIndicators_names and len(selected_outcomeIndicators_names) > 0:
            selected_outcomeIndicators = OutcomeIndicator.objects.filter(Q(value__in=selected_outcomeIndicators_names) | Q(custom_value__in=selected_outcomeIndicators_names))
            rcs_list += [selected_outcomeIndicator.rc_ref for selected_outcomeIndicator in selected_outcomeIndicators]
            
        selected_impactIndicators = []
        if selected_impactIndicators_names and len(selected_impactIndicators_names) > 0:
            selected_impactIndicators = ImpactIndicator.objects.filter(Q(value__in=selected_impactIndicators_names) | Q(custom_value__in=selected_impactIndicators_names))
            rcs_list += [selected_impactIndicator.rc_ref for selected_impactIndicator in selected_impactIndicators]
        
        rcs_list = list(set(rcs_list))

        context["rcs"] = rcs_list
            
        return context

# New views

class NewOutputCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = OutputForm
    model = Output
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(NewOutputCreateView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["target_ref"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
        context['step'] = 3
        context['is_output'] = True
        context['form'].fields["activity_refs"].queryset = Activity.objects.filter(rc_ref=self.kwargs['rc'])
        # Get activities here
        # activities = Activity.objects.filter(rc_ref=context['results_chain'].pk)
        # activities_choises = [[None, 'Выберите из списка']]
        # for activity in activities:
        #     activities_choises.append([str(activity.pk), activity.value])
        # context['activities_choises'] = activities_choises
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        other_outputs = Output.objects.filter(rc_ref = self.object.rc_ref.pk).order_by('-order')
        if len(other_outputs) > 0:
            self.object.order = other_outputs[0].order + 100
        else:
            self.object.order = 0
        # if self.request.POST.get('activity_ref') != None and self.request.POST.get('activity_ref') != '' and self.request.POST.get('activity_ref') != 'None':
        #     self.object.activity_ref = Activity.objects.get(pk=self.request.POST.get('activity_ref'))
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            pass
        else:
            self.object.save()
            form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outputs-table")

# class OutputActivitiesNewView(LoginRequiredMixin, generic.FormView):
#     template_name = 'rcapp/common_create_update.html'
#     form_class = OutputActivitiesNewForm
#     def get_context_data(self, **kwargs):
#         update_last_seen(self.request)
#         context = super(OutputActivitiesNewView, self).get_context_data(**kwargs)
#         context['is_authenticated'] = self.request.user.is_authenticated
#         # context['contacts'] = Contact.objects.order_by('order')
#         # context['links'] = SocialNetworkLink.objects.order_by('order')
#         # context['entity_name'] = self.model._meta.verbose_name.title()
#         # context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
#         # context['form'].fields["target_ref"].queryset = Target.objects.filter(rc_ref=self.kwargs['rc'])
#         # context['step'] = 3
#         context['is_output'] = True
#         context['form'].fields["activity_refs"].queryset = Activity.objects.filter(rc_ref=self.kwargs['rc'])
#     def form_valid(self, form):
#         query_string = "?"
#         for activity_ref in form.activity_refs:
#             query_string += "refs[]=" + str(activity_ref.pk)
#             query_string += "&"
#         query_string = query_string[:-1]
#         return redirect("portal/edit/"+ str(self.kwargs['rc']) +"/output-select-value" + query_string)

# class OutputSelectValueView(LoginRequiredMixin, generic.FormView):
#     template_name = ''

# New ------------------------------------------------------------------------------------------------------

class NewOutputCreateActivitiesView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = OutputActivitiesForm
    model = Output
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(NewOutputCreateActivitiesView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        context['form'].fields["activity_refs"].queryset = Activity.objects.filter(rc_ref=self.kwargs['rc'])
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.rc_ref = ResultsChain.objects.get(pk=self.kwargs['rc'])
        other_outputs = Output.objects.filter(rc_ref = self.object.rc_ref.pk).order_by('-order')
        if len(other_outputs) > 0:
            self.object.order = other_outputs[0].order + 100
        else:
            self.object.order = 0
        self.object.save()
        form.save_m2m()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/new-output-create-select/" + str(self.object.pk))

class NewOutputEditSelectView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rcapp/common_create_update.html'
    form_class = OutputSelectForm
    model = Output
    def get_context_data(self, **kwargs):
        update_last_seen(self.request)
        context = super(NewOutputEditSelectView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['contacts'] = Contact.objects.order_by('order')
        context['delete_link'] = self.kwargs['pk'] + "/delete"
        context['links'] = SocialNetworkLink.objects.order_by('order')
        context['entity_name'] = self.model._meta.verbose_name.title()
        context['results_chain'] = ResultsChain.objects.get(pk=self.kwargs['rc'])
        activities = self.object.activity_refs.all()
        outputs = Output.objects.filter(activity_refs__in = activities)
        output_names = []
        for output in outputs:
            output_name = output.value
            if output_name == "custom":
                output_name = output.custom_value
            if output_name is None or output_name == "":
                continue
            output_names.append((output_name, output_name))
        output_names.append(('custom', 'Введите свой вариант'))
        choices=tuple(output_names)
        context['form'].fields["value"].widget = forms.Select(choices=choices, attrs={"onChange":'select_changed()', 'class':'selector'})
        # (('custom', 'Введите свой вариант'),)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        if self.object.value == 'custom' and self.object.custom_value.strip() == '' or self.object.value == None:
            self.object.delete()
        else:
            self.object.save()
        return redirect("/portal/edit/" + str(self.kwargs['rc']) + "/#outputs-table")