import { Practice } from './practice';
import { Target } from './target';
import { Outcome } from './outcome';
import { ThematicGroup } from './thematicgroup';

export class LogicalModel {
    id: string;
    name: string;
    organization: string;
    target_refs: Target[];
    practice_refs: Practice[];
    outcome_refs: Outcome[];
    thematic_group_ref: ThematicGroup;
    period: string;
    verification_info: string;
    verification_level_regularity: string;
    verification_level_validity: string;
    verification_level_outcome_accessibility: string;
    verification_level_outcome_validity: string;
    model_file: any;
    result_tree_file: any;
    current_user_library: boolean;

    createdby: any
}