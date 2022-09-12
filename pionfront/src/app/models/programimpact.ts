import { Output } from '@angular/core';
import { ProgramMidOutcome } from './programmidoutcome';

export class ProgramImpact {
    id: number;
    name: string;
    program_ref: number;
    info: string;
    program_mid_outcome_ref: ProgramMidOutcome;
    program_mid_outcome_many_refs: ProgramMidOutcome[];
    shouldBeHighlighted:boolean = false;
}