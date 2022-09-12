import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectLibraryComponent } from './select-library.component';

describe('SelectLibraryComponent', () => {
  let component: SelectLibraryComponent;
  let fixture: ComponentFixture<SelectLibraryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SelectLibraryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectLibraryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
