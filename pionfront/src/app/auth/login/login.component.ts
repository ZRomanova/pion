import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { TransportService } from 'src/app/services/transport.service';
import { Router } from '@angular/router';
import { HeaderComponent } from 'src/app/_parts/header/header.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private fb: FormBuilder,
    public header: HeaderComponent,
    public transport: TransportService,
    private router: Router) { }

  public loginForm = this.fb.group({
    email: ['', Validators.required],
    password: ['', Validators.required]
  });

  ngOnInit(): void {
    this.transport.sendToHeader(false)
  }

  onSubmit() {
    this.transport.getToken(this.loginForm.controls['email'].value, this.loginForm.controls['password'].value).then((data: any) => {
      this.transport.sendToHeader(true)
      this.router.navigate(['/']);
    }, () => {
      alert("Некорректные авторизационные данные!");
    });
    
  }

  show_hide_password(){
    let input = document.getElementById('password-input');
    let target = document.getElementById('password-control');
    if (input.getAttribute('type') == 'password') {
      target.classList.add('view');
      target.classList.remove('no_view');
      input.setAttribute('type', 'text');
    } else {
      target.classList.add('no_view');
      target.classList.remove('view');
      input.setAttribute('type', 'password');
    }
  }
}
