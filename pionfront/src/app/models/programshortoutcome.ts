import { ProgramOutput } from './programoutput';

export class ProgramShortOutcome {
    id: number;
    name: string;
    program_ref: number;
    info: string;
    program_output_ref: ProgramOutput;
    program_output_many_refs: ProgramOutput[];
    shouldBeHighlighted:boolean = false;
}