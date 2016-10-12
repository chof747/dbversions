'''
Created on 16. Sep. 2016

@author: chof
'''

from dbversions import astring   
import sys
import operator

class InvalidBranch(Exception):
    pass

class GitAnalyzer(object):
    '''
    classdocs
    '''

    EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


    def __init__(self, config):
    #***************************************************************************
        '''
        Constructor
        '''
        self.cfg = config
        
            
    def getNewestDumpCommit(self, head, dumps):
    #***************************************************************************        
        c = head
        dump = None
        
        while True:
            if c.hexsha in dumps:
                dump = c
                break
        
            if len(c.parents) > 0:
                c = c.parents[0]
            else:
                break
            
        return dump
    
    def checkout(self):
    #***************************************************************************        
        branchname = self.cfg.repo.active_branch.name
        newbranch = self.isNewBranch(self.cfg.repo.active_branch)
        
        return (self.cfg.getHead(), branchname, newbranch)
        
        
    def isNewBranch(self, branch):
    #***************************************************************************
        return len(branch.log()) == 1
        
    def parentChain(self, commit):
        '''
        produces the list of direct ancestors (parent no 1) for a given commit up
        to the root node.
        
        Returns this list in reverse order with the youngest anchestor first
        '''
    #***************************************************************************    
        chain = []
        while len(commit.parents) > 0:
            chain.append(commit)
            commit = commit.parents[0]
        
        chain.append(commit)
            
        return chain
    
    def findLatestCommonAnchestor(self, a, b):
    #***************************************************************************    
        chainA = self.parentChain(a)
        chainB = self.parentChain(b)
        
        #print(chainA)
        #print('===')
        #print(chainB)
        lca = None
                
        while ((len(chainA)>0) and (len(chainB)>0) and 
               (chainA[-1] == chainB[-1])):
            lca = chainA.pop()
            chainB.pop()
            
        return lca
        
    
    def traverse(self, head, stop):
        '''
        returns a list of iterators each representing a path between the head
        and the stop node by traversing the commit tree as follows:
        
        1. go from the head commit to the immedeate parent in the branch of the 
        commit
        
        2. if the parent is the stop commit end the path
        
        3. if the commit has more than one head push the additional parent to a queue and store the visited nodes with it
        
        4. at the end move to the next entry in the queue
        '''
    #***************************************************************************    
        paths = []
        queue = []
        queue.append((head, []))
        
        while len(queue) > 0:
            (commit, path) = queue.pop(0)
               
            while True:
                path.append(commit)

                if commit.hexsha == stop.hexsha:
                    paths.append(path)
                    break
                
                if len(commit.parents) == 0:
                    raise Exception('Loose Path: your current branch is merged with a branch that does not have a the same DB origination!')
                
                if len(commit.parents) > 1:
                    branchPath = list(path)
                    for i in range(1,len(commit.parents)):
                        queue.append((commit.parents[i], branchPath))
                        
                commit = commit.parents[0]

        return paths
    
    def _extractScripts(self, head, dump):
    #***************************************************************************
        scripts = {}
        traverses = self.traverse(head, dump)
        for traverse in traverses:
            pathscripts = {}
            sequence = sys.maxint
            for c in traverse:
                for script in self.extractSetupScripts(c):
                    #store the script with the hash of the commit as value
                    #if the script is not present already
                    #if not pathscripts.has_key(script):
                        pathscripts[script] = sequence, astring(c.hexsha)
                        sequence = sequence - 1
            
            if (set(scripts).issubset(set(pathscripts))):
                scripts = pathscripts
            else:
                raise Exception('Branches contain conflicting DB scripts %s\n---\n%s' %
                                (' '.join(scripts.keys()), ' '.join(pathscripts.keys())))
        
        return scripts

    def extractDBChanges(self, head, dump):
    #***************************************************************************
        scripts = self._extractScripts(head, dump)
        scripts_sorted = sorted(scripts.items(), key=operator.itemgetter(1))
        scripts = []
        for script in scripts_sorted:
            scripts.append((script[0], script[1][1]))
            
        return scripts
    
    def getFilesOfCommit(self, commit, path):
    #***************************************************************************
        if not commit.parents:
            diff = commit.diff(GitAnalyzer.EMPTY_TREE_SHA, path)
        else:
            diff = commit.diff(commit.parents[0], path)
            
        files = []
            
        for f in diff:
            if f.b_path != None:
                files += [ self.cfg.fullpath(f.b_path) ] 
        return files

    
    def extractSetupScripts(self, commit):
    #***************************************************************************
        return self.getFilesOfCommit(commit, self.cfg.setupscriptpath)
    