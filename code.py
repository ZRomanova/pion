#импорты

def download(request):
    program_id = request.GET['program_id']
    program = Program.objects.get(id=program_id)
    targets = program.target_refs.all()
    context = {
        'table_rows': [
        ]
    }
    for target in targets:        
        activities = Activity.objects.filter(program_ref=program_id).filter(target_ref=target.id)
        if activities.count() == 0:
            context['table_rows'].append({
                'target': target.name,
                'activity': '',
                'output': '',
                'shortoutcome': '',
                'midoutcome': '',
                'impact': ''
            })
        else:
            for activity in activities.all():
                outputs = ProgramOutput.objects.filter(program_ref=program_id).filter(activity_ref=activity.id)
                if outputs.count() == 0:
                    context['table_rows'].append({
                        'target': target.name,
                        'activity': activity.name,
                        'output': '',
                        'shortoutcome': '',
                        'midoutcome': '',
                        'impact': ''
                    })
                else:
                    for output in outputs.all():
                        shortoutcomes = ProgramShortOutcome.objects.filter(program_ref=program_id).filter(program_output_many_refs__in=[output.id])
                        if shortoutcomes.count() == 0:
                            context['table_rows'].append({
                                'target': target.name,
                                'activity': activity.name,
                                'output': output.name,
                                'shortoutcome': '',
                                'midoutcome': '',
                                'impact': ''
                            })
                        else:
                            for shortoutcome in shortoutcomes.all():
                                midoutcomes = ProgramMidOutcome.objects.filter(program_ref=program_id).filter(program_short_outcome_many_refs__in=[shortoutcome.id])
                                if midoutcomes.count() == 0:
                                    context['table_rows'].append({
                                        'target': target.name,
                                        'activity': activity.name,
                                        'output': output.name,
                                        'shortoutcome': shortoutcome.name,
                                        'midoutcome': '',
                                        'impact': ''
                                    })
                                else:
                                    for midoutcome in midoutcomes.all():
                                        impacts = ProgramImpact.objects.filter(program_ref=program_id).filter(program_mid_outcome_many_refs__in=[midoutcome.id])
                                        if impacts.count() == 0:
                                            context['table_rows'].append({
                                                'target': target.name,
                                                'activity': activity.name,
                                                'output': output.name,
                                                'shortoutcome': shortoutcome.name,
                                                'midoutcome': midoutcome.name,
                                                'impact': ''
                                            })
                                        else:
                                            for impact in impacts.all():
                                                context['table_rows'].append({
                                                    'target': target.name,
                                                    'activity': activity.name,
                                                    'output': output.name,
                                                    'shortoutcome': shortoutcome.name,
                                                    'midoutcome': midoutcome.name,
                                                    'impact': impact.name
                                                })
                                                
    doc = DocxTemplate(os.path.join(settings.BASE_DIR, "template.docx"))
    doc.render(context)
    # doc.save("generated_doc.docx")
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object
    response = HttpResponse(doc_io.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response['Content-Disposition'] = 'inline; filename=program'+program_id+'.docx'
    return response

def getActivities(target_id, program_id):
        array = []
        activities = Activity.objects.filter(program_ref=program_id).filter(target_ref=target_id)
        for activity in activities.all():
            array.append({
                'item': activity.name,
                'outputs': getOutputs(activity.id, program_id)
            })
        return array

def getOutputs(activity_id, program_id):
    array = []
    outputs = ProgramOutput.objects.filter(program_ref=program_id).filter(activity_ref=activity_id)
    for output in outputs.all():
        array.append({
            'item': output.name,
            'shortoutcomes': getShortOutcomes(output.id, program_id)
        })
    return array

def getShortOutcomes(output_id, program_id):
    array = []
    shortoutcomes = ProgramShortOutcome.objects.filter(program_ref=program_id).filter(program_output_many_refs__in=[output_id])
    for shortoutcome in shortoutcomes.all():
        array.append({
            'item': shortoutcome.name,
            'midoutcomes': getMidOutcomes(shortoutcome.id, program_id)
        })
    return array

def getMidOutcomes(shortoutcome_id, program_id):
    array = []
    midoutcomes = ProgramMidOutcome.objects.filter(program_ref=program_id).filter(program_short_outcome_many_refs__in=[shortoutcome_id])
    for midoutcome in midoutcomes.all():
        array.append({
            'item': midoutcome.name,
            'impacts': getImpacts(midoutcome.id, program_id)
        })
    return array

def getImpacts(midoutcome_id, program_id):
    array = []
    impacts = ProgramImpact.objects.filter(program_ref=program_id).filter(program_mid_outcome_many_refs__in=[midoutcome_id])
    for impact in impacts.all():
        array.append({
            'item': impact.name,
        })
    return array

def downloadNew(request):
    program_id = request.GET['program_id']
    program = Program.objects.get(id=program_id)
    targets = program.target_refs.all()
    context = {
        'table_rows': [
        ]
    }

    for target in targets:        
        context['table_rows'].append({
            'item': target.name,
            'activities': getActivities(target.id, program_id)
        })
                                            
    doc = DocxTemplate(os.path.join(settings.BASE_DIR, "templateprogram.docx"))
    doc.render(context)
    doc_io = io.BytesIO() 
    doc.save(doc_io) 
    doc_io.seek(0)
    response = HttpResponse(doc_io.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response['Content-Disposition'] = 'inline; filename=program'+program_id+'.docx'
    return response