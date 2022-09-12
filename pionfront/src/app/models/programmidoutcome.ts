import { Output } from '@angular/core';
import { ProgramShortOutcome } from './programshortoutcome';

export class ProgramMidOutcome {
    id: number;
    name: string;
    program_ref: number;
    info: string;
    program_short_outcome_ref: ProgramShortOutcome;
    program_short_outcome_many_refs: ProgramShortOutcome[];
    shouldBeHighlighted:boolean = false;
}