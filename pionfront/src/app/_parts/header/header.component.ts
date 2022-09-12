import { Component, Injectable, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TransportService } from 'src/app/services/transport.service';
import { User } from 'src/app/models/user';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {

  baseUrl = environment.baseUrl
  uSub: any
  users: User[];
  currentUser: User;
  toLoad: number = 1;
  displayLibrarySelect: boolean = false;
  displayAdminSelect: boolean = false;

  constructor(private transport: TransportService,
    private router: Router) {
      this.uSub = this.transport.newUser.subscribe(user => {if (user) this.findUser()})
    }

  ngOnInit(): void {    
    this.findUser()
  }

  async findUser() {
    try {
      if (this.displayHeader()) {
        let usersData = await this.transport.get("users/")       
        this.users = usersData.results;
        for (var user in this.users) {
          if (this.users[user].current_user) {
            this.currentUser = this.users[user];
            if (!this.currentUser.first_name)
              this.currentUser.first_name = this.currentUser.username;
            break;
          }
        }
      } else this.currentUser = null
      this.transport.user = this.currentUser
    } catch (e) {
      this.currentUser = null
      console.log(e)
    }
    
    this.toLoad -= 1;
  }

  goLibrary(library: string) {
    this.router.navigate(['/'+library]);
    this.displayLibrarySelect = false;
    this.displayAdminSelect = false;
  }

  exit() {
    var success = confirm("Выйти?");
    if (success) {
      this.transport.accessToken = null;
      this.transport.refreshToken = null;
      this.currentUser = null
      this.router.navigate(['/auth/login']);
    }
  }

  displayHeader(): boolean {
    if (!this.transport.accessToken)
      return false;
    return true;
  }
  
  goLogin() {
    this.router.navigate(['/auth/login'])
  }

  goRegister() {
    this.router.navigate(['/auth/registration'])
  }

  ngOnDestroy(): void {
    this.uSub.unsubscribe()
  }
}
