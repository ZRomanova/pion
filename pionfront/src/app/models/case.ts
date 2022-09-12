import { EvaluationReport } from "./evaluationreport";
import { MonitoringElement } from "./monitoringelement";
import { OrganizationActivity } from "./organizationactivity";
import { Practice } from "./practice";
import { Target } from "./target";
import { ThematicGroup } from "./thematicgroup";

export class Case {
    id: number
    name: string
    case_file: any
    url: string
    organization: string;
    target_refs: Target[];
    practice_ref: Practice;
    organization_activity_refs: OrganizationActivity[]
    monitoring_element_refs: MonitoringElement[]
    thematic_group_ref: ThematicGroup

    verification_info: string;
    verification_level_regularity: string;
    verification_level_validity: string;
    verification_level_outcome_accessibility: string;
    verification_level_outcome_validity: string;
    current_user_library: boolean;

    createdby: any
    add_public_confirm: boolean
}