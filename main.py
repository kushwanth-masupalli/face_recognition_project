from testingmodel import *
from register import *
    
while True :
    n = int(input("enter 0 for registration 1 for taking attendence any other for exit"))

    if n==0:
        register()
    elif n==1 :
        take_attendance()
    else :
        break