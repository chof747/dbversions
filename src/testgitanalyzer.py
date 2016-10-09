#!/usr/bin/env python
'''
Created on 15. Sep. 2016

@author: chof
'''

from phpdbgit import *
from subprocess import call
import getopt
import sys

def usage():
    
    pass
global environment

if __name__ == '__main__':
    environment = "dev"
    
    try:
        command = sys.argv[1]
        optlist, args = getopt.getopt(sys.argv[2:], 'p:', ["projectpath="])
        
        for option, value in optlist:
            if option in ["-p", "--projectpath"]:
                projectpath = value
            else:
                assert False, "unhandled option"    
    except getopt.GetoptError as e:
        print str(e)
        usage()
                
    cfg = Config(projectpath)
    analyzer = GitAnalyzer(cfg)
    dumps = DbDump(cfg)
    
    if (command == 'branchparents'):   
        branch = cfg.repo.heads['change-analyze-transactions']
        c = branch.commit
        for i in range(20):
            commits = ''
            for p in c.parents:
                commits += p.hexsha + ", "
            print("%s --> %s" %(c, commits))
            c = c.parents[0]
                 
        pass
    
    elif (command == 'dump'):
        gitAnalyzer = GitAnalyzer(cfg)
        dump = gitAnalyzer.getNewestDumpCommit(cfg.getHead(), dumps.getAllDumpHashs())
        print dump
        
        
    elif (command == 'traverse'):
        gitAnalyzer = GitAnalyzer(cfg)
        pathes = gitAnalyzer.traverse(cfg.getHead(), gitAnalyzer.getNewestDumpCommit(cfg.getHead(), dumps.getAllDumpHashs()))
        i = 0
        for path in pathes:
            i = i + 1
            print "---------------\nPath: %d" % (i)
            
            for c in path:
              print "  %s" % (c.hexsha)

    elif (command == 'branch'):
        gitAnalyzer = GitAnalyzer(cfg)
        print gitAnalyzer.checkout()
                        
    elif (command == 'scripts'):
        gitAnalyzer = GitAnalyzer(cfg)
        scripts = gitAnalyzer.extractDBChanges(cfg.getHead(), gitAnalyzer.getNewestDumpCommit(cfg.getHead(), dumps.getAllDumpHashs()))
        
        print scripts
