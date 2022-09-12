import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { UserRequest } from 'src/app/models/userrequest';

@Component({
  selector: 'app-profile-card',
  templateUrl: './profile-card.component.html',
  styleUrls: ['./profile-card.component.scss']
})
export class ProfileCardComponent  {

  @Input() currentUserRequest: UserRequest;

  constructor(private router: Router) { }

  updateProfile(event) {
    event.preventDefault();
    
    this.router.navigate(['/auth/profile']);
  }

}
