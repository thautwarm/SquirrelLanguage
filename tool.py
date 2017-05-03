# -*- coding: utf-8 -*-

class Dict(dict):
    def __init__(self,*args,**kwargs):
        super(Dict,self).__init__(*args,**kwargs)
        for key in self.keys():
            self.__setattr__(key,self[key])
    def __setitem__(self,key,value):
        super(Dict,self).__setitem__(key,value)
        super(Dict,self).__setattr__(key,value)
    def __setattr__(self,key,value):
        super(Dict,self).__setitem__(key,value)
        super(Dict,self).__setattr__(key,value)       
    def __delattr__(self,key):
        super(Dict,self).__delattr__(key)
        super(Dict,self).__delitem__(key)
    def __delitem__(self,key):
        self.__delattr__(key)
    def update(self,dic):
        sets=self.keys()|dic.keys()
        items=[self[i]  if i in self else dic[i] for i in sets]
        self.__init__(zip(sets,items))
asciiWords={'/','\\','//',':','.','->','<-','*','+','-','=','==','%','^','!'}
identityWords={';','(',')','<','>'}
ExprSplitSin=[',','-','/','+','*','=','==','>','<','>=','<=','=>']
enum=enumerate
import re
def checkObj(w):
    u=re.findall('[a-zA-Z_]+[\.0123456789\\\]*',w)
    return u and u[0]==w
def check(w,*O):
    for o in O:
         if w in o:
             return True
    return False
import copy
copy=copy.deepcopy
class AncestorList(list):
    def __init__(self,*arg,**kwargs):
        super(AncestorList,self).__init__(self,*arg,**kwargs)
        self.father=None
    def branch(self):
        self.append(AncestorList())
        self[-1].father=self
    def toList(self):
        ret=[i.toList() if isinstance(i,AncestorList) else i for i in self]
        return ret
    
def newSplit(sen,BlockStatus={},CostDict={},mer=';',append=False):
    ret=AncestorList()
    ret.branch()
    obj=ret[-1]
    chsIndentity=[]
    for sen_i in sen:
        if sen_i=='\n':
            continue
        if mer and sen_i ==mer:
            obj=obj.father
            obj.append(mer)
            obj.branch()
            obj=obj[-1]
        elif sen_i in BlockStatus:
            chsIndentity.append(BlockStatus[sen_i])
            for i in range(CostDict[chsIndentity[-1]]):
                obj.branch()
                obj=obj[-1]
                if append:
                    obj.append(sen_i)
        elif chsIndentity and sen_i == chsIndentity[-1]:
            if append:
                obj.append(sen_i)
            for i in range(CostDict[sen_i]):
                obj=obj.father
                
            chsIndentity.pop()
        else:
            obj.append(sen_i)
    ret=ret.toList()
    return ret
     
            
                    
     