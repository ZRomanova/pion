import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { IndexComponent } from './index/index.component';
import { LibraryComponent } from './library/library.component';
import { ProgramComponent } from './program/program.component';
import { ProgramListComponent } from './program-list/program-list.component';
import { RegistrationComponent } from './auth/registration/registration.component';
import { ResultComponent } from './result/result.component';
import { LoginComponent } from './auth/login/login.component';
import { UserRequestsComponent } from './auth/user-requests/user-requests.component';
import { SelectLibraryComponent } from './select-library/select-library.component';
import { ProgramsMonitorComponent } from './programs-monitor/programs-monitor.component';
import { AdminGuard } from './classes/admin.guard';
import { ProgramGuard } from './classes/program.guard';
import { ToolsComponent } from './tools/tools.component';
import { CaseComponent } from './case/case.component';
import { ReportComponent } from './report/report.component';
import { PassResetComponent } from './auth/pass-reset/pass-reset.component';
import { ProfileUpdateComponent } from './auth/profile-update/profile-update.component';

const routes: Routes = [
  { path: 'index', component: ProgramListComponent },
  { path: 'outcomes', component: IndexComponent }, // done
  { path: 'library', component: LibraryComponent },
  { path: 'select-library', component: SelectLibraryComponent },
  { path: 'report/:id', component: ReportComponent },
  { path: 'tools', component: ToolsComponent },
  { path: 'cases', component: CaseComponent },
  { path: 'program', component: ProgramComponent },
  { path: 'program/:id', canActivate: [ProgramGuard],  component: ProgramComponent },
  // { path: 'scheme', component: SchemeComponent },
  { path: 'auth', children:
    [
      { path: 'registration', component: RegistrationComponent },
      { path: 'reset', component: PassResetComponent },
      {path: 'profile', component: ProfileUpdateComponent},
      { path: 'login', component: LoginComponent }, // done
    ]},
  { path: 'admin', canActivate: [AdminGuard], children:
    [
      { path: 'user-requests', component: UserRequestsComponent }, // done
      { path: 'programs-monitor', component: ProgramsMonitorComponent },
    ]},
  { path: 'result/:id', component: ResultComponent }, // done
  { path: '',   redirectTo: '/index', pathMatch: 'full' }, // redirect to `first-component`
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
