from git import Commit

def astring(s):
    
    if isinstance(s, unicode):
        s = s.encode('ascii', 'ignore')
    elif isinstance(s, Commit):
        s = s.hexsha
    return s

from config import Config 
from db import DbDump
from gitanalyzer import GitAnalyzer
from DBConfig import DBConfig

def parseEnvironments(option):
    envs = option.split(',')
    return envs