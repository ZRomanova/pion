import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserRequest } from 'src/app/models/userrequest';
import { TransportService } from 'src/app/services/transport.service';

@Component({
  selector: 'app-profile-update',
  templateUrl: './profile-update.component.html',
  styleUrls: ['./profile-update.component.scss']
})
export class ProfileUpdateComponent implements OnInit {
  
  constructor(private fb: FormBuilder,
    private transport: TransportService,
    private router: Router) { }

// E-mail
// Фамилия
// Имя
// Отчество
// Регион
// Организация
// Веб-сайт или адрес организации<br>в социальных сетях
// Должность
  public profileUpdateForm = this.fb.group({
    email: ['', Validators.required],
    lastname: ['', Validators.required],
    firstname: ['', Validators.required],
    middlename: ['', Validators.required],
    region: [''],
    organization: ['', Validators.required],
    website: ['', Validators.required],
    position: ['', Validators.required]
  });

  currentUserRequest: UserRequest;
  userRequests: UserRequest[];
  toLoad: number = 1;

  ngOnInit(): void {
    this.transport.get("user-requests/").then((userRequestsData) => {
      this.userRequests = userRequestsData.results;
      // console.log(this.userRequests)
      for (var userRequest of this.userRequests) {
        if (userRequest.current_user) {
          this.currentUserRequest = userRequest;
          console.log(this.currentUserRequest)
          break;
        }
      }
      
      if (this.currentUserRequest) {
        this.profileUpdateForm.controls['email'].setValue(this.currentUserRequest.email);
        this.profileUpdateForm.controls['lastname'].setValue(this.currentUserRequest.lastname);
        this.profileUpdateForm.controls['firstname'].setValue(this.currentUserRequest.firstname);
        this.profileUpdateForm.controls['middlename'].setValue(this.currentUserRequest.middlename);
        this.profileUpdateForm.controls['region'].setValue(this.currentUserRequest.region);
        this.profileUpdateForm.controls['organization'].setValue(this.currentUserRequest.organization);
        this.profileUpdateForm.controls['website'].setValue(this.currentUserRequest.website);
        this.profileUpdateForm.controls['position'].setValue(this.currentUserRequest.position);
      }
      this.toLoad -= 1;
    }).catch(error => console.log(error));
  }

  onSubmit() {
    if (this.profileUpdateForm.valid) {
      this.profileUpdateForm.value.id = Number(this.currentUserRequest.id);

    this.transport.put("user-requests/", this.currentUserRequest.id, this.profileUpdateForm.value).then((res: UserRequest) => {
      this.router.navigate(['/index']);
    }, err => {
      alert("Произошла ошибка при сохранении");
      console.error(err);
    });
  }
    else {
      alert("Заполните все обязательные поля!");
    }
  }
}
