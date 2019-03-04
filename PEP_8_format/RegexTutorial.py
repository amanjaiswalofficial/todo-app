#FIND WORD IN THE STRING
import re
if re.search("inform", "this is inform here"):
    print('dasda')

if re.findall('inform',"this is inform and inform"):
    print('asdasd')

#FINDING INDEX FOR A WORD
for i in re.finditer("inform","this is inform and inform"):
    print(i.span())

#FINDING PATTERN
strng="Sat hat mat pat"
allstr=re.findall("[shmp]at",strng)
print(allstr)
allstr=re.findall("[Sshmp]at",strng) #including S adds help find Sat with S as well
print(allstr)

#FINDING FOR A RANGE OF CHARACTERS
print(re.findall("[h-m]at",strng))

#USING EXCLUSION
print(re.findall("[^h-m]at",strng)) # ^ excludes the ones having h-m

#REPLACING AND SUBSTITUTING
life="living dancing singing eating"
regex=re.compile("[danc]ing") #square means anything from inside can be there and it will accept
life=regex.sub("swimming",life)
print(life)

print(re.findall("dancing","living dancing swimming eating"))

food="hat mat pat rat"
regex=re.compile("[r]at")
food=regex.sub("food",food)
print(food)


randstr='this is \\sparta'
print(re.search(r'\\sparta',randstr)) #why use r here no clue, also, on normal printing, the \\ dont display, here they do


randster="12345"
print(re.findall("\d",randster)) #\d means include all digits \D mens exlude the digits
print(randster)

num="1234 1234 11 22 1232"
print(len(re.findall("\d{2,7}",num))) # {x,y} means the number of elements matching should be between that range


num="412-555-1212"
if(re.search("\w{3}-\w{3}-\w{4}",num)):
    print(re.findall("\w{3}-\w{3}-\w{4}",num))

# \w means [A-Za-z0-9_]
# \d means [0-9]
# \W means [^A-Za-z0-9_] excluding these

num="AmanJaiswal is not"
if(re.search("\w{2,20}\s\w{2,20}",num)): 
    #word/number/UScore len 2-20 then a space then word/number/US len 2-20 
    #\s returns Aman Jaiswal for 'Aman Jaiswal'
    #\S excludes the space between and returns true for things like "AmanJaiswal"
    #hence only 2 word pairs come out of it
    print(re.findall("\w{2,20}\s\w{2,20}",num))

email="sk@aol.com md@.com @seo.com dc@.com"
print(re.findall("[\w._%+-]{1,20}@[\w]{2,5}.[\w]{3}",email))

strng="jam and jands"
print(re.findall("j(am|ands)",strng))