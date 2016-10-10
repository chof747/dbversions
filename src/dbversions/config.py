'''
Created on 15. Sep. 2016

@author: chof
'''

import json
import os

from git import Repo
from dbversions import astring
import logging



class Config(object):
    '''
    classdocs
    
    The configuration class takes the project path to initialize the repo and
    also the configuration file for the database (db-config.json) as well as
    the dbversion basics (.dbversion) another json file which is kept seperately
    to enable sandbox specific locations of dump directory and files.
    
    db-config.json is project specific and should be versioned in git
    '''
    
    DBVERSION_CONFIG = '.dbversion'
    
    DEFAULTS = {
        'dbconfig'  : 'database/db-config.json',
        'dumpspath' : 'database/dumps',
        'logger' : {
            'default-verbosity' : 1,
            'logformat'  : '[%(asctime)s | %(name)s | %(levelname)-5s]: %(message)s',
            'logdatefmt' : '%Y-%m-%d %H:%M:%S'
        },
        'environments' : ['dev', 'test']
    }
    
    def __init__(self, projectpath):
        '''
        Constructor
        '''
    #***************************************************************************
        self.repodir = projectpath
        parameters = self._readBaseConfig(projectpath)
        
        dbconfigfile = projectpath + "/" + astring(parameters['dbconfig'])
        
        with open (dbconfigfile) as config_file:
            self._dbconfig = json.load(config_file)
            
        self.repo = Repo(self.repodir)
        self.outputpath = self.fullpath(parameters['dumpspath'])        
        self.setupscriptpath = self.fullpath(self._dbconfig['setupscripts'])
        self.branchIndexFile = self.fullpath(self._dbconfig['branch-index'])
        
        logging.basicConfig(format=parameters['logger']['logformat'],
                            datefmt=parameters['logger']['logdatefmt'])
        self.logger = logging.getLogger('dbversions')
        self.setLoggingVerbosity(parameters['logger']['default-verbosity'])
        self.environments = parameters['environments']
            
    def setLoggingVerbosity(self, verbosity):
    #***************************************************************************
        VERBOSITY = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
        if verbosity > 3:
            verbosity = 3            
        
        self.logger.setLevel(VERBOSITY[verbosity])
        
    def fullpath(self, path):
    #***************************************************************************
        return "%s/%s" % (self.repodir, astring(path))
    
    def databases(self, environment):
    #***************************************************************************
        dbs = self._dbconfig['databases']
        dblist = []
        if not environment == None:
            for db in dbs:
                dblist.append(astring(dbs[db][environment]))
        else:
            for db in dbs:
                dblist.append(astring(db))
        
        return dblist
    
    def getDBName(self, db, env):
    #***************************************************************************
        dbname = ''
        dbs = self._dbconfig['databases']
        if dbs.has_key(db):
            if dbs[db].has_key(env):
                dbname = dbs[db][env]
                
        return dbname
    
    def getEnvironments(self):
        return self.environments
    
    def getHead(self):
    #***************************************************************************
        return self.repo.commit('HEAD')
    
    def getHeadHash(self):
    #***************************************************************************
        return astring(self.getHead().hexsha)
    
    def _readBaseConfig(self, projectpath):
    #***************************************************************************
        dbconfigfile = projectpath + '/' + Config.DBVERSION_CONFIG
        if not os.path.isfile(dbconfigfile) :
            with open(dbconfigfile, 'w') as f:
                json.dump(Config.DEFAULTS, f)
        
        with open(dbconfigfile) as f:
            parameters = json.load(f)
        return parameters
            