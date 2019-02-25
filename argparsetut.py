"""import argparse
parser=argparse.ArgumentParser()
parser.add_argument('echo',nargs='*', default=None)
parser.add_argument('-a',nargs='*',default=None)
parser.add_argument('-l',nargs='*',default=None)


#logic to know user choice
args=parser.parse_args()
#if its simple add, list etc positiona arguments
if(args.echo!=[]):
    inputs=args.echo
#when it's optional -l.-a then insert 'add','list' etc according to need in the start to run the same code
elif(args.a is not None):
    inputs=args.a
    inputs.insert(0,'add')
elif(args.l is not None):
    inputs=args.l
    inputs.insert(0,'list')


#print(args)
def add_items():
    inptlen=len(inputs[1:])
    inputstmt=' '.join(i for i in inputs[1:])
    print(inputstmt)

def list_todo():
    pass

def delete_item():
    pass
    
def sort_todo():
    pass 

def nochoice():
    print('no default choice made, try again')

user_input={'add':add_items,'list':list_todo,None:nochoice}
result_function=user_input.get(inputs[0],nochoice)
result_function()"""

import csv
import pandas as pd
class Todo():
    def __init__(self,itemslist):
        self.itemslist=itemslist
    def list_items(self):
        displayTodo(self.itemslist)
    def add_items():
        pass
    def delete_items(self,serial):
        items=[]
        for item in self.itemslist:
            """if(item.serial_num!=serial):
                #items.append(item)
                print(item.serial_num)
                print(item.message)"""
            print(item)
        """for item in items:
            print(item.message)"""
                
        """df=pd.read_csv('data.csv')
        for i in range(0, len(df)):
        if(df.iloc[i]['id']=='[ ]'):
            df.set_value(i,'checked','[x]')"""
    
    
    def update_items():
        pass


class Todoitems():
    serial_num=0
    status=''
    date=''
    message=''
    def __init__(self,serial_num,status,date,message,project='sample project',context='sample context'):
        self.serial_num=serial_num
        self.status=status
        self.date=date
        self.message=message
        self.project=project
        self.context=context

def displayTodo(args):
    for display_item in args:
        #print(item)
        print('{0:<10}{1:10}{2:20}{3:60}'.format(display_item.serial_num,display_item.status,display_item.date,display_item.message))

def writeTodoFile(args):
    """with open('items.csv','w') as file:
        for items in args:
            fieldnames=['id','checked','date','context']
            csvwriter=csv.DictWriter(file,fieldnames=fieldnames)
            csvwriter.writerow({'id':currentid,'checked':'[ ]','date':duedate,'context':message})"""
    
    
    """df=pd.read_csv('data.csv')
    for i in range(0, len(df)):
        if(df.iloc[i]['id']=='[ ]'):
            df.set_value(i,'checked','[x]')
    df.to_csv('newdata.csv',index=False)"""

def readTodoFile():
    with open('items.csv') as file:
            csvreader=csv.DictReader(file,delimiter=',')
            #next(file)
            items=[]
            for row in csvreader:
                item=Todoitems(row['id'],row['checked'],row['date'],row['context'])
                items.append(item)
            """for itemitem in items:
                if(itemitem.status=='complete'):
                    print(itemitem.message)"""
            return items

readdata=readTodoFile()
todo=Todo(readdata)
#todo.list_items()
todo.delete_items(2)

"""finalresult=readTodoFile()
displayTodo(finalresult)"""

"""item=todoitems(1,'incomplete','Today','Working on project with everyone')
item.displaydata()"""