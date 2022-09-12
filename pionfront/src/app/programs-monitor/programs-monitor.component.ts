import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { TransportService } from '../services/transport.service';
import { Router } from '@angular/router';
import { Program } from '../models/program';
import { UserRequest } from '../models/userrequest';
import { User } from '../models/user';

@Component({
  selector: 'app-programs-monitor',
  templateUrl: './programs-monitor.component.html',
  styleUrls: ['./programs-monitor.component.scss']
})
export class ProgramsMonitorComponent implements OnInit {

  constructor(public fb: FormBuilder,
    public transport: TransportService,
    public router: Router) { }

  toLoad: number = 2;
  programs: Program[];
  userRequests: UserRequest[];

  ngOnInit(): void {
    this.transport.get("programs/").then((programsData) => {
      this.programs = programsData.results;

      this.toLoad -= 1;
    });
    this.transport.get("user-requests/").then((userRequestsData) => {
      this.userRequests = userRequestsData.results;
      this.toLoad -= 1;
    });
  }

  programsForUser(user_ref: User) {
    return this.programs.filter(el => el.user_ref && el.user_ref.id == user_ref.id);
  }

}
