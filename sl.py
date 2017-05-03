# -*- coding: utf-8 -*-
"""
author: thautwarm
this is how we use the compiler.
"""
import os
import sys
import re
from Ex2 import expression
from structure import token
libGLOBAL=\
"""
#include "iostream" 
#include "vector"
#include "functional"
#include "algorithm"
#include "list" 
"""
def squirrel_compile(stats):
    return expression(stats)
def getCompile(in_,out_):
    cache_file=in_.replace('.squirrel',"_cache.cpp")
    with open(in_,encoding="ascii") as f:
        stats=f.read()
    lib,sentences=token(stats)
    produce="%s \n %s \n int main(){%s}"%(libGLOBAL,lib,squirrel_compile(sentences))
    with open(cache_file,'w',encoding='utf-8') as f:
        f.write(re.sub(' {3,}','  ',re.sub('; {2,}',';',produce)))
    os.system("""g++ %s -o %s -std=c++14"""%(cache_file,out_))
if __name__=='__main__':
    getCompile(sys.argv[1],sys.argv[2])
    
