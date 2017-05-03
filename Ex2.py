# -*- coding: utf-8 -*-
"""
author: thautwarm
this is something about explaining the grammar of Squirrel.
"""
from tool import Dict,newSplit,enum,checkObj
var1=Dict({'{':'}','[':']'})
Cost=Dict({'}':2,']':1})
var1_1={')','}',']'}
var2={':=','=','>=','<=','>','<','=>'}
KO=Dict(map='bfunc',reduce='bfunc',filter='bfunc',
         Int='int',Float='double',Str='std::string',
         Vec='std::vector',List='std::list',
         Map='std::map',HashMap='std::hash_map',
         Set='std::set',a='int',b='int',c='int',tuple='std::tuple',tie='std::tie')
def Try(ws,i):
    try:
        ws[i]
        return True
    except:
        return False 
Split=lambda x:newSplit(x,BlockStatus=var1,CostDict=Cost)      
limap=lambda func,*its:list(map(func,its))
lifilter=lambda func,its:list(filter(func,its))
from tool2 import DefineTemplate,Mapping,Class,InstanceTemplate,TypeST,ParamST


JudgeMentDict=Dict({'is':'==','not':'!','and':'&&','or':'||'})
JudgeWeightDict={'not':2,'is':1,'is not':1,'and':0,'or':0}
from copy import deepcopy
def deepReplace(RepDict,obj):
    if type(obj) is str :
        if obj in RepDict :return obj
        return RepDict[obj]
    else:
        summas=[]
        lastWeight=[0]
        unit=[['(']]
        for i,obj_i in enum(obj):
            if type(obj_i) is str :
                if obj_i in RepDict:
                    objt=JudgeMentDict[obj_i]
                    if lastWeight[-1]>=JudgeWeightDict[obj_i]:
                        summas+=['(']+deepcopy(unit[-1])+[')']
                        unit[-1]=[]
                        summas.append(objt)
                    else:
                        if unit[-1]:
                            summas+=['(']+deepcopy(unit[-1][:-1])+[')'] 
                            a=[deepcopy(unit[-1][-1])]
                        else:
                            a=[]
                        unit[-1]=a+[objt]
                    lastWeight[-1]=JudgeWeightDict[obj_i] 
                else:
                    unit[-1].append(obj_i) 
            else:
                unit[-1].append(obj_i) 
        summas+=unit[-1]+[')']
        summas=[deepReplace(RepDict,i)  if type(i) is list else i for i in summas]
        return ' '.join(summas)

def checkDef(sens):
    if sens and len(sens)==4 and sens[1]==':=':
        return True
        
Split2=lambda x:newSplit(x,{'(':')'},{')':1},None,False)    
def Expr(sens):
    if type(sens) is str:
        
        return sens
    if type( sens ) is list :
         ###顺序
        if len(sens)==1:
            sens=sens[0]
            if type(sens) is str:
                jd=lifilter(lambda x: x, sens.split(' '))
                if len(jd)==2 and '=>=>'==jd[0]:    
                    return "goto %s;"%jd[1]
                elif len(jd)==1 and jd[0][0]=='&':
                    return '%s: ;'%jd[0][1:]
            
        if not sens : return ';'
        if len(sens)==1:return sens[0]
        
        elif sens[1]==':=':
                TypeName=sens[0]
                if '=>' in sens[2]:
                    index=sens[2].index('=>')
                    In=ParamST(sens[2][:index]).explain()
                    Out=TypeST(sens[2][index+1:]).explain()
                    Type=Dict(typedef=Mapping,In=In,Out=Out)
                    Action=Expr(sens[3])
                else:
                    Funcs=Expr(lifilter(lambda x: checkDef(x) ,sens[3]))
                    Members=Expr(lifilter(lambda x:not checkDef(x) ,sens[3]))
                    Action=Dict(Funcs=Expr(Funcs),Members=Expr(Members))
                    #toEXPR
                    
                    
                    InParams=ParamST(sens[2]).explain()
                    Type=Dict(typedef=Class,Params=InParams)
                return DefineTemplate(TypeName,Type,Action=Action).explain()
        elif sens[1]==':' and len(sens)==4:
                InstanceName=sens[0]
                Type=TypeST(sens[2]).explain()
                Action=Expr(sens[3])
                
                #toEXPR
                return InstanceTemplate(InstanceName,Type,Action).explain()
        elif sens[1]==':' and  len(sens)==3:
                AnnoName=sens[0]
                Type=TypeST(sens[2]).explain()
                if type(Type) is list:
                    Type="std::tuple<%s >"%(', '.join(Type))
                return "%s %s"%(Type,AnnoName)
        elif sens[0]=='if':
            return\
            """
            if( %s ){
            %s
            ;
            }
            else{
            %s
            ;
            }
            """%(Expr(deepReplace(JudgeMentDict, Split2(sens[1:-3]) )),Expr(sens[-3]),Expr(sens[-1]))

        else:
            sens=' '.join([Expr(sen_i) for sen_i in sens])          
    return sens
        
def expression(ws):
    sens=Split(ws)
    return Expr(sens)



    











