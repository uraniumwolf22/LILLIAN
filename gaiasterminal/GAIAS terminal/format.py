import os
import numpy
import sys
import time as t

def define(userin):

	word = userin

	wordf = word.split(" ")

	pos = wordf.index("is")

	varname = wordf[pos-1]
	varvalue = wordf[pos+1]
	global join
	join = {varname : varvalue}
	return join

