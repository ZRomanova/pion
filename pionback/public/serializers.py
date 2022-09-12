from django.contrib.auth.models import User
from rest_framework import serializers
from public.models import *
from django.db.models import Q


class UserSerializer(serializers.HyperlinkedModelSerializer):
    current_user = serializers.SerializerMethodField()
    def get_current_user(self, obj):
        return obj.id == self.context.get('request').user.id
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'current_user','is_superuser']
        extra_kwargs = {
            'is_superuser': {'read_only': True}
        }


class UserSerializerMail(serializers.HyperlinkedModelSerializer):
    current_user = serializers.SerializerMethodField()
    def get_current_user(self, obj):
        return obj.email == self.context.get('request').user.email
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'current_user']

#=======================================================================================================================

class ThematicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicGroup
        fields = ['id', 'name']

class ToolTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolTag
        fields = ['id', 'name']

class OutcomeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeLevel
        fields = ['id', 'name']

class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = ['id', 'name', 'parent_ref', 'add_public', 'info']

class MonitoringElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringElement
        fields = ['id', 'name']

class OrganizationActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationActivity
        fields = ['id', 'name']

class TargetSerializer(serializers.ModelSerializer):
    parent_ref = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Target
        fields = ['id', 'name', 'parent_ref']

class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = ['id', 'name']

class RepresentationMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepresentationMethod
        fields = ['id', 'name', 'add_public']

class EvaluationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationType
        fields = ['id', 'name', 'add_public']

class AnalysisMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisMethod
        fields = ['id', 'name', 'add_public']

#=======================================================================================================================

class UserRequestSerializer(serializers.HyperlinkedModelSerializer):
    current_user = serializers.SerializerMethodField()
    user_ref = UserSerializer(many=False, read_only=True)
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(UserRequestSerializer, self).__init__(*args, **kwargs)
    def get_current_user(self, obj):
        if obj.user_ref is not None:
            return obj.user_ref.id == self.context.get('request').user.id
        return False
    class Meta:
        model = UserRequest
        fields = ["id", "email", "lastname", "firstname", "middlename", "region", "organization", "website", "position", "createdon", "verifiedon", "lastseenon", "user_ref", "password", "current_user"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class OutcomeMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeMethod
        fields = ['name', 'url', 'id']

class OutcomeSerializer(serializers.ModelSerializer):
    current_user_library = serializers.SerializerMethodField()
    createdby = UserSerializer(read_only=True, many=False)

    def get_current_user_library(self, obj):
        linkers = OutcomeLibraryLink.objects.filter(user_ref=self.context.get('request').user.id).filter(outcome_ref=obj.id)
        return len(linkers) > 0
    class Meta:
        model = Outcome
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_refs'] = PracticeSerializer(many=True, read_only=True)
        self.fields['method_refs'] = OutcomeMethodSerializer(many=True, read_only=True)
        self.fields['thematic_group_refs'] = ThematicGroupSerializer(many=True, read_only=True)
        return super(OutcomeSerializer, self).to_representation(instance)


class OutcomeExactNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeExactName
        fields = ['name', 'id', 'outcome_ref']
    
class OutcomeIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeIndicator
        fields = ['name', 'id', 'outcome_ref']

class LogicalModelSerializer(serializers.ModelSerializer):
    current_user_library = serializers.SerializerMethodField()
    createdby = UserSerializer(read_only=True, many=False)

    def get_current_user_library(self, obj):
        if (self.context.get('request').user is None):
            return False
        linkers = LogicalModelLibraryLink.objects.filter(user_ref=self.context.get('request').user.id).filter(logical_model_ref=obj.id)
        return len(linkers) > 0
    class Meta:
        model = LogicalModel
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_refs'] = PracticeSerializer(many=True, read_only=True)
        self.fields['outcome_refs'] = OutcomeSerializer(many=True, read_only=True)
        self.fields['thematic_group_ref'] = ThematicGroupSerializer(many=False, read_only=True)
        return super(LogicalModelSerializer, self).to_representation(instance)

class ProgramSerializer(serializers.ModelSerializer):
    current_user = serializers.SerializerMethodField()
    user_ref = UserSerializer(read_only=True, many=False)
    def get_current_user(self, obj):
        return obj.user_ref.id == self.context.get('request').user.id
    class Meta:
        model = Program
        fields = ["id", "name", "description", "period", "user_ref", "target_refs", "practice_refs", "current_user"]

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_refs'] = PracticeSerializer(many=True, read_only=True)
        self.fields['user_ref'] = UserSerializer(many=False, read_only=True)
        return super(ProgramSerializer, self).to_representation(instance)

class AssumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assumption
        fields = ['id', 'text', 'program_ref']

class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = ['id', 'text', 'program_ref']

class TargetDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetDescription
        fields = ['id', 'info', 'program_ref', 'target_ref']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'program_ref', 'target_ref', 'info']
    def to_representation(self, instance):
        self.fields['target_ref'] = TargetSerializer(many=False, read_only=True)
        return super(ActivitySerializer, self).to_representation(instance)

class ProgramOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramOutput
        fields = ['id', 'name', 'program_ref', 'info', 'activity_ref']
    def to_representation(self, instance):
        self.fields['activity_ref'] = ActivitySerializer(many=False, read_only=True)
        return super(ProgramOutputSerializer, self).to_representation(instance)

class ProgramShortOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramShortOutcome
        fields = ['id', 'name', 'program_ref', 'info', 'program_output_ref', 'program_output_many_refs', 'outcome_ref']
    def to_representation(self, instance):
        self.fields['program_output_ref'] = ProgramOutputSerializer(many=False, read_only=True)
        self.fields['program_output_many_refs'] = ProgramOutputSerializer(many=True, read_only=True)
        return super(ProgramShortOutcomeSerializer, self).to_representation(instance)

class ProgramMidOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramMidOutcome
        fields = ['id', 'name', 'program_ref', 'info', 'program_short_outcome_ref', 'program_short_outcome_many_refs', 'outcome_ref']
    def to_representation(self, instance):
        self.fields['program_short_outcome_ref'] = ProgramShortOutcomeSerializer(many=False, read_only=True)
        self.fields['program_short_outcome_many_refs'] = ProgramShortOutcomeSerializer(many=True, read_only=True)
        return super(ProgramMidOutcomeSerializer, self).to_representation(instance)

class ProgramImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramImpact
        fields = ['id', 'name', 'program_ref', 'info', 'program_mid_outcome_ref', 'program_mid_outcome_many_refs']
    def to_representation(self, instance):
        self.fields['program_mid_outcome_ref'] = ProgramMidOutcomeSerializer(many=False, read_only=True)
        self.fields['program_mid_outcome_many_refs'] = ProgramMidOutcomeSerializer(many=True, read_only=True)
        return super(ProgramImpactSerializer, self).to_representation(instance)

class MonitoringPlanLineOutputSerializer(serializers.ModelSerializer):
    suitable_tools = serializers.SerializerMethodField(read_only=True)
    suitable_from_tools = serializers.SerializerMethodField(read_only=True)
    tool_url = serializers.SerializerMethodField(read_only=True)
    def get_tool_url(self, obj):        
        tool_name = obj.tool
        tool_type = obj.tool_type
        if tool_type=="OutcomeMethods":
            tool = OutcomeMethod.objects.filter(name=tool_name)
            if len(tool) > 0:
                return tool[0].url
        if tool_type=="Tools":
            tool = Tool.objects.filter(name=tool_name)
            if len(tool) > 0:
                return 'https://pion.org.ru/newpion/tools?id=' + str(tool[0].id)
        return ""

    def get_suitable_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            for method_name in outcome.method_refs.all():
                method_names.append(method_name.name)
        return method_names

    def get_suitable_from_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            tools = Tool.objects.filter(outcome_refs=outcome.id).filter(Q(createdby=self.context.get('request').user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
            for tool in tools.all():
                method_names.append(tool.name)
        return method_names

    class Meta:
        model = MonitoringPlanLineOutput
        fields = ['id', 'sort_index', 'tool_type', 'result_ref', 'name', 'indicator', 'method', 'tool', 'tool_url', 'frequency', 'reporting', 'program_ref', 'suitable_tools', 'suitable_from_tools']
    def to_representation(self, instance):
        self.fields['result_ref'] = ProgramOutputSerializer(many=False, read_only=True)
        self.fields['program_ref'] = ProgramSerializer(many=False, read_only=True)
        return super(MonitoringPlanLineOutputSerializer, self).to_representation(instance)

class MonitoringPlanLineShortOutcomeSerializer(serializers.ModelSerializer):
    suitable_tools = serializers.SerializerMethodField(read_only=True)
    suitable_indicators = serializers.SerializerMethodField(read_only=True)
    suitable_from_tools = serializers.SerializerMethodField(read_only=True)
    tool_url = serializers.SerializerMethodField(read_only=True)

    def get_tool_url(self, obj):        
        tool_name = obj.tool
        tool_type = obj.tool_type
        if tool_type=="OutcomeMethods":
            tool = OutcomeMethod.objects.filter(name=tool_name)
            if len(tool) > 0:
                return tool[0].url
        if tool_type=="Tools":
            tool = Tool.objects.filter(name=tool_name)
            if len(tool) > 0:
                return 'https://pion.org.ru/newpion/tools?id=' + str(tool[0].id)
        return ""

    def get_suitable_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            for method_name in outcome.method_refs.all():
                method_names.append(method_name.name)
        return method_names

    def get_suitable_from_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            tools = Tool.objects.filter(outcome_refs=outcome.id).filter(Q(createdby=self.context.get('request').user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
            for tool in tools.all():
                method_names.append(tool.name)
        return method_names

    def get_suitable_indicators(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        indicator_names = []
        for outcome in outcomes.all():
            for indicator in OutcomeIndicator.objects.filter(outcome_ref=outcome.id).all():
                indicator_names.append(indicator.name)
        return indicator_names
    class Meta:
        model = MonitoringPlanLineShortOutcome
        fields = ['id', 'sort_index', 'tool_type', 'result_ref', 'name', 'indicator', 'method', 'tool', 'tool_url', 'frequency', 'reporting', 'program_ref', 'suitable_tools', 'suitable_from_tools', 'suitable_indicators']
    def to_representation(self, instance):
        self.fields['result_ref'] = ProgramShortOutcomeSerializer(many=False, read_only=True)
        self.fields['program_ref'] = ProgramSerializer(many=False, read_only=True)
        return super(MonitoringPlanLineShortOutcomeSerializer, self).to_representation(instance)

class MonitoringPlanLineMidOutcomeSerializer(serializers.ModelSerializer):
    suitable_tools = serializers.SerializerMethodField(read_only=True)
    suitable_indicators = serializers.SerializerMethodField(read_only=True)
    suitable_from_tools = serializers.SerializerMethodField(read_only=True)
    tool_url = serializers.SerializerMethodField(read_only=True)

    def get_tool_url(self, obj):        
        tool_name = obj.tool
        tool_type = obj.tool_type
        if tool_type=="OutcomeMethods":
            tool = OutcomeMethod.objects.filter(name=tool_name)
            if len(tool) > 0:
                return tool[0].url
        if tool_type=="Tools":
            tool = Tool.objects.filter(name=tool_name)
            if len(tool) > 0:
                return 'https://pion.org.ru/newpion/tools?id=' + str(tool[0].id)
        return ""

    def get_suitable_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            for method_name in outcome.method_refs.all():
                method_names.append(method_name.name)
        return method_names

    def get_suitable_from_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            tools = Tool.objects.filter(outcome_refs=outcome.id).filter(Q(createdby=self.context.get('request').user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
            for tool in tools.all():
                method_names.append(tool.name)
        return method_names
    def get_suitable_indicators(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        indicator_names = []
        for outcome in outcomes.all():
            for indicator in OutcomeIndicator.objects.filter(outcome_ref=outcome.id).all():
                indicator_names.append(indicator.name)
        return indicator_names
    class Meta:
        model = MonitoringPlanLineMidOutcome
        fields = ['id', 'sort_index', 'result_ref', 'tool_type', 'name', 'indicator', 'method', 'tool', 'tool_url', 'frequency', 'reporting', 'program_ref', 'suitable_tools', 'suitable_from_tools', 'suitable_indicators']
    def to_representation(self, instance):
        self.fields['result_ref'] = ProgramMidOutcomeSerializer(many=False, read_only=True)
        self.fields['program_ref'] = ProgramSerializer(many=False, read_only=True)
        return super(MonitoringPlanLineMidOutcomeSerializer, self).to_representation(instance)

class MonitoringPlanLineImpactSerializer(serializers.ModelSerializer):
    suitable_tools = serializers.SerializerMethodField(read_only=True)
    suitable_indicators = serializers.SerializerMethodField(read_only=True)
    suitable_from_tools = serializers.SerializerMethodField(read_only=True)
    tool_url = serializers.SerializerMethodField(read_only=True)
    def get_tool_url(self, obj):        
        tool_name = obj.tool
        tool_type = obj.tool_type
        if tool_type=="OutcomeMethods":
            tool = OutcomeMethod.objects.filter(name=tool_name)
            if len(tool) > 0:
                return tool[0].url
        if tool_type=="Tools":
            tool = Tool.objects.filter(name=tool_name)
            if len(tool) > 0:
                return 'https://pion.org.ru/newpion/tools?id=' + str(tool[0].id)
        return ""

    def get_suitable_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            for method_name in outcome.method_refs.all():
                method_names.append(method_name.name)
        return method_names

    def get_suitable_from_tools(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        method_names = []
        for outcome in outcomes.all():
            tools = Tool.objects.filter(outcome_refs=outcome.id).filter(Q(createdby=self.context.get('request').user.id) & ~Q(createdby=None) | Q(add_public_confirm=True))
            for tool in tools.all():
                method_names.append(tool.name)
        return method_names
    def get_suitable_indicators(self, obj):
        result_name = obj.result_ref.name
        outcomes = Outcome.objects.filter(name=result_name)
        indicator_names = []
        for outcome in outcomes.all():
            for indicator in OutcomeIndicator.objects.filter(outcome_ref=outcome.id).all():
                indicator_names.append(indicator.name)
        return indicator_names
    class Meta:
        model = MonitoringPlanLineImpact
        fields = ['id', 'sort_index', 'result_ref', 'tool_type', 'name', 'indicator', 'method', 'tool', 'tool_url', 'frequency', 'reporting', 'program_ref', 'suitable_tools', 'suitable_from_tools', 'suitable_indicators']
    def to_representation(self, instance):
        self.fields['result_ref'] = ProgramImpactSerializer(many=False, read_only=True)
        self.fields['program_ref'] = ProgramSerializer(many=False, read_only=True)
        return super(MonitoringPlanLineImpactSerializer, self).to_representation(instance)

class MonitoringFormLineOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringFormLineOutput
        fields = ['id', 'sort_index', 'indicator', 'plan', 'period1', 'fact1', 'period2', 'fact2', 'period3', 'fact3', 'period4', 'fact4', 'program_ref', 'mpl_ref']
    def to_representation(self, instance):
        self.fields['program_ref'] = ProgramSerializer(many = False, read_only=True)
        return super(MonitoringFormLineOutputSerializer, self).to_representation(instance)
    def to_internal_value(self, data):
        if data.get('plan') == '':
            data['plan'] = 0
        if data.get('fact1') == '':
            data['fact1'] = 0
        if data.get('fact2') == '':
            data['fact2'] = 0
        if data.get('fact3') == '':
            data['fact3'] = 0
        if data.get('fact4') == '':
            data['fact4'] = 0

        return super(MonitoringFormLineOutputSerializer, self).to_internal_value(data)

class MonitoringFormLineShortOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringFormLineShortOutcome
        fields = ['id', 'sort_index', 'indicator', 'plan', 'period1', 'fact1', 'period2', 'fact2', 'period3', 'fact3', 'period4', 'fact4', 'program_ref', 'mpl_ref']
    def to_representation(self, instance):
        self.fields['program_ref'] = ProgramSerializer(many = False, read_only=True)
        return super(MonitoringFormLineShortOutcomeSerializer, self).to_representation(instance)
    def to_internal_value(self, data):
        if data.get('plan') == '':
            data['plan'] = 0
        if data.get('fact1') == '':
            data['fact1'] = 0
        if data.get('fact2') == '':
            data['fact2'] = 0
        if data.get('fact3') == '':
            data['fact3'] = 0
        if data.get('fact4') == '':
            data['fact4'] = 0

        return super(MonitoringFormLineShortOutcomeSerializer, self).to_internal_value(data)

class MonitoringFormLineMidOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringFormLineMidOutcome
        fields = ['id', 'sort_index', 'indicator', 'plan', 'period1', 'fact1', 'period2', 'fact2', 'period3', 'fact3', 'period4', 'fact4', 'program_ref', 'mpl_ref']
    def to_representation(self, instance):
        self.fields['program_ref'] = ProgramSerializer(many = False, read_only=True)
        return super(MonitoringFormLineMidOutcomeSerializer, self).to_representation(instance)
    def to_internal_value(self, data):
        if data.get('plan') == '':
            data['plan'] = 0
        if data.get('fact1') == '':
            data['fact1'] = 0
        if data.get('fact2') == '':
            data['fact2'] = 0
        if data.get('fact3') == '':
            data['fact3'] = 0
        if data.get('fact4') == '':
            data['fact4'] = 0

        return super(MonitoringFormLineMidOutcomeSerializer, self).to_internal_value(data)

class MonitoringFormLineImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringFormLineImpact
        fields = ['id', 'sort_index', 'indicator', 'plan', 'period1', 'fact1', 'period2', 'fact2', 'period3', 'fact3', 'period4', 'fact4', 'program_ref', 'mpl_ref']
    def to_representation(self, instance):
        self.fields['program_ref'] = ProgramSerializer(many = False, read_only=True)
        return super(MonitoringFormLineImpactSerializer, self).to_representation(instance)
    def to_internal_value(self, data):
        if data.get('plan') == '':
            data['plan'] = 0
        if data.get('fact1') == '':
            data['fact1'] = 0
        if data.get('fact2') == '':
            data['fact2'] = 0
        if data.get('fact3') == '':
            data['fact3'] = 0
        if data.get('fact4') == '':
            data['fact4'] = 0

        return super(MonitoringFormLineImpactSerializer, self).to_internal_value(data)

####################################      TOOL    CASE


class ToolSerializer(serializers.ModelSerializer):
    current_user_library = serializers.SerializerMethodField()
    createdby = UserSerializer(read_only=True, many=False)
    def get_current_user_library(self, obj):
        linkers = ToolLibraryLink.objects.filter(user_ref=self.context.get('request').user.id).filter(tool_ref=obj.id)
        return len(linkers) > 0
    class Meta:
        model = Tool
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_ref'] = PracticeSerializer(many=False, read_only=True)
        self.fields['thematic_group_ref'] = ThematicGroupSerializer(many=False, read_only=True)
        self.fields['method_ref'] = MethodSerializer(many=False, read_only=True)
        self.fields['outcome_level_ref'] = OutcomeLevelSerializer(many=False, read_only=True)
        self.fields['outcome_refs'] = OutcomeSerializer(many=True, read_only=True)
        self.fields['tool_tag_refs'] = ToolTagSerializer(many=True, read_only=True)
        return super(ToolSerializer, self).to_representation(instance)

class CaseSerializer(serializers.ModelSerializer):
    current_user_library = serializers.SerializerMethodField()
    createdby = UserSerializer(read_only=True, many=False)

    def get_current_user_library(self, obj):
        linkers = CaseLibraryLink.objects.filter(user_ref=self.context.get('request').user.id).filter(case_ref=obj.id)
        return len(linkers) > 0

    class Meta:
        model = Case
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_ref'] = PracticeSerializer(many=False, read_only=True)
        self.fields['thematic_group_ref'] = ThematicGroupSerializer(many=False, read_only=True)
        self.fields['organization_activity_refs'] = OrganizationActivitySerializer(many=True, read_only=True)
        self.fields['monitoring_element_refs'] = MonitoringElementSerializer(many=True, read_only=True)
        return super(CaseSerializer, self).to_representation(instance)

class EvaluationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationReport
        fields = '__all__'
    def to_representation(self, instance):
        self.fields['method_refs'] = MethodSerializer(many=True, read_only=True)
        self.fields['analysis_method_refs'] = AnalysisMethodSerializer(many=True, read_only=True)
        self.fields['outcome_refs'] = OutcomeSerializer(many=True, read_only=True)
        self.fields['evaluation_type_ref'] = EvaluationTypeSerializer(many=False, read_only=True)
        self.fields['representation_method_refs'] = RepresentationMethodSerializer(many=True, read_only=True)
        self.fields['case_ref'] = CaseSerializer(many=False, read_only=True)
        return super(EvaluationReportSerializer, self).to_representation(instance)

class EvaluationReportChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationReportChangeRequest
        fields = '__all__'
    def to_representation(self, instance):
        self.fields['method_refs'] = MethodSerializer(many=True, read_only=True)
        self.fields['analysis_method_refs'] = AnalysisMethodSerializer(many=True, read_only=True)
        self.fields['outcome_refs'] = OutcomeSerializer(many=True, read_only=True)
        self.fields['evaluation_type_ref'] = EvaluationTypeSerializer(many=False, read_only=True)
        self.fields['representation_method_refs'] = RepresentationMethodSerializer(many=True, read_only=True)
        self.fields['evalution_report_ref'] = EvaluationReportSerializer(many=False, read_only=True)
        return super(EvaluationReportChangeRequestSerializer, self).to_representation(instance)

class ToolChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolChangeRequest
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_ref'] = PracticeSerializer(many=False, read_only=True)
        self.fields['thematic_group_ref'] = ThematicGroupSerializer(many=False, read_only=True)
        self.fields['method_ref'] = MethodSerializer(many=False, read_only=True)
        self.fields['outcome_level_ref'] = OutcomeLevelSerializer(many=False, read_only=True)
        self.fields['outcome_refs'] = OutcomeSerializer(many=True, read_only=True)
        self.fields['tool_tag_refs'] = ToolTagSerializer(many=True, read_only=True)
        self.fields['tool_ref'] = ToolSerializer(many=False, read_only=True)
        return super(ToolChangeRequestSerializer, self).to_representation(instance)

class LogicalModelChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicalModelChangeRequest
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_refs'] = PracticeSerializer(many=True, read_only=True)
        self.fields['outcome_refs'] = OutcomeSerializer(many=True, read_only=True)
        self.fields['thematic_group_ref'] = ThematicGroupSerializer(many=False, read_only=True)
        self.fields['logical_model_ref'] = LogicalModelSerializer(many=False, read_only=True)
        return super(LogicalModelChangeRequestSerializer, self).to_representation(instance)

class CaseChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseChangeRequest
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['target_refs'] = TargetSerializer(many=True, read_only=True)
        self.fields['practice_ref'] = PracticeSerializer(many=False, read_only=True)
        self.fields['thematic_group_ref'] = ThematicGroupSerializer(many=False, read_only=True)
        self.fields['organization_activity_refs'] = OrganizationActivitySerializer(many=True, read_only=True)
        self.fields['monitoring_element_refs'] = MonitoringElementSerializer(many=True, read_only=True)
        self.fields['case_ref'] = CaseSerializer(many=False, read_only=True)
        return super(CaseChangeRequestSerializer, self).to_representation(instance)