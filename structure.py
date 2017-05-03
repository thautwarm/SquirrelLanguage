import re
def askForLib(lib):
    if lib[0]=='import':    
        with open('./lib/%s.cpp'%lib[1],'r',encoding='ascii') as f:
            return f.read()
        return ''
    elif lib[0]=='using':
        return "using namespace %s;"%lib[1]
    elif lib[0]=='include':
        return '#include "%s"'%lib[1]
def token(sentences):
    library=re.findall('(?<=\$).*(?=\$)',sentences)
    sentences=re.sub('\$.*\$','',sentences)
    library= '\n'.join((map(askForLib,[re.sub(r'\r\s\n','',i).split('<=') for i in library] )))
    return library,re.findall\
    ("""(?<= )is not(?= )|(?<= )is(?= )|(?<= )not(?= )|(?<= )and(?= )|(?<= )or(?= )|&[a-zA-Z_]+|=>=> *[a-zA-Z_]+|=>|[a-zA-Z_]+[0123456789a-zA-Z_<>\.\\\]*|\\\\|\:=|=+|[0123456789]+[0123456789]+|[0123456789]+|->|<-|".+?"|this\.|[!;\./+*\-\%$&():{}\]\[,\n]""",re.sub('#.*#','',sentences))