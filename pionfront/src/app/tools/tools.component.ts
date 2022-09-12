import { Component, OnInit, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Method } from '../models/method';
import { Outcome } from '../models/outcome';
import { OutcomeLevel } from '../models/outcomelevel';
import { Practice } from '../models/practice';
import { Target } from '../models/target';
import { ThematicGroup } from '../models/thematicgroup';
import { Tool } from '../models/tool';
import { ToolTag } from '../models/tooltags';
import { TransportService } from '../services/transport.service';

@Component({
  selector: 'app-tools',
  templateUrl: './tools.component.html',
  styleUrls: ['./tools.component.scss']
})
export class ToolsComponent implements OnInit {

  constructor(public transport: TransportService, 
    public fb: FormBuilder,
    private activateRoute: ActivatedRoute,
    public router: Router) { }

  status: string = 'ЗАГРУЗКА...'
  toLoad = 8
  displayMyLibrary = false
  authenticated: boolean
  targets: Target[];
  tools: Tool[];
  allTools: Tool[];
  myTools: Tool[];
  allMyTools: Tool[];
  practices: Practice[]
  thematicGroups: ThematicGroup[]
  outcomes: Outcome[]
  outcomeLevels: OutcomeLevel[]
  methods: Method[]
  createToolForm: FormGroup
  formPage: number = 0
  file: File
  otherMethod = false
  displayDetails: boolean
  currentTool: Tool
  toolTags: ToolTag[]

  displayAddPersonal: boolean
  displayRemovePersonal: boolean

  public filterForm = this.fb.group({
    targetFilters: new FormArray([]),
    practiceFilters: new FormArray([]),
    outcomeFilters: new FormArray([]),
    olFilters: new FormArray([]),
    methodFilters: new FormArray([]),
    tgFilters: new FormArray([])
  });

  public myFilterForm = this.fb.group({
    targetFilters: new FormArray([]),
    practiceFilters: new FormArray([]),
    outcomeFilters: new FormArray([]),
    olFilters: new FormArray([]),
    methodFilters: new FormArray([]),
    tgFilters: new FormArray([])
  });

  public filterRoot = this.fb.group({
    target: new FormControl(false),
    practice: new FormControl(false),
    outcome: new FormControl(false),
    ol:  new FormControl(false),
    tg: new FormControl(false),
    method: new FormControl(false)
  });

  public myFilterRoot = this.fb.group({
    target: new FormControl(false),
    practice: new FormControl(false),
    outcome: new FormControl(false),
    ol: new FormControl(false),
    tg: new FormControl(false),
    method: new FormControl(false)
  });
  @ViewChild('file_input') file_input

  ngOnInit(): void {
    if (this.transport.accessToken != null && this.transport.accessToken != undefined && this.transport.refreshToken != null && this.transport.refreshToken != undefined)
      this.authenticated = true;

      this.activateRoute.queryParamMap.subscribe(queryParams => {
        let id = queryParams.get('id');
        if (id) this.transport.get("tools/"+id+"/").then(tool => {
          if (this.allTools) {
            tool = this.allTools.find(t => t.id == tool.id)
          } else if (this.methods) {
            tool.method_ref = [tool.method_ref]
            if (tool.method_ref && tool.method_ref.length && typeof tool.method_ref[0].parent_ref) {
              let parent = this.methods.find(el => el.id == tool.method_ref[0].parent_ref)
              if (parent) tool.method_ref.splice(0, 0, parent)
            }
          }
          this.openDetails(tool)
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

      this.transport.get("tool-tags/", !this.authenticated).then((data) => {
        this.toolTags = data.results;    
        this.toLoad -= 1
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

      this.transport.get("outcome-levels/", !this.authenticated).then((outcomeLevelsData) => {
        this.outcomeLevels = outcomeLevelsData.results;    
        this.toLoad -= 1
      }).catch(error => {
        console.log(error)
        this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
      });
  
      this.transport.get("methods/", !this.authenticated).then((methodsData) => {
        const methods = methodsData.results;
        const children = methods.filter(m => typeof m.parent_ref == 'number').reverse()
        for (let method of children) {
          let child_index = methods.indexOf(methods.find(m => m.id == method.id))
          methods.splice(child_index, 1)
          let parent_index = methods.indexOf(methods.find(m => m.id == method.parent_ref))
          methods[parent_index].has_children = true
          methods.splice(parent_index + 1, 0, method)
        }
        this.methods = methods
        this.transport.get("tools/", !this.authenticated).then((toolsData) => {
          this.allTools = toolsData.results;
          for (let tool of this.allTools) {
            tool.method_ref = [tool.method_ref]
            if (tool.method_ref && tool.method_ref.length && typeof tool.method_ref[0].parent_ref == 'number') {
              let parent = this.methods.find(el => el.id == tool.method_ref[0].parent_ref)
              if (parent) tool.method_ref.splice(0, 0, parent)
            }
          }
          this.tools = this.allTools
          this.sortTools() 
          this.toLoad -= 1;
        }).catch(error => {
          console.log(error)
          this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
        });
        this.toLoad -= 1;
      }).catch(error => {
        console.log(error)
        this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
      });
      this.transport.get("outcomes/", !this.authenticated).then((outcomesData) => {
        this.outcomes = outcomesData.results;
        this.toLoad -= 1
      }).catch(error => {
        console.log(error)
        this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
      });
  } 
  sortTools() {
    this.allMyTools = [];
    for (var item in this.allTools) {
      if (this.allTools[item].current_user_library)
        this.allMyTools.push(this.allTools[item]);
      }
    this.myTools = this.allMyTools; 
  }
  addToLibrary() {
    this.transport.post("tools/" + this.currentTool.id + "/add_to_library/", {}).then((addToLibraryResult) => {
      this.tools.find(c => c.id == this.currentTool.id).current_user_library = true;
      this.sortTools() 
    }, (error) => {});
    this.closeAddPersonal()
  }
  removeFromLibrary() {
    this.transport.post("tools/" + this.currentTool.id + "/remove_from_library/", {}).then((addToLibraryResult) => {
      this.tools.find(c => c.id == this.currentTool.id).current_user_library = false;
      this.sortTools() 
    }, (error) => {});
    this.closeAddPersonal()
  }
  closeAddPersonal() {
    this.displayAddPersonal = false;
    this.displayRemovePersonal = false;
  }
  openAddPersonal(model: Tool) {
    if (!model.current_user_library && this.authenticated) {
      this.currentTool= model;
      this.displayAddPersonal = true;
    }
    if (model.current_user_library && this.authenticated) {
      this.currentTool = model;
      this.displayRemovePersonal = true;
    }
  }
  openDetails(tool: Tool) {
    this.router.navigate([], {queryParams: {id: tool.id}})
    this.currentTool = tool
    this.displayDetails = true
  }
  closeDetails() {
    this.router.navigate([])
    this.displayDetails = false
    this.currentTool = null
  }
  addForm(event) {
    event.preventDefault()

    const tFormControls = () => {
      let arr: FormControl[] = []
      for (let target of this.targets) arr.push(new FormControl(false))
      return arr
    }

    const ttFormControls = () => {
      let arr: FormControl[] = []
      for (let tag of this.toolTags) arr.push(new FormControl(false))
      return arr
    }

    const oFormControls = () => {
      let arr: FormControl[] = []
      for (let outcome of this.outcomes) arr.push(new FormControl(false))
      return arr
    }

    this.createToolForm = new FormGroup({
      name: new FormControl('', Validators.required), //
      info: new FormControl('', Validators.required), //
      tool_tag_refs: new FormArray(ttFormControls()),
      practice_ref: new FormControl('', Validators.required), //
      target_refs: new FormArray(tFormControls()), //
      thematic_group_ref: new FormControl('', Validators.required),//
      method_ref: new FormControl(''),
      method_new: new FormControl(''),
      outcome_level_ref: new FormControl('', Validators.required),
      outcome_refs: new FormArray(oFormControls()),
      url: new FormControl(''),
      isNew: new FormControl(true)
    })

    this.formPage = 1
  }

  editForm(event) {
    event.preventDefault()

    const tFormControls = () => {
      let arr: FormControl[] = []
      for (let target of this.targets) arr.push(new FormControl(this.currentTool.target_refs.find(el => +el.id == +target.id) ? true : false))
      return arr
    }
    const ttFormControls = () => {
      let arr: FormControl[] = []
      for (let tag of this.toolTags) arr.push(new FormControl(this.currentTool.tool_tag_refs.find(el => +el.id == +tag.id) ? true : false))
      return arr
    }
    const oFormControls = () => {
      let arr: FormControl[] = []
      for (let outcome of this.outcomes) arr.push(new FormControl(this.currentTool.outcome_refs.find(el => +el.id == +outcome.id) ? true : false))
      return arr
    }

    let method_id = Array.isArray(this.currentTool.method_ref) ? this.currentTool.method_ref[this.currentTool.method_ref.length - 1].id : this.currentTool.method_ref.id
    if (!this.methods.find(el => el.id == method_id)) {
      method_id = this.methods.find(el => el.parent_ref == this.currentTool.method_ref[this.currentTool.method_ref.length - 1].parent_ref && el.name.trim().toLocaleLowerCase() == 'другое').id
      this.otherMethod = true
    }

    this.createToolForm = new FormGroup({
      name: new FormControl(this.currentTool.name, Validators.required), //
      info: new FormControl(this.currentTool.info, Validators.required), //
      tool_tag_refs: new FormArray(ttFormControls()),
      practice_ref: new FormControl(this.currentTool.practice_ref.id, Validators.required), //
      target_refs: new FormArray(tFormControls()), //
      thematic_group_ref: new FormControl(this.currentTool.thematic_group_ref.id, Validators.required),//
      method_ref: new FormControl(method_id, Validators.required),
      method_new: new FormControl(!this.methods.find(el => el.id == method_id) ? this.currentTool.method_ref[this.currentTool.method_ref.length - 1].name : ''),
      outcome_level_ref: new FormControl(this.currentTool.outcome_level_ref.id, Validators.required),
      outcome_refs: new FormArray(oFormControls()),
      url: new FormControl(this.currentTool.url),
      isNew: new FormControl(false)
    })
    this.closeAddPersonal()
    this.formPage = 1
  }

  addToAllLibrary(event) {
    event.preventDefault()
    this.transport.post("tools/" + this.currentTool.id + "/switchData_library/", {}).then(
    (addToLibraryResult) => {
      alert('Запрос успешно отправлен!')
      this.closeForm()
    }, 
    (error) => {
      console.log(error)
      alert('Ошибка. Не удалось отправить запрос')
      this.closeForm()
    })
  }
  createMethod(event) {  
    if (!this.createToolForm.value.method_new) this.onSubmit(event, null)
    else {
      event.preventDefault() 
      let method = this.methods.find(m => m.id == this.createToolForm.value.method_ref)
      let data = {
        name: this.createToolForm.value.method_new,
        add_public: false,
        parent_ref: method.parent_ref
      }
      this.transport.post("methods/", data).then((res) => {
        this.onSubmit(event, res)
        
      }).catch(error => {
        console.log(error)
      }); 
    }
  }
  onSubmit(event, newMethod?: Method) {
    event.preventDefault()   
    const values = {...this.createToolForm.value}
    const boolToObjT = () => {
      let resNum: any[] = []
      let valArr = this.createToolForm.value.target_refs
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
      let valArr = this.createToolForm.value.outcome_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.outcomes[i].id)
      }
      return resNum
    }
    const boolToObjTT = () => {
      let resNum: any[] = []
      let valArr = this.createToolForm.value.tool_tag_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.toolTags[i].id)
      }
      return resNum
    }
    values.target_refs = boolToObjT()
    values.thematic_group_ref =  +this.createToolForm.value.thematic_group_ref
    values.practice_ref =  +this.createToolForm.value.practice_ref
    values.method_ref =  newMethod ? +newMethod.id : +this.createToolForm.value.method_ref
    values.outcome_level_ref =  +this.createToolForm.value.outcome_level_ref
    values.outcome_refs =  boolToObjO()
    values.tool_tag_refs = boolToObjTT()
    delete values.method_new
    delete values.isNew

    if (this.createToolForm.value.isNew) this.post(values)
    if (!this.createToolForm.value.isNew) this.update(values)
  }
  post(values) {
    this.transport.post("tools/", values).then((tool) => {
      tool.method_ref = [tool.method_ref]
      if (tool.method_ref && tool.method_ref.length && tool.method_ref[0].parent_ref) {
        let parent = this.methods.find(el => el.id == tool.method_ref[0].parent_ref)
        if (parent) tool.method_ref.splice(0, 0, parent)
      }
      if (this.file) {
        let fd = new FormData()
        fd.append('tool_file', this.file, this.file.name)
        this.transport.patch("tools/", tool.id, fd).then((toolWithFile) => {
          this.file = null
          let index = this.allTools.indexOf(this.allTools.find(el => el.id == tool.id))
          tool = {...tool, ...toolWithFile}
          if (index) {
            this.allTools[index] = tool
            this.currentTool = tool
          }
        }).catch(error => {
          console.log(error)
          alert("Инсрумент сохранён, ошибка при загрузке файла")
        });
      } 
      this.allTools.push(tool)
      this.currentTool = tool
      this.addToLibrary()
      this.formPage = 2   
    }).catch(error => {
      console.log(error)
      this.closeForm()
    });   
  }
  update(values) {
    let saveArr = []
    this.currentTool.method_ref = this.currentTool.method_ref[this.currentTool.method_ref.length - 1]
    for (let field in values) {
      if (['tool_tag_refs', 'outcome_refs', 'target_refs'].includes(field)) {
        if (this.currentTool[field].length != values[field].length) saveArr.push(field)
        else for (let item of this.currentTool[field]) {
          if (!values[field].includes(+item.id)) {
            saveArr.push(field); 
            break
          }
        }
      } 
      else if (['practice_ref', 'thematic_group_ref', 'method_ref', 'outcome_level_ref'].includes(field)) {
        if (+this.currentTool[field].id != +values[field]) saveArr.push(field)
      } 
      else if (this.currentTool[field] != values[field]) saveArr.push(field)
    }
    
    for (let field in values) 
      if (!saveArr.includes(field)) values[field]=null

    this.transport.post("tool-change-requests/"+ this.currentTool.id + '/upload_data/', values).then((res) => {
      if (res.message == 'edit') {
        this.currentTool = {...this.currentTool, ...res.result}
        this.currentTool.method_ref = [this.currentTool.method_ref]
        if (this.currentTool.method_ref && this.currentTool.method_ref.length && this.currentTool.method_ref[0].parent_ref) {
          let parent = this.methods.find(el => el.id == this.currentTool.method_ref[0].parent_ref)
          if (parent) this.currentTool.method_ref.splice(0, 0, parent)
        }
        let index = this.allTools.indexOf(this.allTools.find(el => el.id == this.currentTool.id))
        if (index) this.allTools[index] = this.currentTool
        if (this.file) {
          let fd = new FormData()
          fd.append('tool_file', this.file, this.file.name)
          this.transport.patch("tools/", String(this.currentTool.id), fd).then((resFile) => {
            this.file = null
            this.currentTool = {...this.currentTool, ...resFile}
            let index = this.allTools.indexOf(this.allTools.find(el => el.id == this.currentTool.id))
            if (index) this.allTools[index] = this.currentTool
          }).catch(error => {
            this.file = null
            console.log(error)
            alert("Инсрумент сохранён, ошибка при загрузке файла")
          });
        }
        this.formPage = 2

      } else if (res.message == 'request') {
        this.currentTool.method_ref = [this.currentTool.method_ref]
        if (this.currentTool.method_ref && this.currentTool.method_ref.length && this.currentTool.method_ref[0].parent_ref) {
          let parent = this.methods.find(el => el.id == this.currentTool.method_ref[0].parent_ref)
          if (parent) this.currentTool.method_ref.splice(0, 0, parent)
        }
        if (!this.file) alert("Запрос на редактирование успешно отправлен")
        else if (this.file) {
          let fd = new FormData()
          fd.append('tool_file', this.file, this.file.name)
          this.transport.patch("tool-change-requests/", String(this.currentTool.id), fd).then((resFile) => {
            this.file = null
            alert("Запрос на редактирование успешно отправлен")
          }).catch(error => {
            this.file = null
            console.log(error)
            alert("Запрос на редактирование успешно отправлен, ошибка при загрузке файла")
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

  closeForm() {
    this.createToolForm.reset()
    this.formPage = 0
  }

  changeMethod() {
    if (this.createToolForm.value.method_ref) {
      const item = this.methods.find(m => m.id == +this.createToolForm.value.method_ref)
      if (item && item.name && item.name.toLocaleLowerCase().trim() == 'другое') {
        this.otherMethod = true
        return
      }
    }
    this.createToolForm.patchValue({method_new: ''})
    this.otherMethod = false
  }

  selectMyLibrary(my: boolean) {
    this.displayMyLibrary = my
    this.tools = this.allTools
    this.filterForm.reset()
    this.myFilterForm.reset()
    this.sortTools()
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
      } else if (checkList == 'methodFilters') {
        const index = this.methods.indexOf(this.methods.find(item => item.id == event.target.value))
        if (!this.methods[index].parent_ref) this.methods[index].checked = true                       //добавляем, нет родителя
        else {
          const parent = this.methods.find(item => item.id == this.methods[index].parent_ref)           //добавляем, есть родитель
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
      } else if (checkList == 'methodFilters') {
        const index = this.methods.indexOf(this.methods.find(item => item.id == event.target.value))
        if (!this.methods[index].parent_ref) {                        //удаляем, нет родителя
          this.methods[index].checked = false
          let children = this.methods.filter(item => item.parent_ref == event.target.value)
          let indexes = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => ctrl.value == child.id)) indexes.push(i)
          })
          for (let i = indexes.length - 1; i >= 0; i--) formArray.removeAt(indexes[i]);
        } else {                                                          //удаляем, родитель есть
          let children = this.methods.filter(item => item.parent_ref == this.methods[index].parent_ref)
          let siblings = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => child.id == ctrl.value)) siblings.push(i)
          });
          if (!siblings.length) formArray.push(new FormControl(String(this.methods[index].parent_ref)));
        }
      }
    }
    this.reviewTools();
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
      } else if (checkList == 'methodFilters') {
        const index = this.methods.indexOf(this.methods.find(item => item.id == event.target.value))
        if (!this.methods[index].parent_ref) this.methods[index].checked = true                       //добавляем, нет родителя
        else {
          const parent = this.methods.find(item => item.id == this.methods[index].parent_ref)           //добавляем, есть родитель
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
      } else if (checkList == 'methodFilters') {
        const index = this.methods.indexOf(this.methods.find(item => item.id == event.target.value))
        if (!this.methods[index].parent_ref) {                        //удаляем, нет родителя
          this.methods[index].checked = false
          let children = this.methods.filter(item => item.parent_ref == event.target.value)
          let indexes = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => ctrl.value == child.id)) indexes.push(i)
          })
          for (let i = indexes.length - 1; i >= 0; i--) formArray.removeAt(indexes[i]);
        } else {                                                          //удаляем, родитель есть
          let children = this.methods.filter(item => item.parent_ref == this.methods[index].parent_ref)
          let siblings = []
          formArray.controls.forEach((ctrl: FormControl, i: number) => {
            if (children.find(child => child.id == ctrl.value)) siblings.push(i)
          });
          if (!siblings.length) formArray.push(new FormControl(String(this.methods[index].parent_ref)));
        }
      }
    }
    this.reviewMyTools();
  }

  reviewTools() {
    const targetFiltersArray: FormArray = this.filterForm.get('targetFilters') as FormArray;
    const practiceFiltersArray: FormArray = this.filterForm.get('practiceFilters') as FormArray;
    const outcomeFiltersArray: FormArray = this.filterForm.get('outcomeFilters') as FormArray;
    const tgFiltersArray: FormArray = this.filterForm.get('tgFilters') as FormArray;
    const methodFiltersArray: FormArray = this.filterForm.get('methodFilters') as FormArray;
    const olFiltersArray: FormArray = this.filterForm.get('olFilters') as FormArray;

    this.tools = this.allTools;

    if (targetFiltersArray.value.length > 0)
        this.tools = this.tools.filter((el:Tool) => {
          return el.target_refs.some((trg:Target) => {return targetFiltersArray.value.includes(String(trg.id))});
        });

    if (practiceFiltersArray.value.length > 0)
        this.tools = this.tools.filter((el:Tool) => {
          return el.practice_ref && practiceFiltersArray.value.includes(String(el.practice_ref.id))
        });

    if (outcomeFiltersArray.value.length > 0)
        this.tools = this.tools.filter((el:Tool) => {
          return el.outcome_refs.some((el:Outcome) => {return outcomeFiltersArray.value.includes(String(el.id))}); 
        });
    if (methodFiltersArray.value.length > 0)
      this.tools = this.tools.filter((el:Tool) => {
        return el.method_ref.some((el:Method) => {return methodFiltersArray.value.includes(String(el.id))}); 
      });

    if (tgFiltersArray.value.length > 0)
        this.tools = this.tools.filter((el:Tool) => {
          return el.thematic_group_ref && tgFiltersArray.value.includes(String(el.thematic_group_ref.id))
        });

    if (olFiltersArray.value.length > 0)
        this.tools = this.tools.filter((el:Tool) => {
          return el.outcome_level_ref && olFiltersArray.value.includes(String(el.outcome_level_ref.id))
        });
      
  }

  reviewMyTools() {
    const targetFiltersArray: FormArray = this.myFilterForm.get('targetFilters') as FormArray;
    const practiceFiltersArray: FormArray = this.myFilterForm.get('practiceFilters') as FormArray;
    const outcomeFiltersArray: FormArray = this.myFilterForm.get('outcomeFilters') as FormArray;
    const tgFiltersArray: FormArray = this.myFilterForm.get('tgFilters') as FormArray;
    const methodFiltersArray: FormArray = this.myFilterForm.get('methodFilters') as FormArray;
    const olFiltersArray: FormArray = this.myFilterForm.get('olFilters') as FormArray;

    this.myTools = this.allMyTools;

    if (targetFiltersArray.value.length > 0)
        this.myTools = this.myTools.filter((el:Tool) => {
          return el.target_refs.some((trg:Target) => {return targetFiltersArray.value.includes(String(trg.id))});
        });

    if (practiceFiltersArray.value.length > 0)
        this.myTools = this.myTools.filter((el:Tool) => {
          return el.practice_ref && practiceFiltersArray.value.includes(String(el.practice_ref.id))
        });

    if (outcomeFiltersArray.value.length > 0)
        this.myTools = this.myTools.filter((el:Tool) => {
          return el.outcome_refs.some((el:Outcome) => {return outcomeFiltersArray.value.includes(String(el.id))});
        });
    if (methodFiltersArray.value.length > 0)
      this.myTools = this.myTools.filter((el:Tool) => {
        return el.method_ref && methodFiltersArray.value.includes(String(el.method_ref.id))
      });

    if (tgFiltersArray.value.length > 0)
        this.myTools = this.myTools.filter((el:Tool) => {
          return el.thematic_group_ref && tgFiltersArray.value.includes(String(el.thematic_group_ref.id))
        });

    if (olFiltersArray.value.length > 0)
        this.myTools = this.myTools.filter((el:Tool) => {
          return el.outcome_level_ref && olFiltersArray.value.includes(String(el.outcome_level_ref.id))
        });
  }

  myCounter(filterName: string, filterValue) {
    if (filterName == "target") {
      return this.myTools.filter((el:Tool) => {
        return el.target_refs.some((trg:Target) => {return trg.id == filterValue.id});
      }).length;
    } else if (filterName == "practice") {
      return this.myTools.filter((el:Tool) => {
        return el.practice_ref && filterValue.id ==el.practice_ref.id
      }).length;
    } else if (filterName == "outcome") {
      return this.myTools.filter((el:Tool) => {
        return el.outcome_refs.some((el:Outcome) => {return el.id == filterValue.id});
      }).length;
    }else if (filterName == "method") {
      return this.myTools.filter((el:Tool) => {
        return el.method_ref.some((m: Method) => {return m.id == filterValue.id || !this.methods.find(method => method.id == filterValue.id) && filterValue.name.trim().toLocaleLowerCase() == "другое" &&  el.method_ref.find(p => filterValue.parent_ref == p.parent_ref)}); 
      }).length;
    } else if (filterName == "outcome_level") {
      return this.myTools.filter((el:Tool) => {
        return el.outcome_level_ref && filterValue.id ==el.outcome_level_ref.id
      }).length;
    }else if (filterName == "thematic_group") {
      return this.myTools.filter((el:Tool) => {
        return el.thematic_group_ref && filterValue.id ==el.thematic_group_ref.id
      }).length;
    }
  }

  counter(filterName: string, filterValue) {
    if (filterName == "target") {
      return this.tools.filter((el:Tool) => {
        return el.target_refs.some((trg:Target) => {return trg.id == filterValue.id});
      }).length;
    } else if (filterName == "practice") {
      return this.tools.filter((el:Tool) => {
        return el.practice_ref && filterValue.id == el.practice_ref.id
      }).length;
    } else if (filterName == "outcome") {
      return this.tools.filter((el:Tool) => {
        return el.outcome_refs.some((el:Outcome) => {return el.id == filterValue.id});
      }).length;
    }else if (filterName == "method") {
      return this.tools.filter((el:Tool) => {
        return el.method_ref.some((m: Method) => {return m.id == filterValue.id || !this.methods.find(method => method.id == filterValue.id) && filterValue.name.trim().toLocaleLowerCase() == "другое" &&  el.method_ref.find(p => filterValue.parent_ref == p.parent_ref)}); 
      }).length;
    } else if (filterName == "outcome_level") {
      return this.tools.filter((el:Tool) => {
        return el.outcome_level_ref && filterValue.id == el.outcome_level_ref.id
      }).length;
    }else if (filterName == "thematic_group") {
      return this.tools.filter((el:Tool) => {
        return el.thematic_group_ref && filterValue.id == el.thematic_group_ref.id
      }).length;
    } 
  }

  changeMyRoot() {
    if (!this.myFilterRoot.value.target) {
      for (let i = 0; i < this.targets.length; i++) this.targets[i].checkedMy = false
      const formArray: FormArray = this.myFilterForm.get('targetFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.method) {
      for (let i = 0; i < this.methods.length; i++) this.methods[i].checkedMy = false
      const formArray: FormArray = this.myFilterForm.get('methodFilters') as FormArray;
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
    if (!this.myFilterRoot.value.tg) {
      const formArray: FormArray = this.myFilterForm.get('tgFilters') as FormArray;
      formArray.clear()
    }
    if (!this.myFilterRoot.value.ol) {
      const formArray: FormArray = this.myFilterForm.get('olFilters') as FormArray;
      formArray.clear()
    }
    this.reviewMyTools()
  }

  changeRoot() {
    if (!this.filterRoot.value.target) {
      for (let i = 0; i < this.targets.length; i++) this.targets[i].checked = false
      const formArray: FormArray = this.filterForm.get('targetFilters') as FormArray;
      formArray.clear()
    }
    if (!this.filterRoot.value.method) {
      for (let i = 0; i < this.methods.length; i++) this.methods[i].checked = false
      const formArray: FormArray = this.filterForm.get('methodFilters') as FormArray;
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
    if (!this.filterRoot.value.ol) {
      const formArray: FormArray = this.filterForm.get('olFilters') as FormArray;
      formArray.clear()
    }
    if (!this.filterRoot.value.practice) {
      const formArray: FormArray = this.filterForm.get('practiceFilters') as FormArray;
      formArray.clear()
    }
    this.reviewTools()
  }

  findTarget(target) {
    return !!this.currentTool.target_refs.find(el => el.id == target.id)
  }

  downloadFile(filePath: string) {
    let link = document.createElement("a");
    link.target = "_blank"
    link.download = "filename";
    link.href = filePath;
    link.click();
    link.remove();
  }

  fileUpload(event) {
    this.file = event.target.files[0]
  }

  triggerFile() {
    this.file_input.nativeElement.click()
  }
}
