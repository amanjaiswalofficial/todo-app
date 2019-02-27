#from argparsetut import displayTodo
import csv
import re

class Todoitems():
    serial_num=0
    status=''
    date=''
    message=''
    def __init__(self,serial_num,status,date,message,project='Default project',context='sample context'):
        self.serial_num=int(serial_num)
        self.status=status
        self.date=date
        self.message=message
        self.project=project
        self.context=context


class Todo():
    def __init__(self,itemslist):
        self.itemslist=itemslist
    
    #SIMPLE DISPLAY NO ARG DONE
    def listTodo(self):
        displayTodo(self.itemslist)
    
    #DONE
    def add_todo(self,inptstmt):
        projects=[]
        input_message=inptstmt.split(' ')
        duedate_current=''

        #FIND DUE WORD AND SETTING THE DUEDATE
        if(inptstmt.find('due') > 0):
            dueindexes=[]
            for words in range(len(input_message)):
                if input_message[words]=='due':
                    dueindexes.append(words)
            dueindex=dueindexes[len(dueindexes)-1]#now we know which index to use
            message=' '.join(msg for msg in input_message[0:dueindex])#get everything before word due
            duedate=[date for date in input_message[dueindex+1:]]#get everything after word due
            if(checkdate(duedate)=='no error'):
                duedate_current = getdate(duedate)
            else:
                print(checkdate(duedate))
        else:
            print('no due')
            duedate_current='tomorrow'
            message=' '.join(msg for msg in input_message[0:])

        #FINDING PROJECT FROM THE STRING        
        project_strings=re.findall('[+][^\s]+',message)
        if(len(project_strings)>=1):
            for items in project_strings:
                project=str(items[1:])
                projects.append(project)
            if(len(projects)>=1):
                projects='|'.join(project for project in projects)
        else:
            projects='personal'



        #FINDING CONTEXT FROM THE MESSAGE
        context_strings=re.findall('[@][^\s]+',message)
        contexts=[]
        if(len(context_strings)>=1):
            for item in context_strings:
                context=str(item[1:])
                contexts.append(context)
            if(len(contexts)>=1):
                context='|'.join(context for context in contexts)
        else:
            context='none'
        
        #TO MAKE TODO OBJECT FROM ABOVE DATA AND WRITE IF NEED BE
        todo=Todoitems(gettodocount(),'incomplete',duedate_current,message,str(projects),str(context))
        #print(str(todo.serial_num)+' '+todo.status+' '+todo.date+' '+todo.project+' '+todo.context+' '+todo.message)
        self.itemslist.append(todo)
        writeTodoFile(self.itemslist)
        
        
    
    #DONE
    def complete_todo(self,serial_number):
        if(checkValidInput(serial_number)):
            serial_num=serial_number[0]
            items=[]
            for item in self.itemslist:
                if(item.serial_num==int(serial_num)):
                    item.status='complete'
                items.append(item)
            writeTodoFile(items)
        else:
            print('Not a valid input, please provide a number that is in the list')            
    
    
    #DONE
    def deleteTodo(self,serial_number):
        if(checkValidInput(serial_number)):
            serial_num=int(serial_number[0])
            items=[]
            for item in self.itemslist:
                if(item.serial_num!=int(serial_num)):
                    items.append(item)
            writeTodoFile(items)
        else:
            print('Not a valid input, please provide a number that is in the list')
    

    def listByProject(self):
        avail_project=getProjectNames(self.itemslist)
        projects=sorted(avail_project)
        for project in projects:
            print(project)
            for item in self.itemslist:
                templist=[]
                if(project in item.project.split('|')):
                    templist.append(item)
                displayTodo(templist)
        
    def listByStatus(self):
        avail_status_complete=[]
        avail_status_incomplete=[]
        for item in self.itemslist:
            if(item.status=='complete'):
                avail_status_complete.append(item)
            else:
                avail_status_incomplete.append(item)
        print('Complete')
        displayTodo(avail_status_complete)
        print('Incomplete')
        displayTodo(avail_status_incomplete)

    def listByProjectName(self,project_name):
        avail_projects=getProjectNames(self.itemslist)
        projects=[]
        if project_name not in avail_projects:
            print('project not present, try again')
        else:
            for item in self.itemslist:
                if(project_name in item.project.split('|')):
                    projects.append(item)
            print(project_name)
            displayTodo(projects)

    def listByDueDate(self,due_dates):
        if(checkdate(due_dates)!='no error'):
            print(checkdate(due_dates))
        else:
            #print(due_dates)
            due_date=due_dates
            #due_date=[i for i in due_dates.split(' ')]

            validdays=['today','tom','tomorrow']
            items=[]
            if(due_date[0] in validdays):
                if(due_date[0]=='tom'):
                    due_date[0]='tomorrow'
                #print(due_date[0])
                for item in self.itemslist:
                    if(item.date==due_date[0]):
                        items.append(item)
                displayTodo(items)
            else:
                if(len(due_date)!=2):
                    print('invalid date, please insert in form of DD MON')
                else:
                    date_check=checkdate(due_date)
                    if(date_check!='no error'):
                        
                        print(date_check)
                    else:
                        due_date=' '.join(item for item in due_date)
                        items=[]
                       
                        for item in self.itemslist:
                            if(item.date==due_date):
                                items.append(item)
                        if(len(items)>0):
                            displayTodo(items)
                        else:
                            print('No todo for given date found')

    def listByOverdue(self):
        items_today=[]
        items_tomorrow=[]
        datedict={}
        month_order=[]
        validitems=[]
        for item in self.itemslist:
            if(item.status=='incomplete'):
                if(item.date=='today'):
                    items_today.append(item)
                elif(item.date=='tomorrow'):
                    items_tomorrow.append(item)
                else:
                    pass
        validmonths=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        for month_name in validmonths:
            count=0
            tempdate=[]
            for item in self.itemslist:
                date=item.date.split(' ')
                if(len(date)>1):
                    if(date[1]==month_name):
                        validitems.append(item)

        displayTodo(items_today)
        displayTodo(items_tomorrow)
        displayTodo(validitems)
   
    def listByContext(self):
            contexts=[]
            for item in self.itemslist:
                if(len(re.findall('|',item.context))!=0):
                    values=item.context.split('|')
                    contexts.extend(values)
            contexts=sorted(set(contexts))
            for context in contexts:
                displayItem=[]
                print(context)
                for item in self.itemslist:
                    if(context in item.context.split('|')):
                        displayItem.append(item)
                displayTodo(displayItem)

    def listByContextName(self,args):
        """if(len(args)>1):
            print('not a valid input, please provide a @context name in the todo')"""
        if(args.isdigit()):
            print('not a valid input, please provide a @context name in the todo')
        else:
            avail_contexts=[]
            final_context_avail=[]
            displayItems=[]
            for item in self.itemslist:
                avail_contexts.append(item.context)
            for item in avail_contexts:
                contexts=item.split('|')
                for context in contexts:
                    final_context_avail.append(context)
            final_context_avail=set(final_context_avail)
            if(args not in final_context_avail):
                print('not a valid input, please provide a @context name in the todo')
            else:
                print(args)
                for item in self.itemslist:
                    if(args in item.context.split('|')):
                        displayItems.append(item)
                displayTodo(displayItems)


    def extend_todo():
        pass

def displayTodo(args):
    for display_item in args:
        #print(item)
        #print('here')
        if(display_item.status=='complete'):
            display_item.symbol='[x]'
        elif(display_item.status=='incomplete'):
            display_item.symbol='[ ]'
        print('{0:<10}{1:10}{2:20}{3:20}{4:20}{5}'.format(display_item.serial_num,display_item.symbol,display_item.date,display_item.project,display_item.context,display_item.message))


#WRITE ALL THE TODO ITEMS IT GETS AS A LIST
def writeTodoFile(args):
    with open('items.csv','w') as file:
        fieldnames=['serial_num','status','date','project','context','message']
        csvwriter=csv.DictWriter(file,fieldnames=fieldnames)
        csvwriter.writeheader()
        for item in args:
            #print(str(item.serial_num)+' '+item.status+' '+item.date+' '+item.project+' '+item.message)
            csvwriter.writerow({'serial_num':item.serial_num,'status':item.status,'date':item.date,'project':item.project,'context':item.context,'message':item.message})
    

#READS ALL THE TODO ITEMS AND RETURN A LIST
def readTodoFile():
    with open('items.csv') as file:
            csvreader=csv.DictReader(file,delimiter=',')
            #next(file)
            items=[]
            for row in csvreader:
                item=Todoitems(row['serial_num'],row['status'],row['date'],row['message'],row['project'],row['context'])
                items.append(item)
            return items

#GET TOTAL NUMBER OF ITEMS IN THE TODO LIST
def gettodocount():
    currentid=0
    with open('items.csv','r') as file:
        content=csv.DictReader(file,delimiter=',')
        for rows in content:
            currentid=int(rows['serial_num'])
    currentid+=1
    return currentid

#GET THE DATE AS A STRING
def getdate(args):
    date=' '.join(item for item in args)
    return str(date)

#CHECK FOR VALIDITY OF THE DATE
def checkdate(args):
    duedate=args
    """print(len(duedate))
    print(duedate[0])"""
    validday=['today','tom','tomorrow']
    duedate_current=''
    if((len(duedate)==1) and (duedate[0] in validday)):
        #duedate_current=duedate[0]
        return 'no error'
            #print(duedate_current)
    elif(len(duedate)==2):
        validdays=range(1,32)
        validmonths=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        day=0
        if(duedate[0].isdigit()):
            day=int(duedate[0])
        else:
            return 'Not correct format, please enter due-date in form of dd mon'
            flag=False
        month=str(duedate[1].lower())
        if(day in validdays and month in validmonths):
            if(month=='feb'):
                if (day in range(1,29)):
                    return 'no error'
                else:
                    return 'The day doesn\'t exist in feb'
                    flag=False
            else:
                return 'no error'
        else:
            return 'Not a valid entry, please insert in the form of dd mon'
            
    else:
            return 'Not a valid entry, please insert in the form of dd mon'


#TO SEE IF PROVIDED INPUT SERIAL NUMBER IS VALID OR NOT
def checkValidInput(inputval):
    if(len(inputval)>1):
        print(inputval)
        print(type(inputval))
        print(len(inputval))
        return False
    else:
        if(inputval[0].isdigit()):
            inputval=int(inputval[0])
            avail_serial_num=[]
            for item in readdata:
                avail_serial_num.append(int(item.serial_num))
            if inputval in avail_serial_num:
                return True
            else:
                return False
        else:
            return False


def checkValidProjectName(inputval):
    if(len(inputval)>1 or inputval[0].isdigit()):
        return 'not a valid name, try again'
    else:
        projects=getProjectNames(readdata)
        if inputval[0] not in projects:
            return 'not a valid name, try again'
        else:
            return 'no error'




def getProjectNames(args):
    avail_project=[]
    for item in args:
        avail_project.append(item.project)
    for item in avail_project:
        if('|' in item):
        #print(itemvalues.index(item))
            values=item.split('|')
            for value in values:
                avail_project.append(value)
        #itemvalues.remove(item)
    projects=set()
    for item in avail_project:
        if('|' not in item):
            projects.add(item)
    return projects

readdata=readTodoFile()
todo=Todo(readdata)