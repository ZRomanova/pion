import { Component, OnInit, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AnalysisMethod } from '../models/analysismethod';
import { Case } from '../models/case';
import { EvaluationReport } from '../models/evaluationreport';
import { EvaluationType } from '../models/evaluationtype';
import { Method } from '../models/method';
import { MonitoringElement } from '../models/monitoringelement';
import { OrganizationActivity } from '../models/organizationactivity';
import { Outcome } from '../models/outcome';
import { Practice } from '../models/practice';
import { RepresentationMethod } from '../models/representationmethod';
import { Target } from '../models/target';
import { ThematicGroup } from '../models/thematicgroup';
import { TransportService } from '../services/transport.service';

@Component({
  selector: 'app-case',
  templateUrl: './case.component.html',
  styleUrls: ['./case.component.scss']
})
export class CaseComponent implements OnInit {

  status: string = 'ЗАГРУЗКА...'
  toLoad = 6
  displayMyLibrary = false
  authenticated: boolean
  targets: Target[];
  cases: Case[];
  allCases: Case[];
  myCases: Case[];
  allMyCases: Case[];
  practices: Practice[]
  thematicGroups: ThematicGroup[]
  monitoringElements: MonitoringElement[]
  organizationActivities: OrganizationActivity[]
  createCaseForm: FormGroup
  addReportForm: FormGroup
  formPage: number = 0
  file: File
  repFile: File
  newParentRef: number

  evaluationTypes: EvaluationType[]
  outcomes: Outcome[]
  methods: Method[]
  analysisMethods: AnalysisMethod[]
  representationMethods: RepresentationMethod[]

  myVerified: boolean = false;
  verified: boolean = false;

  displayDetails: boolean
  currentCase: Case
  evaluationReports: EvaluationReport[]

  otherRepMethod: boolean
  otherAnMethod: boolean
  otherMethod: boolean
  otherEvType: boolean
  displayAddPersonal: boolean
  displayRemovePersonal: boolean

  @ViewChild('file_input') file_input
  @ViewChild('file_rep') file_rep

  constructor(public transport: TransportService, 
    public fb: FormBuilder,
    private activateRoute: ActivatedRoute,
    public router: Router) { }

  public filterForm = this.fb.group({
    targetFilters: new FormArray([]),
    practiceFilters: new FormArray([]),
    meFilters: new FormArray([]),
    oaFilters: new FormArray([]),
    tgFilters: new FormArray([])
  });

  public myFilterForm = this.fb.group({
    targetFilters: new FormArray([]),
    practiceFilters: new FormArray([]),
    meFilters: new FormArray([]),
    oaFilters: new FormArray([]),
    tgFilters: new FormArray([])
  });

  public filterRoot = this.fb.group({
    target: new FormControl(false),
    practice: new FormControl(false),
    me: new FormControl(false),
    oa:  new FormControl(false),
    tg: new FormControl(false),
  });

  public myFilterRoot = this.fb.group({
    target: new FormControl(false),
    practice: new FormControl(false),
    me: new FormControl(false),
    oa: new FormControl(false),
    tg: new FormControl(false),
  });

  ngOnInit(): void {
    if (this.transport.accessToken != null && this.transport.accessToken != undefined && this.transport.refreshToken != null && this.transport.refreshToken != undefined)
      this.authenticated = true;
    else 
      this.authenticated = false;

      this.activateRoute.queryParamMap.subscribe(queryParams => {
        let id = queryParams.get('id');
        if (id) this.transport.get("cases/"+id+"/").then(model => {
          this.openDetails(model)
        }).catch(e => console.log(e))
      })

      this.transport.get("targets/", !this.authenticated).then((targetsData) => {
        const targets = targetsData.results;
        const children = targets.filter(m => typeof m.parent_ref == 'number').reverse()
        for (let target of children) {
          let child_index = targets.indexOf(targets.find(m => m.id == target.id))
          targets.splice(child_index, 1)
          let parent_index = targets.indexOf(targets.find(m => m.id == target.parent_ref))
          targets[parent_index].has_children = true
          targets.splice(parent_index + 1, 0, target)
        }
        this.targets = targets
        this.toLoad -= 1;
      }).catch(error => {
        console.log(error)
        this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
      });

    this.transport.get("practices/", !this.authenticated).then((practicesData) => {
      this.practices = practicesData.results;    
      this.toLoad -= 1
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });

    this.transport.get("cases/", !this.authenticated).then((casesData) => {
      this.cases = casesData.results;
      this.allCases = casesData.results;     
      this.sortCases() 
      this.toLoad -= 1;
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });

    this.transport.get("thematic-groups/", !this.authenticated).then((thematicGroupsData) => {
      this.thematicGroups = thematicGroupsData.results;    
      this.toLoad -= 1
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });

    this.transport.get("monitoring-elements/", !this.authenticated).then((monitoringElementsData) => {
      this.monitoringElements = monitoringElementsData.results;
      this.toLoad -= 1;
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });

    this.transport.get("organization-activities/", !this.authenticated).then((organizationActivitiesData) => {
      this.organizationActivities = organizationActivitiesData.results;    
      this.toLoad -= 1
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });

    this.transport.get("analysis-methods/", !this.authenticated).then((data) => {
      this.analysisMethods = data.results;    
    })

    this.transport.get("evaluation-types/", !this.authenticated).then((data) => {
      this.evaluationTypes = data.results;    
    })

    this.transport.get("representation-methods/", !this.authenticated).then((data) => {
      this.representationMethods= data.results;    
    })

    this.transport.get("methods/", !this.authenticated).then((data) => {
      this.methods = data.results;    
    })

    this.transport.get("outcomes/", !this.authenticated).then((data) => {
      this.outcomes = data.results;    
    })

    this.transport.get("evaluation-reports/", !this.authenticated).then((data) => {
      this.evaluationReports = data.results;    
    })
  }

  selectMyLibrary(my: boolean) {
    this.displayMyLibrary = my
    this.cases = this.allCases
    this.filterForm.reset()
    this.myFilterForm.reset()
    this.verified = false
    this.myVerified = false
    this.sortCases()
  }
  openDetails(caseItem: Case) {
    this.router.navigate([], {queryParams: {id: caseItem.id}})
    this.currentCase = caseItem
    this.displayDetails = true
  }
  closeDetails() {
    this.displayDetails = false
    this.currentCase = null
    this.router.navigate([])
  }
  downloadFile(filePath: string) {
    let link = document.createElement("a");
    link.download = "filename";
    link.href = filePath;
    link.click();
    link.remove();
  }
  addToLibrary() {
    this.transport.post("cases/" + this.currentCase.id + "/add_to_library/", {}).then((addToLibraryResult) => {
      this.cases.find(c => c.id == this.currentCase.id).current_user_library = true;
      this.sortCases() 
    }, (error) => {});
    this.closeAddPersonal()
  }
  removeFromLibrary() {
    this.transport.post("cases/" + this.currentCase.id + "/remove_from_library/", {}).then((addToLibraryResult) => {
      this.cases.find(c => c.id == this.currentCase.id).current_user_library = false;
      this.sortCases() 
    }, (error) => {});
    this.closeAddPersonal()
  }
  closeAddPersonal() {
    this.displayAddPersonal = false;
    this.displayRemovePersonal = false;
  }
  openAddPersonal(model: Case) {
    if (!model.current_user_library && this.authenticated) {
      this.currentCase= model;
      this.displayAddPersonal = true;
    }
    if (model.current_user_library && this.authenticated) {
      this.currentCase = model;
      this.displayRemovePersonal = true;
    }
  }
  closeForm() {
    this.formPage = 0
  }
  addForm(event) {
    event.preventDefault()

    const tFormControls = () => {
      let arr: FormControl[] = []
      for (let target of this.targets) arr.push(new FormControl(false))
      return arr
    }
    const oaFormControls = () => {
      let arr: FormControl[] = []
      for (let oa of this.organizationActivities) arr.push(new FormControl(false))
      return arr
    }
    const meFormControls = () => {
      let arr: FormControl[] = []
      for (let me of this.monitoringElements) arr.push(new FormControl(false))
      return arr
    }
    this.createCaseForm = new FormGroup({
      name: new FormControl('', Validators.required), //
      organization: new FormControl('', Validators.required), //
      practice_ref: new FormControl('', Validators.required), //
      target_refs: new FormArray(tFormControls()), //
      thematic_group_ref: new FormControl('', Validators.required),//
      verification_info: new FormControl(''),//
      verification_level_regularity: new FormControl(''),//
      verification_level_validity: new FormControl(''),//
      verification_level_outcome_accessibility: new FormControl(''),//
      verification_level_outcome_validity: new FormControl(''),//
      organization_activity_refs: new FormArray(oaFormControls()),
      monitoring_element_refs: new FormArray(meFormControls()),
      url: new FormControl(''),
      isNew: new FormControl(true)
    })
    this.formPage = 1
  }

  editForm(event) {
    event.preventDefault()

    const tFormControls = () => {
      let arr: FormControl[] = []
      for (let target of this.targets) arr.push(new FormControl(this.currentCase.target_refs.find(el => +el.id == +target.id) ? true : false))
      return arr
    }

    const oaFormControls = () => {
      let arr: FormControl[] = []
      for (let oa of this.organizationActivities) arr.push(new FormControl(this.currentCase.organization_activity_refs.find(el => +el.id == +oa.id) ? true : false))
      return arr
    }
    const meFormControls = () => {
      let arr: FormControl[] = []
      for (let me of this.monitoringElements) arr.push(new FormControl(this.currentCase.monitoring_element_refs.find(el => +el.id == +me.id) ? true : false))
      return arr
    }

    this.createCaseForm = new FormGroup({
      name: new FormControl(this.currentCase.name, Validators.required), //
      organization: new FormControl(this.currentCase.organization, Validators.required), //
      practice_ref: new FormControl(this.currentCase.practice_ref.id, Validators.required), //
      target_refs: new FormArray(tFormControls()), //
      thematic_group_ref: new FormControl(this.currentCase.thematic_group_ref.id, Validators.required),//
      verification_info: new FormControl(this.currentCase.verification_info),//
      verification_level_regularity: new FormControl(this.currentCase.verification_level_regularity),//
      verification_level_validity: new FormControl(this.currentCase.verification_level_validity),//
      verification_level_outcome_accessibility: new FormControl(this.currentCase.verification_level_outcome_accessibility),//
      verification_level_outcome_validity: new FormControl(this.currentCase.verification_level_outcome_validity),//
      organization_activity_refs: new FormArray(oaFormControls()),
      monitoring_element_refs: new FormArray(meFormControls()), //monitoring_element_refs
      url: new FormControl(this.currentCase.url),
      isNew: new FormControl(false)
    })
    this.closeAddPersonal()
    this.formPage = 1
  }

  changeMethod() {
    let valArr = this.addReportForm.value.method_refs
    for (let i = 0; i < this.methods.length; i++) {
      if (valArr[i]) {
        let name = this.methods[i].name
        if (name.trim().toLocaleLowerCase() == "другое") {
          this.otherMethod = true
          this.newParentRef = this.methods[i].parent_ref
          return
        }
      }
    }
    this.otherMethod = false
    this.newParentRef = null
    this.addReportForm.patchValue({other_method: ''})
  }
  changeRepMethod() {
    let valArr = this.addReportForm.value.representation_method_refs
    for (let i = 0; i < this.representationMethods.length; i++) {
      if (valArr[i]) {
        let name = this.representationMethods[i].name
        if (name.trim().toLocaleLowerCase() == "другое") {
          this.otherRepMethod = true
          return
        }
      }
    }
    this.otherRepMethod = false
    this.addReportForm.patchValue({other_representation_method: ''})
  }
  changeAnMethod() {
    let valArr = this.addReportForm.value.analysis_method_refs
    for (let i = 0; i < this.analysisMethods.length; i++) {
      if (valArr[i]) {
        let name = this.analysisMethods[i].name
        if (name.trim().toLocaleLowerCase() == "другое") {
          this.otherAnMethod = true
          return
        }
      }
    }
    this.otherAnMethod = false
    this.addReportForm.patchValue({other_analysis_method: ''})
  }
  changeEvType() {
    let id = this.addReportForm.value.evaluation_type_ref
    let name = this.evaluationTypes.find(el => el.id == id).name
    if (name.trim().toLocaleLowerCase() == "другое") {
      this.otherEvType = true
      return
    }
    this.otherEvType = false
    this.addReportForm.patchValue({other_evaluation_type: ''})
  }
  addToAllLibrary(event) { 
    event.preventDefault()
    this.transport.post("cases/" + this.currentCase.id + "/switchData_library/", {}).then(
    (addToLibraryResult) => {
      alert('Запрос успешно отправлен!')
      this.formPage = 0
    }, 
    (error) => {
      console.log(error)
      alert('Ошибка. Не удалось отправить запрос')
      this.formPage = 0
    })
  }
  sortCases() {
    this.allMyCases = [];
      for (var item in this.allCases) {
        if (this.allCases[item].current_user_library)
          this.allMyCases.push(this.allCases[item]);
        }
      this.myCases = this.allMyCases; 
  }
  onSubmit(event, evRep?: boolean) { 
    event.preventDefault() 
    const values: any = {...this.createCaseForm.value}

    const boolToObjT = () => {
      let resNum: any[] = []
      let valArr = this.createCaseForm.value.target_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i] && !this.targets[i].parent_ref) resNum.push(+this.targets[i].id)
        else if (valArr[i] && this.targets[i].parent_ref) {
          const parent_index = this.targets.indexOf(this.targets.find(item => item.id == this.targets[i].parent_ref))
          if (valArr[parent_index]) resNum.push(+this.targets[i].id)
        }
      }
      return resNum
    }

    const boolToObjOA = () => {
      let resNum: any[] = []
      let valArr = this.createCaseForm.value.organization_activity_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.organizationActivities[i].id)
      }
      return resNum
    }

    const boolToObjME = () => {
      let resNum: any[] = []
      let valArr = this.createCaseForm.value.monitoring_element_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.monitoringElements[i].id) 
      }
      return resNum
    }

    values.monitoring_element_refs = boolToObjME()
    values.organization_activity_refs = boolToObjOA()
    values.target_refs = boolToObjT()
    values.thematic_group_ref = +this.createCaseForm.value.thematic_group_ref
    values.practice_ref =  +this.createCaseForm.value.practice_ref
    delete values.isNew

    if (this.createCaseForm.value.isNew) this.post(values, evRep)
    if (!this.createCaseForm.value.isNew) this.update(values, evRep)
  }

  post(values, evRep) {
    this.transport.post("cases/", values).then((res) => {
      this.allCases.push(res)
      this.currentCase = res
      this.addToLibrary()
      if (this.file) {
        let fd = new FormData()
        fd.append('case_file', this.file, this.file.name)
        this.transport.patch("cases/", res.id, fd).then((resFile) => {
          this.currentCase = {...this.currentCase, ...resFile}
          if (evRep) this.addReport()
          else this.formPage = 3
        }).catch(error => {
          console.log(error)
          if (evRep) this.addReport()
          else this.formPage = 3
        }).finally(() => this.file = null);
      } else if (evRep) this.addReport()
      else this.formPage = 3
      this.sortCases()
    }).catch(error => {
      console.log(error)
      this.formPage = 0
    }); 
  }

  update(values, evRep) {
    let saveArr = []
    for (let field in values) {
      if (['monitoring_element_refs', 'organization_activity_refs', 'target_refs'].includes(field)) {
        if (this.currentCase[field].length != values[field].length) saveArr.push(field)
        else for (let item of this.currentCase[field]) {
          if (!values[field].includes(+item.id)) {
            saveArr.push(field); 
            break
          }
        }
      } 
      else if (['practice_ref', 'thematic_group_ref'].includes(field)) {
        if (+this.currentCase[field].id != +values[field]) saveArr.push(field)
      } 
      else if (this.currentCase[field] != values[field]) saveArr.push(field)
    }
    
    for (let field in values) 
      if (!saveArr.includes(field)) values[field]=null

    this.transport.post("case-change-requests/"+ this.currentCase.id + '/upload_data/', values).then((res) => {
      if (res.message == 'edit') {
        this.currentCase = {...this.currentCase, ...res.result} 

        let index = this.allCases.indexOf(this.allCases.find(el => el.id == this.currentCase.id))
        if (index) this.allCases[index] = this.currentCase
        if (this.file) {
          let fd = new FormData()
          fd.append('case_file', this.file, this.file.name)
          this.transport.patch("cases/", String(this.currentCase.id), fd).then((resFile) => {
            this.file = null
            this.currentCase = {...this.currentCase, ...resFile}
            let index = this.allCases.indexOf(this.allCases.find(el => el.id == this.currentCase.id))
            if (index) this.allCases[index] = this.currentCase
          }).catch(error => {
            this.file = null
            console.log(error)
            alert("Инсрумент сохранён, ошибка при загрузке файла")
          });
        }
        if (evRep) this.addReport()
        else this.formPage = 3

      } else if (res.message == 'request') {
        if (!this.file) alert("Запрос на редактирование успешно отправлен")
        else if (this.file) {
          let fd = new FormData()
          fd.append('tool_file', this.file, this.file.name)
          this.transport.patch("case-change-requests/", String(this.currentCase.id), fd).then((resFile) => {
            this.file = null
            alert("Запрос на редактирование успешно отправлен")
          }).catch(error => {
            this.file = null
            console.log(error)
            alert("Запрос на редактирование успешно отправлен, ошибка при загрузке файла")
          });
        }
        if (evRep) this.addReport()
        else this.formPage = 3
      } 
    }).catch(error => {
      console.log(error)
      alert("Произошла неизвестная ошибка")
      this.closeForm()
    });   
  }
  openReport(id) {
    this.router.navigate(['/report', id], {queryParams: {case: this.currentCase.id}})
  }

  addReport() {
    const mFormControls = () => {
      let arr: FormControl[] = []
      for (let m of this.methods) arr.push(new FormControl(false))
      return arr
    }
    const rmFormControls = () => {
      let arr: FormControl[] = []
      for (let m of this.representationMethods) arr.push(new FormControl(false))
      return arr
    }
    const amFormControls = () => {
      let arr: FormControl[] = []
      for (let m of this.analysisMethods) arr.push(new FormControl(false))
      return arr
    }
    const oFormControls = () => {
      let arr: FormControl[] = []
      for (let o of this.outcomes) arr.push(new FormControl(false))
      return arr
    }
    this.addReportForm = new FormGroup({
      type: new FormControl('', Validators.required), //
      key_questions: new FormControl('', Validators.required), //
      other_results: new FormControl('', Validators.required), //
      evaluation_type_ref: new FormControl('', Validators.required),//
      method_refs: new FormArray(mFormControls()),
      representation_method_refs: new FormArray(rmFormControls()),
      analysis_method_refs: new FormArray(amFormControls()),
      outcome_refs: new FormArray(oFormControls()),
      other_analysis_method: new FormControl(''), //
      other_evaluation_type: new FormControl(''), //
      other_representation_method: new FormControl(''), //
      other_method: new FormControl('')
    })
    this.formPage = 2
  }
  async methodsSubmit(next: boolean, event) {
    event.preventDefault()
    let newMethod = null
    let newAnMethod = null
    let newRepMethod = null
    let newEvType = null
    let other_method = this.addReportForm.value.other_method
    let other_representation_method = this.addReportForm.value.other_representation_method
    let other_analysis_method = this.addReportForm.value.other_analysis_method
    let other_evaluation_type = this.addReportForm.value.other_evaluation_type
    try {
      if (other_method) {
        newMethod = await this.transport.post("methods/", {
          name: other_method,
          parent_ref: +this.newParentRef
        })
      }
      if (other_analysis_method) {
        newAnMethod = await this.transport.post("analysis-methods/", {
          name: other_analysis_method
        })
      }
      if (other_representation_method) {
        newRepMethod  = await this.transport.post("representation-methods/", {
          name: other_representation_method
        })
      }
      if (other_evaluation_type) {
        newEvType  = await this.transport.post("evaluation-types/", {
          name: other_evaluation_type
        })
      }
    } catch (e) {
      console.log(e)
    }
    
    this.reportSubmit(next, newMethod, newAnMethod, newRepMethod, newEvType)
  }
  reportSubmit(next?: boolean, newMethod?, newAnMethod?, newRepMethod?, newEvType?) {
    const data = this.addReportForm.value
    const boolToObjM = () => {
      let resNum: any[] = []
      let valArr = this.addReportForm.value.method_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i] && !this.methods[i].parent_ref) resNum.push(+this.methods[i].id)
        else if (valArr[i] && this.methods[i].parent_ref) {
          const parent_index = this.methods.indexOf(this.methods.find(item => item.id == this.methods[i].parent_ref))
          if (valArr[parent_index]) resNum.push(+this.methods[i].id)
        }
      }
      if (newMethod) resNum.push(+newMethod.id)
      return resNum
    }
    const boolToObjAM = () => {
      let resNum: any[] = []
      let valArr = this.addReportForm.value.analysis_method_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.analysisMethods[i].id)
      }
      if (newAnMethod) resNum.push(+newAnMethod.id)
      return resNum
    }
    const boolToObjRM = () => {
      let resNum: any[] = []
      let valArr = this.addReportForm.value.representation_method_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(+this.representationMethods[i].id)
      }
      if (newRepMethod) resNum.push( +newRepMethod.id)
      return resNum
    }
    const boolToObjO = () => {
      let resNum: any[] = []
      let valArr = this.addReportForm.value.outcome_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.outcomes[i].id)
      }
      return resNum
    }
    data.evaluation_type_ref = newEvType ? +newEvType.id : +this.addReportForm.value.evaluation_type_ref
    data.outcome_refs = boolToObjO()
    data.representation_method_refs = boolToObjRM()
    data.method_refs = boolToObjM()
    data.analysis_method_refs = boolToObjAM()
    data.case_ref = this.currentCase.id
    if (this.currentCase.add_public_confirm) {
      data.add_public_confirm = false
      data.add_public_will = true
    } else {
      data.add_public_confirm = true
      data.add_public_will = false
    }

    this.transport.post("evaluation-reports/", data).then(report => {
      let fd = new FormData()
      this.evaluationReports.push(report)
      if (this.repFile) fd.append('evaluation_file', this.repFile, this.repFile.name)
      this.transport.patch("evaluation-reports/", String(report.id), fd)
        .then(file => {
          report = {...report, ...file}
          if (this.currentCase.add_public_confirm) {
            this.transport.post("evaluation-reports/" + report.id + "/add_public_confirm/", {}).then(
              (result) => {
                alert("Запрос на добавление отчёта об оценке успешно отправлен")
                if (next) this.addReport()
                else this.formPage = 0
              }).catch(err => {
                this.formPage = 0
              }) 
          } else {
            if (next) this.addReport()
            else this.formPage = 3
          }
        })
        .catch(error => {
          this.formPage = 0
          console.log(error)
        })
        .finally(() => this.repFile = null)
      })
  }
  
  caseFileUpload(event) {
    this.file = event.target.files[0]
  }
  repFileUpload(event) {
    this.repFile = event.target.files[0]
  }
  triggerRepFile() {
    this.file_rep.nativeElement.click()
  }
  triggerFile() {
    this.file_input.nativeElement.click()
  }
  onVerifiedChange(){
    this.verified = !this.verified;
    this.reviewCases()
  }
  onMyVerifiedChange() {
    this.myVerified = !this.myVerified;
    this.reviewMyCases()
  }

  onCheckChange(checkList, event) {
    event.preventDefault()
    const formArray: FormArray = this.filterForm.get(checkList) as FormArray;

    if (event.target.checked) {
      formArray.push(new FormControl(event.target.value));

      if (checkList == 'targetFilters') {
        const index = this.targets.indexOf(this.targets.find(item => item.id == event.target.value))
        if (!this.targets[index].parent_ref) this.targets[index].checked = true                       //добавляем, нет родителя
        else {
          const parent = this.targets.find(item => item.id == this.targets[index].parent_ref)           //добавляем, есть родитель
          let parent_index 
          formArray.controls.forEach((ctrl: FormControl, i: number) => { 
            if (ctrl.value == String(parent.id)) parent_index = i
          })
          if (typeof parent_index == 'number') formArray.removeAt(parent_index);
        }
      } 
    }
    /* unselected */
    else{
      // find the unselected element
      formArray.controls.forEach((ctrl: FormControl, i: number) => {
        if (ctrl.value == event.target.value) {
          formArray.removeAt(i);
          return;
        }  
      });
      if (checkList == 'targetFilters') {
        const index = this.targets.indexOf(this.targets.find(item => item.id == event.target.value))
        if (!this.targets[index].parent_ref) {                        //удаляем, нет родителя
          this.targets[index].checked = false
          let children = this.targets.filter(item => item.parent_ref == event.target.value)
          let indexes = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => ctrl.value == child.id)) indexes.push(i)
          })
          for (let i = indexes.length - 1; i >= 0; i--) formArray.removeAt(indexes[i]);
        } else {                                                          //удаляем, родитель есть
          let children = this.targets.filter(item => item.parent_ref == this.targets[index].parent_ref)
          let siblings = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => child.id == ctrl.value)) siblings.push(i)
          });
          if (!siblings.length) formArray.push(new FormControl(String(this.targets[index].parent_ref)));
        }
      }
    }
    this.reviewCases();
  }
  onMyCheckChange(checkList, event) {
    event.preventDefault()
    const formArray: FormArray = this.myFilterForm.get(checkList) as FormArray;

    if (event.target.checked){
      // Add a new control in the arrayForm
      formArray.push(new FormControl(event.target.value));
      if (checkList == 'targetFilters') {
        const index = this.targets.indexOf(this.targets.find(item => item.id == event.target.value))
        if (!this.targets[index].parent_ref) this.targets[index].checkedMy = true                       //добавляем, нет родителя
        else {
          const parent = this.targets.find(item => item.id == this.targets[index].parent_ref)           //добавляем, есть родитель
          let parent_index 
          formArray.controls.forEach((ctrl: FormControl, i: number) => { 
            if (ctrl.value == String(parent.id)) parent_index = i
          })
          if (typeof parent_index == 'number') formArray.removeAt(parent_index);
        }
      }
    }
    else{
      formArray.controls.forEach((ctrl: FormControl, i: number) => {
        if (ctrl.value == event.target.value) {
          formArray.removeAt(i);
          return;
        }  
      });
      if (checkList == 'targetFilters') {
        const index = this.targets.indexOf(this.targets.find(item => item.id == event.target.value))
        if (!this.targets[index].parent_ref) {                        //удаляем, нет родителя
          this.targets[index].checkedMy = false
          let children = this.targets.filter(item => item.parent_ref == event.target.value)
          let indexes = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => ctrl.value == child.id)) indexes.push(i)
          })
          for (let i = indexes.length - 1; i >= 0; i--) formArray.removeAt(indexes[i]);
        } else {                                                          //удаляем, родитель есть
          let children = this.targets.filter(item => item.parent_ref == this.targets[index].parent_ref)
          let siblings = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => child.id == ctrl.value)) siblings.push(i)
          });
          if (!siblings.length) formArray.push(new FormControl(String(this.targets[index].parent_ref)));
        }
      } 
    }
    this.reviewMyCases();
  }
  reviewCases() {
    const targetFiltersArray: FormArray = this.filterForm.get('targetFilters') as FormArray;
    const practiceFiltersArray: FormArray = this.filterForm.get('practiceFilters') as FormArray;
    const oaFiltersArray: FormArray = this.filterForm.get('oaFilters') as FormArray;
    const tgFiltersArray: FormArray = this.filterForm.get('tgFilters') as FormArray;
    const meFiltersArray: FormArray = this.filterForm.get('meFilters') as FormArray;

    this.cases = this.allCases;

    if (targetFiltersArray.value.length > 0)
        this.cases = this.cases.filter((el:Case) => {
          return el.target_refs.some((trg:Target) => {return targetFiltersArray.value.includes(String(trg.id))});
        });
    if (oaFiltersArray.value.length > 0)
        this.cases = this.cases.filter((el:Case) => {
          return el.organization_activity_refs.some((el:OrganizationActivity) => {return oaFiltersArray.value.includes(String(el.id))});
        });
    if (meFiltersArray.value.length > 0)
        this.cases = this.cases.filter((el:Case) => {
          return el.monitoring_element_refs.some((el:MonitoringElement) => {return meFiltersArray.value.includes(String(el.id))});
        });
    if (practiceFiltersArray.value.length > 0)
        this.cases = this.cases.filter((el:Case) => {
          return el.practice_ref && practiceFiltersArray.value.includes(String(el.practice_ref.id))
        });
    if (tgFiltersArray.value.length > 0)
        this.cases = this.cases.filter((el:Case) => {
          return el.thematic_group_ref && tgFiltersArray.value.includes(String(el.thematic_group_ref.id))
        });
    if (this.verified)
        this.cases = this.cases.filter((el:Case) => {
          return !!el.verification_info;
        });  
  }
  reviewMyCases() {
    const targetFiltersArray: FormArray = this.myFilterForm.get('targetFilters') as FormArray;
    const practiceFiltersArray: FormArray = this.myFilterForm.get('practiceFilters') as FormArray;
    const oaFiltersArray: FormArray = this.myFilterForm.get('oaFilters') as FormArray;
    const tgFiltersArray: FormArray = this.myFilterForm.get('tgFilters') as FormArray;
    const meFiltersArray: FormArray = this.myFilterForm.get('meFilters') as FormArray;

    this.myCases = this.allMyCases;

    if (targetFiltersArray.value.length > 0)
        this.myCases = this.myCases.filter((el:Case) => {
          return el.target_refs.some((trg:Target) => {return targetFiltersArray.value.includes(String(trg.id))});
        });
    if (oaFiltersArray.value.length > 0)
        this.myCases = this.myCases.filter((el:Case) => {
          return el.organization_activity_refs.some((el:OrganizationActivity) => {return oaFiltersArray.value.includes(String(el.id))});
        });
    if (meFiltersArray.value.length > 0)
        this.myCases = this.myCases.filter((el:Case) => {
          return el.monitoring_element_refs.some((el:MonitoringElement) => {return meFiltersArray.value.includes(String(el.id))});
        });
    if (practiceFiltersArray.value.length > 0)
        this.myCases = this.myCases.filter((el:Case) => {
          return el.practice_ref && practiceFiltersArray.value.includes(String(el.practice_ref.id))
        });
    if (tgFiltersArray.value.length > 0)
        this.myCases = this.myCases.filter((el:Case) => {
          return el.thematic_group_ref && tgFiltersArray.value.includes(String(el.thematic_group_ref.id))
        });

    if (this.myVerified)
      this.myCases = this.myCases.filter((el:Case) => {
        return !!el.verification_info;
      });
  }
  myCounter(filterName: string, filterValue) {
    if (filterName == "target") {
      return this.myCases.filter((el:Case) => {
        return el.target_refs.some((trg:Target) => {return trg.id == filterValue.id});
      }).length;
    } else if (filterName == "practice") {
      return this.myCases.filter((el:Case) => {
        return el.practice_ref && filterValue.id == el.practice_ref.id
      }).length;
    }else if (filterName == "thematic_group") {
      return this.myCases.filter((el:Case) => {
        return el.thematic_group_ref && filterValue.id == el.thematic_group_ref.id
      }).length;
    }else if (filterName == "monitoring_element") {
      return this.myCases.filter((el:Case) => {
        return el.monitoring_element_refs.some((el:MonitoringElement) => {return el.id == filterValue.id})
      }).length;
    }else if (filterName == "organization_activity") {
      return this.myCases.filter((el:Case) => {
        return el.organization_activity_refs.some((el:OrganizationActivity) => {return el.id == filterValue.id});
      }).length;
    }
  }
  counter(filterName: string, filterValue) {
    if (filterName == "target") {
      return this.cases.filter((el:Case) => {
        return el.target_refs.some((trg:Target) => {return trg.id == filterValue.id});
      }).length;
    } else if (filterName == "practice") {
      return this.cases.filter((el:Case) => {
        return el.practice_ref && filterValue.id == el.practice_ref.id
      }).length;
    } else if (filterName == "thematic_group") {
      return this.cases.filter((el:Case) => {
        return el.thematic_group_ref && filterValue.id ==el.thematic_group_ref.id
      }).length;
    } else if (filterName == "monitoring_element") {
      return this.cases.filter((el:Case) => {
        return el.monitoring_element_refs.some((el:MonitoringElement) => {return el.id == filterValue.id});
      }).length;
    }else if (filterName == "organization_activity") {
      return this.cases.filter((el:Case) => {
        return el.organization_activity_refs.some((el:OrganizationActivity) => {return el.id == filterValue.id});
      }).length;
    }
  }
  changeMyRoot() {
    if (!this.myFilterRoot.value.target) {
      for (let i = 0; i < this.targets.length; i++) this.targets[i].checkedMy = false
      const formArray: FormArray = this.myFilterForm.get('targetFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.practice) {
      const formArray: FormArray = this.myFilterForm.get('practiceFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.tg) {
      const formArray: FormArray = this.myFilterForm.get('tgFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.me) {
      const formArray: FormArray = this.myFilterForm.get('meFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.oa) {
      const formArray: FormArray = this.myFilterForm.get('oaFilters') as FormArray;
      formArray.clear()
    }
    this.reviewMyCases()
  }
  changeRoot() {
    if (!this.filterRoot.value.target) {
      for (let i = 0; i < this.targets.length; i++) this.targets[i].checked = false
      const formArray: FormArray = this.filterForm.get('targetFilters') as FormArray;
      let i: number = 0;
      formArray.controls.forEach((ctrl: FormControl) => {
        formArray.removeAt(i);
        i++;
      });
    }
    if (!this.filterRoot.value.tg) {
      const formArray: FormArray = this.filterForm.get('tgFilters') as FormArray;
      let i: number = 0;
      formArray.controls.forEach((ctrl: FormControl) => {
        formArray.removeAt(i);
        i++;
      });
    }
    if (!this.filterRoot.value.me) {
      const formArray: FormArray = this.filterForm.get('meFilters') as FormArray;
      let i: number = 0;
      formArray.controls.forEach((ctrl: FormControl) => {
        formArray.removeAt(i);
        i++;
      });
    }
    if (!this.filterRoot.value.practice) {
      const formArray: FormArray = this.filterForm.get('practiceFilters') as FormArray;
      let i: number = 0;
      formArray.controls.forEach((ctrl: FormControl) => {
        formArray.removeAt(i);
        i++;
      });
    }
    if (!this.filterRoot.value.oa) {
      const formArray: FormArray = this.filterForm.get('oaFilters') as FormArray;
      let i: number = 0;
      formArray.controls.forEach((ctrl: FormControl) => {
        formArray.removeAt(i);
        i++;
      });
    }
    this.reviewCases()
  }
  findTarget(target) {
    return !!this.currentCase.target_refs.find(el => el.id == target.id)
  }
  findReports() {
    try {
      return this.evaluationReports.filter(el => el.case_ref.id == this.currentCase.id)
    } catch (e) {
      return []
    }
  }
}
