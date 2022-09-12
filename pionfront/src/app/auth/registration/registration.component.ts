import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { TransportService } from 'src/app/services/transport.service';
import { Router } from '@angular/router';
import { UserRequest } from 'src/app/models/userrequest';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  baseUrl = environment.baseUrl

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
// Пароль
  public registrationForm = this.fb.group({
    email: ['', Validators.required],
    lastname: ['', Validators.required],
    firstname: ['', Validators.required],
    middlename: ['', Validators.required],
    region: [''],
    organization: ['', Validators.required],
    website: ['', Validators.required],
    position: ['', Validators.required],
    password: ['', Validators.required]
  });

  ngOnInit(): void {
  }

  onSubmit() {
    if (this.registrationForm.valid) {
    this.transport.post("user-requests/", this.registrationForm.value, true).then((res:UserRequest) => {
      alert("Спасибо! Мы свяжемся с Вами по электронной почте!");
      this.router.navigate(['/']);
    }, err => {
      alert("Произошла ошибка при сохранении программы");
      console.error(err);
    });
  }
  else {
    alert("Заполните все поля!");
  }
  }

}
