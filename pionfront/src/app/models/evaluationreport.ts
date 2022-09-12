import { AnalysisMethod } from "./analysismethod";
import { Case } from "./case";
import { EvaluationType } from "./evaluationtype";
import { Method } from "./method";
import { Outcome } from "./outcome";
import { RepresentationMethod } from "./representationmethod";

export class EvaluationReport {
    id: number
    type: string;
    evaluation_type_ref: EvaluationType;
    representation_method_refs: RepresentationMethod[];
    analysis_method_refs: AnalysisMethod[];
    outcome_refs: Outcome[];
    method_refs: Method[];
    key_questions: string;
    other_results: string;
    evaluation_file: any;
    case_ref: Case
}