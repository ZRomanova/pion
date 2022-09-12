import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TransportService } from '../services/transport.service';

@Component({
  selector: 'app-select-library',
  templateUrl: './select-library.component.html',
  styleUrls: ['./select-library.component.scss']
})
export class SelectLibraryComponent implements OnInit {

  auth: boolean
  br1Height: number = 0
  br2Height: number = 0

  constructor(public transport: TransportService, private router: Router) { 
  }

  ngOnInit(): void {
    if (this.transport.accessToken) this.auth = true;
    else this.auth = false;

    let br1 = document.querySelectorAll('.br1')
    for (let i = 0; i < br1.length; i++) {
      if (br1[i].clientHeight > this.br1Height) this.br1Height = br1[i].clientHeight
    }
    for (let i = 0; i < br1.length; i++) {
      br1[i].setAttribute('style', 'height: ' + this.br1Height + 'px;')
    }
    let br2 = document.querySelectorAll('.br2')
    for (let i = 0; i < br2.length; i++) {
      if (br2[i].clientHeight > this.br2Height) this.br2Height = br2[i].clientHeight
    }
    for (let i = 0; i < br2.length; i++) {
      br2[i].setAttribute('style', 'height: ' + this.br2Height + 'px !important;')
    }
  }

  goLibrary(library: string) {
    this.router.navigate([library]);
  }
}
