lines = [line.rstrip('\n') for line in open('input_for_parse.csv')]
finish_lines = []
for line in lines:
    line_parts = line.split(';')
    if line_parts[1] == '':
        pass
    elif line_parts[0] == '':
        #append to last line
        finish_lines[-1].append(line_parts[1])
    else:
        finish_lines.append([line_parts[0], line_parts[1]])

output = open('output_of_parse.txt', 'w')
output.write(str(finish_lines))
output.close()