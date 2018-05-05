#!/usr/bin/env python

import sys

prevHead = sys.argv[1]
newHead = sys.argv[2]
branchCheckout = int(sys.argv[3])

if (branchCheckout == 1) and not (prevHead == newHead):
    
    import os
    from dbversions import Config, DBConfig
    
    projectpath = os.getcwd()
    cfg = Config(projectpath)
    cfg.setLoggingVerbosity(2)
    dbconfig = DBConfig(cfg)
    dbconfig.checkout()
    
else:
    pass