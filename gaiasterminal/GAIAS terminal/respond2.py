
import json
def flush(textfile):
    with open(textfile,"w") as some_file:
        some_file.close()
def openfile():
        with open("speechout.txt","r") as file:
                out = file.read()
                global out
        return out

def dwrite(data):
    with open("output.txt","a") as some_file:
        some_file.write(data + "::")

def define(userin):

	word = userin

	wordf = word.split(" ")

	pos = wordf.index("is")

	varname = wordf[pos-1]
	varvalue = wordf[pos+1]
	global join
	join = {varname : varvalue}
	return join

openfile()
if(out.find("is") != -1 ):
        print(define(out))
        dwrite(str(join))
        flush("speechout.txt")
                
exit()
