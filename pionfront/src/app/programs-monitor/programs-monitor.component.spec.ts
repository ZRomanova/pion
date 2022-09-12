import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProgramsMonitorComponent } from './programs-monitor.component';

describe('ProgramsMonitorComponent', () => {
  let component: ProgramsMonitorComponent;
  let fixture: ComponentFixture<ProgramsMonitorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProgramsMonitorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProgramsMonitorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
