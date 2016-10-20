#!/usr/bin/env python
'''
Created on 15. Sep. 2016

@author: chof
'''

from dbversions import Config, DbDump, DBConfig, parseEnvironments
import getopt
import sys


def usage():
#***************************************************************************    
    pass

global environment
global cfg
global dbdumps

if __name__ == '__main__':
    environment = None
    projectpath = '.'
    verbosity = 0
    
    try:
        command = sys.argv[1]
        optlist, args = getopt.getopt(sys.argv[2:], 'vp:e:o:s:', ["projectpath=", "env=", "script="])
        
        for option, value in optlist:
            if option in ["-p", "--projectpath"]:
                projectpath = value
            elif option in ["-s", "--script"]:
                script = value 
            elif option in ['-e', '--env']:
                environment = parseEnvironments(value)
            elif option in ['-v']:
                verbosity = verbosity + 1
            else:
                assert False, "%s is an unhandled option" % (option)    
    except getopt.GetoptError as e:
        print str(e)
        usage()

    cfg = Config(projectpath)
    
    if environment == None:
        environment = cfg.environments
    else:
        cfg.environments = environment
        
    if verbosity > 0 :
        cfg.setLoggingVerbosity(verbosity)
    
    dbconfig = DBConfig(cfg)
    dbdumps = DbDump(cfg)
    
    if (command == 'snapshot'):
        dbconfig.snapshot()
            
    elif (command == 'restore'):
        dbconfig.restore()

    elif (command == 'switch'):
        dbconfig.switch()
        
    elif (command == 'checkout'):
        dbconfig.checkout()
        
    elif (command == 'merge'):
        main = cfg.getHeadOfBranch(args.pop(0))
        topic = cfg.getHeadOfBranch(args.pop(0))
        dbconfig.merge(main, topic)
        
    elif (command == 'execute'):
        try: 
            dbconfig.execute(script)
        except EnvironmentError as e:
            cfg.logger.error(e)


    pass