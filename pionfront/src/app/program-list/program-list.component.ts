import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { TransportService } from '../services/transport.service';
import { Router } from '@angular/router';
import { UserRequest } from '../models/userrequest';
import { Program } from '../models/program';

@Component({
  selector: 'app-program-list',
  templateUrl: './program-list.component.html',
  styleUrls: ['./program-list.component.scss']
})
export class ProgramListComponent implements OnInit {

  constructor(public fb: FormBuilder,
    public transport: TransportService,
    public router: Router) { }

  status: string = 'ЗАГРУЗКА...'
  idToDownload: string = null;
  programs: Program[];
  myPrograms: Program[];
  userRequests: UserRequest[];
  currentUserRequest: UserRequest;
  toLoad = 2

  ngOnInit(): void {
    this.transport.get("programs/").then((programsData) => {
      this.programs = programsData.results;
      this.myPrograms = this.programs.filter(el => el.current_user);
      if (this.myPrograms.length == 0) this.status = "У ВАС НЕТ ПРОГРАММ"
      this.toLoad -= 1
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });;
    this.transport.get("user-requests/").then((userRequestsData) => {
      this.userRequests = userRequestsData.results;
      this.currentUserRequest = this.userRequests.find(el => el.current_user);       
      this.toLoad -= 1
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });;
  }

  newProgram() {
    this.router.navigate(['/program']);
  }

}
