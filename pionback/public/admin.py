from django.contrib import admin
from .models import *

class UserRequestAdmin(admin.ModelAdmin):
    exclude = ['password']

class ToolChangeRequestInline(admin.TabularInline):
    model = ToolChangeRequest
    empty_value_display = ''
    can_delete=False

    readonly_fields = ('created_at', 'name', 'info', 'tool_tag_refs', 'thematic_group_ref', 'target_refs', 'practice_ref', 'method_ref',  'outcome_level_ref', 'outcome_refs', 'tool_file', 'url')
    
    fieldsets = (
        (None, {
            'fields': ('created_at', 'name', 'info', 'tool_tag_refs', 'thematic_group_ref', 'target_refs', 'practice_ref', 'method_ref', 'outcome_level_ref', 'outcome_refs', 'tool_file', 'url', 'add_public_confirm',),
        }),
    )

class ToolAdmin(admin.ModelAdmin):
    inlines = [ToolChangeRequestInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            tool_change = ToolChangeRequest.objects.filter(pk=instance.pk).first()
            tool = Tool.objects.filter(pk=instance.pk).first()
            if tool.add_public_confirm and tool_change.add_public_confirm:
                fields = []
                if tool_change.thematic_group_ref:     
                    tool.thematic_group_ref = tool_change.thematic_group_ref
                    fields.append('thematic_group_ref')
                if tool_change.practice_ref:     
                    tool.practice_ref = tool_change.practice_ref
                    fields.append('practice_ref')
                if tool_change.method_ref: 
                    tool.method_ref = tool_change.method_ref
                    fields.append('method_ref')
                if tool_change.outcome_level_ref: 
                    tool.outcome_level_ref = tool_change.outcome_level_ref
                    fields.append('outcome_level_ref')
                if tool_change.name: 
                    tool.name = tool_change.name
                    fields.append('name')
                if tool_change.info: 
                    tool.info = tool_change.info
                    fields.append('info')
                if tool_change.url: 
                    tool.url = tool_change.url
                    fields.append('url')
                if tool_change.tool_file: 
                    tool.tool_file = tool_change.tool_file
                    fields.append('tool_file')

                tool.save(update_fields=fields)

                if tool_change.tool_tag_refs: 
                    tool_tag_refs = ToolTag.objects.filter(pk__in=[tag.pk for tag in tool_change.tool_tag_refs.all()])
                    tool.tool_tag_refs.set(tool_tag_refs)
                if tool_change.target_refs: 
                    target_refs = Target.objects.filter(pk__in=[target.pk for target in tool_change.target_refs.all()])
                    tool.target_refs.set(target_refs)
                if tool_change.outcome_refs: 
                    outcome_refs = Outcome.objects.filter(pk__in=[outcome.pk for outcome in tool_change.outcome_refs.all()])
                    tool.outcome_refs.set(outcome_refs)

                tool_change.delete()

class LogicalModelChangeRequestInline(admin.TabularInline):
    model = LogicalModelChangeRequest
    empty_value_display = ''
    can_delete=False

    readonly_fields = ('created_at', 'name', 'organization', 'thematic_group_ref', 'target_refs', 'practice_refs', 'outcome_refs', 'period',  'verification_info', 'verification_level_regularity', 'verification_level_validity', 'verification_level_outcome_accessibility', 'verification_level_outcome_validity', 'model_file', 'result_tree_file')
    
    fieldsets = (
        (None, {
            'fields': (
                ('created_at', 'name','organization',  'period', 'thematic_group_ref', 'target_refs', 'practice_refs', 'outcome_refs', 'verification_info', 'verification_level_regularity', 'verification_level_validity', 'verification_level_outcome_accessibility', 'verification_level_outcome_validity', 'model_file', 'result_tree_file', 'add_public_confirm',),
                )
        }),
    )

class LogicalModelAdmin(admin.ModelAdmin):
    inlines = [LogicalModelChangeRequestInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            logical_model_change = LogicalModelChangeRequest.objects.filter(pk=instance.pk).first()
            logical_model = LogicalModel.objects.filter(pk=instance.pk).first()
            if logical_model.add_public_confirm and logical_model_change.add_public_confirm:
                fields = []
                if logical_model_change.thematic_group_ref:     
                    logical_model.thematic_group_ref = logical_model_change.thematic_group_ref
                    fields.append('thematic_group_ref')
                if logical_model_change.organization:     
                    logical_model.organization = logical_model_change.organization
                    fields.append('organization')
                if logical_model_change.period: 
                    logical_model.period = logical_model_change.period
                    fields.append('period')
                if logical_model_change.verification_info: 
                    logical_model.verification_info = logical_model_change.verification_info
                    fields.append('verification_info')
                if logical_model_change.name: 
                    logical_model.name = logical_model_change.name
                    fields.append('name')

                if logical_model_change.verification_level_regularity: 
                    logical_model.verification_level_regularity = logical_model_change.verification_level_regularity
                    fields.append('verification_level_regularity')
                if logical_model_change.verification_level_validity: 
                    logical_model.verification_level_validity = logical_model_change.verification_level_validity
                    fields.append('verification_level_validity')
                if logical_model_change.verification_level_outcome_accessibility: 
                    logical_model.verification_level_outcome_accessibility = logical_model_change.verification_level_outcome_accessibility
                    fields.append('verification_level_outcome_accessibility')
                if logical_model_change.verification_level_outcome_validity: 
                    logical_model.verification_level_outcome_validity = logical_model_change.verification_level_outcome_validity
                    fields.append('verification_level_outcome_validity')

                if logical_model_change.model_file: 
                    logical_model.model_file = logical_model_change.model_file
                    fields.append('model_file')
                if logical_model_change.result_tree_file: 
                    logical_model.result_tree_file = logical_model_change.result_tree_file
                    fields.append('result_tree_file')

                logical_model.save(update_fields=fields)

                if logical_model_change.practice_refs: 
                    practice_refs = Practice.objects.filter(pk__in=[practice.pk for practice in logical_model_change.practice_refs.all()])
                    logical_model.practice_refs.set(practice_refs)
                if logical_model_change.target_refs: 
                    target_refs = Target.objects.filter(pk__in=[target.pk for target in logical_model_change.target_refs.all()])
                    logical_model.target_refs.set(target_refs)
                if logical_model_change.outcome_refs: 
                    outcome_refs = Outcome.objects.filter(pk__in=[outcome.pk for outcome in logical_model_change.outcome_refs.all()])
                    logical_model.outcome_refs.set(outcome_refs)

                logical_model_change.delete()

class CaseChangeRequestInline(admin.TabularInline):
    model = CaseChangeRequest
    empty_value_display = ''
    can_delete=False

    readonly_fields = ('created_at', 'name', 'thematic_group_ref', 'target_refs', 'practice_ref', 'organization_activity_refs', 'monitoring_element_refs', 'organization', 'verification_info', 'verification_level_regularity', 'verification_level_validity', 'verification_level_outcome_accessibility', 'verification_level_outcome_validity', 'url', 'case_file')
    
    fieldsets = (
        (None, {
            'fields': (
                ('created_at', 'name', 'organization', 'thematic_group_ref', 'target_refs', 'practice_ref', 'organization_activity_refs', 'monitoring_element_refs', 'verification_info', 'verification_level_regularity', 'verification_level_validity', 'verification_level_outcome_accessibility', 'verification_level_outcome_validity', 'url', 'case_file', 'add_public_confirm', ),
                )
        }),
    )

class CaseAdmin(admin.ModelAdmin):
    inlines = [CaseChangeRequestInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            case_change = CaseChangeRequest.objects.filter(pk=instance.pk).first()
            case = Case.objects.filter(pk=instance.pk).first()
            if case.add_public_confirm and case_change.add_public_confirm:
                fields = []
                if case_change.thematic_group_ref:     
                    case.thematic_group_ref = case_change.thematic_group_ref
                    fields.append('thematic_group_ref')
                if case_change.organization:     
                    case.organization = case_change.organization
                    fields.append('organization')
                if case_change.url: 
                    case.url = case_change.url
                    fields.append('url')
                if case_change.verification_info: 
                    case.verification_info = case_change.verification_info
                    fields.append('verification_info')
                if case_change.name: 
                    case.name = case_change.name
                    fields.append('name')

                if case_change.verification_level_regularity: 
                    case.verification_level_regularity = case_change.verification_level_regularity
                    fields.append('verification_level_regularity')
                if case_change.verification_level_validity: 
                    case.verification_level_validity = case_change.verification_level_validity
                    fields.append('verification_level_validity')
                if case_change.verification_level_outcome_accessibility: 
                    case.verification_level_outcome_accessibility = case_change.verification_level_outcome_accessibility
                    fields.append('verification_level_outcome_accessibility')
                if case_change.verification_level_outcome_validity: 
                    case.verification_level_outcome_validity = case_change.verification_level_outcome_validity
                    fields.append('verification_level_outcome_validity')

                if case_change.case_file: 
                    case.case_file = case_change.case_file
                    fields.append('case_file')
                if case_change.practice_ref: 
                    case.practice_ref = case_change.practice_ref
                    fields.append('practice_ref')

                case.save(update_fields=fields)

                if case_change.organization_activity_refs: 
                    organization_activity_refs = OrganizationActivity.objects.filter(pk__in=[organization_activity.pk for organization_activity in case_change.organization_activity_refs.all()])
                    case.organization_activity_refs.set(organization_activity_refs)
                if case_change.target_refs: 
                    target_refs = Target.objects.filter(pk__in=[target.pk for target in case_change.target_refs.all()])
                    case.target_refs.set(target_refs)
                if case_change.monitoring_element_refs: 
                    monitoring_element_refs = MonitoringElement.objects.filter(pk__in=[monitoring_element.pk for monitoring_element in case_change.monitoring_element_refs.all()])
                    case.monitoring_element_refs.set(monitoring_element_refs)

                case_change.delete()

class EvaluationReportChangeRequestInline(admin.TabularInline):
    model = EvaluationReportChangeRequest
    empty_value_display = ''
    can_delete=False

    readonly_fields = ('created_at', 'evaluation_file', 'method_refs', 'analysis_method_refs','outcome_refs','representation_method_refs', 'evaluation_type_ref', 'key_questions', 'type', 'other_results')
    
    fieldsets = (
        (None, {
            'fields': ('created_at', 'type', 'evaluation_type_ref', 'key_questions', 'method_refs', 'analysis_method_refs','outcome_refs', 'other_results', 'representation_method_refs', 'evaluation_file', 'add_public_confirm'),
        }),
    )

class EvaluationReportAdmin(admin.ModelAdmin):
    inlines = [EvaluationReportChangeRequestInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            er_change = EvaluationReportChangeRequest.objects.filter(pk=instance.pk).first()
            er = EvaluationReport.objects.filter(pk=instance.pk).first()
            if er.add_public_confirm and er_change.add_public_confirm:
                fields = []
                if er_change.evaluation_type_ref:     
                    er.evaluation_type_ref = er_change.evaluation_type_ref
                    fields.append('evaluation_type_ref')
                if er_change.type:     
                    er.type = er_change.type
                    fields.append('type')
                if er_change.key_questions: 
                    er.key_questions = er_change.key_questions
                    fields.append('key_questions')
                if er_change.other_results: 
                    er.other_results = er_change.other_results
                    fields.append('other_results')
                if er_change.evaluation_file: 
                    er.evaluation_file = er_change.evaluation_file
                    fields.append('evaluation_file')

                er.save(update_fields=fields)

                if er_change.method_refs and er_change.method_refs.count() > 0: 
                    method_refs = Method.objects.filter(pk__in=[m.pk for m in er_change.method_refs.all()])
                    er.method_refs.set(method_refs)
                if er_change.analysis_method_refs and er_change.analysis_method_refs.count() > 0: 
                    analysis_method_refs = AnalysisMethod.objects.filter(pk__in=[am.pk for am in er_change.analysis_method_refs.all()])
                    er.analysis_method_refs.set(analysis_method_refs)
                if er_change.representation_method_refs and er_change.representation_method_refs.count() > 0: 
                    representation_method_refs = RepresentationMethod.objects.filter(pk__in=[rm.pk for rm in er_change.representation_method_refs.all()])
                    er.representation_method_refs.set(representation_method_refs)
                if er_change.outcome_refs and er_change.outcome_refs.count() > 0: 
                    outcome_refs = Outcome.objects.filter(pk__in=[outcome.pk for outcome in er_change.outcome_refs.all()])
                    er.outcome_refs.set(outcome_refs)

                er_change.delete()

admin.site.register(Tool, ToolAdmin)
admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(Target)
admin.site.register(Practice)
admin.site.register(Outcome)
admin.site.register(OutcomeLibraryLink)
admin.site.register(OutcomeExactName)
admin.site.register(OutcomeIndicator)
admin.site.register(OutcomeMethod)
admin.site.register(LogicalModel, LogicalModelAdmin)
admin.site.register(LogicalModelLibraryLink)
admin.site.register(Program)
admin.site.register(Assumption)
admin.site.register(Context)
admin.site.register(Activity)
admin.site.register(ProgramOutput)
admin.site.register(ProgramShortOutcome)
admin.site.register(ProgramMidOutcome)
admin.site.register(ProgramImpact)
admin.site.register(ThematicGroup)
admin.site.register(Method)
admin.site.register(OutcomeLevel)
admin.site.register(MonitoringElement)
admin.site.register(OrganizationActivity)
admin.site.register(RepresentationMethod)
admin.site.register(EvaluationType)
admin.site.register(AnalysisMethod)
admin.site.register(ToolLibraryLink)
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseLibraryLink)
admin.site.register(EvaluationReport, EvaluationReportAdmin)
admin.site.register(ToolTag)