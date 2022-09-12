import { Activity } from './activity';

export class ProgramOutput {
    id: number;
    name: string;
    program_ref: number;
    info: string;
    activity_ref: Activity;
    shouldBeHighlighted:boolean = false;
}