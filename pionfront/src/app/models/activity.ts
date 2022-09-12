import { Target } from './target';

export class Activity {
    id: number;
    name: string;
    program_ref: number;
    target_ref: Target;
    info: string;

    shouldBeHighlighted: boolean = false;
}