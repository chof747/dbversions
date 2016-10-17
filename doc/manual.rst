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
repositories.

2. Installation
===============

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


