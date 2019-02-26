import argparse
import csv
import re
import pandas as pd
parser=argparse.ArgumentParser()
parser.add_argument('echo',nargs='*', default=None)


class UserInteraction:
    inputs=''
    def __init__(self,inputs):
        self.inputs=inputs
    def calladd(self,):
        inptlen=len(self.inputs[1:])
        inputstmt=' '.join(i for i in inputs[1:])
        todo.add_todo(inputstmt)

    def calllist(self):
        todo.list_todo()

    def callcomplete(self):
        todo.complete_todo(int(inputs[1]))

    def calldelete(self,serial_num):
        todo.delete_todo(serial_num)
        
    def sort_todo():
        pass 
    



class Todo():
    def __init__(self,itemslist):
        self.itemslist=itemslist
    
    #SIMPLE DISPLAY NO ARG DONE
    def list_todo(self):
        displayTodo(self.itemslist)
    
    
    #DONE
    def add_todo(self,inptstmt):
        projects=[]
        input_message=inptstmt.split(' ')
        duedate_current=''

        #FIND DUE WORD AND SETTING THE DUEDATE
        if(inptstmt.find('due')>0):
            dueindexes=[]
            for words in range(len(input_message)):
                if input_message[words]=='due':
                    dueindexes.append(words)
            dueindex=dueindexes[len(dueindexes)-1]#now we know which index to use
            message=' '.join(msg for msg in input_message[0:dueindex])#get everything before word due
            duedate=[date for date in input_message[dueindex+1:]]#get everything after word due
            if(checkdate(duedate)=='no error'):
                duedate_current=getdate(duedate)
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
        
        #TO MAKE TODO OBJECT FROM ABOVE DATA AND WRITE IF NEED BE
        todo=Todoitems(gettodocount(),'incomplete',duedate_current,message,str(projects))
        #print(str(todo.serial_num)+' '+todo.status+' '+todo.date+' '+todo.project+' '+todo.message)
        self.itemslist.append(todo)
        writeTodoFile(self.itemslist)
        
        
    

    def complete_todo(self,serial_num):
        print(self.itemslist)
    
    
    #DONE
    def delete_todo(self,serial_num):
        items=[]
        print(serial_num)
        print(type(serial_num))
        print(self.itemslist)
        for item in self.itemslist:
            if(item.serial_num!=int(serial_num)):
                items.append(item)
        #print(items)
        writeTodoFile(items)
        
    
    
    def extend_todo():
        pass


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



#OTHER FUNCITIONS TO BE USED AS A UTILITY

#DISPLAY ALL THE TODO ITEMS IT GETS AS A LIST
def displayTodo(args):
    for display_item in args:
        #print(item)
        if(display_item.status=='complete'):
            display_item.symbol='[x]'
        elif(display_item.status=='incomplete'):
            display_item.symbol='[ ]'
        print('{0:<10}{1:10}{2:20}{3:50}{4}'.format(display_item.serial_num,display_item.symbol,display_item.date,display_item.project,display_item.message))


#WRITE ALL THE TODO ITEMS IT GETS AS A LIST
def writeTodoFile(args):
    with open('items.csv','w') as file:
        fieldnames=['serial_num','status','date','project','message']
        csvwriter=csv.DictWriter(file,fieldnames=fieldnames)
        csvwriter.writeheader()
        for item in args:
            #print(str(item.serial_num)+' '+item.status+' '+item.date+' '+item.project+' '+item.message)
            csvwriter.writerow({'serial_num':item.serial_num,'status':item.status,'date':item.date,'project':item.project,'message':item.message})
    

#READS ALL THE TODO ITEMS AND RETURN A LIST
def readTodoFile():
    with open('items.csv') as file:
            csvreader=csv.DictReader(file,delimiter=',')
            #next(file)
            items=[]
            for row in csvreader:
                item=Todoitems(row['serial_num'],row['status'],row['date'],row['message'],row['project'])
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


#READING DATA TO USE
readdata=readTodoFile()
todo=Todo(readdata)


#logic to know user choice
args=parser.parse_args()
#if its simple add, list etc positiona arguments
if(args.echo!=[]):
    inputs=args.echo

#HANDLING USER INPUT
UI=UserInteraction(inputs[1:])
if (inputs[0]=='a'):
    UI.calladd()
elif(inputs[0]=='l'):
    UI.calllist()
elif(inputs[0]=='d'):
    UI.calldelete(inputs[1])
elif(inputs[0]=='c'):
    UI.callcomplete()
else:
    print('incorrect command try again')