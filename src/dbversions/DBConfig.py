'''
Created on 09. Okt. 2016

@author: chof
'''

from dbversions import astring
from gitanalyzer import GitAnalyzer
from db import DbDump

class DBConfig(object):

    def __init__(self, cfg):
        '''
        Constructor
        '''
        self.gitAnalyzer = GitAnalyzer(cfg)
        self.db = DbDump(cfg)
        self.cfg = cfg
        self.logger = cfg.logger
        
        #set basic stuff
        self.environments = self.cfg.getEnvironments()

    '''
    creates a snapshot from the database for the given commit
    '''        
    def snapshot(self):
    #***************************************************************************    
        for env in self.environments:
            self.logger.info("Make all database snapshots for %s" % (env))
            self.db.makealldumps(env)


    '''
    restore a specific db snapshot without executing any scripts added after
    the snapshot
    
    returns the dump commit
    '''
    def restore(self, dump = None):
    #***************************************************************************    
        
        dump = self.gitAnalyzer.getNewestDumpCommit(self.cfg.getHead(), 
                self.db.getAllDumpHashs()) if dump == None else dump
                
        for env in self.environments:
            self.logger.info("Restore databases for %s from %s" % (env, dump))
            self.db.restorealldumpsforcommit(dump, env) 
        
        return dump
    
    
    def execute(self, script):
    #***************************************************************************    
        for env in self.environments:
            self.db.executeScript(script, env)

    
    '''
    The checkout command takes care of a branch checkout: 
    If the branch 
      - is a new one the branchpoint will be stored in branch-index.json
        and the databases dumped for reference point
      - is an existing one the db will be restored based on the latest restore 
        point and the scripts added since then
    '''
    def checkout(self):
    #***************************************************************************    
        (commit, branch, newbranch) = self.gitAnalyzer.checkout()
        
        if newbranch:
            self.logger.info("New branch %s created: mark and backup state at %s" 
                            % (branch, commit))
            for env in self.environments:
                self.db.makealldumps(env)
        else:
            self.logger.info("Restore db structure for %s" % (branch))
            self.switch()
        
    
    def merge(self, main, topic):
    #***************************************************************************    
        lca = self.gitAnalyzer.findLatestCommonAnchestor(main.commit, topic.commit)
        dump = self.gitAnalyzer.getNewestDumpCommit(lca, self.db.getAllDumpHashs())
        
        self.logger.info('Merging DB scripts from branch %s into %s' % 
                         (astring(topic), astring(main)))
        self.logger.debug('Branch point is %s' % (astring(lca)))
        
        self.restore(dump)
        self._updateDBByScriptsFrom(dump)
        
        self.snapshot()
    
    '''
    The switch command performs a switch of the given environments to the current
    db state of the branch.
    
    This is achieved by the following actions which are executed consecutively:
        1. take the last db hash created in the commit tree of the current head
        2. identify all db scripts commited since the last hash
        3. execute them in the order of their commit (first commited first, 
           no matter how often it has been recommitted since) but in the 
           current state of the head
    '''            
    def switch(self):
    #***************************************************************************    
        self.logger.info("Switch to branch at head %s" % self.cfg.getHead())
        latestDump = self.restore()
        self._updateDBByScriptsFrom(latestDump)
        
    def _updateDBByScriptsFrom(self, latestDump):
    #***************************************************************************    
        scripts = self.gitAnalyzer.extractDBChanges(self.cfg.getHead(), latestDump)
        for script in scripts:
            self.execute(script[0])


    