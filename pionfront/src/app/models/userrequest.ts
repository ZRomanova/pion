import { User } from './user';

export class UserRequest {
    id: string;
    email: string;
    lastname: string;
    firstname: string;
    middlename: string;
    region: string;
    organization: string;
    website: string;
    position: string;
    password: string;
    createdon: Date;
    verifiedon: Date;
    lastseenon: Date;
    user_ref: User;
    current_user: boolean;
}