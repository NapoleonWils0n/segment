#!/usr/bin/env python3 

# import modules
from pilfer import validate, regex, record
import sys, re, getopt, os.path, mimetypes

#=================================================#
# sys       = system access to open files
# re        = regular expressions
# getopt    = check script arguments and options
# os.path   = check if first argument is a file
# mimetypes = check if file is a text file
# unquote   = decode urls
#=================================================#

# argv
argv = sys.argv[1:]

# shortcuts for imported functions
usage = validate.usage
checkurl = validate.checkurl
durationValidated = validate.durationValidated
argLength = validate.argLength
splitUrl = regex.splitUrl
splitEquals = regex.splitEquals

#=================================================#
# main function
#=================================================#

def main(argv):
    ''' main function
    
    check number of arguments passed to script
    '''
    
#=================================================#
# check number of arguments passed to script
#=================================================#

# if script is run with no arguments or more than 4 arguments
# display script usage and exit

    argLength(argv)

#=================================================#
# check options and arguments
#=================================================#

# h = help
# i: = url, the : means i requires an argument which would be the url
# t: = time, the : means t requires an argument which would be the time in 00:00:00 format

    try:
        opts, args = getopt.getopt(argv, "hi:t:", ["help", "url", "time"])
    except getopt.GetoptError as err: 
        print(err)  # will print something like "option -x not recognized"
        usage()     # display script usage
        sys.exit(2) # exit

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # -h or --help = display help
            usage()
            sys.exit()
        elif opt == ("-i") and len(argv) == 2:
            # -i and url or text file - argv length 2, valid options and args
            checkurl(argv[1]) # checkurl function
        elif opt == ("-t") and len(argv) == 2:
            # -t option on its own - invalid
            print("the -t option must be used after the -i option")
            usage()
            sys.exit()
        elif opt in ("-i", "-t") and len(argv) == 4:
            if "-t" in opts[0]:
                # -t option used before -i option - invalid
                print("the -t option must be used after the -i option")
                usage()
                sys.exit()
            else:
                # -i url followed by -t 00:00:00 = valid
                checkurl(argv[1]) # checkurl function
                durationValidated(argv[3])
        else:
            assert False, "unhandled option"

#=================================================#
# slice off script name from arguments
#=================================================#

if __name__ == "__main__":
    main(sys.argv[1:])

    # check if 1 or 3 args are passed to the script
    if len(argv) == 2:
        urlDecoded = checkurl(argv[1])
    elif len(argv) == 4:
        urlDecoded = checkurl(argv[1])
        tflag = "-t"
        duration = durationValidated(argv[3])
    

    # the url stored in a dictionary
    theUrl = splitUrl(urlDecoded)
    
    # url dictionary keys lowercased for searching
    urlDict = {k.lower(): v for k, v in theUrl.items()}

    # ffmpeg dictionary to hold url and ffmpeg options
    ffmpegDict = {}

    if 'url' in urlDict:
        ul = urlDict['url']
        url = '{0}'.format(ul)
        ffmpegDict['url'] = url

    if 'user-agent' in urlDict:
        ua = urlDict['user-agent']
        useragent = "-user-agent '{0}'".format(ua)
        ffmpegDict['user-agent'] = useragent

    if 'referer' in urlDict:
        rf = urlDict['referer']
        referer = "-headers 'Referer: {0}'".format(rf)
        ffmpegDict['referer'] = referer

    if 'cookie' in urlDict:
        cd = re.search('(http|https)://[a-zA-Z0-9.-]*[^/]', url) # cookie domain name
        cookiedomain = cd.group()
        cookieurl = urlDict['cookie']
        cookie = "-cookies '{0}; path=/; {1};'".format(cookieurl, cookiedomain)
        ffmpegDict['cookie'] = cookie

    nltid = re.findall('nltid=[a-zA-Z0-9&%_*=]*', url) # nltid cookie in url

    if nltid:
        cd = re.search('(http|https)://[a-zA-Z0-9.-]*[^/]', url) # cookie domain name
        cookiedomain = cd.group()
        cookieurl = nltid[0]
        cookie = "-cookies '{0}; path=/; {1};'".format(cookieurl, cookiedomain)
        ffmpegDict['nltid'] = cookie


    # http and rtmp regexes
    http = re.compile(r'^(http|https)://')
    rtmp = re.compile(r'^(rtmp|rtmpe)://')


    # check number of args passed to script
    if len(argv) == 2:
        if http.match(url):
            ffrec = record.ffmpeg(**ffmpegDict)
        elif rtmp.match(url):
            rtmprec = record.rtmp(**ffmpegDict)
    elif len(argv) == 4:
        ffmpegDict['tflag'] = tflag # add tflag and duration to ffmpegDict
        ffmpegDict['duration'] = duration
        if http.match(url):
            ffrec = record.ffmpeg(**ffmpegDict)
        elif rtmp.match(url):
            rtmprec = record.rtmp(**ffmpegDict)
