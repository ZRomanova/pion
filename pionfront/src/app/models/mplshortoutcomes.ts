export class MplShortOutcomes {
    id: string;
    result_ref: any;
    name: string;
    indicator: string;
    method: string;
    tool: string;
    tool_url: string;
    frequency: string;
    reporting: string;
    program_ref: any;
    suitable_tools: string[];
    suitable_indicators: string[];
    suitable_from_tools: string[];
    sort_index: number;
    tool_type: 'OutcomeMethods' | 'Tools'

    displayResultRef: boolean = false;
    displayName: boolean = false;
    displayIndicator: boolean = false;
    displayMethod: boolean = false;
    displayTool: boolean = false;
    displayFrequency: boolean = false;
    displayReporting: boolean = false;
}