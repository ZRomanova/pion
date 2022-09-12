import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Program } from 'src/app/models/program';
import { UserRequest } from 'src/app/models/userrequest';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-program-card',
  templateUrl: './program-card.component.html',
  styleUrls: ['./program-card.component.scss']
})

export class ProgramCardComponent {
  baseUrl = environment.baseUrl

  @Input() program: Program
  @Input() currentUserRequest: UserRequest

  constructor(
    private router: Router) { }
  
  idToDownload: string = null;

  openProgram(program: Program) {
    this.router.navigate(['/program/' + program.id]);
  }

  downloadProgram(event) {
    event.preventDefault();

    window.open(this.baseUrl+"newpion/api/download?program_id="+this.idToDownload, "_blank");
  }

  downloadPlan(event) {
    event.preventDefault();

    window.open(this.baseUrl+"newpion/api/download-plan?program_id="+this.idToDownload, "_blank");
  }

  downloadForm(event) {
    event.preventDefault();
    
    window.open(this.baseUrl+"newpion/api/download-form?program_id="+this.idToDownload, "_blank");
  }

}
