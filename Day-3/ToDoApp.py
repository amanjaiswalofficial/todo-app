import argparse
import csv
import re
import pandas as pd
from ToDoClass import *
parser=argparse.ArgumentParser()
parser.add_argument('echo',nargs='*', default=None)


class UserInteraction:
    inputs=''
    def __init__(self,inputs):
        self.inputs=inputs
    def calladd(self):
        inptlen=len(self.inputs[1:])
        inputstmt=' '.join(i for i in inputs[1:])
        todo.add_todo(inputstmt)

    def calllist(self,*args):

        if(len(inputs[1:])==0):
            print('Not valid command, please prefer help')
            return
        elif(len(inputs[1:])==1):
            if(inputs[1]=='all'):
                todo.listTodo()
            elif(inputs[1]=='overdue'):
                todo.listByOverdue()
            else:
                #print('Not valid command, please prefer help')
                #print(inputs[1])
                """x=)
                if(len()==1 and inputs[1].index('+')==0):
                    project_name=inputs[1][1:]
                    todo.listByProjectName(project_name)"""
                
                x=re.findall('[@]',inputs[1])
                if(len(x)==1 and inputs[1].index('@')==0):
                    context_name=inputs[1][1:]
                    todo.listByContextName(context_name)
                else:
                    print('invalid command, please refer help')      
        elif(inputs[1]=='due' and len(inputs[1:])>1):
            date=inputs[2:]
            todo.listByDueDate(date)
        elif(len(inputs[1:])==2):
            if(inputs[1]=='by' and inputs[2]=='project'):
                todo.listByProject()
                return
            elif(inputs[1]=='by' and inputs[2]=='context'):
                todo.listByContext()
                return

    def callcomplete(self):
        todo.complete_todo([inputs[1]])

    def calldelete(self):
        todo.deleteTodo([inputs[1]])

        
    def sort_todo():
        pass 

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
    UI.calldelete()
elif(inputs[0]=='c'):
    UI.callcomplete()
else:
    print('incorrect command try again')