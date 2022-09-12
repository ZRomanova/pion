import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { TransportService } from 'src/app/services/transport.service';

@Component({
  selector: 'app-pass-reset',
  templateUrl: './pass-reset.component.html',
  styleUrls: ['./pass-reset.component.scss']
})
export class PassResetComponent {

  constructor(private fb: FormBuilder,
    private transport: TransportService,
    private router: Router) { }

  public loginForm = this.fb.group({
    username: ['', Validators.required]
  });

  onSubmit() {
    // let fd = new FormData()
    // fd.append('username', this.loginForm.value.username)
    this.transport.get('send-new-user-password/?username='+ this.loginForm.value.username, true).then((data: any) => {
      alert(`Новый пароль отправлен на почту ${data.email}`)
      this.router.navigate(['/auth/login']);
    }).catch((error: any) => {
      alert("Произошла ошибка")
      console.log(error);
    });
  }


}
