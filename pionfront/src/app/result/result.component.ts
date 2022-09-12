import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TransportService } from '../services/transport.service';
import { Outcome } from '../models/outcome';
import { OutcomeName } from '../models/outcomename';
import { Target } from '../models/target';
import { Practice } from '../models/practice';
import { OutcomeIndicator } from '../models/outcomeindicator';
import { OutcomeMethod } from '../models/outcomemethod';
import { Tool } from '../models/tool';
import { EvaluationReport } from '../models/evaluationreport';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Program } from '../models/program';
import { ThematicGroup } from '../models/thematicgroup';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {

  id: string;
  outcome: Outcome;
  outcomeNames: OutcomeName[];
  outcomeIndicators: OutcomeIndicator[];
  targets: Target[];
  practices: Practice[];
  outcomeMethods: OutcomeMethod[];
  toLoad: number = 9;
  tools: Tool[]
  allTools: Tool[]
  reports: EvaluationReport[]
  thematicGroups: ThematicGroup[]

  programId: string;
  programBackReferenceId: string;
  programResultLevel:string;

  authenticated: boolean = false;

  indicatorForm: FormGroup
  toolForm: FormGroup
  programs: Program[]
  form: number = 0

  results = []
  mpl = []

  constructor(private activateRoute: ActivatedRoute,
    public transport: TransportService,
    public router: Router) {
    this.id = activateRoute.snapshot.params['id'];
  }

  ngOnInit(): void {
    if (this.transport.accessToken != null && this.transport.accessToken != undefined && this.transport.refreshToken != null && this.transport.refreshToken != undefined)
      this.authenticated = true;

    this.activateRoute.queryParamMap.subscribe(queryParams => {
      this.programId = queryParams.get('programid');
      this.programBackReferenceId = queryParams.get('programbackreferenceid');
      this.programResultLevel = queryParams.get('programresultlevel');
    })
    this.transport.getExact("outcomes", this.id, !this.authenticated).then((outcomeResult) => {
      this.outcome = outcomeResult;
      this.toLoad -= 1;
      this.transport.get("outcome-names/?outcome_ref=" + this.id, !this.authenticated).then((outcomeNames) => {
        this.outcomeNames = outcomeNames.results;
        this.toLoad -= 1;
      });
      this.transport.get("targets/", !this.authenticated).then((targetsResult) => {
        this.targets = targetsResult.results;
        for (var target in this.targets) {
          this.targets[target].current = this.outcome.target_refs.some(el => el.id == this.targets[target].id);
        }
        this.toLoad -= 1;
      });
      this.transport.get("practices/", !this.authenticated).then((practicesResult) => {
        this.practices = practicesResult.results;

        for (var practice in this.practices) {
          this.practices[practice].current = this.outcome.practice_refs.some(el => el.id == this.practices[practice].id);
        }
        this.toLoad -= 1;
      });
      this.transport.get("outcome-indicators/?outcome_ref=" + this.id, !this.authenticated).then((indicatorsResult) => {
        this.outcomeIndicators = indicatorsResult.results;

        this.toLoad -= 1;
      });

      this.transport.get("outcome-methods/?outcome_ref=" + this.id, !this.authenticated).then((methodsResult) => {
        this.outcomeMethods = methodsResult.results;
        this.toLoad -= 1;
      });
      this.transport.get("tools/?outcome_refs=" + this.id, !this.authenticated).then((toolsResult) => {
        this.tools = toolsResult.results;
        this.toLoad -= 1;
      });
      this.transport.get("evaluation-reports/?outcome_refs=" + this.id, !this.authenticated).then((reportsResult) => {
        this.reports = reportsResult.results;
        this.toLoad -= 1;
      })
      this.transport.get("thematic-groups/", !this.authenticated).then((thematicGroupsData) => {
        this.thematicGroups = thematicGroupsData.results;   
        for (var tg in this.thematicGroups) {
          this.thematicGroups[tg].current = this.outcome.thematic_group_refs.some(el => el.id == this.thematicGroups[tg].id);
        } 
        this.toLoad -= 1
      })
      
    },
      (error) => {
        this.router.navigate(["/outcomes"]);
      });
  }

  addToLibrary() {
    this.transport.post("outcomes/" + this.id + "/add_to_library/", {}).then((addToLibraryResult) => {
      this.outcome.current_user_library = true;
    }, (error) => {});
  }

  removeFromLibrary() {
    this.transport.post("outcomes/" + this.id + "/remove_from_library/", {}).then((addToLibraryResult) => {
      this.outcome.current_user_library = false;
    }, (error) => {});
  }

  goBack(event) {
    event.preventDefault();

    if (!this.programId)
    this.router.navigate(["outcomes"]);
    else {
      var link = '/outcomes?programid='+this.programId+'&programresultlevel='+this.programResultLevel;

      var backReferenceId:string = null;
      if (this.programBackReferenceId)
        backReferenceId = this.programBackReferenceId;

      if (backReferenceId)
        link += "&programbackreferenceid=" + backReferenceId;
      
      this.router.navigateByUrl(link);
    }
  }

  addTool() {
    this.toolForm = new FormGroup({
      tool: new FormControl('', Validators.required)
    })
    this.transport.get("tools/").then((toolsResult) => {
      this.allTools = toolsResult.results;
      this.form = 1
    });
  }

  addIndicator() {
    this.indicatorForm = new FormGroup({
      program: new FormControl('', Validators.required),
      level: new FormControl('', Validators.required),
      indicator: new FormControl('', Validators.required),
      result:  new FormControl('', Validators.required)
    })
    this.transport.get("programs/").then((programsData) => {
      this.programs = programsData.results
      this.form = 2
    })
  }

  toolFormSubmit() {
    this.transport.post('tools/'+ this.toolForm.value.tool + '/add_outcome/?outcome_ref=' + this.outcome.id, {}).then(resInd =>{
      let tool = this.allTools.find(t => t.id == this.toolForm.value.tool)
      this.tools.push(tool)
      this.closeForm()
    }).catch(e => console.log(e))
  }

  indicatorFormSubmit() {
    let dataInd = {name: this.indicatorForm.value.indicator, outcome_ref: this.outcome.id}
    this.transport.post('outcome-indicators/', dataInd).then(resInd => {
      this.outcomeIndicators.push(resInd)
      this.closeForm()
    }).catch(e => console.log(e))
  }

  closeForm() {
    this.form = 0
  }

  isToolSelected(id) {
    return !!this.tools.find(tool => tool.id == id)
  }

  isIndicatorSelected(item) {
    return !!this.outcomeIndicators.find(i => i.name.trim() == item.trim())
  }

  changeLevel() {
    if (!this.indicatorForm.value.level || !this.indicatorForm.value.program) this.results = []
    else {
      this.transport.get("program-"+ this.indicatorForm.value.level +"/?program_ref=" + this.indicatorForm.value.program).then(result => {
        this.results = result.results 
        this.indicatorForm.patchValue({result: ''})
      })
    }
  }

  changeResult() {
    this.transport.get("mpl-" + this.indicatorForm.value.level + "/?program_ref=" + this.indicatorForm.value.program).then((mpl) => {
      this.mpl = mpl.results.filter(e => e.indicator);
    })
  }
}
