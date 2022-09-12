import { Method } from "./method";
import { Outcome } from "./outcome";
import { OutcomeLevel } from "./outcomelevel";
import { Practice } from "./practice";
import { Target } from "./target";
import { ThematicGroup } from "./thematicgroup";
import { ToolTag } from "./tooltags";

export class Tool {
    id: number
    name: string; 
    info: string;
    thematic_group_ref: ThematicGroup;
    target_refs: Target[];
    practice_ref: Practice;
    method_ref: any;
    outcome_level_ref: OutcomeLevel;
    outcome_refs: Outcome[];
    current_user_library: boolean;
    tool_file: any
    url: string
    tool_tag_refs: ToolTag[]

    createdby: any
}