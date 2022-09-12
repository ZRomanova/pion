import { OutcomeMethod } from './outcomemethod';
import { Practice } from './practice';
import { Target } from './target';
import { ThematicGroup } from './thematicgroup';

export class Outcome {
    id: string;
    name: string;
    target_refs: Target[];
    practice_refs: Practice[];
    method_refs: OutcomeMethod[]
    thematic_group_refs: ThematicGroup[];
    current_user_library: boolean;

    createdby: any
}