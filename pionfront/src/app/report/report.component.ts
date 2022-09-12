import { Component, OnInit, ViewChild } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AnalysisMethod } from '../models/analysismethod';
import { EvaluationReport } from '../models/evaluationreport';
import { EvaluationType } from '../models/evaluationtype';
import { Method } from '../models/method';
import { Outcome } from '../models/outcome';
import { RepresentationMethod } from '../models/representationmethod';
import { TransportService } from '../services/transport.service';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent implements OnInit {

  id: string;
  case: string
  report: EvaluationReport
  authenticated: boolean = false;
  toLoad = 5
  evaluationTypes: EvaluationType[]
  methods: Method[]
  analysisMethods: AnalysisMethod[]
  representationMethods: RepresentationMethod[]
  editReportForm: FormGroup
  outcomes: Outcome[]
  formPage = 0

  otherRepMethod: boolean
  otherAnMethod: boolean
  otherMethod: boolean
  otherEvType: boolean
  newParentRef: number
  repFile: File

  @ViewChild('file_rep') file_rep

  constructor(private activateRoute: ActivatedRoute,
    public transport: TransportService,
    public router: Router) {
    this.id = this.activateRoute.snapshot.params['id'];
    this.activateRoute.queryParams.subscribe(
      params => this.case = params['case'])
  }

  ngOnInit(): void {
    if (this.transport.accessToken != null && this.transport.accessToken != undefined && this.transport.refreshToken != null && this.transport.refreshToken != undefined)
      this.authenticated = true;
    if (!this.id) this.router.navigate(['cases']) 

    this.transport.get("outcomes/", !this.authenticated).then((data) => {
      this.outcomes = data.results;    
    })

    this.transport.get("evaluation-reports/"+this.id+'/', !this.authenticated).then(report => {
      this.report = report
      this.toLoad -= 1

      this.load()
    }).catch(e => {
      console.log(e)
      this.router.navigate(['/cases']) 
    })
  }

  load() {
    this.transport.get("analysis-methods/", !this.authenticated).then((data) => {
      this.analysisMethods = data.results;
      for (let am of this.report.analysis_method_refs) {
        if (!this.analysisMethods.find(el => am.id == el.id)) this.analysisMethods.push(am)
      }
      for (var element in this.analysisMethods) {
        this.analysisMethods[element].current = this.report.analysis_method_refs.some(el => el.id == this.analysisMethods[element].id);
      }   
      this.toLoad -= 1
    })

    this.transport.get("evaluation-types/", !this.authenticated).then((data) => {
      this.evaluationTypes = data.results; 

      let index = this.evaluationTypes.indexOf(this.evaluationTypes.find(el => this.report.evaluation_type_ref.id == el.id))
      if (index > -1) this.evaluationTypes[index].current = true
      else {
        this.report.evaluation_type_ref.current = true
        this.evaluationTypes.push(this.report.evaluation_type_ref)
      }  
      this.toLoad -= 1
    })

    this.transport.get("representation-methods/", !this.authenticated).then((data) => {
      this.representationMethods= data.results;  
      for (let re of this.report.representation_method_refs) {
        if (!this.representationMethods.find(el => re.id == el.id)) this.representationMethods.push(re)
      }  
      for (var element in this.representationMethods) {
        this.representationMethods[element].current = this.report.representation_method_refs.some(el => el.id == this.representationMethods[element].id);
      }   
      this.toLoad -= 1
    })

    this.transport.get("methods/", !this.authenticated).then((data) => {
      this.methods = data.results;
      for (let method of this.methods) {
        if (typeof method.parent_ref == 'string') {
          let data = method.parent_ref.split('/')
          method.parent_ref = +data[data.length - 2]
        }
      }
      for (let m of this.report.method_refs) {
        if (!this.methods.find(el => m.id == el.id)) this.methods.push(m)
      }
      for (var element in this.methods) {
        this.methods[element].checked = this.report.method_refs.some(el => el.id == this.methods[element].id);
      }         
      this.toLoad -= 1
    })
  }

  goBack(event) {
    event.preventDefault();
    this.router.navigate(["/cases"], {queryParams: {id: this.case ? this.case : this.report.case_ref.id}});
  }

  downloadFile() {
    let link = document.createElement("a");
    link.download = "filename";
    link.href = this.report.evaluation_file;
    link.click();
    link.remove();
  }

  editReport(event) {
    event.preventDefault()

    const mFormControls = () => {
      let arr: FormControl[] = []
      for (let m of this.methods) arr.push(new FormControl(this.report.method_refs.find(el => +el.id == +m.id) ? true : false))
      return arr
    }

    const rmFormControls = () => {
      let arr: FormControl[] = []
      for (let rm of this.representationMethods) arr.push(new FormControl(this.report.representation_method_refs.find(el => +el.id == +rm.id) ? true : false))
      return arr
    }

    const amFormControls = () => {
      let arr: FormControl[] = []
      for (let am of this.analysisMethods) arr.push(new FormControl(this.report.analysis_method_refs.find(el => +el.id == +am.id) ? true : false))
      return arr
    }
    const oFormControls = () => {
      let arr: FormControl[] = []
      for (let o of this.outcomes) arr.push(new FormControl(this.report.outcome_refs.find(el => +el.id == +o.id) ? true : false))
      return arr
    }
    this.editReportForm = new FormGroup({
      type: new FormControl(this.report.type, Validators.required), //
      key_questions: new FormControl(this.report.key_questions, Validators.required), //
      other_results: new FormControl(this.report.other_results, Validators.required), //
      evaluation_type_ref: new FormControl(this.report.evaluation_type_ref.id, Validators.required),//
      method_refs: new FormArray(mFormControls()),
      representation_method_refs: new FormArray(rmFormControls()),
      analysis_method_refs: new FormArray(amFormControls()),
      outcome_refs: new FormArray(oFormControls()),
      other_analysis_method: new FormControl(''), //
      other_evaluation_type: new FormControl(''), //
      other_representation_method: new FormControl(''), //
      other_method: new FormControl('')
    })
    this.formPage = 1
  }

  changeMethod() {
    let valArr = this.editReportForm.value.method_refs
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
    this.editReportForm.patchValue({other_method: ''})
  }
  changeRepMethod() {
    let valArr = this.editReportForm.value.representation_method_refs
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
    this.editReportForm.patchValue({other_representation_method: ''})
  }
  changeAnMethod() {
    let valArr = this.editReportForm.value.analysis_method_refs
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
    this.editReportForm.patchValue({other_analysis_method: ''})
  }
  changeEvType() {
    let id = this.editReportForm.value.evaluation_type_ref
    let name = this.evaluationTypes.find(el => el.id == id).name
    if (name.trim().toLocaleLowerCase() == "другое") {
      this.otherEvType = true
      return
    }
    this.otherEvType = false
    this.editReportForm.patchValue({other_evaluation_type: ''})
  }
  closeForm() {
    this.formPage = 0
  }

  async methodsSubmit(event) {
    event.preventDefault()
    let newMethod = null
    let newAnMethod = null
    let newRepMethod = null
    let newEvType = null
    let other_method = this.editReportForm.value.other_method
    let other_representation_method = this.editReportForm.value.other_representation_method
    let other_analysis_method = this.editReportForm.value.other_analysis_method
    let other_evaluation_type = this.editReportForm.value.other_evaluation_type
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
    this.onSubmit(newMethod, newAnMethod, newRepMethod, newEvType)
  }

  onSubmit(newMethod, newAnMethod, newRepMethod, newEvType) {
    const data = {...this.editReportForm.value}
    const boolToObjM = () => {
      let resNum: any[] = []
      let valArr = this.editReportForm.value.method_refs
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
      let valArr = this.editReportForm.value.analysis_method_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.analysisMethods[i].id)
      }
      if (newAnMethod) resNum.push(+newAnMethod.id)
      return resNum
    }
    const boolToObjRM = () => {
      let resNum: any[] = []
      let valArr = this.editReportForm.value.representation_method_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(+this.representationMethods[i].id)
      }
      if (newRepMethod) resNum.push( +newRepMethod.id)
      return resNum
    }
    const boolToObjO = () => {
      let resNum: any[] = []
      let valArr = this.editReportForm.value.outcome_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.outcomes[i].id)
      }
      return resNum
    }
    data.evaluation_type_ref = newEvType ? +newEvType.id : +this.editReportForm.value.evaluation_type_ref
    data.outcome_refs = boolToObjO()
    data.representation_method_refs = boolToObjRM()
    data.method_refs = boolToObjM()
    data.analysis_method_refs = boolToObjAM()
    data.case_ref = this.report.case_ref.id
    if (this.report.case_ref.add_public_confirm) {
      data.add_public_confirm = false
      data.add_public_will = true
      this.request(data)
    } else {
      data.add_public_confirm = true
      data.add_public_will = false
      this.udpate(data)
    }
  }
  udpate(data) {
    this.transport.put("evaluation-reports/", String(this.report.id), data).then(report => {
      let fd = new FormData()
      this.report = report
      if (this.repFile) fd.append('evaluation_file', this.repFile, this.repFile.name)
      this.transport.patch("evaluation-reports/", String(report.id), fd)
        .then(file => {
          this.report = {...report, ...file}
          this.formPage = 0
          this.toLoad += 4
          this.load()
        })
        .catch(error => {
          this.formPage = 0
          console.log(error)
        })
        .finally(() => this.repFile = null)
    })
  }

  request(values) {
    let saveArr = []
    for (let field in values) {
      if (['method_refs', 'representation_method_refs', 'analysis_method_refs', 'outcome_refs'].includes(field)) {
        if (this.report[field].length != values[field].length) saveArr.push(field)
        else for (let item of this.report[field]) {
          if (!values[field].includes(+item.id)) {
            saveArr.push(field); 
            break
          }
        }
      }
      else if (['evaluation_type_ref'].includes(field)) {
        if (+this.report[field].id != +values[field]) saveArr.push(field)
      } 
      else if (this.report[field] != values[field]) saveArr.push(field)
    }
    
    for (let field in values) 
      if (!saveArr.includes(field)) values[field]= ['method_refs', 'representation_method_refs', 'analysis_method_refs', 'outcome_refs'].includes(field) ? [] : null

    values.evalution_report_ref = this.report.id
    this.transport.put("evaluation-report-change-requests/", String(this.report.id), values).then(report => {
      let fd = new FormData()
      if (this.repFile) fd.append('evaluation_file', this.repFile, this.repFile.name)
      this.transport.patch("evaluation-report-change-requests/", String(this.report.id), fd)
        .then(file => {
          this.transport.post("evaluation-report-change-requests/" + this.report.id + "/add_public_confirm/", {}).then(
            (result) => {
              alert("Запрос на добавление отчёта об оценке успешно отправлен")
            }).catch(err => {
              console.log(err)
            }).finally(() => this.formPage = 0)
        })
        .catch(error => {
          this.formPage = 0
          console.log(error)
        })
        .finally(() => this.repFile = null)
    })
  }

  triggerRepFile() {
    this.file_rep.nativeElement.click()
  }
  repFileUpload(event) {
    this.repFile = event.target.files[0]
  }
}
