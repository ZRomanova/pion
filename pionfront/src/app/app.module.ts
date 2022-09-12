import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { DatePipe } from '@angular/common';
import {AutosizeModule} from 'ngx-autosize';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './_parts/header/header.component';
import { FooterComponent } from './_parts/footer/footer.component';
import { IndexComponent } from './index/index.component';
import { LibraryComponent } from './library/library.component';
import { ProgramComponent } from './program/program.component';
import { ProgramListComponent } from './program-list/program-list.component';
import { RegistrationComponent } from './auth/registration/registration.component';
import { ResultComponent } from './result/result.component';
import { HttpClientModule } from '@angular/common/http';
import { LoginComponent } from './auth/login/login.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UserRequestsComponent } from './auth/user-requests/user-requests.component';
import { SelectLibraryComponent } from './select-library/select-library.component';
import { ProgramsMonitorComponent } from './programs-monitor/programs-monitor.component';
import { SchemeComponent } from './_parts/scheme/scheme.component';
import { PassResetComponent } from './auth/pass-reset/pass-reset.component';
import { TheadPlanComponent } from './program/thead-plan/thead-plan.component';
import { TheadFormComponent } from './program/thead-form/thead-form.component';
import { ToolsComponent } from './tools/tools.component';
import { CaseComponent } from './case/case.component'
import { ProfileUpdateComponent } from './auth/profile-update/profile-update.component';
import { ProgramCardComponent } from './program-list/program-card/program-card.component';
import { ProfileCardComponent } from './program-list/profile-card/profile-card.component';
import { ReportComponent } from './report/report.component';
import { TestComponent } from './test/test.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ShowModalComponent } from './show-modal/show-modal.component';
import { RefDirective } from './classes/ref.directive';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    IndexComponent,
    LibraryComponent,
    ProgramComponent,
    ProgramListComponent,
    RegistrationComponent,
    ResultComponent,
    LoginComponent,
    UserRequestsComponent,
    SelectLibraryComponent,
    ProgramsMonitorComponent,
    SchemeComponent,
    PassResetComponent,
    TheadPlanComponent,
    TheadFormComponent,
    ToolsComponent,
    CaseComponent,
    ProfileUpdateComponent,
    ProgramCardComponent,
    ProfileCardComponent,
    ReportComponent,
    TestComponent,
    ShowModalComponent,
    RefDirective
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    AutosizeModule
  ],
  providers: [DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
