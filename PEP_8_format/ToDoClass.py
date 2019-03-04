import csv
import re
import datetime
from termcolor import colored

class AnyPossibleError(Exception):
    pass


class Todoitems():
    serial_num = 0
    status = ''
    date = ''
    message = ''

    def __init__(self, serial_num, status, date, message, project='Default project', context='sample context'):
        self.serial_num = int(serial_num)
        self.status = status
        self.date = date
        self.message = message
        self.project = project
        self.context = context


class Todo():
    def __init__(self, items_list):
        self.items_list = items_list

    def list_todo(self):
        """Displays all the todo items without any filtering"""
        display_todo(self.items_list)

    def get_context(inpt_stmt):
        """Extracts the context out of the provided message"""
        context_strings = re.findall('[@][^\s]+', inpt_stmt)
        contexts = []
        if(len(context_strings) >= 1):
            for item in context_strings:
                context = str(item[1:])
                contexts.append(context)
            if(len(contexts) >= 1):
                context = '|'.join(context for context in contexts)
        else:
            context = 'none'
        return context

    def get_project(inpt_stmt):
        """Extracts the projects from the user input message"""
        project_strings = re.findall('[+][^\s]+', inpt_stmt)
        projects=[]
        if(len(project_strings) >= 1):
            for items in project_strings:
                project = str(items[1:])
                projects.append(project)
            if(len(projects) >= 1):
                projects = '|'.join(project for project in projects)
        else:
            projects = 'personal'
        return projects

    def get_duedate(inpt_stmt):
        """gets the word 'due' to find the due date and message"""
        input_message = inpt_stmt.split(' ')
        duedate_current = ''

        if(inpt_stmt.find('due') > 0):
            due_indexes = []
            for words in range(len(input_message)):
                if input_message[words] == 'due':
                    due_indexes.append(words)
            due_index = due_indexes[len(due_indexes)-1]
            message = ' '.join(msg for msg in input_message[0:due_index])
            duedate = [date for date in input_message[due_index+1:]]
            if(check_date(duedate) == 'no error'):
                duedate_current = get_date(duedate)
            else:
                print(check_date(duedate))
        else:
            duedate_current = 'tomorrow'
        return duedate_current, message

    def add_todo_validator(args):
        """runs all the needed methods to get the message, due date, project and context"""
        project = Todo.get_project(args)
        context = Todo.get_context(args)
        duedate, message = Todo.get_duedate(args)
        return duedate, message, project, context

    def add_todo(self, inpt_stmt):
        """adds the input to the to do list"""
        duedate_current, message, projects, context = Todo.add_todo_validator(inpt_stmt)
        todo = Todoitems(get_todo_count(), 'incomplete',duedate_current, message, str(projects), str(context))
        self.items_list.append(todo)
        write_todo_file(self.items_list)

    def complete_todo(self, serial_number):
        """Completes a todo after taking it's serial number as input"""
        if(check_valid_input(serial_number)):
            serial_num = serial_number[0]
            items = []
            for item in self.items_list:
                if(item.serial_num == int(serial_num)):
                    item.status = 'complete'
                items.append(item)
            write_todo_file(items)
        else:
            print('Not a valid input, please provide a number that is in the list')

    def delete_todo(self, serial_number):
        """Deletes a todo item from the list using the given serial number"""
        if(check_valid_input(serial_number)):
            serial_num = int(serial_number[0])
            items = []
            for item in self.items_list:
                if(item.serial_num != int(serial_num)):
                    items.append(item)
            write_todo_file(items)
        else:
            print('Not a valid input, please provide a number that is in the list')

    def list_by_project(self):
        """Lists all the todo Items on the basis of project names"""
        avail_project = get_project_names(self.items_list)
        projects = sorted(avail_project)
        for project in projects:
            print(project)
            for item in self.items_list:
                temp_list = []
                if(project in item.project.split('|')):
                    temp_list.append(item)
                display_todo(temp_list)

    def list_by_status(self):
        """displays all the todo items ordering the completed and then the incomplete"""
        avail_status_complete = []
        avail_status_incomplete = []
        for item in self.items_list:
            if(item.status == 'complete'):
                avail_status_complete.append(item)
            else:
                avail_status_incomplete.append(item)
        print('Complete')
        display_todo(avail_status_complete)
        print('Incomplete')
        display_todo(avail_status_incomplete)

    def list_by_project_name(self, project_name):
        """Displays records for a particular project"""
        avail_projects = get_project_names(self.items_list)
        projects = []
        if project_name.lower() not in avail_projects:
            print('project not present, try again')
        else:
            for item in self.items_list:
                if(project_name.lower() in item.project.split('|')):
                    projects.append(item)
            print(project_name)
            display_todo(projects)

    def list_by_duedate(self, due_dates):
        """Display the records based on a due date"""
        if(check_date(due_dates) != 'no error'):
            print(check_date(due_dates))
        else:
            due_date = due_dates
            validdays = ['today', 'tom', 'tomorrow']
            items = []
            if(due_date[0] in validdays and due_date[0] == 'tom'):
                due_date[0] = 'tomorrow'
                # print(due_date[0])
                for item in self.items_list:
                    if(item.date == due_date[0]):
                        items.append(item)
                display_todo(items)
            else:
                due_date = ' '.join(item for item in due_date)
                items = []
                for item in self.items_list:
                    if(item.date == due_date):
                        items.append(item)
                if(len(items) > 0):
                    display_todo(items)
                else:
                    print('No todo for given date found')

    def list_by_overdue(self):
        """Displays the records which are due and incomplete"""
        items_today = []
        items_tomorrow = []
        date_dict = {}
        month_order = []
        valid_items = []
        valid_months = ['jan', 'feb', 'mar', 'apr', 'may','jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        for item in self.items_list:
            if(item.date == 'today' and item.status == 'incomplete'):
                    items_today.append(item)
            elif(item.date == 'tomorrow' and item.status == 'incomplete'):
                    items_tomorrow.append(item)
        for month_name in valid_months:
            count = 0
            tempdate = []
            for item in self.items_list:
                date = item.date.split(' ')
                if(len(date) > 1):
                    if(date[1] == month_name):
                        valid_items.append(item)
        display_todo(items_today)
        display_todo(items_tomorrow)
        display_todo(valid_items)

    def list_by_context(self):
        """Display all the todo Items on basis of context"""
        contexts = []
        for item in self.items_list:
            if(len(re.findall('|', item.context)) != 0):
                values = item.context.split('|')
                contexts.extend(values)
        contexts = sorted(set(contexts))
        for context in contexts:
            display_item = []
            print(context)
            for item in self.items_list:
                if(context in item.context.split('|')):
                    display_item.append(item)
            display_todo(display_item)

    def list_by_context_name(self, context_name):
        """Display the ToDo items based on a context"""
        display_items=[]
        print(context_name)
        for item in self.items_list:
            if(context_name.lower() in item.context.split('|')):
                display_items.append(item)
        display_todo(display_items)

    def extend_todo(self,serial_num,new_due_date):
        items=[]
        for item in self.items_list:
            if(item.serial_num==int(serial_num)):
                item
            pass
    


def display_todo(args):
    """To display all the todo items given in the input in form of a list""" 
    for display_item in args:
        if(display_item.status == 'complete'):
            display_item.symbol = '[x]'
        elif(display_item.status == 'incomplete'):
            display_item.symbol = '[ ]'
        #colored_date=colored(display_item.serial_num,'yellow')
        print('{0:<10}{1:10}{2:20}{3:20}'.format(display_item.serial_num, display_item.symbol,
                                                        display_item.date, display_item.message))

def write_todo_file(args):
    """Write all the items to the file, based on the input that is a list of items"""
    today,tomorrow=get_today_tomorrow()
    with open('items.csv', 'w') as file:
        field_names = ['serial_num', 'status',
                    'date', 'project', 'context', 'message']
        csvwriter = csv.DictWriter(file, fieldnames=field_names)
        csvwriter.writeheader()
        for item in args:
            if(item.date=='today'):
                item.date=today
            elif(item.date=='tomorrow' or item.date=='tom'):
                item.date=tomorrow
            #print(str(item.serial_num)+' '+item.status+' '+item.date+' '+item.project+' '+item.message)
            csvwriter.writerow({'serial_num': item.serial_num, 'status': item.status, 'date': item.date.lower(),
                                'project': item.project.lower(), 'context': item.context.lower(), 'message': item.message})

def read_todo_file():
    """Reads all the records from the file and return them as a list"""
    with open('items.csv') as file:
        today,tomorrow=get_today_tomorrow()
        csvreader = csv.DictReader(file, delimiter=',')
        items = []
        for row in csvreader:
            if(row['date']==today):
                row['date']='today'
            elif(row['date']==tomorrow):
                row['date']='tomorrow'
            #colored_date=colored(display_item.serial_num,'yellow')
            item = Todoitems(row['serial_num'], row['status'], row['date'],
                            row['message'], row['project'], row['context'])
            items.append(item)
        return items

def get_today_tomorrow():
    """Extract the value of today and tomorrow to display records accordingly"""
    now=datetime.datetime.now()
    today_day=str(now.day)
    today_month=str(now.strftime("%b").lower())
    today=today_day+' '+today_month
    now+=datetime.timedelta(days=1)
    tomorrow_day=str(now.day)
    tomorrow_month=str(now.strftime("%b").lower())
    tomorrow=tomorrow_day+' '+tomorrow_month
    return today, tomorrow

def get_todo_count():
    """Get the count for total number of items in the todo"""
    current_id = 0
    with open('items.csv', 'r') as file:
        content = csv.DictReader(file, delimiter=',')
        for rows in content:
            current_id = int(rows['serial_num'])
    current_id += 1
    return current_id

def get_date(args):
    """Returns a string of the date from the input"""
    date = ' '.join(item for item in args)
    return str(date)

def get_project_names(args):
    """Get list of all the available project names"""
    avail_project = []
    for item in args:
        avail_project.append(item.project)
    for item in avail_project:
        if('|' in item):
            values = item.split('|')
            for value in values:
                avail_project.append(value)
    projects = set()
    for item in avail_project:
        if('|' not in item):
            projects.add(item)
    return projects

def check_date(args):
    """Checks the date to see if it's valid or not"""
    due_date = args
    valid_day = ['today', 'tom', 'tomorrow']
    duedate_current = ''
    if((len(due_date) == 1) and (due_date[0] in valid_day)):
        return 'no error'
    elif(len(due_date) == 2):
        valid_days = range(1, 32)
        valid_months = ['jan', 'feb', 'mar', 'apr', 'may',
                    'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        day = 0
        if(due_date[0].isdigit()):
            day = int(due_date[0])
        else:
            return 'Not correct format, please enter due-date in form of dd mon'
            flag = False
        month = str(due_date[1].lower())
        if(day in valid_days and month in valid_months):
            if(month == 'feb'):
                if (day in range(1, 29)):
                    return 'no error'
                else:
                    return 'The day doesn\'t exist in feb'
                    flag = False
            else:
                return 'no error'
        else:
            return 'Not a valid entry, please insert in the form of dd mon'

    else:
        return 'Not a valid entry, please insert in the form of dd mon'

def check_valid_input(input_val):
    """To see if provided input for delete or complete is valid or not"""
    if(len(input_val) > 1):
        print(input_val)
        print(type(input_val))
        print(len(input_val))
        return False
    else:
        if(input_val[0].isdigit()):
            input_val = int(input_val[0])
            avail_serial_num = []
            for item in readdata:
                avail_serial_num.append(int(item.serial_num))
            if input_val in avail_serial_num:
                return True
            else:
                return False
        else:
            return False

def check_valid_project_name(input_val):
    """Get whether the given project name is valid or not"""
    projects = get_project_names(readdata)
    if input_val.lower() not in projects:
        return False
    else:
        return True

def check_valid_context_name(input_val):
    """Check if the context given to search is valid or not"""
    avail_contexts = []
    final_context_avail = []
    for item in readdata:
        avail_contexts.append(item.context)
    for item in avail_contexts:
        contexts = item.split('|')
        for context in contexts:
            final_context_avail.append(context)
    final_context_avail = set(final_context_avail)
    if(input_val.lower() not in final_context_avail):
        return False
    else:
        return True

def default():
        print('not applicable choice, try again')

def check_project_context(inputs):
    """Check if the given input can be a project name or a context"""
    FirstChar = re.findall('[@]', inputs[1])
    if(len(FirstChar) == 1 and inputs[1].index('@') == 0):
        context_name = inputs[1][1:]
        if(check_valid_context_name(context_name)):
            todo.list_by_context_name(context_name)
        else:
            print('Context not found, try again')
    else:
        FirstChar=re.findall('[+]', inputs[1])
        if(len(FirstChar) == 1 and inputs[1].index('+') == 0):
            project_name = inputs[1][1:]
            if(check_valid_project_name(project_name)):
                todo.list_by_project_name(project_name)
            else:
                print('Project Not found, try again')
        else:
            default() 

def check_by_due_date(inputs):
    """Check for input to call Listing by Due Date"""
    if(inputs[1] == 'due' and len(inputs[1:]) > 1):
        date = inputs[2:]
        todo.list_by_duedate(date)
    else:
        print('not an applicable choice, try again')

readdata = read_todo_file()
todo = Todo(readdata)
