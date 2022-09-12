import {ActivatedRoute, ActivatedRouteSnapshot, CanActivate, CanActivateChild, Router, RouterStateSnapshot} from '@angular/router'
import { Injectable } from '@angular/core'
import { TransportService } from '../services/transport.service'
import { User } from '../models/user'
import { Program } from '../models/program'

@Injectable({
    providedIn: 'root'
})
export class ProgramGuard implements CanActivate, CanActivateChild {
    
    users: User[] 
    currentUser: User;
    program: Program
    id: string

    constructor(private transport: TransportService,
        private activateRoute: ActivatedRoute,
        private router: Router){
            this.id = activateRoute.snapshot.params['id'];
        }

     async canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> {
        try {
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
            if (this.currentUser.is_superuser || !this.id) {
                return (true)
            }
            else {
                
                    this.program = await this.transport.get('programs/' + this.id)      
                    if (this.program && this.program.current_user) {
                        return (true)
                    }
                this.router.navigate(['/index'])
                return (false)
            }
        } catch (e) {
            console.log(e)
            this.router.navigate(['/index'])
            return (false)
        }
    }

    canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> {
        return this.canActivate(route, state)
    }
}