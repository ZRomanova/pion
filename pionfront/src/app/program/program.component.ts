import { Component, ComponentFactoryResolver, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, Validators, FormArray, FormControl, FormGroup } from '@angular/forms';
import { TransportService } from '../services/transport.service';
import { Program } from '../models/program';
import { UserRequest } from '../models/userrequest';
import { Practice } from '../models/practice';
import { Target } from '../models/target';
import { Context } from '../models/context';
import { Assumption } from '../models/assumption';
import { Activity } from '../models/activity';
import { ProgramOutput } from '../models/programoutput';
import { ProgramShortOutcome } from '../models/programshortoutcome';
import { ProgramMidOutcome } from '../models/programmidoutcome';
import { ProgramImpact } from '../models/programimpact';
import { MplImpacts } from '../models/mplimpacts';
import { MplMidOutcomes } from '../models/mplmidoutcomes';
import { MplOutputs } from '../models/mploutputs';
import { MplShortOutcomes } from '../models/mplshortoutcomes';
import { MflOutputs } from '../models/mfloutputs';
import { MflShortOutcomes } from '../models/mflshortoutcomes';
import { MflMidOutcomes } from '../models/mflmidoutcomes';
import { MflImpacts } from '../models/mflimpacts';
import { TargetDescription } from '../models/targetdescription';
import { OutcomeMethod } from '../models/outcomemethod';
import { OutcomeIndicator } from '../models/outcomeindicator';
import { environment } from 'src/environments/environment';
import { Method } from '../models/method';
import { Tool } from '../models/tool';
import { RefDirective } from '../classes/ref.directive';
import { ShowModalComponent } from '../show-modal/show-modal.component';

// import { debug } from 'console';


@Component({
  selector: 'app-program',
  templateUrl: './program.component.html',
  styleUrls: ['./program.component.scss']
})

export class ProgramComponent implements OnInit {
  @ViewChild('help_block') help_block: ElementRef 
  @ViewChild('helpItem1') helpItem1: ElementRef 
  @ViewChild('helpItem2') helpItem2: ElementRef 
  @ViewChild(RefDirective) refDir: RefDirective

  id: string;
  baseUrl = environment.baseUrl
  constructor(private activateRoute: ActivatedRoute,
    private resolver: ComponentFactoryResolver,
    public fb: FormBuilder,
    public transport: TransportService,
    public router: Router) {
    this.id = activateRoute.snapshot.params['id'];
  }

  public programForm = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    period: ['', Validators.required],
    user_ref: ['', Validators.required],
    target_refs: new FormArray([]),
    practice_refs: new FormArray([]),
  });
  
  public programEdit = this.fb.group({
    contexts: new FormArray([]), 
    assumptions: new FormArray([])
  });

  public assumptionAddForm = this.fb.group({
    text: ['', Validators.required]
  });
  public contextAddForm = this.fb.group({
    text: ['', Validators.required]
  });
  public targetDescriptionAddForm = this.fb.group({
    info: [''],
    target_ref: ['']
  });
  public activityAddForm = this.fb.group({
    name: ['', Validators.required],
    target_ref: [''],
    info: ['']
  });
  public programOutputAddForm = this.fb.group({
    name: ['', Validators.required],
    activity_ref: [''],
    info: ['']
  });
  public programShortOutcomeAddForm = this.fb.group({
    name: ['', Validators.required],
    program_output_ref: [''],
    info: [''],
    program_output_many_refs: new FormArray([]),
  });
  public programMidOutcomeAddForm = this.fb.group({
    name: ['', Validators.required],
    program_short_outcome_ref: [''],
    info: [''],
    program_short_outcome_many_refs: new FormArray([]),
  });
  public programImpactAddForm = this.fb.group({
    name: ['', Validators.required],
    program_mid_outcome_ref: [''],
    info: [''],
    program_mid_outcome_many_refs: new FormArray([]),
  });

  program: Program;
  userRequests: UserRequest[];
  currentUserRequest: UserRequest;
  practices: Practice[];
  targets: Target[];
  toLoad: number = 4;

  contexts: Context[] = [];
  assumptions: Assumption[] = [];
  activities: Activity[] = [];
  programOutputs: ProgramOutput[] = [];
  programShortOutcomes: ProgramShortOutcome[] = [];
  programMidOutcomes: ProgramMidOutcome[] = [];
  programImpacts: ProgramImpact[] = [];

  mplOutputs: MplOutputs[] = [];
  mplShortOutcomes: MplShortOutcomes[] = [];
  mplMidOutcomes: MplMidOutcomes[] = [];
  mplImpacts: MplImpacts[] = [];

  mflOutputs: MflOutputs[] = [];
  mflShortOutcomes: MflShortOutcomes[] = [];
  mflMidOutcomes: MflMidOutcomes[] = [];
  mflImpacts: MflImpacts[] = [];

  showAssumptionAdd: boolean = false;
  showContextAdd: boolean = false;
  showTargetDescription: boolean = false;
  showActivityAdd: boolean = false;
  showProgramOutputAdd: boolean = false;
  showShortProgramOutcomeAdd: boolean = false;
  showMidProgramOutcomeAdd: boolean = false;
  showProgramImpactAdd: boolean = false;

  editingAssumption: Assumption;
  editingContext: Context;
  editingTargetDescription: TargetDescription;
  editingTargetDescriptionSubject: Target;
  editingActivity: Activity;
  editingProgramOutput: ProgramOutput;
  editingShortProgramOutcome: ProgramShortOutcome;
  editingMidProgramOutcome: ProgramMidOutcome;
  editingProgramImpact: ProgramImpact;
  methods: Method[]
  tools: Tool[]

  displayDownloader: boolean = false;
  displayProgramDetails: boolean = false;
  displayChain: boolean = false;
  displayInnerChain: boolean = false;
  displayPlanForm: boolean = false;
  displayPlan: boolean = false;
  displayPlanOutput: boolean = false;
  displayPlanShortOutcome: boolean = false;
  displayPlanMidOutcome: boolean = false;
  displayPlanImpact: boolean = false;
  displayForm: boolean = false;
  displayFormOutput: boolean = false;
  displayFormShortOutcome: boolean = false;
  displayFormMidOutcome: boolean = false;
  displayFormImpact: boolean = false;

  displayProgressLine: boolean = false;

  itemNum1Active: boolean = false;
  itemNum2Active: boolean = false;
  itemNum3Active: boolean = false;
  itemNum4Active: boolean = false;
  itemNum5Active: boolean = false;
  itemNum6Active: boolean = false;
  itemNum7Active: boolean = false;

  outcomeIndicators: OutcomeIndicator[]
  outcomeMethods: OutcomeMethod[]

  ngOnInit(): void {
    this.programForm.disable()
    // console.log(this.programForm)
    if (!this.id) {
      this.displayProgramDetails = true;
      this.program = new Program();
      this.program.target_refs = [];
      this.program.practice_refs = [];
      this.programForm.enable()
      this.toLoad -= 1;
    } else {
      this.transport.getExact('programs', this.id).then(programData => {
        this.program = programData;
        this.programForm.controls['name'].setValue(this.program.name);
        this.programForm.controls['description'].setValue(this.program.description);
        this.programForm.controls['period'].setValue(this.program.period);
        this.programForm.controls['user_ref'].setValue(this.program.user_ref.id);
        this.fillFormArrayWithId('target_refs', this.program.target_refs);
        this.fillFormArrayWithId('practice_refs', this.program.practice_refs);
        this.programForm.enable()
        this.toLoad -= 1;

        this.program.target_refs.forEach(target => {
          this.transport.get("target-descriptions/?program_ref=" + this.id + "&target_ref=" + target.id).then(targetDescriptionsData => {
            if (targetDescriptionsData.results && targetDescriptionsData.results.length > 0)
              target.targetDescription = targetDescriptionsData.results[0];
          })
        });

      });
    }

    this.transport.get("user-requests/").then((userRequestsData) => {
      this.userRequests = userRequestsData.results;
      for (var userRequest of this.userRequests) {
        if (userRequest.current_user) {
          this.currentUserRequest = userRequest;
          this.programForm.controls['user_ref'].setValue(this.currentUserRequest.user_ref.id);
          break;
        }
      }
      this.toLoad -= 1;
    });

    this.transport.get("practices/").then((practicesData) => {
      this.practices = practicesData.results;
      this.toLoad -= 1;
    });

    this.transport.get("targets/?parent_ref=0").then((targetsData) => {
      this.targets = targetsData.results;

      this.toLoad -= 1;
    });

    if (this.id) {
      this.transport.get("contexts/?program_ref=" + this.id).then((contextsData) => {
        this.contexts = contextsData.results;
        let lenght = this.contexts.length;
        for (let i = 0; i < lenght; i++) {
          let contexts = this.programEdit.get('contexts') as FormArray;
          contexts.push(new FormGroup({context_name: new FormControl(this.contexts[i].text), context_edit: new FormControl(false)}));
        }
      });

      this.transport.get("assumptions/?program_ref=" + this.id).then((assumptionsData) => {
        this.assumptions = assumptionsData.results;
        let lenght = this.assumptions.length;
        for (let i = 0; i < lenght; i++) {
          let assumptions = this.programEdit.get('assumptions') as FormArray;
          assumptions.push(new FormGroup({assumption_name: new FormControl(this.assumptions[i].text), assumption_edit: new FormControl(false)}));
        }
      });

      this.transport.get("activities/?program_ref=" + this.id).then((activitiesData) => {
        this.activities = activitiesData.results;
      });

      this.transport.get("program-outputs/?program_ref=" + this.id).then((programOutputData) => {
        this.programOutputs = programOutputData.results;
      });

      this.transport.get("program-short-outcomes/?program_ref=" + this.id).then((programShortOutcomeData) => {
        this.programShortOutcomes = programShortOutcomeData.results;
      });

      this.transport.get("program-mid-outcomes/?program_ref=" + this.id).then((programMidOutcomeData) => {
        this.programMidOutcomes = programMidOutcomeData.results;
      });

      this.transport.get("program-impacts/?program_ref=" + this.id).then((programImpactData) => {
        this.programImpacts = programImpactData.results;
      });

      this.transport.get("mpl-outputs/?program_ref=" + this.id).then((mplOutputsData) => {
        this.mplOutputs = mplOutputsData.results;
      });

      this.transport.get("mpl-short-outcomes/?program_ref=" + this.id).then((mplShortOutcomesData) => {
        this.mplShortOutcomes = mplShortOutcomesData.results;
      });

      this.transport.get("mpl-mid-outcomes/?program_ref=" + this.id).then((mplMidOutcomesData) => {
        this.mplMidOutcomes = mplMidOutcomesData.results;
      });

      this.transport.get("mpl-impacts/?program_ref=" + this.id).then((mplImpactsData) => {
        this.mplImpacts = mplImpactsData.results;
      });

      this.transport.get("mfl-outputs/?program_ref=" + this.id).then((mflOutputsData) => {
        this.mflOutputs = mflOutputsData.results;
      });

      this.transport.get("mfl-short-outcomes/?program_ref=" + this.id).then((mflShortOutcomesData) => {
        this.mflShortOutcomes = mflShortOutcomesData.results;
      });

      this.transport.get("mfl-mid-outcomes/?program_ref=" + this.id).then((mflMidOutcomesData) => {
        this.mflMidOutcomes = mflMidOutcomesData.results;
      });

      this.transport.get("mfl-impacts/?program_ref=" + this.id).then((mflImpactsData) => {
        this.mflImpacts = mflImpactsData.results;
      });

      this.transport.get("methods/?parent_ref=0").then((methodsData) => {
        this.methods = methodsData.results;
      }).catch(error => {
        console.log(error)
      });

      // this.transport.get("tools/").then((methodsData) => {
      //   this.tools = methodsData.results;
      // }).catch(error => {
      //   console.log(error)
      // });

    }

    // scheme
    // var self = this;

    // var canvas: any = document.getElementById("np-canvas");

    // var translatePos = {
    //   x: canvas.width / 2,
    //   y: canvas.height / 2
    // };

    // var scale = 1.0;
    // var scaleMultiplier = 0.8;
    // var startDragOffset: any = {};
    // var mouseDown = false;

    // // add button event listeners
    // document.getElementById("plus").addEventListener("click", function () {
    //   scale /= scaleMultiplier;
    //   self.draw(scale, translatePos);
    // }, false);

    // document.getElementById("minus").addEventListener("click", function () {
    //   scale *= scaleMultiplier;
    //   self.draw(scale, translatePos);
    // }, false);

    // // add event listeners to handle screen drag
    // canvas.addEventListener("mousedown", function (evt) {
    //   mouseDown = true;
    //   startDragOffset.x = evt.clientX - translatePos.x;
    //   startDragOffset.y = evt.clientY - translatePos.y;
    // });

    // canvas.addEventListener("mouseup", function (evt) {
    //   mouseDown = false;
    // });

    // canvas.addEventListener("mouseover", function (evt) {
    //   mouseDown = false;
    // });

    // canvas.addEventListener("mouseout", function (evt) {
    //   mouseDown = false;
    // });

    // canvas.addEventListener("mousemove", function (evt) {
    //   if (mouseDown) {
    //     translatePos.x = evt.clientX - startDragOffset.x;
    //     translatePos.y = evt.clientY - startDragOffset.y;
    //     self.draw(scale, translatePos);
    //   }
    // });

    // self.draw(scale, translatePos);
  }

  onSubmit() {
    console.dir(this.programForm);

    if (this.id) {
      // PUT data
      this.programForm.value.id = Number(this.id);
      this.transport.put("programs/", this.id, this.programForm.value).then((res: Program) => {
        this.program = res
        this.openNotification(false)
      }, err => {
         
        this.openNotification(true)
        console.dir(err);
      });
    } else {
      // POST data
      this.transport.post("programs/", this.programForm.value).then((res: Program) => {
        this.router.navigate(['program/' + res.id]);
      }, err => {
        this.openNotification(true)
        console.dir(err);
      });
    }    
  }

  hideHelpBlock() {
    this.help_block.nativeElement.remove()
  }

  hideHelpItem(item) {
    if (item === 1) {
      this.helpItem1.nativeElement.remove()
    } else if (item === 2) {
      this.helpItem2.nativeElement.remove()
    }
  }

  clickEditContext(i) {
    const newValue = !this.programEdit.value.contexts[i].context_edit
    let contexts = this.programEdit.get('contexts') as FormArray;
    let context = contexts.at(i) as FormGroup
    context.patchValue({context_edit: newValue})
  }

  clickEditAssumption(i) {
    const newValue = !this.programEdit.value.assumptions[i].assumption_edit
    let assumptions = this.programEdit.get('assumptions') as FormArray;
    let assumption = assumptions.at(i) as FormGroup
    assumption.patchValue({assumption_edit: newValue})
  }

  deleteAssumption(i) {
    const id = this.assumptions[i].id
    this.transport.delete("assumptions/", String(id)).then((res: any) => {
      this.assumptions.splice(i, 1)
      let assumptions = this.programEdit.get('assumptions') as FormArray;
      assumptions.removeAt(i)
    }, error => { console.dir(error) });
  }

  deleteContext(i) {  
    const id = this.contexts[i].id
    this.transport.delete("contexts/", String(id)).then((res: any) => {
      this.contexts.splice(i, 1)
      let contexts = this.programEdit.get('contexts') as FormArray;
      contexts.removeAt(i)         
    }, error => { console.dir(error) });
  }

  onCheckChange(formArrayName, event) {
    let formArray: FormArray;

    if (formArrayName == 'program_output_many_refs') {
      formArray = this.programShortOutcomeAddForm.get(formArrayName) as FormArray;;
    }
    else if (formArrayName == 'program_short_outcome_many_refs') {
      formArray = this.programMidOutcomeAddForm.get(formArrayName) as FormArray;;
    }
    else if (formArrayName == 'program_mid_outcome_many_refs') {
      formArray = this.programImpactAddForm.get(formArrayName) as FormArray;;
    } else {
      formArray = this.programForm.get(formArrayName) as FormArray;;
    }

    /* Selected */
    if (event.target.checked) {
      // Add a new control in the arrayForm
      formArray.push(new FormControl(Number(event.target.value)));
    }
    /* unselected */
    else {
      // find the unselected element
      let i: number = 0;

      formArray.controls.forEach((ctrl: FormControl) => {
        if (ctrl.value == event.target.value) {
          // Remove the unselected element from the arrayForm
          formArray.removeAt(i);
          return;
        }

        i++;
      });
    }
  }

  fillFormArrayWithId(formArrayName: string, dataList: any[]) {
     
    let formArray: FormArray;

    if (formArrayName == 'program_output_many_refs') {
      formArray = this.programShortOutcomeAddForm.get(formArrayName) as FormArray;
    }
    else if (formArrayName == 'program_short_outcome_many_refs') {
      formArray = this.programMidOutcomeAddForm.get(formArrayName) as FormArray;;
    }
    else if (formArrayName == 'program_mid_outcome_many_refs') {
      formArray = this.programImpactAddForm.get(formArrayName) as FormArray;;
    } else {
      formArray = this.programForm.get(formArrayName) as FormArray;;
    }

    if (dataList != null && dataList != undefined) {
      for (let index = 0; index < dataList.length; index++) {
        const element = dataList[index];
        formArray.push(new FormControl(element.id));
      }
    }
    // dataList.forEach(element => {

    // });
  }

  practiceShouldBeChecked(practice: Practice): boolean {
    return this.program.practice_refs.some(el => el.id == practice.id);
  }
  targetShouldBeChecked(target: Target): boolean {
    return this.program.target_refs.some(el => el.id == target.id);
  }
  programOutputShouldBeChecked(programOutput: ProgramOutput): boolean { // editingShortProgramOutcome && editingShortProgramOutcome.program_output_ref && (editingShortProgramOutcome.program_output_ref == programOutput.id || editingShortProgramOutcome.program_output_ref.id == programOutput.id)
    if (!this.editingShortProgramOutcome || !this.editingShortProgramOutcome.program_output_many_refs)
      return false;
    return this.editingShortProgramOutcome.program_output_many_refs.some(el => el.id == programOutput.id);
  }
  programShortOutcomeShouldBeChecked(programShortOutcome: ProgramShortOutcome): boolean { // editingMidProgramOutcome && editingMidProgramOutcome.program_short_outcome_ref && editingMidProgramOutcome.program_short_outcome_ref.id == programShortOutcome.id
    if (!this.editingMidProgramOutcome || !this.editingMidProgramOutcome.program_short_outcome_many_refs)
      return false;
    return this.editingMidProgramOutcome.program_short_outcome_many_refs.some(el => el.id == programShortOutcome.id);
  }
  programMidOutcomeShouldBeChecked(programMidOutcome: ProgramMidOutcome): boolean { // editingProgramImpact && editingProgramImpact.program_mid_outcome_ref && editingProgramImpact.program_mid_outcome_ref.id == programMidOutcome.id
    if (!this.editingProgramImpact || !this.editingProgramImpact.program_mid_outcome_many_refs)
      return false;
    return this.editingProgramImpact.program_mid_outcome_many_refs.some(el => el.id == programMidOutcome.id);
  }

  openAssumptionAdd() {
    this.showAssumptionAdd = true;
  }
  openContextAdd() {
    this.showContextAdd = true;
  }
  openActivityAdd() {
    this.showActivityAdd = true;
  }
  openProgramOutputAdd() {
    this.showProgramOutputAdd = true;
  }
  openShortProgramOutcomeAdd() {
    this.showShortProgramOutcomeAdd = true;
  }
  openMidProgramOutcomeAdd() {
    this.showMidProgramOutcomeAdd = true;
  }
  openProgramImpactAdd() {
    this.showProgramImpactAdd = true;
  }

  openAssumptionEdit(editingObject) {
    this.editingAssumption = editingObject;
    this.assumptionAddForm.controls['text'].setValue(editingObject.text)
    this.showAssumptionAdd = true;
  }
  openContextEdit(editingObject) {
    this.editingContext = editingObject;
    this.contextAddForm.controls['text'].setValue(editingObject.text);
    this.showContextAdd = true;
  }
  openTargetDescriptionEdit(editingObject) {
    this.editingTargetDescriptionSubject = editingObject;
    this.targetDescriptionAddForm.controls['target_ref'].setValue(editingObject.id);
    if (editingObject.targetDescription) {
      this.editingTargetDescription = editingObject.targetDescription;
      this.targetDescriptionAddForm.controls['info'].setValue(this.editingTargetDescription.info);
    }
    this.showTargetDescription = true;
  }
  openActivityEdit(editingObject) {
    this.editingActivity = editingObject;
    this.activityAddForm.controls['name'].setValue(editingObject.name);
    if (editingObject.target_ref)
      this.activityAddForm.controls['target_ref'].setValue(editingObject.target_ref.id);
    this.activityAddForm.controls['info'].setValue(editingObject.info);
    this.showActivityAdd = true;
  }
  openProgramOutputEdit(editingObject) {
    this.editingProgramOutput = editingObject;
    this.programOutputAddForm.controls['name'].setValue(editingObject.name);
    if (editingObject.activity_ref)
      this.programOutputAddForm.controls['activity_ref'].setValue(editingObject.activity_ref.id);
    this.programOutputAddForm.controls['info'].setValue(editingObject.info);

    this.showProgramOutputAdd = true;
  }
  openShortProgramOutcomeEdit(editingObject) {
    this.editingShortProgramOutcome = editingObject;
    this.programShortOutcomeAddForm.controls['name'].setValue(editingObject.name);
    if (editingObject.program_output_ref)
      this.programShortOutcomeAddForm.controls['program_output_ref'].setValue(editingObject.program_output_ref.id);
    this.programShortOutcomeAddForm.controls['info'].setValue(editingObject.info);

    // this.programShortOutcomeAddForm.controls['program_output_many_refs'].setValue(new FormArray([]));

    this.fillFormArrayWithId('program_output_many_refs', editingObject.program_output_many_refs);

    this.showShortProgramOutcomeAdd = true;
  }
  openMidProgramOutcomeEdit(editingObject) {
    this.editingMidProgramOutcome = editingObject;
    this.programMidOutcomeAddForm.controls['name'].setValue(editingObject.name);
    if (editingObject.program_short_outcome_ref)
      this.programMidOutcomeAddForm.controls['program_short_outcome_ref'].setValue(editingObject.program_short_outcome_ref.id);
    this.programMidOutcomeAddForm.controls['info'].setValue(editingObject.info);

    // this.programMidOutcomeAddForm.controls['program_short_outcome_many_refs'].setValue(new FormArray([]));

    this.fillFormArrayWithId('program_short_outcome_many_refs', editingObject.program_short_outcome_many_refs);

    this.showMidProgramOutcomeAdd = true;
  }
  openProgramImpactEdit(editingObject) {
    this.editingProgramImpact = editingObject;
    this.programImpactAddForm.controls['name'].setValue(editingObject.name);
    if (editingObject.program_mid_outcome_ref)
      this.programImpactAddForm.controls['program_mid_outcome_ref'].setValue(editingObject.program_mid_outcome_ref.id);
    this.programImpactAddForm.controls['info'].setValue(editingObject.info);

    // this.programImpactAddForm.controls['program_mid_outcome_many_refs'].setValue(new FormArray([]));

    this.fillFormArrayWithId('program_mid_outcome_many_refs', editingObject.program_mid_outcome_many_refs);

    this.showProgramImpactAdd = true;
  }


  closeAssumptionAdd() {
    this.showAssumptionAdd = false;
    this.editingAssumption = null;
    this.assumptionAddForm = this.fb.group({
      text: ['', Validators.required]
    });
  }
  closeContextAdd() {
    this.showContextAdd = false;
    this.editingContext = null;
    this.contextAddForm = this.fb.group({
      text: ['', Validators.required]
    });
  }
  closeActivityAdd() {
    this.showActivityAdd = false;
    this.editingActivity = null;
    this.activityAddForm = this.fb.group({
      name: ['', Validators.required],
      target_ref: [''],
      info: ['']
    });
  }
  closeTargetDescription() {
    this.showTargetDescription = false;

    this.editingTargetDescription = null;
    this.editingTargetDescriptionSubject = null;

    this.targetDescriptionAddForm = this.fb.group({
      info: [''],
      target_ref: ['']
    });
  }
  closeProgramOutputAdd() {
    this.showProgramOutputAdd = false;
    this.editingProgramOutput = null;
    this.programOutputAddForm = this.fb.group({
      name: ['', Validators.required],
      activity_ref: [''],
      info: ['']
    });
  }
  closeShortProgramOutcomeAdd() {
    this.showShortProgramOutcomeAdd = false;
    this.editingShortProgramOutcome = null;
    this.programShortOutcomeAddForm = this.fb.group({
      name: ['', Validators.required],
      program_output_ref: [''],
      info: [''],
      program_output_many_refs: new FormArray([])
    });
  }
  closeMidProgramOutcomeAdd() {
    this.showMidProgramOutcomeAdd = false;
    this.editingMidProgramOutcome = null;
    this.programMidOutcomeAddForm = this.fb.group({
      name: ['', Validators.required],
      program_short_outcome_ref: [''],
      info: [''],
      program_short_outcome_many_refs: new FormArray([])
    });
  }
  closeProgramImpactAdd() {
    this.showProgramImpactAdd = false;
    this.editingProgramImpact = null;
    this.programImpactAddForm = this.fb.group({
      name: ['', Validators.required],
      program_mid_outcome_ref: [''],
      info: [''],
      program_mid_outcome_many_refs: new FormArray([])
    });
  }

  onAssumptionAdd() {
    this.assumptionAddForm.value.program_ref = Number(this.id);
    this.transport.post("assumptions/", this.assumptionAddForm.value).then((assumption: Assumption) => {
      this.assumptions.push(assumption);
      let assumptions = this.programEdit.get('assumptions') as FormArray;
      assumptions.push(new FormGroup({assumption_name: new FormControl(assumption.text), assumption_edit: new FormControl(false)}));
      this.assumptionAddForm = this.fb.group({
        text: ['', Validators.required]
      });

    }, error => { console.dir(error) });
    this.closeAssumptionAdd();
  }
  onContextAdd() {
    this.contextAddForm.value.program_ref = Number(this.id);
    this.transport.post("contexts/", this.contextAddForm.value).then((context: Context) => {
      this.contexts.push(context);
      let contexts = this.programEdit.get('contexts') as FormArray;
      contexts.push(new FormGroup({context_name: new FormControl(context.text), context_edit: new FormControl(false)}));
        
      this.contextAddForm = this.fb.group({
        text: ['', Validators.required]
      });

    }, error => { console.dir(error) });
    this.closeContextAdd();
  }
  onAssumptionEdit(i) {
    const data = {
      text: this.programEdit.value.assumptions[i].assumption_name,
      program_ref: Number(this.id)
    }
    this.transport.put("assumptions/", String(this.assumptions[i].id), data).then((assumption: Assumption) => {
      this.assumptions[i] = assumption
      let assumptions = this.programEdit.get('assumptions') as FormArray;
      let assumption_fg = assumptions.at(i) as FormGroup;
      assumption_fg.patchValue({assumption_name: assumption.text, assumption_edit: false})
    }, error => { console.dir(error) });
  }
  onContextEdit(i) {
    const data = {
      text: this.programEdit.value.contexts[i].context_name,
      program_ref: Number(this.id)
    }
    this.transport.put("contexts/", String(this.contexts[i].id), data).then((context: Context) => {
      this.contexts[i] = context
      let contexts = this.programEdit.get('contexts') as FormArray;
      let context_fg = contexts.at(i) as FormGroup;
      context_fg.patchValue({context_name: context.text, context_edit: false})

    }, error => { console.dir(error) });
  }

  onTargetDescriptionAdd() {
    this.targetDescriptionAddForm.value.program_ref = Number(this.id);
    if (!this.editingTargetDescription) {
      this.transport.post("target-descriptions/", this.targetDescriptionAddForm.value).then((targetDescription: TargetDescription) => {
        this.editingTargetDescriptionSubject.targetDescription = targetDescription;

        this.closeTargetDescription();

      }, error => { console.dir(error) });
    } else {
      this.transport.put("target-descriptions/", String(this.editingTargetDescription.id), this.targetDescriptionAddForm.value).then((targetDescription: TargetDescription) => {
        // this.activities.push(activity);
        this.editingTargetDescription.target_ref = targetDescription.target_ref;
        this.editingTargetDescription.info = targetDescription.info;

        this.closeTargetDescription();

      }, error => { console.dir(error) });
    }
  }
  onActivityAdd() {
     
    this.activityAddForm.value.program_ref = Number(this.id);
    if (!this.editingActivity) {
      this.transport.post("activities/", this.activityAddForm.value).then((activity: Activity) => {
        this.activities.push(activity);

        this.closeActivityAdd();

      }, error => { console.dir(error) });
    } else {
      // this.activityAddForm.value.target_ref = this.activityAddForm.value.target_ref.id;
      this.transport.put("activities/", String(this.editingActivity.id), this.activityAddForm.value).then((activity: Activity) => {
        // this.activities.push(activity);
        this.editingActivity.name = activity.name;
        this.editingActivity.target_ref = activity.target_ref;
        this.editingActivity.info = activity.info;

        this.closeActivityAdd();

      }, error => { console.dir(error) });
    }
  }
  onProgramOutputAdd() {
     
    this.programOutputAddForm.value.program_ref = Number(this.id);
    if (!this.editingProgramOutput) {
      this.transport.post("program-outputs/", this.programOutputAddForm.value).then((programOutput: ProgramOutput) => {
        this.programOutputs.push(programOutput);
      }, error => { console.dir(error) });
      this.closeProgramOutputAdd();
    } else {
      // this.programOutputAddForm.value.activity_ref = Number(this.programOutputAddForm.value.activity_ref.id);
      this.programOutputAddForm.value.id = Number(this.editingProgramOutput.id);
      this.transport.put("program-outputs/", String(this.editingProgramOutput.id), this.programOutputAddForm.value).then((programOutput: ProgramOutput) => {
        this.editingProgramOutput.name = programOutput.name;
        this.editingProgramOutput.info = programOutput.info;
        this.editingProgramOutput.activity_ref = programOutput.activity_ref;
        this.closeProgramOutputAdd();
      })
    }
  }

  deleteTargetDescription(targetDescriptionToDelete, event) {
    event.preventDefault();
    this.transport.delete("target-descriptions/", String(this.editingTargetDescription.id)).then(res => {
      this.editingTargetDescriptionSubject.targetDescription = null;
      this.closeProgramOutputAdd();
    }, error => { console.error(error) });
  }
  deleteOutput(outputToDelete, event) {
    event.preventDefault();
    if (outputToDelete.id) {
      this.transport.delete("program-outputs/", String(outputToDelete.id)).then(res => {
        // this.transport.get("program-outputs/?program_ref=" + this.id).then((programOutputData) => {
        //   this.programOutputs = programOutputData.results;
        this.programOutputs.splice(this.programOutputs.indexOf(outputToDelete), 1)
        this.closeProgramOutputAdd();
        // });
      }, error => { console.error(error) });
    } else {
      this.programOutputs.splice(this.programOutputs.indexOf(outputToDelete), 1)
    }
  }
  deleteShortOutcome(outcomeToDelete, event) {
    event.preventDefault();
      if (outcomeToDelete.id) {
        this.transport.delete("program-short-outcomes/", String(outcomeToDelete.id)).then(res => {
        this.programShortOutcomes.splice(this.programShortOutcomes.indexOf(outcomeToDelete), 1)
        // this.transport.get("program-short-outcomes/?program_ref=" + this.id).then((programShortOutcomesData) => {
        //   this.programShortOutcomes = programShortOutcomesData.results;
          
        this.closeShortProgramOutcomeAdd();
        // });
      }, error => { console.error(error) });
    } else {
      this.programShortOutcomes.splice(this.programShortOutcomes.indexOf(outcomeToDelete), 1)
    }
  }
  deleteMidOutcome(outcomeToDelete, event) {
    event.preventDefault();
    if (outcomeToDelete.id) {
      this.transport.delete("program-mid-outcomes/", String(outcomeToDelete.id)).then(res => {
        // this.transport.get("program-mid-outcomes/?program_ref=" + this.id).then((programMidOutcomesData) => {
        //   this.programMidOutcomes = programMidOutcomesData.results;
        this.programMidOutcomes.splice(this.programMidOutcomes.indexOf(outcomeToDelete), 1)
        this.closeMidProgramOutcomeAdd();
        // });
      }, error => { console.error(error) });
    } else 
      this.programMidOutcomes.splice(this.programMidOutcomes.indexOf(outcomeToDelete), 1)
  }
  deleteImpact(outcomeToDelete, event) {
    event.preventDefault();
    if (outcomeToDelete.id)
      this.transport.delete("program-impacts/", String(outcomeToDelete.id)).then(res => {
        // this.transport.get("program-impacts/?program_ref=" + this.id).then((programMidOutcomesData) => {
        //   this.programImpacts = programMidOutcomesData.results;
        this.programImpacts.splice(this.programImpacts.indexOf(outcomeToDelete), 1)
        this.closeProgramImpactAdd();
        // });
      }, error => { console.error(error) });
    else this.programImpacts.splice(this.programImpacts.indexOf(outcomeToDelete), 1) 
  }
  deleteActivity(outcomeToDelete, event) {
    event.preventDefault();
    this.transport.delete("activities/", String(outcomeToDelete.id)).then(res => {
      this.transport.get("activities/?program_ref=" + this.id).then((programMidOutcomesData) => {
        this.activities = programMidOutcomesData.results;
        this.closeActivityAdd();
      });
    }, error => { console.error(error) });
  }

  onProgramShortOutcomeAdd() {
    this.programShortOutcomeAddForm.value.program_ref = Number(this.id);
    if (!this.editingShortProgramOutcome) {
      this.transport.post("program-short-outcomes/", this.programShortOutcomeAddForm.value).then((programShortOutcome: ProgramShortOutcome) => {
        this.programShortOutcomes.push(programShortOutcome);

      }, error => { console.dir(error) });
      this.closeShortProgramOutcomeAdd();
    } else {

      this.programShortOutcomeAddForm.value.id = Number(this.editingShortProgramOutcome.id);
      this.transport.put("program-short-outcomes/", String(this.editingShortProgramOutcome.id), this.programShortOutcomeAddForm.value).then((programOutput: ProgramShortOutcome) => {
        this.editingShortProgramOutcome.name = programOutput.name;
        this.editingShortProgramOutcome.info = programOutput.info;
        this.editingShortProgramOutcome.program_output_ref = programOutput.program_output_ref;
        this.editingShortProgramOutcome.program_output_many_refs = programOutput.program_output_many_refs;
        this.closeShortProgramOutcomeAdd();
      });
    }
  }
  onProgramMidOutcomeAdd() {
    this.programMidOutcomeAddForm.value.program_ref = Number(this.id);
    if (!this.editingMidProgramOutcome) {
      this.transport.post("program-mid-outcomes/", this.programMidOutcomeAddForm.value).then((programMidOutcome: ProgramMidOutcome) => {
        this.programMidOutcomes.push(programMidOutcome);


      }, error => { console.dir(error) });
      this.closeMidProgramOutcomeAdd();
    } else {
      // this.programMidOutcomeAddForm.value.program_short_outcome_ref = Number(this.programMidOutcomeAddForm.value.program_short_outcome_ref.id);
      this.programMidOutcomeAddForm.value.id = Number(this.editingMidProgramOutcome.id);
      this.transport.put("program-mid-outcomes/", String(this.editingMidProgramOutcome.id), this.programMidOutcomeAddForm.value).then((programOutput: ProgramMidOutcome) => {
        this.editingMidProgramOutcome.name = programOutput.name;
        this.editingMidProgramOutcome.info = programOutput.info;
        this.editingMidProgramOutcome.program_short_outcome_ref = programOutput.program_short_outcome_ref;
        this.editingMidProgramOutcome.program_short_outcome_many_refs = programOutput.program_short_outcome_many_refs;
        this.closeMidProgramOutcomeAdd();
      });
    }

  }
  onProgramImpactAdd() {
    this.programImpactAddForm.value.program_ref = Number(this.id);
    if (!this.editingProgramImpact) {
      this.transport.post("program-impacts/", this.programImpactAddForm.value).then((programImpact: ProgramImpact) => {
        this.programImpacts.push(programImpact);
        this.programImpactAddForm = this.fb.group({
          name: ['', Validators.required],
          program_mid_outcome_ref: [''],
          info: ['']
        });

      }, error => { console.dir(error) });
      this.closeProgramImpactAdd();
    } else {
      // this.programImpactAddForm.value.program_mid_outcome_ref = Number(this.programImpactAddForm.value.program_mid_outcome_ref.id);
      this.programImpactAddForm.value.id = Number(this.editingProgramImpact.id);
      this.transport.put("program-impacts/", String(this.editingProgramImpact.id), this.programImpactAddForm.value).then((programOutput: ProgramImpact) => {
        this.editingProgramImpact.name = programOutput.name;
        this.editingProgramImpact.info = programOutput.info;
        this.editingProgramImpact.program_mid_outcome_ref = programOutput.program_mid_outcome_ref;
        this.editingProgramImpact.program_mid_outcome_many_refs = programOutput.program_mid_outcome_many_refs;
        this.closeProgramImpactAdd();
      });
    }
  }

  goToLibrary(level) {
     
    let link = '/outcomes?programid=' + this.id + '&programresultlevel=' + level;

    var backReferenceIds: string = null;
    if (level == "program-short-outcomes") {
      var refsneeded = this.programShortOutcomeAddForm.value.program_output_many_refs;
      for (let index = 0; index < refsneeded.length; index++) {
        const refNeeded = refsneeded[index];
        if (index != 0)
          backReferenceIds += "+";
        backReferenceIds += refNeeded;
      }
    } else if (level == "program-mid-outcomes") {
      // backReferenceIds = this.programMidOutcomeAddForm.value.program_short_outcome_ref;
      var refsneeded = this.programMidOutcomeAddForm.value.program_short_outcome_many_refs;
      for (let index = 0; index < refsneeded.length; index++) {
        const refNeeded = refsneeded[index];
        if (index != 0)
          backReferenceIds += "+";
        backReferenceIds += refNeeded;
      }
    } else if (level == "program-impacts") {
      // backReferenceIds = this.programImpactAddForm.value.program_mid_outcome_ref;
      var refsneeded = this.programImpactAddForm.value.program_mid_outcome_many_refs;
      for (let index = 0; index < refsneeded.length; index++) {
        const refNeeded = refsneeded[index];
        if (index != 0)
          backReferenceIds += "+";
        backReferenceIds += refNeeded;
      }
    }

    if (backReferenceIds)
      link += "&programbackreferenceid=" + backReferenceIds;

    this.router.navigateByUrl(link);
  }

  addMplOutput(index = this.mplOutputs.length) {
    this.mplOutputs.splice(index, 0, new MplOutputs())
    this.mplOutputs[index].program_ref = this.program
    this.mplOutputs[index].sort_index = index
    this.createMplOutput()
  }
  addMplShortOutcome(index = this.mplShortOutcomes.length) {
    this.mplShortOutcomes.splice(index, 0, new MplShortOutcomes());
    this.mplShortOutcomes[index].program_ref = this.program
    this.mplShortOutcomes[index].sort_index = index
    this.createMplShortOutcome()
  }
  addMplMidOutcome(index = this.mplMidOutcomes.length) {
    this.mplMidOutcomes.splice(index, 0, new MplMidOutcomes());
    this.mplMidOutcomes[index].program_ref = this.program
    this.mplMidOutcomes[index].sort_index = index
    this.createMplMidOutcome()
  }
  addMplImpact(index = this.mplImpacts.length) {
    this.mplImpacts.splice(index, 0, new MplImpacts());
    this.mplImpacts[index].program_ref = this.program
    this.mplImpacts[index].sort_index = index
    this.createMplImpact()
  }

  addMflOutput(index = this.mflOutputs.length) {
    this.mflOutputs.splice(index, 0, new MflOutputs());
    this.mflOutputs[index].sort_index = index
    this.createMflOutput(this.mflOutputs[index])
  }
  addMflShortOutcome(index = this.mflShortOutcomes.length) {
    this.mflShortOutcomes.splice(index, 0, new MflShortOutcomes());
    this.mflShortOutcomes[index].sort_index = index
    this.createMflShortOutcome(this.mflShortOutcomes[index])
  }
  addMflMidOutcome(index = this.mflMidOutcomes.length) {
    this.mflMidOutcomes.splice(index, 0, new MflMidOutcomes());
    this.mflMidOutcomes[index].sort_index = index
    this.createMflMidOutcome(this.mflMidOutcomes[index])
  }
  addMflImpact(index = this.mflImpacts.length) {
    this.mflImpacts.splice(index, 0, new MflImpacts());
    this.mflImpacts[index].sort_index = index
    this.createMflImpact(this.mflImpacts[index])
  }
  outputShouldBeSelected(mplOutput, output) {
    if (!mplOutput.result_ref && output == null)
      return true;

    if (!mplOutput.result_ref)
      return false;

    if (mplOutput.result_ref.id == output)
      return true;
    return false;
  }

  createMplOutput(outcome?, save?) {
    if (save) {
      for (let item of this.mplOutputs) {
        if (!item.result_ref) {
          alert('Чтобы сохранить, заполните поле "Результат" во всех строках!')
          return
        }
      }
    }
    for (let i = outcome && outcome.sort_index ? outcome.sort_index : 0; i < this.mplOutputs.length; i++) {
      let mplResult = this.mplOutputs[i]
      mplResult.program_ref = this.program.id;
      if (mplResult.result_ref) mplResult.result_ref = mplResult.result_ref.id;
      else continue
      mplResult.sort_index = i
      if (mplResult.id) {
        this.transport.put("mpl-outputs/", mplResult.id, mplResult).then((res: MplOutputs) => {
          this.mplOutputs[mplResult.sort_index] = res
          if (res.name) {
            let newMflOutput = new MflOutputs();
            let found = this.mflOutputs.find(el => el.mpl_ref == res.id);
            if (found) newMflOutput = found;
            else newMflOutput.sort_index = this.mflOutputs.length
            newMflOutput.indicator = mplResult.indicator;
            newMflOutput.mpl_ref = res.id;
            
            if (!found)
              this.mflOutputs.push(newMflOutput);
            this.createMflOutput(newMflOutput);
          }
        });
      } else {
        this.transport.post("mpl-outputs/", mplResult).then((res: MplOutputs) => {
          this.mplOutputs[mplResult.sort_index] = res

          let newMflOutput = new MflOutputs();
          newMflOutput.indicator = mplResult.indicator;
          newMflOutput.mpl_ref = res.id;
          newMflOutput.sort_index = this.mflOutputs.length
          this.mflOutputs.push(newMflOutput);
          this.createMflOutput(newMflOutput);
        });
      }
    }
  }
  createMplShortOutcome(outcome?, save?) { 
    if (save) {
      for (let item of this.mplShortOutcomes) {
        if (!item.result_ref) {
          alert('Чтобы сохранить, заполните поле "Результат" во всех строках!')
          return
        }
      }
    }
    for (let i = outcome && outcome.sort_index ? outcome.sort_index : 0; i < this.mplShortOutcomes.length; i++) {
      let mplResult = this.mplShortOutcomes[i]
      mplResult.program_ref = this.program.id;
      if (mplResult.result_ref) mplResult.result_ref = mplResult.result_ref.id;
      else continue
      mplResult.sort_index = i
      if (mplResult.id) {
        this.transport.put("mpl-short-outcomes/", mplResult.id, mplResult).then((res: MplShortOutcomes) => {
          this.mplShortOutcomes[mplResult.sort_index] = res
          if (res.name) {
            let newMfl = new MflShortOutcomes();
            let found = this.mflShortOutcomes.find(el => el.mpl_ref == res.id);
            if (found) newMfl = found;
            else newMfl.sort_index = this.mflShortOutcomes.length
            newMfl.indicator = mplResult.indicator;
            newMfl.mpl_ref = res.id;
            
            if (!found)
              this.mflShortOutcomes.push(newMfl);
            this.createMflShortOutcome(newMfl);
          }
        }).catch(error => console.log(error));
      } else {
        this.transport.post("mpl-short-outcomes/", mplResult).then((res: MplShortOutcomes) => {
          this.mplShortOutcomes[mplResult.sort_index] = res
          let newMfl = new MflShortOutcomes();
          newMfl.indicator = mplResult.indicator;
          newMfl.mpl_ref = res.id;
          newMfl.sort_index = this.mflShortOutcomes.length
          this.mflShortOutcomes.push(newMfl);
          this.createMflShortOutcome(newMfl);
        }).catch(error => console.log(error));
      }
    }
    // console.log(this.mplShortOutcomes)
  }
  createMplMidOutcome(outcome?, save?) { 
    if (save) {
      for (let item of this.mplMidOutcomes) {
        if (!item.result_ref) {
          alert('Чтобы сохранить, заполните поле "Результат" во всех строках!')
          return
        }
      }
    }
    for (let i = outcome && outcome.sort_index ? outcome.sort_index : 0; i < this.mplMidOutcomes.length; i++) {
      let mplResult = this.mplMidOutcomes[i]
      mplResult.program_ref = this.program.id;
      if (mplResult.result_ref) mplResult.result_ref = mplResult.result_ref.id;
      else continue
      mplResult.sort_index = i
      if (mplResult.id) {
        this.transport.put("mpl-mid-outcomes/", mplResult.id, mplResult).then((res: MplMidOutcomes) => {
          this.mplMidOutcomes[mplResult.sort_index] = res
          if (res.name) {
            let newMfl = new MflMidOutcomes();
            let found = this.mflMidOutcomes.find(el => el.mpl_ref == res.id);
            if (found) newMfl = found;
            else newMfl.sort_index = this.mflMidOutcomes.length
            newMfl.indicator = mplResult.indicator;
            newMfl.mpl_ref = res.id;
            
            if (!found)
              this.mflMidOutcomes.push(newMfl);
            this.createMflMidOutcome(newMfl);
          }
        }).catch(error => console.log(error));
      } else {
        this.transport.post("mpl-mid-outcomes/", mplResult).then((res: MplMidOutcomes) => {
          this.mplMidOutcomes[mplResult.sort_index] = res
          
          let newMfl = new MflMidOutcomes();
          newMfl.indicator = mplResult.indicator;
          newMfl.mpl_ref = res.id;
          newMfl.sort_index = this.mflMidOutcomes.length
          this.mflMidOutcomes.push(newMfl);
          this.createMflMidOutcome(newMfl);
        }).catch(error => console.log(error));
      }
    }
  }
  createMplImpact(outcome?, save?) {
    if (save) {
      for (let item of this.mplImpacts) {
        if (!item.result_ref) {
          alert('Чтобы сохранить, заполните поле "Результат" во всех строках!')
          return
        }
      }
    }
    for (let i = outcome && outcome.sort_index ? outcome.sort_index : 0; i < this.mplImpacts.length; i++) {
      let mplResult = this.mplImpacts[i]
      mplResult.program_ref = this.program.id;
      if (mplResult.result_ref) mplResult.result_ref = mplResult.result_ref.id;
      else continue
      mplResult.sort_index = i
      if (mplResult.id) {


        this.transport.put("mpl-impacts/", mplResult.id, mplResult).then((res: MplImpacts) => {
          this.mplImpacts[mplResult.sort_index] = res
          if (res.name) {
            let newMfl = new MflImpacts();
            let found = this.mflImpacts.find(el => el.mpl_ref == res.id);
            if (found) newMfl = found;
            else newMfl.sort_index = this.mflImpacts.length

            newMfl.indicator = mplResult.indicator;
            newMfl.mpl_ref = res.id;
            if (!found)
              this.mflImpacts.push(newMfl);
            this.createMflImpact(newMfl);
          }
        });
      } else {
        this.transport.post("mpl-impacts/", mplResult).then((res: MplImpacts) => {
          this.mplImpacts[mplResult.sort_index] = res
          let newMfl = new MflImpacts();
          newMfl.indicator = mplResult.indicator;
          newMfl.mpl_ref = res.id;
          newMfl.sort_index = this.mflImpacts.length
          this.mflImpacts.push(newMfl);
          this.createMflImpact(newMfl);
        });
      }
    }
    // this.transport.get("mpl-impacts/?program_ref=" + this.id).then((mplImpactsData) => {
    //   this.mplImpacts = mplImpactsData.results;
    // });
  }

  createMflOutput(line?) {
    for (let i = line && line.sort_index ? line.sort_index : 0; i < this.mflOutputs.length; i++) {
      const mflResult = this.mflOutputs[i]
      mflResult.sort_index = i
      mflResult.program_ref = this.program.id;
      if (mflResult.id) {
        this.transport.put("mfl-outputs/", String(mflResult.id), mflResult).then((res: MflOutputs) => {
          this.mflOutputs[i] = res
        });
      } else {
        this.transport.post("mfl-outputs/", mflResult).then((res: MflOutputs) => {
          this.mflOutputs[i] = res
        });
      }
    }
  }
  createMflShortOutcome(line?) {
    for (let i = line && line.sort_index ? line.sort_index : 0; i < this.mflShortOutcomes.length; i++) {
      const mflResult = this.mflShortOutcomes[i]
      mflResult.sort_index = i
      mflResult.program_ref = this.program.id;
      if (mflResult.id) {
        this.transport.put("mfl-short-outcomes/", String(mflResult.id), mflResult).then((res: MflShortOutcomes) => {
          this.mflShortOutcomes[i] = res
        });
      } else {
        this.transport.post("mfl-short-outcomes/", mflResult).then((res: MflShortOutcomes) => {
          this.mflShortOutcomes[i] = res
        });
      }
    }
  }
  createMflMidOutcome(line?) {
    for (let i = line && line.sort_index ? line.sort_index : 0; i < this.mflMidOutcomes.length; i++) {
      const mflResult = this.mflMidOutcomes[i]
      mflResult.sort_index = i
      mflResult.program_ref = this.program.id;
      if (mflResult.id) {
        this.transport.put("mfl-mid-outcomes/", String(mflResult.id), mflResult).then((res: MflMidOutcomes) => {
          this.mflMidOutcomes[i] = res
        });
      } else {
        this.transport.post("mfl-mid-outcomes/", mflResult).then((res: MflMidOutcomes) => {
          this.mflMidOutcomes[i] = res
        });
      }
    }
  }
  createMflImpact(line?) {
    for (let i = line && line.sort_index ? line.sort_index : 0; i < this.mflImpacts.length; i++) {
      const mflResult = this.mflImpacts[i]
      mflResult.sort_index = i
      mflResult.program_ref = this.program.id;
      if (mflResult.id) {
        this.transport.put("mfl-short-outcomes/", String(mflResult.id), mflResult).then((res: MflImpacts) => {
          this.mflImpacts[i] = res
        });
      } else {
        this.transport.post("mfl-short-outcomes/", mflResult).then((res: MflImpacts) => {
          this.mflImpacts[i] = res
        });
      }
    }
  }

  changeOutputRef(mplResult, event, createUpdateFunction) {
    for (var programOutput of this.programOutputs) {
      if (programOutput.id == event.target.value) {
        mplResult.result_ref = programOutput;
        if (createUpdateFunction == "output")
          this.createMplOutput(mplResult);
        if (createUpdateFunction == "shortoutcome")
          this.createMplShortOutcome(mplResult);
        if (createUpdateFunction == "midoutcome")
          this.createMplMidOutcome(mplResult);
        return;
      }
    }
  }

  changeShortOutcomeRef(mplResult, event, createUpdateFunction) {
    for (var programShortOutcome of this.programShortOutcomes) {
      if (programShortOutcome.id == event.target.value) {
        mplResult.result_ref = programShortOutcome;
        if (createUpdateFunction == "output")
          this.createMplOutput(mplResult);
        if (createUpdateFunction == "shortoutcome")
          this.createMplShortOutcome(mplResult);
        if (createUpdateFunction == "midoutcome")
          this.createMplMidOutcome(mplResult);
        return;
      }
    }
  }

  changeMidOutcomeRef(mplResult, event, createUpdateFunction) {
    for (var programMidOutcome of this.programMidOutcomes) {
      if (programMidOutcome.id == event.target.value) {
        mplResult.result_ref = programMidOutcome;
        if (createUpdateFunction == "output")
          this.createMplOutput(mplResult);
        if (createUpdateFunction == "shortoutcome")
          this.createMplShortOutcome(mplResult);
        if (createUpdateFunction == "midoutcome")
          this.createMplMidOutcome(mplResult);
        return;
      }
    }
  }

  changeImpactRef(mplResult, event, createUpdateFunction) {
    for (var programImpact of this.programImpacts) {
      if (programImpact.id == event.target.value) {
        mplResult.result_ref = programImpact;
        if (createUpdateFunction == "output")
          this.createMplOutput(mplResult);
        if (createUpdateFunction == "shortoutcome")
          this.createMplShortOutcome(mplResult);
        if (createUpdateFunction == "midoutcome")
          this.createMplMidOutcome(mplResult);
        if (createUpdateFunction == "impact")
          this.createMplImpact(mplResult);
        return;
      }
    }
  }

  changeName(mplResult, event, createUpdateFunction) {
    mplResult.name = event.target.value;
    if (createUpdateFunction == "output")
      this.createMplOutput(mplResult);
    if (createUpdateFunction == "shortoutcome")
      this.createMplShortOutcome(mplResult);
    if (createUpdateFunction == "midoutcome")
      this.createMplMidOutcome(mplResult);
    if (createUpdateFunction == "impact")
      this.createMplImpact(mplResult);
  }

  changeIndicator(mplResult, event, createUpdateFunction) {
    mplResult.indicator = event.target.value;
    if (createUpdateFunction == "output")
      this.createMplOutput(mplResult);
    if (createUpdateFunction == "shortoutcome")
      this.createMplShortOutcome(mplResult);
    if (createUpdateFunction == "midoutcome")
      this.createMplMidOutcome(mplResult);
    if (createUpdateFunction == "impact")
      this.createMplImpact(mplResult);
  }

  changeMethod(mplResult, event, createUpdateFunction) {
    mplResult.method = event.target.value;
    if (createUpdateFunction == "output")
      this.createMplOutput(mplResult);
    if (createUpdateFunction == "shortoutcome")
      this.createMplShortOutcome(mplResult);
    if (createUpdateFunction == "midoutcome")
      this.createMplMidOutcome(mplResult);
    if (createUpdateFunction == "impact")
      this.createMplImpact(mplResult);
  }

  changeTool(mplResult, event, createUpdateFunction) {
    let value: any[] = event.target.value.split('$$$')
    mplResult.tool = value[0];
    mplResult.tool_type = value[1];
    if (createUpdateFunction == "output")
      this.createMplOutput(mplResult);
    if (createUpdateFunction == "shortoutcome")
      this.createMplShortOutcome(mplResult);
    if (createUpdateFunction == "midoutcome")
      this.createMplMidOutcome(mplResult);
    if (createUpdateFunction == "impact")
      this.createMplImpact(mplResult);
  }

  changeFrequency(mplResult, event, createUpdateFunction) {
    mplResult.frequency = event.target.value;
    if (createUpdateFunction == "output")
      this.createMplOutput(mplResult);
    if (createUpdateFunction == "shortoutcome")
      this.createMplShortOutcome(mplResult);
    if (createUpdateFunction == "midoutcome")
      this.createMplMidOutcome(mplResult);
    if (createUpdateFunction == "impact")
      this.createMplImpact(mplResult);
  }

  changeReporting(mplResult, event, createUpdateFunction) {
    mplResult.reporting = event.target.value;
    if (createUpdateFunction == "output")
      this.createMplOutput(mplResult);
    if (createUpdateFunction == "shortoutcome")
      this.createMplShortOutcome(mplResult);
    if (createUpdateFunction == "midoutcome")
      this.createMplMidOutcome(mplResult);
    if (createUpdateFunction == "impact")
      this.createMplImpact(mplResult);
  }

  setDisplayResultRef(result: any) {
    result.displayResultRef = true;
    result.displayName = false;
    result.displayIndicator = false;
    result.displayMethod = false;
    result.displayTool = false;
    result.displayFrequency = false;
    result.displayReporting = false;
  }

  setDisplayName(result: any) {
    result.displayResultRef = false;
    result.displayName = true;
    result.displayIndicator = false;
    result.displayMethod = false;
    result.displayTool = false;
    result.displayFrequency = false;
    result.displayReporting = false;
  }

  setDisplayIndicator(result: any) {
    result.displayResultRef = false;
    result.displayName = false;
    result.displayIndicator = true;
    result.displayMethod = false;
    result.displayTool = false;
    result.displayFrequency = false;
    result.displayReporting = false;
  }

  setDisplayMethod(result: any) {
    result.displayResultRef = false;
    result.displayName = false;
    result.displayIndicator = false;
    result.displayMethod = true;
    result.displayTool = false;
    result.displayFrequency = false;
    result.displayReporting = false;
  }

  setDisplayTool(result: any) {
    if (result.tool_url) {
      window.open(result.tool_url, "_blank");
    }
    result.displayResultRef = false;
    result.displayName = false;
    result.displayIndicator = false;
    result.displayMethod = false;
    result.displayTool = true;
    result.displayFrequency = false;
    result.displayReporting = false;
  }

  setDisplayFrequency(result: any) {
    result.displayResultRef = false;
    result.displayName = false;
    result.displayIndicator = false;
    result.displayMethod = false;
    result.displayTool = false;
    result.displayFrequency = true;
    result.displayReporting = false;
  }

  setDisplayReporting(result: any) {
    result.displayResultRef = false;
    result.displayName = false;
    result.displayIndicator = false;
    result.displayMethod = false;
    result.displayTool = false;
    result.displayFrequency = false;
    result.displayReporting = true;
  }

  indicatorChanged(result, event, resultName) {
    result.indicator = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  planChanged(result, event, resultName) {
    result.plan = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  period1Changed(result, event, resultName) {
    result.period1 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  fact1Changed(result, event, resultName) {
    result.fact1 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  period2Changed(result, event, resultName) {
    result.period2 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  fact2Changed(result, event, resultName) {
    result.fact2 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  period3Changed(result, event, resultName) {
    result.period3 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  fact3Changed(result, event, resultName) {
    result.fact3 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  period4Changed(result, event, resultName) {
    result.period4 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }
  fact4Changed(result, event, resultName) {
    result.fact4 = event.target.value;
    if (resultName == "output")
      this.createMflOutput(result);
    if (resultName == "shortoutcome")
      this.createMflShortOutcome(result);
    if (resultName == "midoutcome")
      this.createMflMidOutcome(result);
    if (resultName == "impact")
      this.createMflImpact(result);

  }

  makeHighlighted(target) {
    target.shouldBeHighlighted = true;

    for (var activity of this.activities) {
      if (activity.shouldBeHighlighted) continue;
      if (activity.target_ref && activity.target_ref.id == target.id) {
        activity.shouldBeHighlighted = true;
        for (var output of this.programOutputs) {
          if (output.shouldBeHighlighted) continue;
          if (output.activity_ref && output.activity_ref.id == activity.id) {
            output.shouldBeHighlighted = true;
            for (var shortOutcome of this.programShortOutcomes) {
              if (shortOutcome.shouldBeHighlighted) continue;
              if (shortOutcome.program_output_many_refs && shortOutcome.program_output_many_refs.some(el => el.id == output.id)) {
                shortOutcome.shouldBeHighlighted = true;
                for (var midOutcome of this.programMidOutcomes) {
                  if (midOutcome.shouldBeHighlighted) continue;
                  if (midOutcome.program_short_outcome_many_refs && midOutcome.program_short_outcome_many_refs.some(el => el.id == shortOutcome.id)) {
                    midOutcome.shouldBeHighlighted = true;
                    for (var impact of this.programImpacts) {
                      if (impact.shouldBeHighlighted) continue;
                      if (impact.program_mid_outcome_many_refs && impact.program_mid_outcome_many_refs.some(el => el.id == midOutcome.id)) {
                        impact.shouldBeHighlighted = true;
                      }
                      else {
                        impact.shouldBeHighlighted = false;
                      }
                    }
                  }
                  else {
                    midOutcome.shouldBeHighlighted = false;
                  }
                }
              }
              else {
                shortOutcome.shouldBeHighlighted = false;
              }
            }
          }
          else {
            output.shouldBeHighlighted = false;
          }
        }
      } else {
        activity.shouldBeHighlighted = false;
      }
    }
  }
  makeUnhighlighted(target) {
    target.shouldBeHighlighted = false;

    for (var activity of this.activities) {
      activity.shouldBeHighlighted = false;
    }
    for (var output of this.programOutputs) {
      output.shouldBeHighlighted = false;
    }
    for (var shortoutcome of this.programShortOutcomes) {
      shortoutcome.shouldBeHighlighted = false;
    }
    for (var midoutcome of this.programMidOutcomes) {
      midoutcome.shouldBeHighlighted = false;
    }
    for (var impact of this.programImpacts) {
      impact.shouldBeHighlighted = false;
    }
  }

  downloadProgram(event) {
    event.preventDefault();
    window.open(this.baseUrl+"newpion/api/download?program_id=" + this.id, "_blank");
  }

  downloadPlan(event) {
    event.preventDefault();

    window.open(this.baseUrl+"newpion/api/download-plan?program_id=" + this.id, "_blank");
  }
  downloadForm(event) {
    event.preventDefault();

    window.open(this.baseUrl+"newpion/api/download-form?program_id=" + this.id, "_blank");
  }

  downloadPlanAndForm(event) {
    event.preventDefault();
    window.open(this.baseUrl+"newpion/api/download-plan?program_id=" + this.id, "_blank");
    window.open(this.baseUrl+"newpion/api/download-form?program_id=" + this.id, "_blank");


  }

  mplOutputDelete(event, mplOutput) {
    event.preventDefault();
    this.mplOutputs.splice(this.mplOutputs.indexOf(mplOutput), 1)
    if (!mplOutput.id) return
    this.transport.delete("mpl-outputs/", String(mplOutput.id)).then(res => {
      this.createMplOutput()
      // for (let i = 0; i < this.mplOutputs.length; i++) {
      //   this.mplOutputs[i].sort_index = i
      //   this.mplOutputs[i].result_ref = this.mplOutputs[i].result_ref.id
      //   this.mplOutputs[i].program_ref = this.id
      //   this.transport.put('mpl-outputs/', this.mplOutputs[i].id, this.mplOutputs[i]).then(res => {
      //     // console.log(res)
      //   }).catch(error => console.log(error))
      // }

      // this.transport.get("mpl-outputs/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mplOutputs = mplOutputsData.results;
      // });
      // this.transport.get("mfl-outputs/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mflOutputs = mplOutputsData.results;
      // });
    }, error => { console.error(error) });
  }
  mplShortOutcomeDelete(event, mplShortOutcome) {
    event.preventDefault();
    this.mplShortOutcomes.splice(this.mplShortOutcomes.indexOf(mplShortOutcome), 1)
    if (!mplShortOutcome.id) return
    this.transport.delete("mpl-short-outcomes/", String(mplShortOutcome.id)).then(res => {
      this.createMplShortOutcome()
      // for (let i = 0; i < this.mplShortOutcomes.length; i++) {
      //   this.mplShortOutcomes[i].sort_index = i
      //   this.mplShortOutcomes[i].result_ref = this.mplShortOutcomes[i].result_ref.id
      //   this.mplShortOutcomes[i].program_ref = this.id
      //   this.transport.put('mpl-short-outcomes/', String(this.mplShortOutcomes[i].id), this.mplShortOutcomes[i]).then(res => {
      //     // console.log(res)
      //   }).catch(error => console.log(error))
      // }
      // this.transport.get("mpl-short-outcomes/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mplShortOutcomes = mplOutputsData.results;
      // });
      // this.transport.get("mfl-short-outcomes/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mflShortOutcomes = mplOutputsData.results;
      // });
    }, error => { console.error(error) });
  }
  mplMidOutcomeDelete(event, mplMidOutcome) {
    event.preventDefault();
    this.mplMidOutcomes.splice(this.mplMidOutcomes.indexOf(mplMidOutcome), 1)
    if (!mplMidOutcome.id) return
    this.transport.delete("mpl-mid-outcomes/", String(mplMidOutcome.id)).then(res => {
      this.createMplMidOutcome()
      // for (let i = 0; i < this.mplMidOutcomes.length; i++) {
      //   this.mplMidOutcomes[i].sort_index = i
      //   this.mplMidOutcomes[i].result_ref = this.mplMidOutcomes[i].result_ref.id
      //   this.mplMidOutcomes[i].program_ref = this.id
      //   this.transport.put('mpl-mid-outcomes/', this.mplMidOutcomes[i].id, this.mplMidOutcomes[i]).then(res => {
      //     // console.log(res)
      //   }).catch(error => console.log(error))
      // }
      // this.transport.get("mpl-mid-outcomes/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mplMidOutcomes = mplOutputsData.results;
      // });
      // this.transport.get("mfl-mid-outcomes/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mflMidOutcomes = mplOutputsData.results;
      // });
    }, error => { console.error(error) });
  }
  mplImpactDelete(event, mplImpact) {
    event.preventDefault();
    this.mplImpacts.splice(this.mplImpacts.indexOf(mplImpact), 1)
    if (!mplImpact.id) return
    this.transport.delete("mpl-impacts/", String(mplImpact.id)).then(res => {
      this.createMplImpact()
      // for (let i = 0; i < this.mplImpacts.length; i++) {
      //   this.mplImpacts[i].sort_index = i
      //   this.mplImpacts[i].result_ref = this.mplImpacts[i].result_ref.id
      //   this.mplImpacts[i].program_ref = this.id
      //   this.transport.put('mpl-impacts/', this.mplImpacts[i].id, this.mplImpacts[i]).then(res => {
      //     // console.log(res)
      //   }).catch(error => console.log(error))
      // }
      // this.transport.get("mpl-impacts/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mplImpacts = mplOutputsData.results;
      // });
      // this.transport.get("mfl-impacts/?program_ref=" + this.id).then((mplOutputsData) => {
      //   this.mflImpacts = mplOutputsData.results;
      // });
    }, error => { console.error(error) });
  }

  mflOutputDelete(event, mflOutput?) {
    if (!mflOutput) mflOutput = this.mplOutputs[this.mplOutputs.length - 1]
    event.preventDefault();
    this.mflOutputs.splice(this.mplOutputs.indexOf(mflOutput), 1)
    if (!mflOutput.id) return
    this.transport.delete("mfl-outputs/", String(mflOutput.id)).then(res => {
      this.createMflOutput()
    }, error => { console.error(error) });
  }
  mflShortOutcomeDelete(event, mflShortOutcome?) {
    if (!mflShortOutcome) mflShortOutcome = this.mplShortOutcomes[this.mplShortOutcomes.length - 1]
    event.preventDefault();
    this.mflShortOutcomes.splice(this.mflShortOutcomes.indexOf(mflShortOutcome), 1)
    if (!mflShortOutcome.id) return
    this.transport.delete("mfl-short-outcomes/", String(mflShortOutcome.id)).then(res => {
      this.createMflShortOutcome()
    }, error => { console.error(error) });
  }
  mflMidOutcomeDelete(event, mflMidOutcome?) {
    if (!mflMidOutcome) mflMidOutcome = this.mplMidOutcomes[this.mplMidOutcomes.length - 1]
    event.preventDefault();
    this.mflMidOutcomes.splice(this.mplMidOutcomes.indexOf(mflMidOutcome), 1)
    if (!mflMidOutcome.id) return
    this.transport.delete("mfl-mid-outcomes/", String(mflMidOutcome.id)).then(res => {
      this.createMflMidOutcome()
    }, error => { console.error(error) });
  }
  mflImpactDelete(event, mflImpact?) {
    if (!mflImpact) mflImpact = this.mplImpacts[this.mplImpacts.length - 1]
    event.preventDefault();
    this.mflImpacts.splice(this.mflImpacts.indexOf(mflImpact), 1)
    if (!mflImpact.id) return
    this.transport.delete("mfl-impacts/", String(mflImpact.id)).then(res => {
      this.createMflImpact()
    }, error => { console.error(error) });
  }

  deleteLastMplOutput(event) {
    this.mplOutputDelete(event, this.mplOutputs[this.mplOutputs.length - 1]);
  }
  deleteLastMplShortOutcome(event) {
    this.mplShortOutcomeDelete(event, this.mplShortOutcomes[this.mplShortOutcomes.length - 1]);
  }
  deleteLastMplMidOutcome(event) {
    this.mplMidOutcomeDelete(event, this.mplMidOutcomes[this.mplMidOutcomes.length - 1]);
  }
  deleteLastMplImpact(event) {
    this.mplImpactDelete(event, this.mplImpacts[this.mplImpacts.length - 1]);
  }

  printAt(context , text, x, y, lineHeight, fitWidth) {
    fitWidth = fitWidth || 0;
    
    if (fitWidth <= 0)
    {
         context.fillText( text, x, y );
        return;
    }
    
    for (var idx = 1; idx <= text.length; idx++)
    {
        var str = text.substr(0, idx);
        console.log(str, context.measureText(str).width, fitWidth);
        if (context.measureText(str).width > fitWidth)
        {
            context.fillText( text.substr(0, idx-1), x, y );
            this.printAt(context, text.substr(idx-1), x, y + lineHeight, lineHeight,  fitWidth);
            return;
        }
    }
    context.fillText( text, x, y );
  }

  draw(scale, translatePos) {
    if (this.toLoad > 0) {
      setTimeout(() => { this.draw(scale, translatePos) }, 1000);
      return;
    }
    // canvas sizes
    var cwidth = 851;
    var cheight = 500;

    var ltpx = -(cwidth / 2.0);
    var ltpy = -(cheight / 2.0);

    // colors

    // Целевая группа 
    var targetFill = "#9ee8f4";
    var targetBorder = "#45c6db";

    // Активность
    var activityFill = "#adfbdd";
    var activityBorder = "#2ca978";

    // Непосредственный результат
    var outputFill = "#fee6b1";
    var outputBorder = "#ee860b";

    // Краткосрочный социальный результат
    var shortOutcomeFill = "#f3c9ee";
    var shortOutcomeBorder = "#bf44af";

    // Среднесрочный социальный результат
    var midOutcomeFill = "#c1b9f4";
    var midOutcomeBorder = "#6a5faf";

    // Социальный эффект
    var impactFill = "#f4c2b9";
    var impactBorder = "#ff330b";

    var canvas: any = document.getElementById("np-canvas");
    var context = canvas.getContext("2d");

    // clear canvas
    // work with zooming, do not touch
    context.clearRect(0, 0, canvas.width, canvas.height);

    context.save();
    context.translate(translatePos.x, translatePos.y);
    context.scale(scale, scale);
    //  end of work with zooming, do not touch

    // border of initiating canvas. for debug only
    context.strokeStyle = "#000000";
    context.strokeRect(ltpx - 1, ltpy - 1, cwidth + 2, cheight + 2);

    var i = 0;
    context.strokeStyle = impactBorder;
    context.strokeRect(ltpx, ltpy + (cheight / 6.0) * i, cwidth, cheight / 6.0);
    context.strokeRect(ltpx + (cheight / 18.0), ltpy + (cheight / 6.0) * i + (cheight / 18.0), cwidth - (cheight / 9.0), cheight / 18.0);
    var impactY = ltpy + (cheight / 6.0) * i + (cheight / 18.0);

    i += 1;
    context.strokeStyle = midOutcomeBorder;
    context.strokeRect(ltpx, ltpy + (cheight / 6.0) * i, cwidth, cheight / 6.0);
    context.strokeRect(ltpx + (cheight / 18.0), ltpy + (cheight / 6.0) * i + (cheight / 18.0), cwidth - (cheight / 9.0), cheight / 18.0);
    var midOutcomeY = ltpy + (cheight / 6.0) * i + (cheight / 18.0);

    i += 1;
    context.strokeStyle = shortOutcomeBorder;
    context.strokeRect(ltpx, ltpy + (cheight / 6.0) * i, cwidth, cheight / 6.0);
    context.strokeRect(ltpx + (cheight / 18.0), ltpy + (cheight / 6.0) * i + (cheight / 18.0), cwidth - (cheight / 9.0), cheight / 18.0);
    var shortOutcomeY = ltpy + (cheight / 6.0) * i + (cheight / 18.0);

    i += 1;
    context.strokeStyle = outputBorder;
    context.strokeRect(ltpx, ltpy + (cheight / 6.0) * i, cwidth, cheight / 6.0);
    context.strokeRect(ltpx + (cheight / 18.0), ltpy + (cheight / 6.0) * i + (cheight / 18.0), cwidth - (cheight / 9.0), cheight / 18.0);
    var outputY = ltpy + (cheight / 6.0) * i + (cheight / 18.0);

    i += 1;
    context.strokeStyle = activityBorder;
    context.strokeRect(ltpx, ltpy + (cheight / 6.0) * i, cwidth, cheight / 6.0);
    context.strokeRect(ltpx + (cheight / 18.0), ltpy + (cheight / 6.0) * i + (cheight / 18.0), cwidth - (cheight / 9.0), cheight / 18.0);
    var activityY = ltpy + (cheight / 6.0) * i + (cheight / 18.0);

    i += 1;
    context.strokeStyle = targetBorder;
    context.strokeRect(ltpx, ltpy + (cheight / 6.0) * i, cwidth, cheight / 6.0);
    context.strokeRect(ltpx + (cheight / 18.0), ltpy + (cheight / 6.0) * i + (cheight / 18.0), cwidth - (cheight / 9.0), cheight / 18.0);
    var targetY = ltpy + (cheight / 6.0) * i + (cheight / 18.0);
    // end of border of initiating canvas. for debug only

    // data

    // var outcomes:Outcome[] = [
    //   new Outcome() {name: 'Улучшение эмоционального состояния ребенка'},
    //   {name: 'Повышен уровень социально-бытовой адаптации'},
    //   {name: 'Улучшение внутрисемейных отношений, включая детско-родительские отношения'},
    // ];

    var anyX = ltpx + (cheight / 18.0);
    var anyHeight = cheight / 18.0;
    var lineWidth = cwidth - (cheight / 9.0);
    // end of data

    if (this.programImpacts) {
      for (let index = 0; index < this.programImpacts.length; index++) {
        const impact = this.programImpacts[index];
        
        context.strokeStyle = impactBorder;
        context.fillStyle = impactFill;

        var rectX = 5 + anyX + index * (lineWidth / this.programImpacts.length);
        var rectY = impactY;
        var rectHeight = anyHeight;
        var rectWidth = (lineWidth / this.programImpacts.length)-10;

        this.roundRect(context, rectX, rectY, rectWidth, rectHeight, 3, true, true);

        context.textAlign="center"; 
        context.textBaseline = "top";
        context.fillStyle = "#000000";
        context.font = "3px sans-serif";
        // var fontSize = 24;
        // while(fontSize > 1)
        // {
        //   context.font = "" + fontSize + "px sans-serif";
        //   if (context.measureText(impact.name).width < rectWidth)
        //   {
        //     break;
        //   }
        //   fontSize -= 1;
        // }

        var textToFill = impact.name;

        // if (fontSize == 1)
        // {
        //   while(context.measureText(textToFill).width > rectWidth) {
        //     textToFill = textToFill.substr(0, textToFill.length - 1);
        //   }
        // }
        this.printAt(context, textToFill, rectX+(rectWidth/2), rectY, rectHeight/7, rectWidth);
        // context.fillText(textToFill/*.substr(0, 125/this.programImpacts.length)*/, rectX+(rectWidth/2),rectY+(rectHeight/2));
      }
    }

    if (this.programMidOutcomes) {
      for (let index = 0; index < this.programMidOutcomes.length; index++) {
        const midOutcome = this.programMidOutcomes[index];

        context.strokeStyle = midOutcomeBorder;
        context.fillStyle = midOutcomeFill;
        
        var rectX = 5 + anyX + index * (lineWidth / this.programMidOutcomes.length);
        var rectY = midOutcomeY;
        var rectHeight = anyHeight;
        var rectWidth = (lineWidth / this.programMidOutcomes.length)-10;

        this.roundRect(context, rectX, rectY, rectWidth, rectHeight, 3, true, true);

        context.textAlign="center"; 
        //context.textBaseline = "middle";
        context.fillStyle = "#000000";

        // var fontSize = 24;
        // while(fontSize > 1)
        // {
        //   context.font = "" + fontSize + "px sans-serif";
        //   if (context.measureText(midOutcome.name).width < rectWidth)
        //   {
        //     break;
        //   }
        //   fontSize -= 1;
        // }

        var textToFill = midOutcome.name;

        // if (fontSize == 1)
        // {
        //   while(context.measureText(textToFill).width > rectWidth) {
        //     textToFill = textToFill.substr(0, textToFill.length - 1);
        //   }
        // }
        this.printAt(context, textToFill, rectX+(rectWidth/2), rectY, rectHeight/7, rectWidth);

        // context.fillText(textToFill/*.substr(0, 125/this.programMidOutcomes.length)*/, rectX+(rectWidth/2),rectY+(rectHeight/2));
      }
    }
    
    if (this.programShortOutcomes) {
      for (let index = 0; index < this.programShortOutcomes.length; index++) {
        const shortOutcome = this.programShortOutcomes[index];
        
        context.strokeStyle = shortOutcomeBorder;
        context.fillStyle = shortOutcomeFill;
        
        var rectX = 5 + anyX + index * (lineWidth / this.programShortOutcomes.length);
        var rectY = shortOutcomeY;
        var rectHeight = anyHeight;
        var rectWidth = (lineWidth / this.programShortOutcomes.length)-10;

        this.roundRect(context, rectX, rectY, rectWidth, rectHeight, 3, true, true);

        context.textAlign="center"; 
        //context.textBaseline = "middle";
        context.fillStyle = "#000000";

        // var fontSize = 24;
        // while(fontSize > 1)
        // {
        //   context.font = "" + fontSize + "px sans-serif";
        //   if (context.measureText(shortOutcome.name).width < rectWidth)
        //   {
        //     break;
        //   }
        //   fontSize -= 1;
        // }

        var textToFill = shortOutcome.name;

        // if (fontSize == 1)
        // {
        //   while(context.measureText(textToFill).width > rectWidth) {
        //     textToFill = textToFill.substr(0, textToFill.length - 1);
        //   }
        // }
        this.printAt(context, textToFill, rectX+(rectWidth/2), rectY, rectHeight/7, rectWidth);
        // context.fillText(textToFill/*.substr(0, 125/this.programShortOutcomes.length)*/, rectX+(rectWidth/2),rectY+(rectHeight/2));
      }
    }
    
    for (let index = 0; index < this.programOutputs.length; index++) {
      const output = this.programOutputs[index];
      
      context.strokeStyle = outputBorder;
      context.fillStyle = outputFill;

      var rectX = 5 + anyX + index * (lineWidth / this.programOutputs.length);
      var rectY = outputY;
      var rectHeight = anyHeight;
      var rectWidth = (lineWidth / this.programOutputs.length)-10;

      this.roundRect(context, rectX, rectY, rectWidth, rectHeight, 3, true, true);

      context.textAlign="center"; 
      //context.textBaseline = "middle";
      context.fillStyle = "#000000";

      // var fontSize = 24;
      // while(fontSize > 1)
      // {
      //   context.font = "" + fontSize + "px sans-serif";
      //   if (context.measureText(output.name).width < rectWidth)
      //   {
      //     break;
      //   }
      //   fontSize -= 1;
      // }

      var textToFill = output.name;

      // if (fontSize == 1)
      // {
      //   while(context.measureText(textToFill).width > rectWidth) {
      //     textToFill = textToFill.substr(0, textToFill.length - 1);
      //   }
      // }
      this.printAt(context, textToFill, rectX+(rectWidth/2), rectY, rectHeight/7, rectWidth);
      // context.fillText(textToFill/*.substr(0, 125/this.programOutputs.length)*/, rectX+(rectWidth/2),rectY+(rectHeight/2));
    }
    
    if (this.activities) {
      for (let index = 0; index < this.activities.length; index++) {
        const activity = this.activities[index];
        
        context.strokeStyle = activityBorder;
        context.fillStyle = activityFill;

        var rectX = 5 + anyX + index * (lineWidth / this.activities.length);
        var rectY = activityY;
        var rectHeight = anyHeight;
        var rectWidth = (lineWidth / this.activities.length)-10;

        this.roundRect(context, rectX, rectY, rectWidth, rectHeight, 3, true, true);

        context.textAlign="center"; 
        //context.textBaseline = "middle";
        context.fillStyle = "#000000";

        // var fontSize = 24;
        // while(fontSize > 1)
        // {
        //   context.font = "" + fontSize + "px sans-serif";
        //   if (context.measureText(activity.name).width < rectWidth)
        //   {
        //     break;
        //   }
        //   fontSize -= 1;
        // }

        var textToFill = activity.name;

        // if (fontSize == 1)
        // {
        //   while(context.measureText(textToFill).width > rectWidth) {
        //     textToFill = textToFill.substr(0, textToFill.length - 1);
        //   }
        // }
        this.printAt(context, textToFill, rectX+(rectWidth/2), rectY, rectHeight/7, rectWidth);
        // context.fillText(textToFill/*.substr(0, 125/this.activities.length)*/, rectX+(rectWidth/2),rectY+(rectHeight/2));
      }
    }
    
    if (this.targets) {
      for (let index = 0; index < this.targets.length; index++) {
        const target = this.targets[index];
        
            context.strokeStyle = targetBorder;
            context.fillStyle = targetFill;
        
        var rectX = 5 + anyX + index * (lineWidth / this.targets.length);
        var rectY = targetY;
        var rectHeight = anyHeight;
        var rectWidth = (lineWidth / this.targets.length)-10;

        this.roundRect(context, rectX, rectY, rectWidth, rectHeight, 3, true, true);

        context.textAlign="center"; 
        //context.textBaseline = "middle";
        context.fillStyle = "#000000";

        // var fontSize = 24;
        // while(fontSize > 1)
        // {
        //   context.font = "" + fontSize + "px sans-serif";
        //   if (context.measureText(target.name).width < rectWidth)
        //   {
        //     break;
        //   }
        //   fontSize -= 1;
        // }

        var textToFill = target.name;

        // if (fontSize == 1)
        // {
        //   while(context.measureText(textToFill).width > rectWidth) {
        //     textToFill = textToFill.substr(0, textToFill.length - 1);
        //   }
        // }
        this.printAt(context, textToFill, rectX+(rectWidth/2), rectY, rectHeight/7, rectWidth);
        // context.fillText(textToFill/*.substr(0, 125/this.targets.length)*/, rectX+(rectWidth/2),rectY+(rectHeight/2));
      }
    }


    // context.strokeStyle = "#0000ff";
    // context.fillStyle = "#aaaaee";

    // this.roundRect(context, -10, -10, 20, 20, 1, true, true);

    // context.fill();

    // context.lineWidth = 5;
    // context.strokeStyle = "#0000ff";
    // context.stroke();
    context.restore();
  }

  roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    if (typeof stroke === 'undefined') {
      stroke = true;
    }
    if (typeof radius === 'undefined') {
      radius = 5;
    }
    if (typeof radius === 'number') {
      radius = { tl: radius, tr: radius, br: radius, bl: radius };
    } else {
      var defaultRadius = { tl: 0, tr: 0, br: 0, bl: 0 };
      for (var side in defaultRadius) {
        radius[side] = radius[side] || defaultRadius[side];
      }
    }
    ctx.beginPath();
    ctx.moveTo(x + radius.tl, y);
    ctx.lineTo(x + width - radius.tr, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
    ctx.lineTo(x + width, y + height - radius.br);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
    ctx.lineTo(x + radius.bl, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
    ctx.lineTo(x, y + radius.tl);
    ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    ctx.closePath();
    if (fill) {
      ctx.fill();
    }
    if (stroke) {
      ctx.stroke();
    }
  }

  select(outcome) {
    let elSelectNative: any = document.getElementsByClassName("js-selectNative")[0];
    let elSelectCustom: any = document.getElementsByClassName("js-selectCustom")[0];
    let elSelectCustomBox: any = elSelectCustom.children[0];
    let elSelectCustomOpts: any = elSelectCustom.children[1];
    let customOptsList: any[] = Array.from(elSelectCustomOpts.children);

    let optionChecked = "";
    let optionHoveredIndex = -1;

    
    const isClosed = !elSelectCustom.classList.contains("isActive");

    if (isClosed) {
      openSelectCustom();
    } else {
      closeSelectCustom();
    }
    

    function openSelectCustom() {
      elSelectCustom.classList.add("isActive");
      elSelectCustom.setAttribute("aria-hidden", 'false');
      if (optionChecked) {
        const optionCheckedIndex = customOptsList.findIndex(
        (el: any) => el.getAttribute("data-value") === optionChecked);
        updateCustomSelectHovered(optionCheckedIndex);
      }
      document.addEventListener("click", watchClickOutside);
    }

    function closeSelectCustom() {
      elSelectCustom.classList.remove("isActive");
      elSelectCustom.setAttribute("aria-hidden", 'true');
      updateCustomSelectHovered(-1);
      document.removeEventListener("click", watchClickOutside);
    }

    function updateCustomSelectHovered(newIndex) {
      const prevOption = elSelectCustomOpts.children[optionHoveredIndex];
      const option = elSelectCustomOpts.children[newIndex];

      if (prevOption)prevOption.classList.remove("isHover");
      if (option) option.classList.add("isHover");

      optionHoveredIndex = newIndex;
    }

    function updateCustomSelectChecked(value, text) {
      const prevValue = optionChecked;

      const elPrevOption = elSelectCustomOpts.querySelector(`[data-value="${prevValue}"`);

      const elOption = elSelectCustomOpts.querySelector(`[data-value="${value}"`);

      if (elPrevOption) elPrevOption.classList.remove("isActive");
    
      if (elOption) elOption.classList.add("isActive");
      elSelectCustomBox.textContent = text;
      optionChecked = value;
    }

    function watchClickOutside(e: any) {
      const didClickedOutside: any = !elSelectCustom.contains(event.target);
      if (didClickedOutside) {
        closeSelectCustom();
      }
    }

    // // Update selectCustom value when selectNative is changed.
    elSelectNative.addEventListener("change", (e: any) => {
      const value = e.target.value ? e.target.value :  elSelectNative.value ? elSelectNative.value : outcome.method;
      const elRespectiveCustomOption = elSelectCustomOpts.querySelector(
      `[data-value="${value}"]`);

      updateCustomSelectChecked(value, elRespectiveCustomOption ? elRespectiveCustomOption.textContent : 'null');
    });

    // Update selectCustom value when an option is clicked or hovered
    customOptsList.forEach(function (elOption: any, index) {
      elOption.addEventListener("click", (e: any) => {
        const value = e.target.getAttribute("data-value");
        // Sync native select to have the same value
        elSelectNative.value = value;
        elSelectNative.dispatchEvent(new Event('change'))
        unselect()
        updateCustomSelectChecked(value, e.target.textContent);
        closeSelectCustom();
      });

      elOption.addEventListener("mouseenter", e => {
        updateCustomSelectHovered(index);
      });

      // TODO: Toggle these event listeners based on selectCustom visibility
    });

    function unselect() {
      elSelectCustom = elSelectCustom.cloneNode(true);
      elSelectNative = elSelectNative.cloneNode(true);
      elSelectCustomBox = elSelectCustomBox.cloneNode(true);
      elSelectCustomOpts = elSelectCustomOpts.cloneNode(true);
      for (let element of customOptsList) element = element.cloneNode(true);
    }
  }

  showShadow() {
    const elements = document.querySelectorAll('textarea.shadow_program_label, input.shadow_program_label')
    for (let i = 0; i < elements.length; i++) elements[i].classList.add('shadow_program')
  }

  hideShadow() {
    const elements = document.querySelectorAll('textarea.shadow_program_label, input.shadow_program_label')
    for (let i = 0; i < elements.length; i++) elements[i].classList.remove('shadow_program')
  }
  
  openNotification(isError) {
    const modalFactory = this.resolver.resolveComponentFactory(ShowModalComponent)

    this.refDir.containerRef.clear()
    const component = this.refDir.containerRef.createComponent(modalFactory)

    component.instance.error = isError

    component.instance.close.subscribe(ans => {
      if (ans) this.refDir.containerRef.clear()
    })
  }
}