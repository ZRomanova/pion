import { Component, OnInit } from '@angular/core';
import { Target } from '../models/target';
import { TransportService } from '../services/transport.service';
import { Practice } from '../models/practice';
import { Outcome } from '../models/outcome';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { Program } from '../models/program';
import { ThematicGroup } from '../models/thematicgroup';
import { OutcomeMethod } from '../models/outcomemethod';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {

  constructor(private fb: FormBuilder,
    public transport: TransportService,
    public router: Router,
    private activateRoute: ActivatedRoute) {}

  public filterForm = this.fb.group({
    targetFilters: new FormArray([]),
    practiceFilters: new FormArray([]),
    tgFilters: new FormArray([])
  });

  public filterRoot = this.fb.group({
    target: new FormControl(false),
    practice: new FormControl(false),
    tg: new FormControl(false),
  });

  status: string = "ЗАГРУЗКА..."
  displayMyLibrary: boolean = false;
  toLoad: number = 4;
  targets: Target[];
  practices: Practice[];
  outcomes: Outcome[];
  allOutcomes: Outcome[];
  thematicGroups: ThematicGroup[]
  groupedOutcomes: any[] = [];
  fromProgram: boolean = false;
  programId: string;
  programBackReferenceId: string;
  programResultLevel:string;
  authenticated: boolean = false;
  form: Number = 0;
  programs: Program[]
  selectForm: FormGroup
  results = []
  selectedOutcome = null
  selectedProgram: Program
  editForm: FormGroup
  mpl: any[]
  mplInd: any[]
  mplMeth: any[]
  newId: number

  outcome_names: string[] = ['']

  groupBy = (array, key) => {
    // Return the end result
    return array.reduce((result, currentValue) => {
      // If an array already present for key, push it to the array. Else create an array and push the object
      (result[currentValue[key]] = result[currentValue[key]] || []).push(
        currentValue
      );
      // Return the current iteration `result` value, this will be taken as next iteration `result` value and accumulate
      return result;
    }, {}); // empty object is the initial value for result object
  };

  ngOnInit(): void {
    if (this.transport.accessToken != null && this.transport.accessToken != undefined && this.transport.refreshToken != null && this.transport.refreshToken != undefined)
      this.authenticated = true;

    //  
    this.activateRoute.queryParamMap.subscribe(queryParams => {
      this.programId = queryParams.get('programid');
      this.programBackReferenceId = queryParams.get('programbackreferenceid');
      this.programResultLevel = queryParams.get('programresultlevel');

      if (this.programId) {
        this.fromProgram = true;
        this.displayMyLibrary = true;
      }
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
      
      this.transport.get("practices/", !this.authenticated).then((practicesData) => {
        this.practices = practicesData.results;
        
        this.toLoad -= 1;
        
        this.transport.get("outcomes/", !this.authenticated).then((outcomesData) => {
          this.allOutcomes = outcomesData.results;
          this.sortOutcomes()
          this.toLoad -= 1;
        }).catch(error => {
          console.log(error)
          this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
        });;
      }).catch(error => {
        console.log(error)
        this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
      });;
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });;

    this.transport.get("thematic-groups/", !this.authenticated).then((thematicGroupsData) => {
      this.thematicGroups = thematicGroupsData.results;    
      this.toLoad -= 1
    }).catch(error => {
      console.log(error)
      this.status = "ПРОИЗОШЛА ОШИБКА. ПОПРОБУЙТЕ ОБНОВИТЬ СТАНИЦУ ИЛИ ВЕРНИТЕСЬ ПОЗЖЕ"
    });

  }
  sortOutcomes() {
    this.outcomes = this.allOutcomes;
    for (var target in this.targets) {
      for (var practice in this.practices) {
        var current_outcomes = [];
        for (var outcome in this.allOutcomes) {
          if (this.allOutcomes[outcome].current_user_library && this.allOutcomes[outcome].target_refs.some(el => el.id == this.targets[target].id) && this.allOutcomes[outcome].practice_refs.some(el => el.id == this.practices[practice].id)) {
            current_outcomes.push(this.allOutcomes[outcome]);
          }
        }
        if (current_outcomes.length > 0)
          this.groupedOutcomes.push({practice: this.practices[practice], target: this.targets[target], outcomes: current_outcomes});
      }
    }
  }
  closeForm() {
    this.selectForm.reset()
    this.outcome_names = ['']
    this.results = []
    this.form = 0
  }

  openForm1() {
    this.selectForm = new FormGroup({
      program: new FormControl('', Validators.required),
      level: new FormControl('', Validators.required),
      result:  new FormControl('', Validators.required)
    })
    this.transport.get("programs/").then((programsData) => {
      this.programs = programsData.results
      this.form = 1
    })
  }

  openForm2() {
    this.selectedOutcome = this.results.find(outcome => outcome.id == this.selectForm.value.result)
    this.selectedProgram = this.programs.find(p => p.id == this.selectForm.value.program)
    const target_refs: Number[] = Array.from(this.selectedProgram.target_refs, x => +x.id)
    const practice_refs: Number[] = Array.from(this.selectedProgram.practice_refs, x => +x.id)
    const t_r_generator = () => {
      let arr = []
      for (let i = 1; i < this.targets.length + 1; i++) {
        arr.push(new FormControl(target_refs.includes(i) ? true : false))
      }
      return arr
    }

    const p_r_generator = () => {
      let arr = []
      for (let i = 1; i < this.practices.length + 1; i++) arr.push(new FormControl(practice_refs.includes(i) ? true : false))
      return arr
    }

    const t_g_generator = () => {
      let arr = []
      for (let i of this.thematicGroups) arr.push(new FormControl(false))
      return arr
    }

    this.transport.get("mpl-" + this.selectForm.value.level + "/?program_ref=" + this.selectedProgram.id).then((mpl) => {
      this.mpl = mpl.results.filter(e => ("id" in e.result_ref) ? e.result_ref.id == this.selectedOutcome.id : false);
      this.mplInd = this.mpl.filter(e => e.indicator)
      this.mplMeth = this.mpl.filter(e => e.tool)

      const i_r_generator = () => {
        let arr = []
        for (let mpl of this.mplInd) arr.push(new FormControl(true)) 
        return arr
      }
      const m_r_generator = () => {
        let arr = []
        for (let mpl of this.mplMeth) arr.push(new FormControl(true));
        return arr
      }

      this.editForm = new FormGroup({
        name: new FormControl(this.selectedOutcome.name),
        outcome_names: new FormArray([new FormControl()]),
        thematic_group_refs: new FormArray(t_g_generator()),
        target_refs: new FormArray(t_r_generator()),
        practice_refs: new FormArray(p_r_generator()),
        indicators: new FormArray(i_r_generator()),
        methods:  new FormArray(m_r_generator())
      })
      this.form = 2
      
    });
  }

  addName() {
    const formArray: FormArray = this.editForm.get('outcome_names') as FormArray
    formArray.push(new FormControl(''))
    this.outcome_names.push('')  
  }

  openForm3() {
    this.editForm.disable()

    const boolToObjP = () =>  {
      let resNum: any[] = []
      let valArr = this.editForm.value.practice_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(+this.practices[i].id)
      }
      return resNum
    }

    const boolToObjT = () => {
      let resNum: any[] = []
      let valArr = this.editForm.value.target_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i] && !this.targets[i].parent_ref) resNum.push(+this.targets[i].id)
        else if (valArr[i] && this.targets[i].parent_ref) {
          const parent_index = this.targets.indexOf(this.targets.find(item => item.id == this.targets[i].parent_ref))
          if (valArr[parent_index]) resNum.push(+this.targets[i].id)
        }
      }
      return resNum
    }

    const boolToObjTG = () => {
      let resNum: any[] = []
      let valArr = this.editForm.value.thematic_group_refs
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(+this.thematicGroups[i].id)
      }
      return resNum
    }

    const boolToObjI = () =>{
      let resNum: String[] = []
      let valArr = this.editForm.value.indicators
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i]) resNum.push(this.mplInd[i].indicator)
      }
      return resNum
    }

    const boolToObjOM = () => {
      let resNum: any[] = []
      let valArr = this.editForm.value.methods
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i] && this.mplMeth[i].tool_type == 'OutcomeMethods') resNum.push(this.mplMeth[i])
      }
      return resNum
    }

    const boolToObjTM = () => {
      let resNum: any[] = []
      let valArr = this.editForm.value.methods
      for (let i = 0; i < valArr.length; i++) {
        if (valArr[i] && this.mplMeth[i].tool_type == 'Tools') resNum.push(this.mplMeth[i])
      }
      return resNum
    }

    let form = this.editForm.value
    form.target_refs = boolToObjT()
    form.practice_refs = boolToObjP()
    form.thematic_group_refs = boolToObjTG()
    if (this.editForm.value.outcome_names && this.editForm.value.outcome_names.length) 
      this.outcome_names = this.editForm.value.outcome_names.filter(el => el && el.length)
    delete form.outcome_names
    let indicators = boolToObjI()
    let methods = boolToObjOM()
    let tools = boolToObjTM()
    this.postMethods(methods).then(method_refs => {
      form.method_refs = method_refs

      this.transport.post("outcomes/", form).then(res => {
        this.allOutcomes.push(res)
        this.newId = res.id
        this.addToLibrary(this.newId)
        for (let i = 0; i < indicators.length; i++) {
          let dataInd = {name: indicators[i], outcome_ref: this.newId}
          this.transport.post('outcome-indicators/', dataInd).then(resInd =>{
          }).catch(e => console.log(e))
        }
        for (let tool of tools) {
          let array = tool.tool_url.split('?id=')
          if (array[1]) this.transport.post('tools/'+ array[1] + '/add_outcome/?outcome_ref=' + this.newId, {}).then(resInd =>{
          }).catch(e => console.log(e))
        }
        if (this.outcome_names && this.outcome_names.length) 
          for (let i = 0; i < this.outcome_names.length; i++) {
            let dataName = {name: this.outcome_names[i], outcome_ref:  this.newId}
            this.transport.post('outcome-names/', dataName).then(resName => {
            }).catch(e => console.log(e))
          }
        this.form = 3
        }).catch(error => {
          this.editForm.enable()
          console.log(error);
        })
    }).catch(e => {console.log(e); alert('Ошибка!')})
  }

  async postMethods(methods) {
    let method_refs = []
    try {     
      for (let i = 0; i < methods.length; i++) {
        let res = await this.transport.post("outcome-methods/", {name: methods[i].tool, url: methods[i].tool_url ? methods[i].tool_url : 'https://pion.org.ru'})
        method_refs.push(res.id)
      }
      return method_refs
    } catch (e) {
      console.log(e)
      return method_refs
    }
  }

  openModal(add: boolean) {
    if (add) {
      this.transport.post("outcomes/" + this.newId + "/switchData_library/", {}).then((addToLibraryResult) => {
          alert('Запрос успешно отправлен!')
          this.closeForm()   
        }, 
        (error) => {
          console.log(error)
          alert('Ошибка. Не удалось отправить запрос')
          this.closeForm()   
        })
    }
    else this.closeForm()   
  }

  changeLevel() {
    if (!this.selectForm.value.level || !this.selectForm.value.program) this.results = []
    else {
      this.transport.get("program-"+ this.selectForm.value.level +"/?program_ref=" + this.selectForm.value.program).then(result => {
        this.results = result.results 
        //console.log(this.results)
        this.selectForm.patchValue({result: ''})
      })
    }
  }

  selectMyLibrary(selected: boolean) {
    this.displayMyLibrary = selected;
  }

  goToOutcome(outcomeId: string) {
    if (!this.programId)
      this.router.navigate(["/result/"+outcomeId]);
    else {
      var link = "/result/" + outcomeId + '?programid='+this.programId+'&programresultlevel='+this.programResultLevel;

      var backReferenceId:string = null;
      if (this.programBackReferenceId)
        backReferenceId = this.programBackReferenceId;
  
      if (backReferenceId)
        link += "&programbackreferenceid=" + backReferenceId;
      
      this.router.navigateByUrl(link);
    }
  }

  addToLibrary(id) {
    this.transport.post("outcomes/" + id + "/add_to_library/", {}).then((addToLibraryResult) => {
      this.outcomes.find(c => c.id == id).current_user_library = true;
      this.sortOutcomes()
    }, (error) => {});
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
    this.reviewOutcomes();
  }

  reviewOutcomes() {
    const targetFiltersArray: FormArray = this.filterForm.get('targetFilters') as FormArray;
    const practiceFiltersArray: FormArray = this.filterForm.get('practiceFilters') as FormArray;
    const tgFiltersArray: FormArray = this.filterForm.get('tgFilters') as FormArray;

    this.outcomes = this.allOutcomes;

    if (targetFiltersArray.value.length > 0)
      // for(let target of targetFiltersArray.value) {
        this.outcomes = this.outcomes.filter((el:Outcome) => {
          return el.target_refs.some((trg:Target) => {return targetFiltersArray.value.includes(String(trg.id))});
        });
      // }

    if (practiceFiltersArray.value.length > 0)
      // for(let practice of practiceFiltersArray.value) {
        this.outcomes = this.outcomes.filter((el:Outcome) => {
          return el.practice_refs.some((prc:Practice) => {return practiceFiltersArray.value.includes(String(prc.id))});
        });
      // }
    if (tgFiltersArray.value.length > 0)
      this.outcomes = this.outcomes.filter((el:Outcome) => {
        return el.thematic_group_refs.some((prc:ThematicGroup) => {return tgFiltersArray.value.includes(String(prc.id))})
      });
  }

  counter(filterName: string, filterValue) {
    if (filterName == "target") {
      return this.outcomes.filter((el:Outcome) => {
        return el.target_refs.some((trg:Target) => {return trg.id == filterValue.id});
      }).length;
    } else if (filterName == "practice") {
      return this.outcomes.filter((el:Outcome) => {
        return el.practice_refs.some((prc:Practice) => {return prc.id == filterValue.id});
      }).length;
    } else if (filterName == "thematic_group") {
      return this.outcomes.filter((el:Outcome) => {
        return el.thematic_group_refs.some((prc:ThematicGroup) => {return prc.id == filterValue.id})
      }).length;
    }
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
    if (!this.filterRoot.value.tg) {
      const formArray: FormArray = this.filterForm.get('tgFilters') as FormArray;
      formArray.clear()
    }
    this.reviewOutcomes()
  }

  addToProgram(outcome:Outcome) {
     

    let newResultAdd:any = {};

    newResultAdd.name = outcome.name;
    var splitted:any = [];
    if (this.programBackReferenceId) {
       
      splitted = this.programBackReferenceId.split(" ");
    }
    if (this.programBackReferenceId) {
      if (this.programResultLevel == "program-short-outcomes")
        newResultAdd.program_output_many_refs = splitted;
      if (this.programResultLevel == "program-mid-outcomes")
        newResultAdd.program_short_outcome_many_refs = splitted;
      if (this.programResultLevel == "program-impacts")
        newResultAdd.program_mid_outcome_many_refs = splitted;
    }

    newResultAdd.program_ref = Number(this.programId);
    this.transport.post(this.programResultLevel + "/", newResultAdd).then((result: any) => {
      this.router.navigate(["program/" + this.programId])
    }, error => {console.error(error)});
  }

}
