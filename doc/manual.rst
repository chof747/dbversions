=============================================
**dbversions** - Database Versioning with Git
=============================================

-----------
User Manual
-----------

1. Purpose and underlying concept
=================================

If you have a software project you usually keep it under version control to be
able to have different versions in production and in development and to be able
to fix issues in the productive branch even if the development branch is 
currently unstable and cannot be deployed with the required fix to your 
production.

This is in general a very useful thing and will save you many troubles with your
users, clients and bosses. And if you only deal with flat files (code, 
configuration, data ...) this is sufficient enough, but it becomes a different
story if your software also uses a database which is also changing with the 
different versions of your application.

In such cases you can either hope that your database is always downward 
compatible or you can use a tool such as liquibase_ which offers a lot of 
functionality including database refactoring but is rather cumbersome to 
install and requires specific formatting of your database change scripts.

.. _liquibase: http://www.liquibase.org

**dbversions** offers a third way which is not as powerful as liquibase_ or
similar tools but offers basic operations in terms of different database 
versions compared with an easy to use setup and integration into existing
repositories. The basic concept is that :

* snapshots of the databases of a project are stored for distinct commits
  (e.g. at branch points or after a merge - but can be any commit)
  
* on checkout of another branch the latest commits are restored and all
  db scripts in a specific directory which have been added/changed since 
  this commit are executed on the restored database to get the structure
  for that specific branch

* on merge take the database snapshot closest to the specific branch
  point, restore it and execute all db scripts added/changed since then
  in the old and new branch (thereby checking if scripts are conflicting)

* handling databases for different environments (e.g. a set of development and
  test databases, or staging and test ...)
  
Besides this basic workflow the tool has the following features:

* setup generic scripts so that they can be executed on any environment
* execute generic scripts on one, a set of or all of your environments
* snapshot and restore database dumps related to any commit

2. Installation
===============

To install the tool you have the following possibilities:

2.1 Installing the package
__________________________

2.1.1 Install package from pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simply install **dbversions** from PyPi with the following command::

  pip install dbversions

This will install the tool in your standard python site packages and the scripts 
in an executable path. No further steps are necessary except for initializing a 
specific repository.

2.1.2 Install from source
~~~~~~~~~~~~~~~~~~~~~~~~~

When installing from source you have to 

1. download the source distribution from ##add link here##. 

2. extract the source into a new, empty directory::

    tar zfx dbversions-<version>.tar.gz
    cd dbversions-<version>

3. execute the setup script::

    sudo python setup.py install
    

2.2 Initialize a Repository
___________________________

After installing the package either via pip or via the source package you are
ready to use it by initializing any existing Git repository with dbversion_init.
To do this go to the respective main directory of the repository (the parent 
directory of .git) and execute the following command::

   dbversions_init.py -p .
  
Where

  -p .. provides the path to the git repository (you can also state here any
  other path to a valid git repository  
  
This will do the following things:

* Create a ``database`` directory under the directory given by -p this is the main
  directory where the setup scripts and the database dumps for the respective
  repositories will be stored

* Initialize a default db-config.json_ file in that directory which holds the 
  major - repository wide - configurations for dbversions  
  
* Setup a dbversions_ config file in the main path of the repository which
  contains important configurations for your specific use of dbversions
  
* Link the hook script for ``post-checkout`` to the hooks of your repository if
  no post-checkout hook exists. Otherwise it warns you and you will have to 
  place the hook yourself in order to avoid any male functions with other git
  tools.

3. Main Operations
==================

.. _general parameters:
.. _projectpath:                     
.. _verbosity:
.. _environments:

3.0 ``dbconfig`` and general parameters
_______________________________________

The ``dbconfig.py`` script is the working horse of **dbversions**. It is copied
by the installation procedure to the local bin directory to be executable from
all locations on the system.

``dbconfig.py`` script takes as the first argument the action to be performed 
which are described in the sections below. In general the script accepts the 
following parameters:

-v                   The verbosity is the level of logging applied for the 
                     current call of the script. You can use the parameter more 
                     times to increase the `level of logging`_
-p path              path to the root of the repository. The current path of the  
                     shell is the default. 
                     Has also a long version ``-projectpath=`` *path*.
-e environments      A comma separated list of environments (e.g. ``dev,test``) 
                     that should be considered for the dedicated operation. If 
                     set the db dumps and database scripts are done for all the 
                     given environments. If any environment is not available for
                     a Dump a warning is stated

.. _level of logging:

3.0.1 Level of logging:
~~~~~~~~~~~~~~~~~~~~~~~

========= ========= ========================================================
 # of -v   Level     Description
========= ========= ========================================================
 0         ERROR     Only errors that cause the program to abort are logged
                     Works as silent mode
 1         WARN      Situation that cause the omission of some part of the 
                     execution are reported, in order to give the user a 
                     hint that manual intervention is needed afterwards.
                     (The default level)
 2         INFO      Information about the different steps in the execution 
                     sequence are logged and reported to the user
 3         DEBUG     Very verbose logging also of debugging statements.
========= ========= ========================================================


3.1 Take a snapshot
___________________

A snapshot of the databases at the current commit of the current branch can be
triggered by::

  dbconfig.py snapshot [-p path] [-v[vv]] [-e env1,env2]
  
creates a snapshot of all logical databases out of the current state of the 
database schemas associates with the given environments ``env1`` and ``env2`` in
the git repository rooted at ``path`` and stores them in the folder specified in
the .dbversions_ file for the database dumps onder the sha key of the current 
commit.

**Example:**
  If you have 
  
  * a repository under ``/home/user/git/repo1`` which has been 
    initialized for **dbversions**
  * the database dumps for ``repo1`` are stored in the folder
    ``/home/user/dbdumps/repo1`` as specified in repo1's .dbversions_ file. 
  * the project under version control in repo1 uses the logical databases  
    ``customers`` and ``products`` 
  * and the head revision sha key of the working copy in repo1 is 
    ``0466f46428413c68c8bdec81d42ad848c0b30f15`` 
  
  executing the command::
  
    dbconfig.py snapshot -p /home/user/git/repo1 -env test,dev 
    
  will create the SQL dumps:
    - customertest.sql
    - customerdev.sql
    - productstest.sql and
    - productsdev.sql
    
  in the directory ``/home/user/dbdumps/repo1/0466f46428413c68c8bdec81d42ad848c0b30f15``.

3.2 Restore from a snapshot
___________________________

The restore command will always restore the youngest snapshot of the database
based on the commit sequence of the repository::

   dbconfig.py restore [-p path] [-v[vv]] [-e env1,env2]
  
The parameters are descripted under `general parameters`_

3.3 Executing DB scripts
________________________

With **dbversions** you can also write the database update scripts written for
a specific topic in a environment agnostic way by using the logical database
schema names and use the following command to execute them for more than one
environment::

   dbconfig.py execute -s script [-p path] [-v[vv]] [-e env1,env2]

This will execute the SQL script ``script`` for the environments env1 and env2
of the given repository.

3.3.1 Make SQL Scripts environment agnostic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When writing SQL scripts to be executed by **dbversions** one simply has to use 
not physical database schema names in the SQL code but refer to the logical
database names in the form ``{database}``. When executing the script the tool 
searches for logical database names in braces and replaces them with the
physical DB schema name for the respective environment.

**Example**:

The script::

      CREATE TABLE `{auxilbase}`.`account` (
        `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `ACCOUNT_NAME` varchar(80) DEFAULT NULL,
        `FK_OWNER_ID` int(10) unsigned NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `FK_ACCOUNT_OWNER` (`FK_OWNER_ID`),
        CONSTRAINT `FK_ACCOUNT_OWNER` FOREIGN KEY (`FK_OWNER_ID`) REFERENCES `{primebase}`.`a` (`ID`) ON DELETE CASCADE ON UPDATE NO ACTION
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;
        
when executed for the ``deb`` environment will exchange ``{auxilbase}`` with
the phyiscal schema name  ``auxildev``and ``{primebase}`` with the physical
name ``primebasedev``.

Any errors are written back to the console like for mysql.    

3.4 Checkout a different branch
_______________________________

Checkout is performed either automatically (by the post-checkout hook) or it can
be triggered with::

   dbconfig.py checkout  [-p path] [-v[vv]] [-e env1,env2]
   
The checkout command performs the following:

1. Based on the checked out branch it searches for the most recent database 
   dump and restores it
2. All commits since the commit associated with the database dump are searched
   for changed or added sql scripts in the path specified under ``setupscripts``
   in the `db-config.json'_ configuration file
3. If no conflicts are identified within these scripts the scripts are executed
   in the order of their first commit for all specified environments
   

3.5 Merge two branches
______________________

When a feature/topic branch has been merged into the master or another topic 
branch the database scripts have to be merged by the command::

   dbconfig.py merge target source [-p path] [-v[vv]] [-e env1,env2]

where ``target`` is the receiving (main) branch and  ``source`` is the branch
which has been merged into main.

The merge command performs the following actions:

1. It searches in the commit tree for the branching point of the two branches
2. It restores the most recent database dump on the main/target branch prior or
   at the branch point
3. It traverses all branches involved in the merge to collect all database setup
   scripts updated/added since the restored database dump
   
   **Note**:
     If there are scripts on one branch which are not included in the scripts of
     the other branch (i.e. you have updated the database structure in both
     branches of the merge). An error or warning is provided depending on the 
     settings of the tool. Note that in this case the scripts have to be merged
     manually
     
4. The scripts are executed if no conflicts occure (in the order of the earliest
   commit) 
   
5. A database dump is performed for the current commit

4. Configuration
================
.. _db-config.json:

4.1 *db-config.json* repository wide configuration
__________________________________________________

The ``db-config.json`` file is the configuration file which contains the 
database configuration for the respective repository which is valid for all 
branches and in all sand boxes. An example basic configuration of this file can
look like this::

   {
     "db-system": {
       "name" : "mysql",
       "version" : ">5.1"
     }, 
     "databases":{
       "db1":{
         "dev":"db1dev",
         "test":"db1test",
         "prod":"db1"
       },
       "db2":{
         "dev":"db2dev",
         "test":"db2test",
         "prod":"db2"
       }
     },
     "setupscripts": "database/setup",
   }
   
The meaning of the different entries are as follows:

**db-system**:
   the name and version of the database system used for the project.
   At the moment the only option is ``mysql`` and the version does not have an
   effect.
   
**databases**:
  This section contains the description of the different databases. Each logical
  database of the project consists of a set of key/value pairs which define the 
  physical database schema names as values for each environment as key.
  
  E.g. in the example above the logical database ``db1`` is represented by 
  ``db1dev``, ``db1test`` and ``db1`` in the development, test and production
  environment respectively.
  
  In database sql setup scripts executed with the ``dbconfig.py`` tool the logical 
  database names can be used as placeholders for the real physical schema names
  which will be replaced for the respective environments during the execution.
  
**setupscripts**:
  This is the relative path (from the root of the repository) to the folder 
  containing the database setup scripts. This folder will be scanned in case of
  checkout and merge operations to collect all database scripts that need to be
  executed when switching from the dump at a specific commit to the head of the
  current branch.
  
**Note**: It is strongly recommended to commit the ``db-config.json`` to the 
repository in order to make it available in all sandboxes which are using
the **dbversions** tool.

.. _dbversions:

4.2 *.dbversions* repository wide configuration
_______________________________________________

The ``.dbversions`` file is a configuration file for the settings in that
particular working copy/sandbox of the repository and is located at the root
directory of the repository. It usually has the following structure::

   {
     "dumpspath": "database/dumps", 
     "logger": {
       "logdatefmt": "%Y-%m-%d %H:%M:%S", 
       "default-verbosity": 1, 
       "logformat": "[%(asctime)s | %(name)s | %(levelname)-5s]: %(message)s"
     }, 
     "dbconfig": "database/db-config.json", 
     "environments": [
       "dev", 
       "test"
     ]
   }

The meaning of the different options is as follows:

**dumpspath**:
  Specifies the directory where the database dumps for specific commits are 
  stored. As the dumps are only suitable for a specific working copy the dumps
  directory should not be placed under version control as it can cause conflicts 
  with different branches checked out.
  
**logger**:
   A group of settings for the logging facility of **dbversions** it contains
   the following options:
   
     *logdatefmt*:
       equivalent to the python logging formatter construction parameter
       datefmt_
       
       .. _datefmt: https://docs.python.org/2/library/logging.html#formatter-objects
       
     *logformat*:
       equivalent to the python logging formatter construction parameter
       fmt_
       
       .. _fmt: https://docs.python.org/2/library/logging.html#formatter-objects
       
     *default-verbosity*:
       Specifies the default logging level. 1 corresponds to a command line
       parameter of -v, 2 to -vv and so forth. See verbosity_ for further 
       information.
       
**dbconfig**: 
  Specifies the relative path to the repository configuration file 
  db-config.json_. If you relocate this file within your repository you have to
  change this value.
  
**environments**:
  A list of the default environments that need to be considered when dbconfig or
  the post-checkout scripts are executed (see the common environments_ parameter)
  
  
**Note**: The intention of the ``.dbversions`` file is to be the specific 
configuration for a particular working copy. Thus it should not be checked in,
but put on the ``.gitignore`` list.