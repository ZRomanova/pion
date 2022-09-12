import { TargetDescription } from './targetdescription';

export class Target {
    id: string;
    name: string;
    current: boolean;
    targetDescription: TargetDescription;
    shouldBeHighlighted: boolean = false;
    parent_ref: any
    has_children: boolean
    checked: boolean
    checkedMy: boolean
}