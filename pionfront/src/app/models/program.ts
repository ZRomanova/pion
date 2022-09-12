import { Practice } from './practice';
import { Target } from './target';
import { User } from './user';

export class Program {
    id: string;
    name: string;
    description: string;
    period: string;
    user_ref: User;
    target_refs: Target[];
    practice_refs: Practice[];
    current_user: boolean;
}