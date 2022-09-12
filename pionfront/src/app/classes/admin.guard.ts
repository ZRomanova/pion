import {ActivatedRouteSnapshot, CanActivate, CanActivateChild, Router, RouterStateSnapshot} from '@angular/router'
import { Injectable } from '@angular/core'
import { TransportService } from '../services/transport.service'
import { User } from '../models/user'

@Injectable({
    providedIn: 'root'
})
export class AdminGuard implements CanActivate, CanActivateChild {
    
    users: User[] 
    currentUser: User;

    constructor(private transport: TransportService,
                private router: Router){}

     async canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> {
        
        const usersData = await this.transport.get("users/")
        
        this.users = usersData.results;
        for (var user in this.users) {
            if (this.users[user].current_user) {
                this.currentUser = this.users[user];
                if (!this.currentUser.first_name)
                    this.currentUser.first_name = this.currentUser.username;
                break;
            }
        }
        if (this.currentUser.is_superuser) {
            return (true)
        }
        else {
            this.router.navigate(['/index'])
            return (false)
        }
    }

    canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> {
        return this.canActivate(route, state)
    }
}