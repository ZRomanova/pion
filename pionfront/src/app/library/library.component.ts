import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { DatePipe, formatDate  } from '@angular/common';
import { Target } from '../models/target';
import { Practice } from '../models/practice';
import { Outcome } from '../models/outcome';
import { TransportService } from '../services/transport.service';
import { ActivatedRoute, Router } from '@angular/router';
import { LogicalModel } from '../models/logicalModel';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Program } from '../models/program';
import { ThematicGroup } from '../models/thematicgroup';

@Component({
  selector: 'app-library',
  templateUrl: './library.component.html',
  styleUrls: ['./library.component.scss']
})
export class LibraryComponent implements OnInit {

  constructor(public fb: FormBuilder,
    private datePipe: DatePipe, 
    public transport: TransportService,
    private activateRoute: ActivatedRoute,
    public router: Router) { }

    public filterForm = this.fb.group({
      // email: [''],
      targetFilters: new FormArray([]),
      practiceFilters: new FormArray([]),
      outcomeFilters: new FormArray([]),
      tgFilters: new FormArray([])
    });

    public myFilterForm = this.fb.group({
      // email: [''],
      targetFilters: new FormArray([]),
      practiceFilters: new FormArray([]),
      outcomeFilters: new FormArray([]),
      tgFilters: new FormArray([])
    });

    public filterRoot = this.fb.group({
      target: new FormControl(false),
      practice: new FormControl(false),
      tg: new FormControl(false),
      outcome: new FormControl(false),
    });
  
    public myFilterRoot = this.fb.group({
      target: new FormControl(false),
      practice: new FormControl(false),
      outcome: new FormControl(false),
      tg: new FormControl(false),
    });
  @ViewChild('model') modelFileRef: ElementRef
  @ViewChild('result_tree') resultTreeFileRef: ElementRef

  status: string = "ЗАГРУЗКА..."
  displayMyLibrary: boolean = false;
  toLoad: number = 5;
  targets: Target[];
  practices: Practice[];
  outcomes: Outcome[];
  logicalModels: LogicalModel[];
  allLogicalModels: LogicalModel[];
  myLogicalModels: LogicalModel[];
  allMyLogicalModels: LogicalModel[];
  thematicGroups: ThematicGroup[]
  displayDetails: boolean = false;
  displayAddPersonal: boolean = false;
  currentModel: LogicalModel;
  displayRemovePersonal: boolean = false;

  myVerified: boolean = false;
  verified: boolean = false;

  authenticated: boolean = false;

  formSelectProgram: FormGroup
  formEditModel: FormGroup
  formPage: number = 0
  programs: Program[]
  selectProgram: Program

  model_file: File
  result_tree_file: File

  ngOnInit(): void {
    if (this.transport.accessToken != null && this.transport.accessToken != undefined && this.transport.refreshToken != null && this.transport.refreshToken != undefined)
      this.authenticated = true;

    this.activateRoute.queryParamMap.subscribe(queryParams => {
      let id = queryParams.get('id');
      if (id) this.transport.get("logical-models/"+id+"/").then(model => {
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

    this.transport.get("outcomes/", !this.authenticated).then((outcomesData) => {
      this.outcomes = outcomesData.results;
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
    
    this.transport.get("logical-models/", !this.authenticated).then((logicalModels) => {
      this.logicalModels = logicalModels.results;
      this.allLogicalModels = logicalModels.results;     
      this.sortModels()
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

  }

  sortModels() {
    this.allMyLogicalModels = [];
    for (var logicalModel in this.allLogicalModels) {
      if (this.allLogicalModels[logicalModel].current_user_library)
        this.allMyLogicalModels.push(this.allLogicalModels[logicalModel]);
    }
    this.myLogicalModels = this.allMyLogicalModels;  
  }

  addForm(event) {
    event.preventDefault()
    this.formSelectProgram = new FormGroup({
      program: new FormControl('start')
    })
    this.transport.get("programs/").then((programsData) => {
      this.programs = programsData.results
      this.formPage = 1
    })
  }

  editForm(event) {
    event.preventDefault()
    this.selectProgram = this.programs.find(p => p.id == this.formSelectProgram.value.program)
    console.log(this.selectProgram)
    const target_refs = Array.from(this.selectProgram.target_refs, x => x.id)
    const practice_refs = Array.from(this.selectProgram.practice_refs, x => x.id)

    const tFormControls = () => {
      let arr = []
      for (let i = 0; i < this.targets.length; i++) {
        arr.push(new FormControl(target_refs.includes(this.targets[i].id) ? true : false))
      }
      return arr
    }

    const pFormControls = () => {
      let arr = []
      for (let i = 0; i < this.practices.length; i++) {
        arr.push(new FormControl(practice_refs.includes(this.practices[i].id) ? true : false))
      }
      return arr
    }

    const oFormControls = () => {
      let arr = []
      for (let i = 0; i < this.outcomes.length; i++) {
        arr.push(new FormControl(false))
      }
      return arr
    }

    this.formEditModel = new FormGroup({
      name: new FormControl(this.selectProgram.name, Validators.required),
      period: new FormControl(this.selectProgram.period, Validators.required),
      thematic_group_ref: new FormControl('', Validators.required),
      organization: new FormControl('', Validators.required),
      target_refs: new FormArray(tFormControls()),
      practice_refs: new FormArray(pFormControls()),
      outcome_refs: new FormArray(oFormControls()),
      verification_info: new FormControl(''),
      verification_level_regularity: new FormControl(''),
      verification_level_validity: new FormControl(''),
      verification_level_outcome_accessibility: new FormControl(''),
      verification_level_outcome_validity: new FormControl(''),
      isNew: new FormControl(true)
    })
    this.formPage = 2 
  }

  editFormFromLibrary(event) {
    event.preventDefault()

    const tFormControls = () => {
      let arr: FormControl[] = []
      for (let target of this.targets) arr.push(new FormControl(this.currentModel.target_refs.find(el => +el.id == +target.id) ? true : false))
      return arr
    }
    const pFormControls = () => {
      let arr: FormControl[] = []
      for (let tag of this.practices) arr.push(new FormControl(this.currentModel.practice_refs.find(el => +el.id == +tag.id) ? true : false))
      return arr
    }

    const oFormControls = () => {
      let arr: FormControl[] = []
      for (let tag of this.outcomes) arr.push(new FormControl(this.currentModel.outcome_refs.find(el => +el.id == +tag.id) ? true : false))
      return arr
    }

    this.formEditModel = new FormGroup({
      name: new FormControl(this.currentModel.name, Validators.required),
      period: new FormControl(this.currentModel.period, Validators.required),
      thematic_group_ref: new FormControl(this.currentModel.thematic_group_ref.id, Validators.required),
      organization: new FormControl(this.currentModel.organization, Validators.required),
      target_refs: new FormArray(tFormControls()),
      practice_refs: new FormArray(pFormControls()),
      outcome_refs: new FormArray(oFormControls()),
      verification_info: new FormControl(this.currentModel.verification_info),
      verification_level_regularity: new FormControl(this.currentModel.verification_level_regularity),
      verification_level_validity: new FormControl(this.currentModel.verification_level_validity),
      verification_level_outcome_accessibility: new FormControl(this.currentModel.verification_level_outcome_accessibility),
      verification_level_outcome_validity: new FormControl(this.currentModel.verification_level_outcome_validity),
      isNew: new FormControl(false)
    })

    this.closeAddPersonal()
    this.formPage = 2
  }

  editProgramFormSubmit(event) {
    event.preventDefault()
    this.formEditModel.disable()

    const boolToObjP = () =>{
      let resNum: any[] = []
      let valArr = this.formEditModel.value.practice_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.practices[i].id)
      }
      return resNum
    }

    const boolToObjT = () => {
      let resNum: any[] = []
      let valArr = this.formEditModel.value.target_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i] && !this.targets[i].parent_ref) resNum.push(+this.targets[i].id)
        else if (valArr[i] && this.targets[i].parent_ref) {
          const parent_index = this.targets.indexOf(this.targets.find(item => item.id == this.targets[i].parent_ref))
          if (valArr[parent_index]) resNum.push(+this.targets[i].id)
        }
      }
      return resNum
    }
    const boolToObjO = () => {
      let resNum: any[] = []
      let valArr = this.formEditModel.value.outcome_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.outcomes[i].id)
      }
      return resNum
    }

    const form = {...this.formEditModel.value}
    form.target_refs = boolToObjT()
    form.practice_refs = boolToObjP()
    form.thematic_group_ref = +this.formEditModel.value.thematic_group_ref
    form.outcome_refs = boolToObjO()
    delete form.isNew

    if (!this.formEditModel.value.isNew) this.update(form)
    else if (this.formEditModel.value.isNew) this.post(form)
  }

  post(form) {
    this.transport.post("logical-models/", form).then((res: LogicalModel) => {
      this.allLogicalModels.push(res)
      this.currentModel = res
      this.addToLibrary()
      if (this.model_file || this.result_tree_file) {
        let fd = new FormData()
        if (this.model_file) fd.append('model_file', this.model_file, this.model_file.name)
        if (this.result_tree_file) fd.append('result_tree_file', this.result_tree_file, this.result_tree_file.name)
  
        this.transport.patch("logical-models/", String(res.id), fd).then((result) => {
          this.currentModel = {...this.currentModel, ...result}
          this.result_tree_file = null
          this.model_file = null
          this.formPage = 3 
        }, 
        err => {
          this.formEditModel.enable()
          this.formPage = 3 
          this.result_tree_file = null
          this.model_file = null
          alert("Произошла ошибка при сохранении файлов");
          console.dir(err);
        })
      } else this.formPage = 3 
    }, err => {
      this.formEditModel.enable()
      alert("Произошла ошибка при сохранении логической модели");
      this.formPage = 0
      console.dir(err);
    });  
  }
  update(values) {
    let saveArr = []

    for (let field in values) {
      if (['practice_refs', 'outcome_refs', 'target_refs'].includes(field)) {
        if (this.currentModel[field].length != values[field].length) saveArr.push(field)
        else for (let item of this.currentModel[field]) {
          if (!values[field].includes(+item.id)) {
            saveArr.push(field); 
            break
          }
        }
      } 
      else if (['thematic_group_ref'].includes(field)) {
        if (+this.currentModel[field].id != +values[field]) saveArr.push(field)
      } 
      else if (this.currentModel[field] != values[field]) saveArr.push(field)
    }
    
    for (let field in values) 
      if (!saveArr.includes(field)) values[field]=null

    this.transport.post("logical-model-change-requests/"+ this.currentModel.id + '/upload_data/', values).then((res) => {
      if (res.message == 'edit') {
        this.currentModel = {...this.currentModel, ...res.result}

        let index = this.allLogicalModels.indexOf(this.allLogicalModels.find(el => el.id == this.currentModel.id))
        if (index) this.allLogicalModels[index] = this.currentModel
        if (this.model_file || this.result_tree_file) {
          let fd = new FormData()
          if (this.model_file) fd.append('model_file', this.model_file, this.model_file.name)
          if (this.result_tree_file) fd.append('result_tree_file', this.result_tree_file, this.result_tree_file.name)
          this.transport.patch("logical-models/", String(this.currentModel.id), fd).then((result) => {
            this.result_tree_file = null
            this.model_file = null
            this.currentModel = {...this.currentModel, ...result}
            if (index) this.allLogicalModels[index] = this.currentModel
            this.formPage = 3 
          }).catch(error => {
            this.result_tree_file = null
            this.model_file = null
            console.log(error)
            alert("Модель сохранёна, ошибка при загрузке файлов")
          });
        }
        this.formPage = 3
      } else if (res.message == 'request') {
        if (!this.model_file && !this.result_tree_file) alert("Запрос на редактирование успешно отправлен")
        else {
          let fd = new FormData()
          if (this.model_file) fd.append('model_file', this.model_file, this.model_file.name)
          if (this.result_tree_file) fd.append('result_tree_file', this.result_tree_file, this.result_tree_file.name)
          this.transport.patch("logical-model-change-requests/", String(this.currentModel.id), fd).then((resFile) => {
            this.result_tree_file = null
            this.model_file = null
            alert("Запрос на редактирование успешно отправлен")
          }).catch(error => {
            this.result_tree_file = null
            this.model_file = null
            console.log(error)
            alert("Запрос на редактирование успешно отправлен, ошибка при загрузке файлов")
          });
        }
        this.closeForm()
      } 
    }).catch(error => {
      console.log(error)
      alert("Произошла неизвестная ошибка")
      this.closeForm()
    });   
  }

  addToAllLibrary(event) {
    event.preventDefault()
    this.transport.post("logical-models/" + this.currentModel.id + "/switchData_library/", {}).then(
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

  closeForm() {
    this.formPage = 0
  }

  triggerModelFile() {
    this.modelFileRef.nativeElement.click()
  }

  triggerResultTreeFile() {
    this.resultTreeFileRef.nativeElement.click()
  }

  modelUpload(event: any) {
    this.model_file = event.target.files[0]
  }

  resultTreeUpload(event: any) {
    this.result_tree_file = event.target.files[0]
  }

  selectMyLibrary(selected: boolean) {
    this.displayMyLibrary = selected;
    this.logicalModels = this.allLogicalModels
    this.filterForm.reset()
    this.myFilterForm.reset()
    this.verified = false
    this.myVerified = false
    this.sortModels()
  }

  openDetails(model: LogicalModel) {
    this.router.navigate([], {queryParams: {id: model.id}})
    this.currentModel = model;
    this.displayDetails = true;
  }

  openAddPersonal(model: LogicalModel) {
    if (!model.current_user_library && this.authenticated) {
      this.currentModel = model;
      this.displayAddPersonal = true;
    }
    if (model.current_user_library && this.authenticated) {
      this.currentModel = model;
      this.displayRemovePersonal = true;
    }
  }

  closeDetails() {
    this.displayDetails = false;
    this.router.navigate([])
  }

  closeAddPersonal() {
    this.displayAddPersonal = false;
    this.displayRemovePersonal = false;
  }

  addToLibrary() {
    this.transport.post("logical-models/" + this.currentModel.id + "/add_to_library/", {}).then((addToLibraryResult) => {
      this.currentModel.current_user_library = true;
      let index = this.allLogicalModels.indexOf(this.allLogicalModels.find(e => e.id == this.currentModel.id))
      this.allLogicalModels[index].current_user_library = true
      this.currentModel = null
      this.sortModels()
      this.reviewMyLogicalModels()
    }, (error) => {
       console.log(error)
    });
    this.closeAddPersonal();
  }

  removeFromLibrary() {
    this.transport.post("logical-models/" + this.currentModel.id + "/remove_from_library/", {}).then((addToLibraryResult) => {
      this.currentModel.current_user_library = false;
      let index = this.allLogicalModels.indexOf(this.allLogicalModels.find(e => e.id == this.currentModel.id))
      this.allLogicalModels[index].current_user_library = false
      this.currentModel = null
      this.sortModels()
      this.reviewMyLogicalModels()
    }, (error) => console.log(error));
    this.closeAddPersonal();
  }

  downloadFile(filePath: string) {
    let link = document.createElement("a");
    link.download = "filename";
    link.href = filePath;
    link.click();
    link.remove();
  }

  onVerifiedChange() {
    this.verified = !this.verified;
    this.reviewLogicalModels();
  }
  onMyVerifiedChange() {
    this.myVerified = !this.myVerified;
    this.reviewMyLogicalModels();
  }

  reviewLogicalModels() {
    const targetFiltersArray: FormArray = this.filterForm.get('targetFilters') as FormArray;
    const practiceFiltersArray: FormArray = this.filterForm.get('practiceFilters') as FormArray;
    const outcomeFiltersArray: FormArray = this.filterForm.get('outcomeFilters') as FormArray;
    const tgFiltersArray: FormArray = this.filterForm.get('tgFilters') as FormArray;
    this.logicalModels = this.allLogicalModels;

    if (targetFiltersArray.value.length > 0)
        this.logicalModels = this.logicalModels.filter((el:LogicalModel) => {
          return el.target_refs.some((trg:Target) => {return targetFiltersArray.value.includes(String(trg.id))});
        });

    if (practiceFiltersArray.value.length > 0)
        this.logicalModels = this.logicalModels.filter((el:LogicalModel) => {
          return el.practice_refs.some((prc:Practice) => {return practiceFiltersArray.value.includes(String(prc.id))});
        });

    if (outcomeFiltersArray.value.length > 0)
        this.logicalModels = this.logicalModels.filter((el:LogicalModel) => {
          return el.outcome_refs.some((ocm:Outcome) => {return outcomeFiltersArray.value.includes(String(ocm.id))});
        });

    if (tgFiltersArray.value.length > 0)
        this.logicalModels = this.logicalModels.filter((el:LogicalModel) => {
          return el.thematic_group_ref && tgFiltersArray.value.includes(String(el.thematic_group_ref.id))
        });
      
    if (this.verified)
        this.logicalModels = this.logicalModels.filter((el:LogicalModel) => {
          return el.verification_info != null && el.verification_info != undefined && el.verification_info != "";
        });
  }
  reviewMyLogicalModels() {
    const targetFiltersArray: FormArray = this.myFilterForm.get('targetFilters') as FormArray;
    const practiceFiltersArray: FormArray = this.myFilterForm.get('practiceFilters') as FormArray;
    const outcomeFiltersArray: FormArray = this.myFilterForm.get('outcomeFilters') as FormArray;
    const tgFiltersArray: FormArray = this.myFilterForm.get('tgFilters') as FormArray;
    
    this.myLogicalModels = this.allMyLogicalModels;

    if (targetFiltersArray.value.length > 0)
        this.myLogicalModels = this.myLogicalModels.filter((el:LogicalModel) => {
          return el.target_refs.some((trg:Target) => {return targetFiltersArray.value.includes(String(trg.id))});
        });

    if (practiceFiltersArray.value.length > 0)
        this.myLogicalModels = this.myLogicalModels.filter((el:LogicalModel) => {
          return el.practice_refs.some((prc:Practice) => {return practiceFiltersArray.value.includes(String(prc.id))});
        });

    if (outcomeFiltersArray.value.length > 0)
        this.myLogicalModels = this.myLogicalModels.filter((el:LogicalModel) => {
          return el.outcome_refs.some((ocm:Outcome) => {return outcomeFiltersArray.value.includes(String(ocm.id))});
        });

    if (tgFiltersArray.value.length > 0)
        this.myLogicalModels = this.myLogicalModels.filter((el:LogicalModel) => {
          return el.thematic_group_ref && tgFiltersArray.value.includes(String(el.thematic_group_ref.id))
        });
    
    if (this.myVerified)
        this.myLogicalModels = this.myLogicalModels.filter((el:LogicalModel) => {
          return el.verification_info != null && el.verification_info != undefined && el.verification_info != "";
        });
  }

  myCounter(filterName: string, filterValue) {
    if (filterName == "target") {
      return this.myLogicalModels.filter((el:LogicalModel) => {
        return el.target_refs.some((trg:Target) => {return trg.id == filterValue.id});
      }).length;
    } else if (filterName == "practice") {
      return this.myLogicalModels.filter((el:LogicalModel) => {
        return el.practice_refs.some((prc:Practice) => {return prc.id == filterValue.id});
      }).length;
    } else if (filterName == "outcome") {
      return this.myLogicalModels.filter((el:LogicalModel) => {
        return el.outcome_refs.some((ocm:Outcome) => {return ocm.id == filterValue.id});
      }).length;
    } else if (filterName == "thematic_group") {
      return this.myLogicalModels.filter((el:LogicalModel) => {
        return el.thematic_group_ref && filterValue.id ==el.thematic_group_ref.id
      }).length;
    }
  }
  counter(filterName: string, filterValue) {
    if (filterName == "target") {
      return this.logicalModels.filter((el:LogicalModel) => {
        return el.target_refs.some((trg:Target) => {return trg.id == filterValue.id});
      }).length;
    } else if (filterName == "practice") {
      return this.logicalModels.filter((el:LogicalModel) => {
        return el.practice_refs.some((prc:Practice) => {return prc.id == filterValue.id});
      }).length;
    } else if (filterName == "outcome") {
      return this.logicalModels.filter((el:LogicalModel) => {
        return el.outcome_refs.some((ocm:Outcome) => {return ocm.id == filterValue.id});
      }).length;
    } else if (filterName == "thematic_group") {
      return this.logicalModels.filter((el:LogicalModel) => {
        return el.thematic_group_ref && filterValue.id == el.thematic_group_ref.id
      }).length;
    }
  }

  changeMyRoot() {
    if (!this.myFilterRoot.value.target) {
      const formArray: FormArray = this.myFilterForm.get('targetFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.tg) {
      const formArray: FormArray = this.myFilterForm.get('tgFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.practice) {
      const formArray: FormArray = this.myFilterForm.get('practiceFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.outcome) {
      const formArray: FormArray = this.myFilterForm.get('outcomeFilters') as FormArray;
      formArray.clear()
    }
    this.reviewMyLogicalModels()
  }

  changeRoot() {
    if (!this.filterRoot.value.target) {
      const formArray: FormArray = this.filterForm.get('targetFilters') as FormArray;
      formArray.clear()
    }
    if (!this.filterRoot.value.practice) {
      const formArray: FormArray = this.filterForm.get('practiceFilters') as FormArray;
      formArray.clear()
    }
    if (!this.filterRoot.value.outcome) {
      const formArray: FormArray = this.filterForm.get('outcomeFilters') as FormArray;
      formArray.clear()
    }
    if (!this.filterRoot.value.tg) {
      const formArray: FormArray = this.filterForm.get('tgFilters') as FormArray;
      formArray.clear()
    }
    this.reviewLogicalModels()
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
    this.reviewLogicalModels();
  }

  onMyCheckChange(checkList, event) {
    event.preventDefault()
    const formArray: FormArray = this.myFilterForm.get(checkList) as FormArray;

    if (event.target.checked){
      // Add a new control in the arrayForm
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
    this.reviewMyLogicalModels();
  }
}
