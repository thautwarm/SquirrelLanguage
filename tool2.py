# -*- coding: utf-8 -*-
from TypeSign import Mapping,Class
from tool import Dict,re
def makeCtype(types):
    if type(types) is str:
        return types
    else:
        In=types[0]
        Out=types[1]
        return "std::function<%s , %s>"%(makeCtype(In),makeCtype(Out))
        
class OBJ:
    def __init__(self,name,type):
        self.name=name
        self.type=type

class DefineTemplate:
    
    def __init__(self,Name,type,Action):
        
        """
        Param: list[OBJ]
        """
        self.Name=Name
        self.Type=type
        self.Action=Action
    def explain(self):
        
        if self.Type.typedef == Mapping:
            In=self.Type.In
            InType=In.InType
            params=In.params
            
            Out=self.Type.Out
            template=\
            """
             std::function<%s (%s)> %s = [ = ](%s) 
             {
             %s
             };
            """%(
                 Out,InType,self.Name,params,
                 self.Action)
            
            
            """
            squirrel v0.1:
                
            template=\
            "
             %s
             std::function<%s(%s) > = [ & ](%s) 
             {
             %s
             };
            "%('; '.join(self.Action.ReadyStack),
                 self.Name,self.Type.In,
                 '; '.join(Action.InStack))
            """
            
            
        elif self.Type.typedef == Class:
            template=\
           """
           
           class %s 
           {
           public:
             
            %s
            %s
            %s(){}
            
             %s(%s)
             {
                     
                 %s
             
             }
             
            };
           """  %(
                  self.Name,
                  self.Type.Params.params.replace(',',';\n')+';',
                  self.Action.Funcs,
                  self.Name,self.Name,
                  self.Type.Params.params,
                  re.sub('this(?![a-zA-Z_])','(*this)',self.Action.Members)
                  )
        return template
        
class InstanceTemplate:
    def __init__(self,Name,type,Action):
        self.Name=Name
        self.Type=type
        self.Action=Action  
    def explain(self):
        template=\
            """
             %s %s(%s);
            
            """%(
                 self.Type,self.Name,self.Action
                 )
        return template
class ParamST:
    def __init__(self,params):
        self.params=params
    def explain(self):
        if type(self.params) is str:
            return str
        else:
            types=[]
            names=[]
            name=True
            for i in self.params:
                if name and i!=',':
                    names.append(i)
                    name=False
                elif i in [',',':']:
                    continue
                elif not name :
                    types.append(TypeST(i).explain())
                    name=True
            ret=list(zip(names,types))
            
            getOneParam=lambda x:"%s %s"%(x[1],x[0])
            retP=Dict({'params':','.join(list(map(getOneParam,ret)))
            if type(ret) is list else ret, 'InType':','.join(types)})
            return retP
class TypeST:
    def __init__(self,typing):
        self.typing=typing
    def explain(self):
        typing=self.typing
        if type(typing) is str:
            return typing
        else:
            ret=[]
            mapp=False
            for type_i in typing:
                 if type_i=='=>':
                     mapp=True
                 elif type_i ==',':continue
                 else:
                     if mapp:
                         ret[-1]='std::function<%s(%s)>'%(TypeST(type_i).explain(),ret[-1])
                         mapp=False
                     else:
                         ret.append(TypeST(type_i).explain())
        if len(ret)==1:ret=ret[0]
        return ','.join(ret) if type(ret) is list else ret

        


    
            
            
            
            
            
            
            
            
            
            