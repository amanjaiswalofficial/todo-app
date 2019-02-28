import argparse
add_help_string='add'
delete_help_string='delete'
parser = argparse.ArgumentParser()
parser.add_argument('echo', nargs='*', default=None,help='Print this')
parser.add_argument('--add',help=add_help_string)
"""parser.add_argument('--delete help',)
#parser.add_argument('d',help=delete_help_string)
"""
args = parser.parse_args()
if(args.echo!=[]):
    print(args.echo)
else:
    print(add_help_string)
