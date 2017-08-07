#!/usr/bin/env python3 

import re

#=================================================#
# split url
#=================================================#

result = []
urlparams = ''
urlist = []

def splitUrl(urldata):
    ''' split url
    
    split url on slash or ampersand
    '''
    localproxy = re.compile(r'^http://127.0.0.1[:0-9]?')
    rtmp = re.compile(r'^(rtmp|rtmpe)://')
    #amp = re.compile(r'(?=[&][a-zA-Z_]+=+[-a-zA-Z0-9.]?)')
    if '|' in urldata:
        print("match |")
        ud_split = urldata.split(r'|')
        ud_split_a = ud_split[0] # url before |
        ud_split_b = ud_split[1] # url after |
        urldata = [ud_split_a, ud_split_b] 
        urlist.extend(urldata)
        return urlist
    elif rtmp.match(urldata):
        print("rtmp")
        urlist.append(urldata)
        return urlist
    elif localproxy.match(urldata):
        print("localproxy")
        urlist.append(urldata)
        return urlist
    else:
        print("full url")
        urlist.append(urldata)
        return urlist


# regex patterns
patterns = {
           'user-agent': 'u?User-a?Agent=[a-zA-Z0-9/.()\s,:;%+_-]+',
           'referer': 'r?Referer=[a-zA-Z0-9/.()\s,:;%+_-]+',
           'x-forward': 'X-Forwarded-For=[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
           'cookie': '[cC]ookie=[a-zA-Z0-9/&%_*~;=_\s]+'
           }

# master function calls match_func
def master(urlparams):
    for match_func in rules:
        if match_func(urlparams):
            result.append(match_func(urlparams))
    return result

# match regular expressions
def match_func(pattern, urlparams):
    def match_rule(urlparams):
        itererator = re.finditer(pattern, urlparams)
        for match in itererator:
            return match.group()
    return match_rule

# rules must go after match_func
rules = [match_func(pattern, urlparams) for (pattern) in patterns.values()]

# split string on = and store in dict
def splitEquals(tosplit):
    return dict([v.split('=', 1) for v in tosplit if '=' in v])
