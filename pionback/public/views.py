from statistics import mean
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.views.generic import ListView, View
from public.serializers import * 
from public.models import * 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse, Http404
from docxtpl import DocxTemplate, RichText
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives

import requests
import json
import urllib.parse

import os, io

#from django.db.models import Q

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserRequestViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_anonymous==True:
            query_set = []
        elif self.request.user.is_superuser==False:
            query_set = queryset.filter(user_ref=self.request.user.id)
        else:
            query_set = queryset.all()
        return query_set

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        userRequest = self.get_object()
        userRequest.accept()
        return Response({'status': 'ok'})
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        userRequest = self.get_object()
        userRequest.decline()
        return Response({'status': 'ok'})

def TestItem(request):
    res = requests.get('http://proj22.vh413286.eurodir.ru/programs.json')
    json2 = res.json() 

    data_test = ""
    for one_object in json2['results']:
        if Program.objects.filter(id=one_object['user_ref']['id']).exists():
            owner = LogicalModel.objects.filter(id=one_object['user_ref']['id']).first()
            data_test += "{} | {}<br>".format(one_object['user_ref']['id'], owner.id)


    return HttpResponse(data_test)



def SendNewUserPassword(request):
    if UserRequest.objects.filter(user_ref__username=request.GET.get('username')).exists():

        password = User.objects.make_random_password()
        owner = UserRequest.objects.filter(user_ref__username=request.GET.get('username')).first()

        user = owner.user_ref
        user.set_password(password)
        user.save(update_fields=['password'])

        template = get_template('password.html')
        context = {'password': password}
        text_content = 'Новый пароль: ' + password
        html_content = template.render(context)
        msg = EmailMultiAlternatives('Новый пароль сайта pion.org.ru', text_content, from_email='mail@pion.org.ru', to=[owner.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({'status':'ok','email': owner.email})
        #return HttpResponse(password)
    else:
        #return HttpResponse("error")
        return JsonResponse({'status':'error'})

class ThematicGroupViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = ThematicGroup.objects.all()
    serializer_class = ThematicGroupSerializer

class ToolTagViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = ToolTag.objects.all()
    serializer_class = ToolTagSerializer


#Библиотека инструментов================================================================================================

class ToolViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def get_queryset(self):
        queryset = self.queryset
        if 'outcome_refs' in self.request.GET:
            query_set = queryset.filter(outcome_refs=self.request.GET['outcome_refs']).filter(Q(createdby=self.request.user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
        else:
            query_set = queryset.filter(Q(createdby=self.request.user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
        return query_set
    
    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

    @action(detail=True, methods=['post'])
    def switchData_library(self, request, pk=None):
        tool_ref = self.get_object()
        tool_ref.add_public_will = True
        tool_ref.save()
        send_mail(
            'Заявка pion.org.ru/newpion',
            'Заявка на добавление инструмента в общую библиотеку https://pion.org.ru/newpion/api/admin/public/tool/{}/change/'.format(tool_ref.id),
            'mail@pion.org.ru',
            ['info@ep.org.ru', 'kolega212@yandex.ru'],
            fail_silently=False,
        )
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'])
    def add_to_library(self, request, pk=None):
        tool = self.get_object()
        linkers = ToolLibraryLink.objects.filter(user_ref=self.request.user.id).filter(tool_ref=tool.id)
        if len(linkers) == 0:
            ToolLibraryLink.objects.create(user_ref=self.request.user, tool_ref=tool)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'])
    def remove_from_library(self, request, pk=None):
        tool = self.get_object()
        linkers = ToolLibraryLink.objects.filter(user_ref=self.request.user.id).filter(tool_ref=tool.id)
        if len(linkers) != 0:
            linkers.delete()
        return Response({'status': 'ok'})

    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        tool = self.get_object()
        tool.tool_file = request.FILES['tool_file'].encode('utf-8')
        tool.save()
        return tool

    @action(detail=True, methods=['post'])
    def add_outcome(self, request, pk=None):
        tool = self.get_object()
        outcome_ref = Outcome.objects.get(id=int(request.GET['outcome_ref']))
        tool.outcome_refs.add(outcome_ref)
        return Response({'status': 'ok'})

class ToolChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ToolChangeRequest.objects.all()
    serializer_class = ToolChangeRequestSerializer

    @action(detail=True, methods=['post'])
    def upload_data(self, request, pk=None):
        data = request.data
        tool = Tool.objects.filter(Q(pk=pk) & Q(createdby=request.user)).first()
        if tool:
            fields = []
            if tool.add_public_confirm:
                tchr, created = ToolChangeRequest.objects.get_or_create(pk=pk)
                for key, value in data.items():
                    if (key in ['outcome_refs', 'target_refs', 'tool_tag_refs'])==False:
                        fields.append(key)
                if data['thematic_group_ref']: 
                    thematic_group_ref = ThematicGroup.objects.get(id=int(data['thematic_group_ref']))    
                    tchr.thematic_group_ref = thematic_group_ref
                if data['practice_ref']: 
                    practice_ref = Practice.objects.get(id=int(data['practice_ref']))    
                    tchr.practice_ref = practice_ref
                if data['method_ref']: 
                    method_ref = Method.objects.get(id=int(data['method_ref']))    
                    tchr.method_ref = method_ref
                if data['outcome_level_ref']: 
                    outcome_level_ref = OutcomeLevel.objects.get(id=int(data['outcome_level_ref']))
                    tchr.outcome_level_ref = outcome_level_ref
                if data['name']: tchr.name = data['name']
                if data['info']: tchr.info = data['info']
                if data['url']: tchr.url = data['url']

                tchr.save(update_fields=fields)

                if data['tool_tag_refs']: 
                    tool_tag_refs = ToolTag.objects.filter(pk__in=[int(key) for key in data['tool_tag_refs']])
                    tchr.tool_tag_refs.set(tool_tag_refs)
                if data['target_refs']: 
                    target_refs = Target.objects.filter(pk__in=[int(key) for key in data['target_refs']])
                    tchr.target_refs.set(target_refs)
                if data['outcome_refs']: 
                    outcome_refs = Outcome.objects.filter(pk__in=[int(key) for key in data['outcome_refs']])
                    tchr.outcome_refs.set(outcome_refs)

                send_mail(
                    'Заявка pion.org.ru/newpion',
                    'Заявка на редактирование инструмента из общей библиотеки https://pion.org.ru/newpion/api/admin/public/tool/{}/change/'.format(tool.id),
                    'mail@pion.org.ru',
                    ['romanova.zoya.2002@mail.ru', 'info@ep.org.ru', 'kolega212@yandex.ru'],
                    fail_silently=False,
                )
                return Response({'status': 'ok', 'message': 'request'})
            else:
                for key, value in data.items():
                    if value and (key in ['outcome_refs', 'target_refs', 'tool_tag_refs'])==False:
                        fields.append(key)

                if data['name']: tool.name = data['name']
                if data['info']: tool.info = data['info']
                if data['thematic_group_ref']: 
                    thematic_group_ref = ThematicGroup.objects.get(id=int(data['thematic_group_ref']))    
                    tool.thematic_group_ref = thematic_group_ref
                if data['target_refs']: 
                    target_refs = Target.objects.filter(pk__in=[int(key) for key in data['target_refs']])
                    tool.target_refs.set(target_refs)
                if data['practice_ref']: 
                    practice_ref = Practice.objects.get(id=int(data['practice_ref']))    
                    tool.practice_ref = practice_ref
                if data['method_ref']: 
                    method_ref = Method.objects.get(id=int(data['method_ref']))    
                    tool.method_ref = method_ref
                if data['outcome_level_ref']: 
                    outcome_level_ref = OutcomeLevel.objects.get(id=int(data['outcome_level_ref']))
                    tool.outcome_level_ref = outcome_level_ref
                if data['outcome_refs']: 
                    outcome_refs = Outcome.objects.filter(pk__in=[int(key) for key in data['outcome_refs']])
                    tool.outcome_refs.set(outcome_refs)
                if data['url']: tool.url = data['url']
                if data['tool_tag_refs']: 
                    tool_tag_refs = ToolTag.objects.filter(pk__in=[int(key) for key in data['tool_tag_refs']])
                    tool.tool_tag_refs.set(tool_tag_refs)

                tool.save(update_fields=fields)
                serializer = self.get_serializer(tool) 
                return JsonResponse({'status': 'ok', 'message': 'edit', 'result': serializer.data})
        else:
            return Response({'status': 'error'})

    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        tool = self.get_object()
        tool.tool_file = request.FILES['tool_file'].encode('utf-8')
        tool.save()
        return tool

#=======================================================================================================================

class CaseViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(Q(createdby=self.request.user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
        return query_set
    
    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

    @action(detail=True, methods=['post'])
    def switchData_library(self, request, pk=None):
        case_ref = self.get_object()
        case_ref.add_public_will = True
        case_ref.save()
        send_mail(
            'Заявка pion.org.ru/newpion',
            'Заявка на добавление кейса в общую библиотеку https://pion.org.ru/newpion/api/admin/public/case/{}/change/'.format(case_ref.id),
            'mail@pion.org.ru',
            ['info@ep.org.ru', 'kolega212@yandex.ru'],
            fail_silently=False,
        )
        return Response({'status': 'ok'})


    @action(detail=True, methods=['post'])
    def add_to_library(self, request, pk=None):
        case = self.get_object()
        linkers = CaseLibraryLink.objects.filter(user_ref=self.request.user.id).filter(case_ref=case.id)
        if len(linkers) == 0:
            CaseLibraryLink.objects.create(user_ref=self.request.user, case_ref=case)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'])
    def remove_from_library(self, request, pk=None):
        case = self.get_object()
        linkers = CaseLibraryLink.objects.filter(user_ref=self.request.user.id).filter(case_ref=case.id)
        if len(linkers) != 0:
            linkers.delete()
        return Response({'status': 'ok'})

    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        case = self.get_object()
        case.case_file = request.FILES['case_file'].encode('utf-8')
        case.save()
        return case


class CaseChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = CaseChangeRequest.objects.all()
    serializer_class = CaseChangeRequestSerializer

    @action(detail=True, methods=['post'])
    def upload_data(self, request, pk=None):
        data = request.data
        case = Case.objects.filter(Q(pk=pk) & Q(createdby=request.user)).first()
        if case:
            fields = []
            if case.add_public_confirm:
                tchr, created = CaseChangeRequest.objects.get_or_create(pk=pk)
                for key, value in data.items():
                    if (key in ['organization_activity_refs', 'target_refs', 'monitoring_element_refs'])==False:
                        fields.append(key)

                if data['thematic_group_ref']: 
                    thematic_group_ref = ThematicGroup.objects.get(id=int(data['thematic_group_ref']))    
                    tchr.thematic_group_ref = thematic_group_ref
                if data['practice_ref']: 
                    practice_ref = Practice.objects.get(id=int(data['practice_ref']))    
                    tchr.practice_ref = practice_ref
                if data['name']: tchr.name = data['name']
                if data['organization']: tchr.organization = data['organization']
                if data['url']: tchr.url = data['url']
                if data['verification_info']: tchr.verification_info = data['verification_info']
                if data['verification_level_regularity']: tchr.verification_level_regularity = data['verification_level_regularity']
                if data['verification_level_validity']: tchr.verification_level_validity = data['verification_level_validity']
                if data['verification_level_outcome_accessibility']: tchr.verification_level_outcome_accessibility = data['verification_level_outcome_accessibility']
                if data['verification_level_outcome_validity']: tchr.verification_level_outcome_validity = data['verification_level_outcome_validity']

                tchr.save(update_fields=fields)

                if data['organization_activity_refs']: 
                    organization_activity_refs = OrganizationActivity.objects.filter(pk__in=[int(key) for key in data['organization_activity_refs']])
                    tchr.organization_activity_refs.set(organization_activity_refs)
                if data['target_refs']: 
                    target_refs = Target.objects.filter(pk__in=[int(key) for key in data['target_refs']])
                    tchr.target_refs.set(target_refs)
                if data['monitoring_element_refs']: 
                    monitoring_element_refs = MonitoringElement.objects.filter(pk__in=[int(key) for key in data['monitoring_element_refs']])
                    tchr.monitoring_element_refs.set(monitoring_element_refs)

                send_mail(
                    'Заявка pion.org.ru/newpion',
                    'Заявка на редактирование кейса из общей библиотеки https://pion.org.ru/newpion/api/admin/public/case/{}/change/'.format(case.id),
                    'mail@pion.org.ru',
                    ['romanova.zoya.2002@mail.ru', 'info@ep.org.ru', 'kolega212@yandex.ru'],
                    fail_silently=False,
                )
                return Response({'status': 'ok', 'message': 'request'})
            else:
                for key, value in data.items():
                    if value and (key in ['organization_activity_refs', 'target_refs', 'monitoring_element_refs'])==False:
                        fields.append(key)

                if data['thematic_group_ref']: 
                    thematic_group_ref = ThematicGroup.objects.get(id=int(data['thematic_group_ref']))    
                    case.thematic_group_ref = thematic_group_ref
                if data['practice_ref']: 
                    practice_ref = Practice.objects.get(id=int(data['practice_ref']))    
                    case.practice_ref = practice_ref
                if data['name']: case.name = data['name']
                if data['organization']: case.organization = data['organization']
                if data['url']: case.url = data['url']
                if data['verification_info']: case.verification_info = data['verification_info']
                if data['verification_level_regularity']: case.verification_level_regularity = data['verification_level_regularity']
                if data['verification_level_validity']: case.verification_level_validity = data['verification_level_validity']
                if data['verification_level_outcome_accessibility']: case.verification_level_outcome_accessibility = data['verification_level_outcome_accessibility']
                if data['verification_level_outcome_validity']: case.verification_level_outcome_validity = data['verification_level_outcome_validity']
                if data['organization_activity_refs']: 
                    organization_activity_refs = OrganizationActivity.objects.filter(pk__in=[int(key) for key in data['organization_activity_refs']])
                    case.organization_activity_refs.set(organization_activity_refs)
                if data['target_refs']: 
                    target_refs = Target.objects.filter(pk__in=[int(key) for key in data['target_refs']])
                    case.target_refs.set(target_refs)
                if data['monitoring_element_refs']: 
                    monitoring_element_refs = MonitoringElement.objects.filter(pk__in=[int(key) for key in data['monitoring_element_refs']])
                    case.monitoring_element_refs.set(monitoring_element_refs)

                case.save(update_fields=fields)
                serializer = self.get_serializer(case) 
                return JsonResponse({'status': 'ok', 'message': 'edit', 'result': serializer.data})
        else:
            return Response({'status': 'error'})


    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        case = self.get_object()
        case.case_file = request.FILES['case_file'].encode('utf-8')
        case.save()
        return case

#=======================================================================================================================

class RepresentationMethodViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = RepresentationMethod.objects.all()
    serializer_class = RepresentationMethodSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(add_public=True)
        return query_set

class EvaluationTypeViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = EvaluationType.objects.all()
    serializer_class = EvaluationTypeSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(add_public=True)
        return query_set

class AnalysisMethodViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = AnalysisMethod.objects.all()
    serializer_class = AnalysisMethodSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(add_public=True)
        return query_set

class TargetViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def get_queryset(self):
        queryset = self.queryset
        if 'parent_ref' in self.request.GET:
            if self.request.GET['parent_ref'] == '0':
                query_set = queryset.filter(parent_ref__isnull=True)
            else:
                query_set = queryset.filter(parent_ref=self.request.GET['parent_ref'])
        else:
            query_set = queryset.all()

        return query_set

class PracticeViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Practice.objects.all()
    serializer_class = PracticeSerializer

class MethodViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Method.objects.all()
    serializer_class = MethodSerializer

    def get_queryset(self):
        queryset = self.queryset
        if 'parent_ref' in self.request.GET:
            if self.request.GET['parent_ref'] == '0':
                query_set = queryset.filter(parent_ref__isnull=True).filter(add_public=True)
            else:
                query_set = queryset.filter(parent_ref=self.request.GET['parent_ref']).filter(add_public=True)
        else:
            query_set = queryset.filter(add_public=True)
        return query_set

class OutcomeLevelViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = OutcomeLevel.objects.all()
    serializer_class = OutcomeLevelSerializer

class MonitoringElementViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = MonitoringElement.objects.all()
    serializer_class = MonitoringElementSerializer

class OrganizationActivityViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = OrganizationActivity.objects.all()
    serializer_class = OrganizationActivitySerializer

class EvaluationReportViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = EvaluationReport.objects.all()
    serializer_class = EvaluationReportSerializer

    def get_queryset(self):
        queryset = self.queryset
        if 'outcome_refs' in self.request.GET:
            if self.request.GET['outcome_refs'] == '0':
                query_set = queryset.filter(Q(case_ref__createdby=self.request.user.id) & ~Q(case_ref__createdby=None) | Q(add_public_confirm=True))
            else:
                cases = Case.objects.filter(Q(createdby=self.request.user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
                reports = queryset.filter(Q(case_ref__createdby=self.request.user.id) & ~Q(case_ref__createdby=None) | Q(add_public_confirm=True)).filter(case_ref__in=cases)    
                query_set = []
                for report in reports.all():
                    for outcome in report.outcome_refs.all():
                        if int(self.request.GET['outcome_refs']) == outcome.pk: 
                            query_set.append(report)

        else:
            query_set = queryset.filter(Q(case_ref__createdby=self.request.user.id) & ~Q(case_ref__createdby=None) | Q(add_public_confirm=True))

        return query_set

    @action(detail=True, methods=['post'])
    def add_public_confirm(self, request, pk=None):
        report = self.get_object()
        report.add_public_will = True
        report.add_public_confirm = False
        report.save()
        send_mail(
            'Заявка pion.org.ru/newpion',
            'Заявка на добавление отчёта об оценке к кейсу из общей библиотеки https://pion.org.ru/newpion/api/admin/public/evaluationreport/{}/change/'.format(report.id),
            'mail@pion.org.ru',
            ['romanova.zoya.2002@mail.ru', 'info@ep.org.ru', 'kolega212@yandex.ru'],
            fail_silently=False,
        )
        return Response({'status': 'ok'})

    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        report = self.get_object()
        report.evaluation_file = request.FILES['evaluation_file'].encode('utf-8')
        report.save()
        return report


class EvaluationReportChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = EvaluationReportChangeRequest.objects.all()
    serializer_class = EvaluationReportChangeRequestSerializer

    def get_object(self):
          if self.request.method == 'PUT':
              obj, created = EvaluationReportChangeRequest.objects.get_or_create(pk=self.kwargs.get('pk'))
              return obj
          else:
              return super(EvaluationReportChangeRequestViewSet, self).get_object()

    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        report = self.get_object()
        report.evaluation_file = request.FILES['evaluation_file'].encode('utf-8')
        report.save()
        return report

    @action(detail=True, methods=['post'])
    def add_public_confirm(self, request, pk=None):
        report = self.get_object()
        report.add_public_confirm = False
        report.save()
        send_mail(
            'Заявка pion.org.ru/newpion',
            'Заявка на редактирование отчёта об оценке кейса из общей библиотеки https://pion.org.ru/newpion/api/admin/public/evaluationreport/{}/change/'.format(report.pk),
            'mail@pion.org.ru',
            ['romanova.zoya.2002@mail.ru', 'info@ep.org.ru', 'kolega212@yandex.ru'],
            fail_silently=False,
        )
        return Response({'status': 'ok'})

class OutcomeViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(Q(createdby=self.request.user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
        return query_set

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

    @action(detail=True, methods=['post'])
    def switchData_library(self, request, pk=None):
        outcome_ref = self.get_object()
        #linkers = OutcomeLibraryLink.objects.filter(user_ref=self.request.user.id).filter(outcome_ref=outcome_ref.id).first()
        outcome_ref.add_public_will = True
        outcome_ref.save()
        send_mail(
            'Заявка pion.org.ru/newpion',
            'Заявка на добавление социального результата в общую библиотеку https://pion.org.ru/newpion/api/admin/outcome/{}/change/'.format(outcome_ref.id),
            'mail@pion.org.ru',
            ['info@ep.org.ru', 'kolega212@yandex.ru'],
            fail_silently=False,
        )
        return Response({'status': 'ok'})
  
    @action(detail=True, methods=['post'])
    def add_to_library(self, request, pk=None):
        outcome = self.get_object()
        linkers = OutcomeLibraryLink.objects.filter(user_ref=self.request.user.id).filter(outcome_ref=outcome.id)
        if len(linkers) == 0:
            OutcomeLibraryLink.objects.create(user_ref=self.request.user, outcome_ref=outcome)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'])
    def remove_from_library(self, request, pk=None):
        outcome = self.get_object()
        linkers = OutcomeLibraryLink.objects.filter(user_ref=self.request.user.id).filter(outcome_ref=outcome.id)
        if len(linkers) != 0:
            linkers.delete()
        return Response({'status': 'ok'})

class OutcomeExactNameViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = OutcomeExactName.objects.all()
    serializer_class = OutcomeExactNameSerializer
    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(outcome_ref=self.request.GET['outcome_ref'])
        return query_set

class OutcomeIndicatorViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = OutcomeIndicator.objects.all()
    serializer_class = OutcomeIndicatorSerializer
    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(outcome_ref=self.request.GET['outcome_ref'])
        return query_set

class OutcomeMethodViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = OutcomeMethod.objects.all()
    serializer_class = OutcomeMethodSerializer
    def get_queryset(self):
        outcome = Outcome.objects.get(pk=self.request.GET['outcome_ref'])
        queryset = self.queryset
        query_set = queryset.filter(pk__in=[outcome_method.pk for outcome_method in outcome.method_refs.all()])
        return query_set

class LogicalModelViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = LogicalModel.objects.all()
    serializer_class = LogicalModelSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(Q(createdby=self.request.user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
        return query_set

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

    @action(detail=True, methods=['post'])
    def switchData_library(self, request, pk=None):
        logical_model = self.get_object()
#        linkers = LogicalModelLibraryLink.objects.filter(user_ref=self.request.user.id).filter(logical_model_ref=logical_model.id).first()
        logical_model.add_public_will = True
        logical_model.save()
        send_mail(
            'Заявка pion.org.ru/newpion',
            'Заявка на добавление логической модели в общую библиотеку https://pion.org.ru/newpion/api/admin/logicalmodel/{}/change/'.format(logical_model.id),
            'mail@pion.org.ru',
            ['info@ep.org.ru', 'kolega212@yandex.ru'],
            fail_silently=False,
        )
        return Response({'status': 'ok'})
    
    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        logical_model = self.get_object()
        logical_model.result_tree_file = request.FILES['result_tree_file'].encode('utf-8')
        logical_model.model_file = request.FILES['model_file'].encode('utf-8')
        logical_model.save()
        return logical_model


    @action(detail=True, methods=['post'])
    def add_to_library(self, request, pk=None):
        logical_model = self.get_object()
        linkers = LogicalModelLibraryLink.objects.filter(user_ref=self.request.user.id).filter(logical_model_ref=logical_model.id)
        if len(linkers) == 0:
            LogicalModelLibraryLink.objects.create(user_ref=self.request.user, logical_model_ref=logical_model)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'])
    def remove_from_library(self, request, pk=None):
        logical_model = self.get_object()
        linkers = LogicalModelLibraryLink.objects.filter(user_ref=self.request.user.id).filter(logical_model_ref=logical_model.id)
        if len(linkers) != 0:
            linkers.delete()
        return Response({'status': 'ok'})

class LogicalModelChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = LogicalModelChangeRequest.objects.all()
    serializer_class = LogicalModelChangeRequestSerializer

    @action(detail=True, methods=['post'])
    def upload_data(self, request, pk=None):
        data = request.data
        logical_model = LogicalModel.objects.filter(Q(pk=pk) & Q(createdby=request.user)).first()
        if logical_model:
            fields = []
            if logical_model.add_public_confirm:
                tchr, created = LogicalModelChangeRequest.objects.get_or_create(pk=pk)
                for key, value in data.items():
                    if (key in ['outcome_refs', 'target_refs', 'practice_refs'])==False:
                        fields.append(key)
                if data['thematic_group_ref']: 
                    thematic_group_ref = ThematicGroup.objects.get(id=int(data['thematic_group_ref']))    
                    tchr.thematic_group_ref = thematic_group_ref
                if data['name']: tchr.name = data['name']
                if data['organization']: tchr.organization = data['organization']
                if data['period']: tchr.period = data['period']
                if data['verification_info']: tchr.verification_info = data['verification_info']
                if data['verification_level_regularity']: tchr.verification_level_regularity = data['verification_level_regularity']
                if data['verification_level_validity']: tchr.verification_level_validity = data['verification_level_validity']
                if data['verification_level_outcome_accessibility']: tchr.verification_level_outcome_accessibility = data['verification_level_outcome_accessibility']
                if data['verification_level_outcome_validity']: tchr.verification_level_outcome_validity = data['verification_level_outcome_validity']

                tchr.save(update_fields=fields)

                if data['practice_refs']: 
                    practice_refs = Practice.objects.filter(pk__in=[int(key) for key in data['practice_refs']])
                    tchr.practice_refs.set(practice_refs)
                if data['target_refs']: 
                    target_refs = Target.objects.filter(pk__in=[int(key) for key in data['target_refs']])
                    tchr.target_refs.set(target_refs)
                if data['outcome_refs']:
                    outcome_refs = Outcome.objects.filter(pk__in=[int(key) for key in data['outcome_refs']])
                    tchr.outcome_refs.set(outcome_refs)

                send_mail(
                    'Заявка pion.org.ru/newpion',
                    'Заявка на редактирование логической модели из общей библиотеки https://pion.org.ru/newpion/api/admin/public/logicalmodel/{}/change/'.format(logical_model.id),
                    'mail@pion.org.ru',
                    ['romanova.zoya.2002@mail.ru', 'info@ep.org.ru', 'kolega212@yandex.ru'],
                    fail_silently=False,
                )
                return Response({'status': 'ok', 'message': 'request'})
            else:
                for key, value in data.items():
                    if value and (key in ['outcome_refs', 'target_refs', 'practice_refs'])==False:
                        fields.append(key)

                if data['thematic_group_ref']: 
                    thematic_group_ref = ThematicGroup.objects.get(id=int(data['thematic_group_ref']))    
                    logical_model.thematic_group_ref = thematic_group_ref
                if data['name']: logical_model.name = data['name']
                if data['organization']: logical_model.organization = data['organization']
                if data['period']: logical_model.period = data['period']
                if data['verification_info']: logical_model.verification_info = data['verification_info']
                if data['verification_level_regularity']: logical_model.verification_level_regularity = data['verification_level_regularity']
                if data['verification_level_validity']: logical_model.verification_level_validity = data['verification_level_validity']
                if data['verification_level_outcome_accessibility']: logical_model.verification_level_outcome_accessibility = data['verification_level_outcome_accessibility']
                if data['verification_level_outcome_validity']: logical_model.verification_level_outcome_validity = data['verification_level_outcome_validity']

                if data['practice_refs']: 
                    practice_refs = Practice.objects.filter(pk__in=[int(key) for key in data['practice_refs']])
                    logical_model.practice_refs.set(practice_refs)
                if data['target_refs']: 
                    target_refs = Target.objects.filter(pk__in=[int(key) for key in data['target_refs']])
                    logical_model.target_refs.set(target_refs)
                if data['outcome_refs']: 
                    outcome_refs = Outcome.objects.filter(pk__in=[int(key) for key in data['outcome_refs']])
                    logical_model.outcome_refs.set(outcome_refs)

                logical_model.save(update_fields=fields)
                serializer = self.get_serializer(logical_model) 
                return JsonResponse({'status': 'ok', 'message': 'edit', 'result': serializer.data})
        else:
            return Response({'status': 'error'})

    @action(detail=True, methods=['patch'])
    def upload_files(self, request, filename, format=None):
        logical_model = self.get_object()
        logical_model.result_tree_file = request.FILES['result_tree_file'].encode('utf-8')
        logical_model.model_file = request.FILES['model_file'].encode('utf-8')
        logical_model.save()
        return logical_model

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_superuser==False:
            query_set = queryset.filter(user_ref=self.request.user.id)
        else:
            query_set = queryset.all()
        return query_set

    def perform_create(self, serializer):
        serializer.save(user_ref=self.request.user)

class AssumptionViewSet(viewsets.ModelViewSet):
    queryset = Assumption.objects.all()
    serializer_class = AssumptionSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class ContextViewSet(viewsets.ModelViewSet):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class TargetDescriptionViewSet(viewsets.ModelViewSet):
    queryset = TargetDescription.objects.all()
    serializer_class = TargetDescriptionSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET and 'target_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref']).filter(target_ref=self.request.GET['target_ref'])
        else:
            query_set = queryset
        return query_set

class ProgramOutputViewSet(viewsets.ModelViewSet):
    queryset = ProgramOutput.objects.all()
    serializer_class = ProgramOutputSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set.order_by('priority')
    @action(detail=True, methods=['post'])
    def change_priority(self, request, pk=None):
        logical_model = self.get_object()
        raise Exception(request['priority'])
        return Response({'status': 'ok'})

class ProgramShortOutcomeViewSet(viewsets.ModelViewSet):
    queryset = ProgramShortOutcome.objects.all()
    serializer_class = ProgramShortOutcomeSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set.order_by('priority')
    @action(detail=True, methods=['post'])
    def change_priority(self, request, pk=None):
        logical_model = self.get_object()
        raise Exception(request['priority'])
        return Response({'status': 'ok'})

class ProgramMidOutcomeViewSet(viewsets.ModelViewSet):
    queryset = ProgramMidOutcome.objects.all()
    serializer_class = ProgramMidOutcomeSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set.order_by('priority')
    @action(detail=True, methods=['post'])
    def change_priority(self, request, pk=None):
        logical_model = self.get_object()
        raise Exception(request['priority'])
        return Response({'status': 'ok'})

class ProgramImpactViewSet(viewsets.ModelViewSet):
    queryset = ProgramImpact.objects.all()
    serializer_class = ProgramImpactSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set.order_by('priority')
    @action(detail=True, methods=['post'])
    def change_priority(self, request, pk=None):
        logical_model = self.get_object()
        raise Exception(request['priority'])
        return Response({'status': 'ok'})

class MonitoringPlanLineOutputViewSet(viewsets.ModelViewSet):
    queryset = MonitoringPlanLineOutput.objects.all().order_by('sort_index')
    serializer_class = MonitoringPlanLineOutputSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class MonitoringPlanLineShortOutcomeViewSet(viewsets.ModelViewSet):
    queryset = MonitoringPlanLineShortOutcome.objects.all().order_by('sort_index')
    serializer_class = MonitoringPlanLineShortOutcomeSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class MonitoringPlanLineMidOutcomeViewSet(viewsets.ModelViewSet):
    queryset = MonitoringPlanLineMidOutcome.objects.all().order_by('sort_index')
    serializer_class = MonitoringPlanLineMidOutcomeSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class MonitoringPlanLineImpactViewSet(viewsets.ModelViewSet):
    queryset = MonitoringPlanLineImpact.objects.all().order_by('sort_index')
    serializer_class = MonitoringPlanLineImpactSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class MonitoringFormLineOutputViewSet(viewsets.ModelViewSet):
    queryset = MonitoringFormLineOutput.objects.all().order_by('sort_index')
    serializer_class = MonitoringFormLineOutputSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class MonitoringFormLineShortOutcomeViewSet(viewsets.ModelViewSet):
    queryset = MonitoringFormLineShortOutcome.objects.all().order_by('sort_index')
    serializer_class = MonitoringFormLineShortOutcomeSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class MonitoringFormLineMidOutcomeViewSet(viewsets.ModelViewSet):
    queryset = MonitoringFormLineMidOutcome.objects.all().order_by('sort_index')
    serializer_class = MonitoringFormLineMidOutcomeSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

class MonitoringFormLineImpactViewSet(viewsets.ModelViewSet):
    queryset = MonitoringFormLineImpact.objects.all().order_by('sort_index')
    serializer_class = MonitoringFormLineImpactSerializer
    def get_queryset(self):
        queryset = self.queryset
        if 'program_ref' in self.request.GET:
            query_set = queryset.filter(program_ref=self.request.GET['program_ref'])
        else:
            query_set = queryset
        return query_set

def getActivities(target_id, program_id):
        array = []
        activities = Activity.objects.filter(program_ref=program_id).filter(target_ref=target_id)
        for activity in activities.all():
            array.append({
                'item': activity.name,
                'outputs': getOutputs(activity.id, program_id)
            })
        # if len(activities) == 0:
        #     array.append({
        #         'item': '',
        #         'outputs': getOutputs(None, program_id)
        #     })
        return array

def getOutputs(activity_id, program_id):
    array = []
    outputs = ProgramOutput.objects.filter(program_ref=program_id).filter(activity_ref=activity_id)
    for output in outputs.all():
        array.append({
            'item': output.name,
            'shortoutcomes': getShortOutcomes(output.id, program_id)
        })
    # if len(outputs) == 0:
    #     array.append({
    #     'item': '',
    #     'shortoutcomes': getShortOutcomes(None, program_id)
    # })
    return array

def getShortOutcomes(output_id, program_id):
    array = []
    shortoutcomes = ProgramShortOutcome.objects.filter(program_ref=program_id).filter(program_output_many_refs__in=[output_id])
    for shortoutcome in shortoutcomes.all():
        array.append({
            'item': shortoutcome.name,
            'midoutcomes': getMidOutcomes(shortoutcome.id, program_id)
        })
    # if len(shortoutcomes) == 0:
    #     array.append({
    #     'item': '',
    #     'midoutcomes': getMidOutcomes(None, program_id)
    # })
    return array

def getMidOutcomes(shortoutcome_id, program_id):
    array = []
    midoutcomes = ProgramMidOutcome.objects.filter(program_ref=program_id).filter(program_short_outcome_many_refs__in=[shortoutcome_id])
    for midoutcome in midoutcomes.all():
        array.append({
            'item': midoutcome.name,
            'impacts': getImpacts(midoutcome.id, program_id)
        })
    # if len(midoutcomes) == 0:
    #     array.append({
    #     'item': '',
    #     'ipmacts': getImpacts(None, program_id)
    # })
    return array

def getImpacts(midoutcome_id, program_id):
    array = []
    impacts = ProgramImpact.objects.filter(program_ref=program_id).filter(program_mid_outcome_many_refs__in=[midoutcome_id])
    for impact in impacts.all():
        array.append({
            'item': impact.name,
        })
    # if len(impacts) == 0:
    #     array.append({
    #     'item': ''
    # })
    return array

def download(request):
    program_id = request.GET['program_id']
    program = Program.objects.get(id=program_id)
    targets = program.target_refs.all()
    context = {
        'table_rows': [
        ]
    }

    for target in targets:        
        context['table_rows'].append({
            'item': target.name,
            'activities': getActivities(target.id, program_id)
        })
                                            
    doc = DocxTemplate(os.path.join(settings.BASE_DIR, "templateprogram.docx"))
    doc.render(context)
    doc_io = io.BytesIO() 
    doc.save(doc_io) 
    doc_io.seek(0)
    response = HttpResponse(doc_io.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response['Content-Disposition'] = 'inline; filename=program'+program_id+'.docx'
    return response

def downloadOld(request):
    program_id = request.GET['program_id']
    program = Program.objects.get(id=program_id)
    targets = program.target_refs.all()
    context = {
        'table_rows': [
        ]
    }
    for target in targets:        
        activities = Activity.objects.filter(program_ref=program_id).filter(target_ref=target.id)
        if activities.count() == 0:
            context['table_rows'].append({
                'target': target.name,
                'activity': '',
                'output': '',
                'shortoutcome': '',
                'midoutcome': '',
                'impact': ''
            })
        else:
            for activity in activities.all():
                outputs = ProgramOutput.objects.filter(program_ref=program_id).filter(activity_ref=activity.id)
                if outputs.count() == 0:
                    context['table_rows'].append({
                        'target': target.name,
                        'activity': activity.name,
                        'output': '',
                        'shortoutcome': '',
                        'midoutcome': '',
                        'impact': ''
                    })
                else:
                    for output in outputs.all():
                        shortoutcomes = ProgramShortOutcome.objects.filter(program_ref=program_id).filter(program_output_many_refs__in=[output.id])
                        if shortoutcomes.count() == 0:
                            context['table_rows'].append({
                                'target': target.name,
                                'activity': activity.name,
                                'output': output.name,
                                'shortoutcome': '',
                                'midoutcome': '',
                                'impact': ''
                            })
                        else:
                            for shortoutcome in shortoutcomes.all():
                                midoutcomes = ProgramMidOutcome.objects.filter(program_ref=program_id).filter(program_short_outcome_many_refs__in=[shortoutcome.id])
                                if midoutcomes.count() == 0:
                                    context['table_rows'].append({
                                        'target': target.name,
                                        'activity': activity.name,
                                        'output': output.name,
                                        'shortoutcome': shortoutcome.name,
                                        'midoutcome': '',
                                        'impact': ''
                                    })
                                else:
                                    for midoutcome in midoutcomes.all():
                                        impacts = ProgramImpact.objects.filter(program_ref=program_id).filter(program_mid_outcome_many_refs__in=[midoutcome.id])
                                        if impacts.count() == 0:
                                            context['table_rows'].append({
                                                'target': target.name,
                                                'activity': activity.name,
                                                'output': output.name,
                                                'shortoutcome': shortoutcome.name,
                                                'midoutcome': midoutcome.name,
                                                'impact': ''
                                            })
                                        else:
                                            for impact in impacts.all():
                                                context['table_rows'].append({
                                                    'target': target.name,
                                                    'activity': activity.name,
                                                    'output': output.name,
                                                    'shortoutcome': shortoutcome.name,
                                                    'midoutcome': midoutcome.name,
                                                    'impact': impact.name
                                                })
                                                
    doc = DocxTemplate(os.path.join(settings.BASE_DIR, "template.docx"))
    doc.render(context)
    # doc.save("generated_doc.docx")
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object
    response = HttpResponse(doc_io.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response['Content-Disposition'] = 'inline; filename=program'+program_id+'.docx'
    return response

def getToolUrl(tool_name, tool_type):
    if tool_type=="OutcomeMethods" or bool(tool_type)==False:
        tool = OutcomeMethod.objects.filter(name=tool_name)
        if len(tool) > 0:
            return tool[0].url
    if tool_type=="Tools":
        tool = Tool.objects.filter(name=tool_name)
        if len(tool) > 0:
            return 'https://pion.org.ru/newpion/tools?id=' + str(tool[0].id)
    return ""

def downloadPlan(request):
    doc = DocxTemplate(os.path.join(settings.BASE_DIR, "templateplan.docx"))
    program_id = request.GET['program_id']
    context = {}
    mploutputs = MonitoringPlanLineOutput.objects.filter(program_ref=program_id).all()
    if mploutputs.count() > 0:
        context['output_rows'] = []
        for row in mploutputs:
            result_row = {}
            if row.result_ref:
                result_row['result'] = row.result_ref.name
            result_row['name'] = row.name if row.name else ""
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['method'] = row.method if row.method else ""
            tool_url = getToolUrl(row.tool, row.tool_type)
            rt = RichText()
            if tool_url != "":
                rt.add(row.tool, url_id=doc.build_url_id(tool_url))
                result_row['tool'] = rt
            else:
                result_row['tool'] = row.tool if row.tool else ""
            result_row['frequency'] = row.frequency if row.frequency else ""
            result_row['reporting'] = row.reporting if row.reporting else ""
            context['output_rows'].append(result_row)

    mplshortoutcomes = MonitoringPlanLineShortOutcome.objects.filter(program_ref=program_id).all()
    if mplshortoutcomes.count() > 0:
        context['short_outcome_rows'] = []
        for row in mplshortoutcomes:
            result_row = {}
            if row.result_ref:
                result_row['result'] = row.result_ref.name
            result_row['name'] = row.name if row.name else ""
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['method'] = row.method if row.method else ""
            tool_url = getToolUrl(row.tool, row.tool_type)
            rt = RichText()
            if tool_url != "":
                rt.add(row.tool, url_id=doc.build_url_id(tool_url))
                result_row['tool'] = rt
            else:
                result_row['tool'] = row.tool if row.tool else ""
            result_row['frequency'] = row.frequency if row.frequency else ""
            result_row['reporting'] = row.reporting if row.reporting else ""
            context['short_outcome_rows'].append(result_row)

    mplmidoutcomes = MonitoringPlanLineMidOutcome.objects.filter(program_ref=program_id).all()
    if mplmidoutcomes.count() > 0:
        context['mid_outcome_rows'] = []
        for row in mplmidoutcomes:
            result_row = {}
            if row.result_ref:
                result_row['result'] = row.result_ref.name
            result_row['name'] = row.name if row.name else ""
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['method'] = row.method if row.method else ""
            tool_url = getToolUrl(row.tool, row.tool_type)
            rt = RichText()
            if tool_url != "":
                rt.add(row.tool, url_id=doc.build_url_id(tool_url))
                result_row['tool'] = rt
            else:
                result_row['tool'] = row.tool if row.tool else ""
            result_row['frequency'] = row.frequency if row.frequency else ""
            result_row['reporting'] = row.reporting if row.reporting else ""
            context['mid_outcome_rows'].append(result_row)

    mplimpacts = MonitoringPlanLineImpact.objects.filter(program_ref=program_id).all()
    if mplimpacts.count() > 0:
        context['impact_rows'] = []
        for row in mplimpacts:
            result_row = {}
            if row.result_ref:
                result_row['result'] = row.result_ref.name
            result_row['name'] = row.name if row.name else ""
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['method'] = row.method if row.method else ""
            tool_url = getToolUrl(row.tool, row.tool_type)
            rt = RichText()
            if tool_url != "":
                rt.add(row.tool, url_id=doc.build_url_id(tool_url))
                result_row['tool'] = rt
            else:
                result_row['tool'] = row.tool if row.tool else ""
            result_row['frequency'] = row.frequency if row.frequency else ""
            result_row['reporting'] = row.reporting if row.reporting else ""
            context['impact_rows'].append(result_row)
                                    
    
    doc.render(context)
    # doc.save("generated_doc.docx")
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object
    response = HttpResponse(doc_io.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response['Content-Disposition'] = 'inline; filename=program'+program_id+'.docx'
    return response

def downloadForm(request):
    program_id = request.GET['program_id']
    context = {}
    mfloutputs = MonitoringFormLineOutput.objects.filter(program_ref=program_id).all()
    if mfloutputs.count() > 0:
        context['output_rows'] = []
        for row in mfloutputs:
            result_row = {}
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['plan'] = row.plan if row.plan else ""
            result_row['period1'] = row.period1 if row.period1 else ""
            result_row['fact1'] = row.fact1 if row.fact1 else ""
            result_row['period2'] = row.period2 if row.period2 else ""
            result_row['fact2'] = row.fact2 if row.fact2 else ""
            result_row['period3'] = row.period3 if row.period3 else ""
            result_row['fact3'] = row.fact3 if row.fact3 else ""
            result_row['period4'] = row.period4 if row.period4 else ""
            result_row['fact4'] = row.fact4 if row.fact4 else ""
            context['output_rows'].append(result_row)

    mflshortoutcomes = MonitoringFormLineShortOutcome.objects.filter(program_ref=program_id).all()
    if mflshortoutcomes.count() > 0:
        context['short_outcome_rows'] = []
        for row in mflshortoutcomes:
            result_row = {}
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['plan'] = row.plan if row.plan else ""
            result_row['period1'] = row.period1 if row.period1 else ""
            result_row['fact1'] = row.fact1 if row.fact1 else ""
            result_row['period2'] = row.period2 if row.period2 else ""
            result_row['fact2'] = row.fact2 if row.fact2 else ""
            result_row['period3'] = row.period3 if row.period3 else ""
            result_row['fact3'] = row.fact3 if row.fact3 else ""
            result_row['period4'] = row.period4 if row.period4 else ""
            result_row['fact4'] = row.fact4 if row.fact4 else ""
            context['short_outcome_rows'].append(result_row)

    mflmidoutcomes = MonitoringFormLineMidOutcome.objects.filter(program_ref=program_id).all()
    if mflmidoutcomes.count() > 0:
        context['mid_outcome_rows'] = []
        for row in mflmidoutcomes:
            result_row = {}
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['plan'] = row.plan if row.plan else ""
            result_row['period1'] = row.period1 if row.period1 else ""
            result_row['fact1'] = row.fact1 if row.fact1 else ""
            result_row['period2'] = row.period2 if row.period2 else ""
            result_row['fact2'] = row.fact2 if row.fact2 else ""
            result_row['period3'] = row.period3 if row.period3 else ""
            result_row['fact3'] = row.fact3 if row.fact3 else ""
            result_row['period4'] = row.period4 if row.period4 else ""
            result_row['fact4'] = row.fact4 if row.fact4 else ""
            context['mid_outcome_rows'].append(result_row)

    mflimpacts = MonitoringFormLineImpact.objects.filter(program_ref=program_id).all()
    if mflimpacts.count() > 0:
        context['impact_rows'] = []
        for row in mflimpacts:
            result_row = {}
            result_row['indicator'] = row.indicator if row.indicator else ""
            result_row['plan'] = row.plan if row.plan else ""
            result_row['period1'] = row.period1 if row.period1 else ""
            result_row['fact1'] = row.fact1 if row.fact1 else ""
            result_row['period2'] = row.period2 if row.period2 else ""
            result_row['fact2'] = row.fact2 if row.fact2 else ""
            result_row['period3'] = row.period3 if row.period3 else ""
            result_row['fact3'] = row.fact3 if row.fact3 else ""
            result_row['period4'] = row.period4 if row.period4 else ""
            result_row['fact4'] = row.fact4 if row.fact4 else ""
            context['impact_rows'].append(result_row)
                                    
    doc = DocxTemplate(os.path.join(settings.BASE_DIR, "templateform.docx"))
    doc.render(context)
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object
    response = HttpResponse(doc_io.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response['Content-Disposition'] = 'inline; filename=program'+program_id+'.docx'
    return response

