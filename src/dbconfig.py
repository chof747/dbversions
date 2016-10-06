#!/usr/bin/env python
'''
Created on 15. Sep. 2016

@author: chof
'''

from phpdbgit import Config, DbDump, GitAnalyzer
from subprocess import call
import getopt
import sys
import logging
import phpdbgit

def usage():
    
    pass
global environment

if __name__ == '__main__':
    environment = "dev"
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
                environment = phpdbgit.parseEnvironments(value)
            elif option in ['-v']:
                verbosity = verbosity + 1
            else:
                assert False, "%s is an unhandled option" % (option)    
    except getopt.GetoptError as e:
        print str(e)
        usage()

    cfg = Config(projectpath)
    if verbosity > 0 :
        cfg.setLoggingVerbosity(verbosity)
    dbdumps = DbDump(cfg)
    
    if (command == 'snapshot'):
        for env in environment:
            cfg.logger.info("Make all database snapshots for %s" % (env))
            dbdumps.makealldumps(env)
            
    elif (command == 'restore'):
        gitAnalyzer = GitAnalyzer(cfg)
        dump = gitAnalyzer.getNewestDumpCommit(cfg.getHead(), dbdumps.getAllDumpHashs())
        for env in environment:
            cfg.logger.info("Restore databases for %s from %s" % (env, dump))
            dbdumps.restorealldumpsforcommit(dump, env) 
        
    elif (command == 'execute'):
        try:
            result = dbdumps.executeScript(script, environment)
        except EnvironmentError as e:
            cfg.logger.error(e)

    pass