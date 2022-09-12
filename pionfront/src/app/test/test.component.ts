import { Component, OnInit } from '@angular/core';
import { LogicalModel } from '../models/logicalModel';
import { TransportService } from '../services/transport.service';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent implements OnInit {

  logicalModels: LogicalModel[]
  authenticated: boolean

  constructor(private transport: TransportService) { }

  ngOnInit(): void {
    if (this.transport.accessToken != null && this.transport.accessToken != undefined && this.transport.refreshToken != null && this.transport.refreshToken != undefined)
      this.authenticated = true;

    
    this.transport.getOld("https://pion.org.ru/newpion/api/logical-models/").then((logicalModels) => {
      this.logicalModels = logicalModels.results;
      console.log(this.logicalModels)
      // for (let model of this.logicalModels) {
      //   this.transport.patch('logical-models/', String(model.id), {model_file: model.model_file, result_tree_file: model.result_tree_file}).then(res => {
      //     console.log('ok')
      //   }).catch(e => console.log(e))
      // }
    }).catch(error => {
      console.log(error)
    });
  }

}
