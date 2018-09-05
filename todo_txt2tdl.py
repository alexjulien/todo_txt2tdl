import re
SEP='\t' # tab separated
ENCODING = 'utf-8'
txt = r'D:\ALeX\repo\tasks\todo.txt'
tdl = 'tasks.csv'
header = ['Title', 'Parent', 'Task ID', 'Creation Date', 'Due Date', 'Category']

task_id = 0
tasks = {'':[0,[]]}

for line in open(txt,'r', encoding=ENCODING).readlines():
    if line.startswith('x'):
        continue
    task_id+=1
    creation_date, task = line.split(' ',1)
    due_date   = re.findall(r'(due:[0-9-]*)',task)
    if due_date:
        due_date = due_date[0]
    categories = re.findall(r'(@[A-zÁ-úÑñ]*)', task)
    parent     = re.findall(r'(\+[A-zÁ-úÑñ]*)',task)
    
    if due_date:
        task = task.replace(due_date,'')
    for c in categories:
        task = task.replace(c,'')

    if due_date:
        y,m,d = due_date.split('-')
        due_date = "%s/%s/%s" % (d,y,m)
    else:
        due_date = ''
    y,m,d = creation_date.split('-')
    creation_date = "%s/%s/%s" % (d,y,m)
    
    categories = '+'.join(categories)
    
    if parent:
        parent_name = parent[0]
        if parent_name not in tasks.keys():
            parent_id = len(tasks.keys()) * 1000 # parent task ids go in multiples of 1000. Change if you have 1000+ tasks in your source file
            tasks[parent_name] = [parent_id,[[parent_name, '0', str(parent_id), '01/01/2018', '', ''],]] # 01/01/2018 = arbitrary creation date
        else:
            parent_id = tasks[parent_name][0]
        task = task.replace(parent_name,'')
    else:
        parent_id = 0
        parent_name = ''
   
    full_task = [task.strip(), str(parent_id), str(task_id), creation_date, due_date, categories]
    tasks[parent_name][1].append(full_task)

out = open(tdl,'w',encoding=ENCODING)
out.write(SEP.join(header))
out.write('\n')
for project in tasks.values():
    for line in project[1]:
        out.write(SEP.join(line))
        out.write('\n')
out.close()
