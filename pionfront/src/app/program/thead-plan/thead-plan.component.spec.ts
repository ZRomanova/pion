import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TheadPlanComponent } from './thead-plan.component';

describe('TheadPlanComponent', () => {
  let component: TheadPlanComponent;
  let fixture: ComponentFixture<TheadPlanComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TheadPlanComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TheadPlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
