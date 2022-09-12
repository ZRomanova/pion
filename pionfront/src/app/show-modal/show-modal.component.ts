import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-show-modal',
  templateUrl: './show-modal.component.html',
  styleUrls: ['./show-modal.component.scss']
})
export class ShowModalComponent implements OnInit, OnDestroy {

  @Input() error: boolean
  @Output() close = new EventEmitter<boolean>()

  interval: any

  constructor() {}

  ngOnInit(): void {
    this.interval = setTimeout(() => this.closeModal(), 3000)
  }

  closeModal() {
    this.close.emit(true)
  }

  ngOnDestroy(): void {
    clearTimeout(this.interval);
  }
}
