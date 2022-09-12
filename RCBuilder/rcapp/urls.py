from django.conf.urls import url
from django.urls import reverse

from . import views

urlpatterns = [
    url(r'^$', views.RCsListView.as_view(), name='index'),
    url(r'^(?P<pk>\d{1,9})/{0,1}$', views.RCView.as_view(), name='rcview'),
    url(r'^assign/(?P<pk>\d{1,9})/{0,1}$', views.AssignView.as_view(), name='rcassign'),
    url(r'^assign_organization/(?P<pk>\d{1,9})/{0,1}$', views.AddUserToCompany.as_view(), name='rcassign'),
    
    url(r'^edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.RCDelete.as_view(), name='rcview'),
    url(r'^edit/(?P<rc>\d{1,9})/target-create/{0,1}$', views.TargetCreateView.as_view(), name='targetcreate'),
    url(r'^edit/(?P<rc>\d{1,9})/target-edit/(?P<pk>\d{1,9})/{0,1}$', views.TargetEditView.as_view(), name='targetedit'),
    url(r'^edit/(?P<rc>\d{1,9})/target-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.TargetDelete.as_view(), name='targetedit'),

    url(r'^edit/(?P<rc>\d{1,9})/resource-create/{0,1}$', views.ResourceCreateView.as_view(), name='resourcecreate'),
    url(r'^edit/(?P<rc>\d{1,9})/resource-edit/(?P<pk>\d{1,9})/{0,1}$', views.ResourceEditView.as_view(), name='resourceedit'),
    url(r'^edit/(?P<rc>\d{1,9})/resource-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.ResourceDelete.as_view(), name='resourceedit'),

    url(r'^edit/(?P<rc>\d{1,9})/activity-create/{0,1}$', views.ActivityCreateView.as_view(), name='activitycreate'),
    url(r'^edit/(?P<rc>\d{1,9})/activity-edit/(?P<pk>\d{1,9})/{0,1}$', views.ActivityEditView.as_view(), name='activityedit'),
    url(r'^edit/(?P<rc>\d{1,9})/activity-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.ActivityDelete.as_view(), name='activityedit'),

    url(r'^edit/(?P<rc>\d{1,9})/output-create/{0,1}$', views.OutputCreateView.as_view(), name='outputcreate'),
    url(r'^edit/(?P<rc>\d{1,9})/output-edit/(?P<pk>\d{1,9})/{0,1}$', views.OutputEditView.as_view(), name='outputedit'),
    url(r'^edit/(?P<rc>\d{1,9})/output-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.OutputDelete.as_view(), name='outputedit'),
    # new

    url(r'^edit/(?P<rc>\d{1,9})/new-output-create-activities/{0,1}$', views.NewOutputCreateActivitiesView.as_view(), name='outputcreateactivities'),
    url(r'^edit/(?P<rc>\d{1,9})/new-output-create-select/(?P<pk>\d{1,9})/{0,1}$', views.NewOutputEditSelectView.as_view(), name='outputcreateselect'),
    url(r'^edit/(?P<rc>\d{1,9})/new-output-create-select/(?P<pk>\d{1,9})/delete/{0,1}$', views.OutputDelete.as_view(), name='outputedit'),
    # url(r'^edit/(?P<rc>\d{1,9})/output-activities-new/{0,1}$', views.OutputActivitiesNewView.as_view(), name='outputcreate'),
    # url(r'^edit/(?P<rc>\d{1,9})/output-select-value/{0,1}$', views.OutputCreateView.as_view(), name='outputcreate'),

    url(r'^edit/(?P<rc>\d{1,9})/outcome-create/{0,1}$', views.OutcomeCreateView.as_view(), name='outcomecreate'),
    url(r'^edit/(?P<rc>\d{1,9})/outcome-edit/(?P<pk>\d{1,9})/{0,1}$', views.OutcomeEditView.as_view(), name='outcomeedit'),
    url(r'^edit/(?P<rc>\d{1,9})/outcome-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.OutcomeDelete.as_view(), name='outcomeedit'),

    url(r'^edit/(?P<rc>\d{1,9})/impact-create/{0,1}$', views.ImpactCreateView.as_view(), name='impactcreate'),
    url(r'^edit/(?P<rc>\d{1,9})/impact-edit/(?P<pk>\d{1,9})/{0,1}$', views.ImpactEditView.as_view(), name='impactedit'),
    url(r'^edit/(?P<rc>\d{1,9})/impact-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.ImpactDelete.as_view(), name='impactedit'),

    url(r'^edit/(?P<rc>\d{1,9})/output-edit/(?P<parent>\d{1,9})/indicator-create/{0,1}$', views.OutputIndicatorCreateView.as_view(), name='optindicatorcreate'),
    url(r'^edit/(?P<rc>\d{1,9})/outcome-edit/(?P<parent>\d{1,9})/indicator-create/{0,1}$', views.OutcomeIndicatorCreateView.as_view(), name='ocmindicatorcreate'),
    url(r'^edit/(?P<rc>\d{1,9})/impact-edit/(?P<parent>\d{1,9})/indicator-create/{0,1}$', views.ImpactIndicatorCreateView.as_view(), name='impindicatorcreate'),

    url(r'^edit/(?P<rc>\d{1,9})/output-edit/(?P<parent>\d{1,9})/indicator-edit/(?P<pk>\d{1,9})/{0,1}$', views.OutputIndicatorEditView.as_view(), name='optindicatoredit'),
    url(r'^edit/(?P<rc>\d{1,9})/outcome-edit/(?P<parent>\d{1,9})/indicator-edit/(?P<pk>\d{1,9})/{0,1}$', views.OutcomeIndicatorEditView.as_view(), name='ocmindicatoredit'),
    url(r'^edit/(?P<rc>\d{1,9})/impact-edit/(?P<parent>\d{1,9})/indicator-edit/(?P<pk>\d{1,9})/{0,1}$', views.ImpactIndicatorEditView.as_view(), name='impindicatoredit'),


    url(r'^edit/(?P<rc>\d{1,9})/output-edit/(?P<parent>\d{1,9})/indicator-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.OutputIndicatorDelete.as_view(), name='optindicatoredit'),
    url(r'^edit/(?P<rc>\d{1,9})/outcome-edit/(?P<parent>\d{1,9})/indicator-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.OutcomeIndicatorDelete.as_view(), name='ocmindicatoredit'),
    url(r'^edit/(?P<rc>\d{1,9})/impact-edit/(?P<parent>\d{1,9})/indicator-edit/(?P<pk>\d{1,9})/delete/{0,1}$', views.ImpactIndicatorDelete.as_view(), name='impindicatoredit'),

    url(r'^register/{0,1}$', views.UserRequestCreateView.as_view(), name='register'),

    url(r'^create/{0,1}$', views.RCCreateView.as_view(), name='rccreateview'),
    url(r'^edit/(?P<pk>\d{1,9})/{0,1}$', views.RCEditView.as_view(), name='rceditview'),
    url(r'^calendar/(?P<pk>\d{1,9})/{0,1}$', views.CalendarView.as_view(), name='rccalendar'),
    url(r'^edit/duplicate/(?P<pk>\d{1,9})/{0,1}$', views.DuplicateView.as_view(), name='rcduplicateview'),
    url(r'^(?P<rc>\d{1,9})/pdf/{0,1}$', views.get_pdf_view, name='getpdf'),
    url(r'^(?P<rc>\d{1,9})/indicators/{0,1}$', views.get_indicator_monitoring_form_xlsx_file, name='getpdf'),
    url(r'^(?P<rc>\d{1,9})/indicator-values/{0,1}$', views.get_indicator_values_monitoring_form_xlsx_file, name='getpdf'),
    url(r'^(?P<pk>\d{1,9})/rc-download/{0,1}$', views.DownloadView.as_view(), name='download'),
    url(r'^company-view/(?P<pk>\d{1,9})/{0,1}$', views.CompanyView.as_view(), name='comp_view'),
    url(r'^companies/{0,1}$', views.Companies.as_view(), name='comp_view'),
    url(r'^search/{0,1}$', views.SearchView.as_view(), name='search_view'),
    url(r'^company-edit/(?P<pk>\d{1,9})/{0,1}$', views.CompanyEdit.as_view(), name='comp_edit'),
    url(r'^company-create/{0,1}$', views.CompanyCreate.as_view(), name='comp_create'),
    url(r'^companies-view/{0,1}$', views.ViewTotalData.as_view(), name='comp_create'),
    url(r'^companies-view-new/{0,1}$', views.ViewTotalDataNew.as_view(), name='comp_create'),
    url(r'^(?P<prev>[a-zA-Z0-9\/-]*)comment_create$', views.PageCommentCreateView.as_view(), name='commentcreate'),
    url(r'^(?P<rc>\d{1,9})/pdf-iframe/{0,1}$', views.RCPdfView.as_view(), name='viewpdf'),
    url(r'^(?P<rc>\d{1,9})/xlsx-indicator-monitoring/{0,1}$', views.get_indicator_monitoring_form_xlsx_file, name='get-xlsx'),
    url(r'^(?P<rc>\d{1,9})/xlsx-indicator-values-monitoring/{0,1}$', views.get_indicator_values_monitoring_form_xlsx_file, name='get-xlsx'),
    
    url(r'^helper/{0,1}$', views.ViewHelperPage.as_view(), name='helper_view'),
    url(r'^user_requests_list/{0,1}$', views.UserRequestsListView.as_view(), name='helper_view'),
    url(r'^user_requests_monitor/{0,1}$', views.UserRequestsMonitorView.as_view(), name='helper_view'),
    url(r'^registration_success/{0,1}$', views.RegistrationSuccess.as_view(), name='helper_view'),
    url(r'^user_exists/{0,1}$', views.UserExists.as_view(), name='helper_view'),
    url(r'^user_in_progress/{0,1}$', views.UserInProgress.as_view(), name='helper_view'),
    # url(r'^request/(?P<pk>\d{1,9})/{0,1}$', views.UserRequestView.as_view(), name='helper_view'),
    url(r'^request-decline/(?P<pk>\d{1,9})/{0,1}$', views.UserRequestViewDecline.as_view(), name='helper_view'),
    
    url(r'^create_company_data/{0,1}$', views.CreateCompanyData.as_view(), name='helper_view'),
    url(r'^remove_company_data/{0,1}$', views.RemoveCompanyData.as_view(), name='helper_view'),
    
    url(r'^new_helper/rc/{0,1}$', views.ViewNewRCHelperPage.as_view(), name='rc_helper_view'),
    url(r'^new_helper/targets/{0,1}$', views.ViewNewTargetsHelperPage.as_view(), name='rc_helper_view'),
    url(r'^new_helper/resources/{0,1}$', views.ViewNewResourcesHelperPage.as_view(), name='rc_helper_view'),
    url(r'^new_helper/activities/{0,1}$', views.ViewNewActivitiesHelperPage.as_view(), name='rc_helper_view'),
    url(r'^new_helper/outputs/{0,1}$', views.ViewNewOutputsHelperPage.as_view(), name='rc_helper_view'),
    url(r'^new_helper/outcomes/{0,1}$', views.ViewNewOutcomesHelperPage.as_view(), name='rc_helper_view'),
    url(r'^new_helper/impacts/{0,1}$', views.ViewNewImpactsHelperPage.as_view(), name='rc_helper_view'),
    url(r'^new_helper/additional/{0,1}$', views.ViewNewAdditionalHelperPage.as_view(), name='rc_helper_view'),
    
    url(r'^library/(?P<pk>\d{1,9})/{0,1}$', views.LibraryPageData.as_view(), name='rcview'),
    url(r'^indicators_library/{0,1}$', views.IndicatorsLibraryView.as_view(), name='indicators_library'),

    url(r'^benchmarking_parameters/{0,1}$', views.BenchmarkingParametersView.as_view(), name="benchmarking_parameters"),
    url(r'^benchmarking_results/{0,1}$', views.BenchmarkingResultsView.as_view(), name="benchmarking_results")
]