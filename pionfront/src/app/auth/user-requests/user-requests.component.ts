import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { TransportService } from 'src/app/services/transport.service';
import { Router, ActivatedRoute } from '@angular/router';
import { UserRequest } from 'src/app/models/userrequest';

@Component({
  selector: 'app-user-requests',
  templateUrl: './user-requests.component.html',
  styleUrls: ['./user-requests.component.scss']
})
export class UserRequestsComponent implements OnInit {

  constructor(private fb: FormBuilder,
    public transport: TransportService,
    public router: Router,
    private activateRoute: ActivatedRoute) { }

  userrequests: UserRequest[];

  ngOnInit(): void {
    this.transport.get("user-requests/").then((userRequestsData) => {
      this.userrequests = userRequestsData.results;
      console.log(this.userrequests)
    });
  }

  accept(userrequest:UserRequest) {
    this.transport.post("user-requests/" + userrequest.id + "/accept/", {}).then((res) => {
      this.transport.get("user-requests/").then((userRequestsData) => {
        this.userrequests = userRequestsData.results;
      });
    }, (error) => {
      console.error(error);
    });
  }
  decline(userrequest:UserRequest) {
    this.transport.post("user-requests/" + userrequest.id + "/decline/", {}).then((res) => {
      this.transport.get("user-requests/").then((userRequestsData) => {
        this.userrequests = userRequestsData.results;
      });
    }, (error) => {
      console.error(error);
    });
  }
}
