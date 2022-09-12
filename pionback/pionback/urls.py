from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from public import views
from django.views.generic.base import TemplateView
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

#router.register(r'user_pass', views.NewPass)

router.register(r'user-requests', views.UserRequestViewSet)
router.register(r'targets', views.TargetViewSet)
router.register(r'practices', views.PracticeViewSet)
router.register(r'outcomes', views.OutcomeViewSet)
router.register(r'outcome-names', views.OutcomeExactNameViewSet)
router.register(r'outcome-indicators', views.OutcomeIndicatorViewSet)
router.register(r'outcome-methods', views.OutcomeMethodViewSet)
router.register(r'logical-models', views.LogicalModelViewSet)
router.register(r'logical-model-change-requests', views.LogicalModelChangeRequestViewSet)
router.register(r'programs', views.ProgramViewSet)
router.register(r'assumptions', views.AssumptionViewSet)
router.register(r'contexts', views.ContextViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'target-descriptions', views.TargetDescriptionViewSet)
router.register(r'program-outputs', views.ProgramOutputViewSet)
router.register(r'program-short-outcomes', views.ProgramShortOutcomeViewSet)
router.register(r'program-mid-outcomes', views.ProgramMidOutcomeViewSet)
router.register(r'program-impacts', views.ProgramImpactViewSet)

router.register(r'mpl-outputs', views.MonitoringPlanLineOutputViewSet)
router.register(r'mpl-short-outcomes', views.MonitoringPlanLineShortOutcomeViewSet)
router.register(r'mpl-mid-outcomes', views.MonitoringPlanLineMidOutcomeViewSet)
router.register(r'mpl-impacts', views.MonitoringPlanLineImpactViewSet)

router.register(r'mfl-outputs', views.MonitoringFormLineOutputViewSet)
router.register(r'mfl-short-outcomes', views.MonitoringFormLineShortOutcomeViewSet)
router.register(r'mfl-mid-outcomes', views.MonitoringFormLineMidOutcomeViewSet)
router.register(r'mfl-impacts', views.MonitoringFormLineImpactViewSet)

#Загрузка разделов
router.register(r'thematic-groups', views.ThematicGroupViewSet)
router.register(r'methods', views.MethodViewSet)
router.register(r'tool-tags', views.ToolTagViewSet)
router.register(r'outcome-levels', views.OutcomeLevelViewSet)
router.register(r'monitoring-elements', views.MonitoringElementViewSet)
router.register(r'organization-activities', views.OrganizationActivityViewSet)

#Библиотека инструментов
router.register(r'tools', views.ToolViewSet)
router.register(r'tool-change-requests', views.ToolChangeRequestViewSet)

#Библиотека кейсов
router.register(r'cases', views.CaseViewSet)
router.register(r'case-change-requests', views.CaseChangeRequestViewSet)
router.register(r'evaluation-reports', views.EvaluationReportViewSet)
router.register(r'evaluation-report-change-requests', views.EvaluationReportChangeRequestViewSet)



#Представления данных в отчете
router.register(r'representation-methods', views.RepresentationMethodViewSet)

#Вид оценки
router.register(r'evaluation-types', views.EvaluationTypeViewSet)

#Метод анализа
router.register(r'analysis-methods', views.AnalysisMethodViewSet)


urlpatterns = [

    path('api/send-new-user-password/', views.SendNewUserPassword, name="user_pass"),


    path('api/testItem/', views.TestItem, name="testItem"),



    path('api/', include(router.urls)),
    path('api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/mainapp/', include('mainapp.urls')),
    path('api/admin/', admin.site.urls),
    path('api/download', views.download),
    path('api/download-plan', views.downloadPlan),
    path('api/download-form', views.downloadForm),
    url('^.*', TemplateView.as_view(template_name="index.html")),
]