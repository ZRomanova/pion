import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TheadFormComponent } from './thead-form.component';

describe('TheadFormComponent', () => {
  let component: TheadFormComponent;
  let fixture: ComponentFixture<TheadFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TheadFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TheadFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
