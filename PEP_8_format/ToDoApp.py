import argparse
import csv
import re
import pandas as pd
from ToDoClass import *
parser = argparse.ArgumentParser()
parser.add_argument('echo', nargs='*', default=None)


try:
    class UserInteraction:
        inputs = ''

        def __init__(self, inputs):
            self.inputs = inputs

        def call_add(self):
            inptlen = len(self.inputs[1:])
            if(len(self.inputs[1:]) != 0):
                input_stmt = ' '.join(i for i in inputs[1:])
                todo.add_todo(input_stmt)
            else:
                raise AnyPossibleError

        def call_list(self, *args):
            def call_check_by_due_date():
                check_by_due_date(inputs)

            def call_check_project_context():
                check_project_context(inputs)

            def no_function():
                raise AnyPossibleError

            def list_one_argument():
                calling_func = {'all': todo.list_todo,
                                'overdue': todo.list_by_overdue}
                call_method = calling_func.get(
                    inputs[1], call_check_project_context)
                call_method()

            def list_two_argument():
                calling_func = {'by project': todo.list_by_project,
                                'by context': todo.list_by_context}
                call_method = calling_func.get(
                    inputs[1]+' '+inputs[2], call_check_by_due_date)
                call_method()

            input_len = {0: no_function, 1: list_one_argument,
                         2: list_two_argument, 3: list_two_argument}
            result_method = input_len.get(len(inputs[1:]), default)
            result_method()

        def call_complete(self):
            todo.complete_todo([inputs[1]])

        def call_delete(self):
            todo.delete_todo([inputs[1]])

        def sort_todo():
            pass

    readdata = read_todo_file()
    todo = Todo(readdata)

    args = parser.parse_args()
    if(args.echo != []):
        inputs = args.echo

    UI = UserInteraction(inputs[1:])
    choice = {'a': UI.call_add, 'l': UI.call_list,
              'c': UI.call_complete, 'd': UI.call_delete}

    def default():
        print('not applicable choice, try again')
    result = choice.get(inputs[0], default)
    result()

except AnyPossibleError:
    print('Invalid Command please refer help')
