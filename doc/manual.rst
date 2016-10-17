===============================================
 **dbversions** - Database Versioning with Git
===============================================

-------------
 User Manual
-------------

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
  
Besides this basic workflow the tool has the following features:

* setup generic scripts so that they can be executed on any environment
* execute generic scripts on one, a set of or all of your environments
* snapshot and restore database dumps related to any commit

2. Installation
===============

To install the tool you have the following possibilities:

2.1 Install package from pip
____________________________

Simply install **dbversions** from PyPi with the following command::

pip install dbversions

This will install the tool in your standard python site packages and the scripts in an executable path. No further steps are necessary except for initializing a specific repository.

2.2 Install from source
_______________________


When installing from source you have to 

1. download the source distribution from ##add link here##. 

2. extract the source into a new, empty directory 

3. execute the setup script 


3. Main Operations
==================

3.1 Take a snapshot
___________________


3.2 Restore from a snapshot
___________________________


3.3 Checkout a different branch
_______________________________


3.4 Merge two branches
______________________


