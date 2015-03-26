

===============================
EUPS: New Packages and Releases
===============================

Your installed ``products/`` directory tree probably looks something like this::

    $ tree /path/to/products/
    |-- EupsBuildDir                 # temporary place where packages are built
    |-- Linux64                      # Where packages are installed
    |   `-- <many product dirs>
    |-- eups
    |   |-- default -> master/       # symlink to master/
    |   `-- master                   # eups code (version 'master')
    |-- site
    |   |-- manifest.remap           # 
    |   `-- startup.py               # System-wide code used by eups (hooks, macros, globals, etc)
    `-- ups_db                       # EUPS's database of info
        `-- <many product dbs>

startup.py
----------

:download:`startup.py`

In order to use the outline provided here, you'll need an extra
parameter file ``startup.py`` which defines various hooks and macros
for EUPS to use.  These are needed any time you use ``eups distrib
create`` (described below).  **If you're not creating distributions,
you don't need the extra settings in the file above**.

There are two places you can put this file.  **Be sure to append the
above code to your file if it already exists**::

    # the system-wide startup.py file:
    /path/to/products/site/startup.py

    # OR ... your user-level startup.py file:
    /home/username/.eups/startup.py
    
    
Create a new package
--------------------

If you wish to add a package to a distribution, these are the steps to
follow.  The necessary steps are shown first with no explanation as a
quick reference, and this is followed by complete instructions.  There
are two examples shown, and both are for external packages.

Quick start
^^^^^^^^^^^

::

    $ git clone ssh://gituser@hsc-repo.mtk.nao.ac.jp:10022//home/gituser/repositories/buildFiles.git
    $ cd buildFiles
    # < create build and table files (see below for examples) >

    # test your build and tables, by installing from this directory
    $ EUPS_PKGROOT=dream:. eups distrib install php 5.6.7 --noclean

    # create the distribution (create version-specific build,table files in packages/ directory)
    $ eups distrib create php 5.6.7 -v -s $HOME/public_html/packages -S buildFilePath=$PWD

    # try installing on another machine
    $ ssh some.other.machine.edu
    $ . /path/to/products/eups/default/bin/setups.sh
    $ export EUPS_PKGROOT=$EUPS_PKGROOT'|'http://old.domain.edu/~user/packages/
    $ eups distrib install php 5.6.7

    # don't forget to check-in and push your build files.
    
    
New Package steps in Detail
^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Get the buildFiles.git repository::

    # get the buildFiles repo
    $ git clone ssh://gituser@hsc-repo.mtk.nao.ac.jp:10022//home/gituser/repositories/buildFiles.git
    $ cd buildFiles
    

#. Create a build file in the buildFiles/ directory.  Below are
   examples for PHP (no Python needed) and SQLAlchemy (Python needed).
   No matter what you're building, it won't quite be like either
   example, but hopefully these are sufficient to allow you create
   your own.  In the buildFiles/ package, there are many existing
   packages which you can use to help get your build file working.

    * Be sure to edit the location for the download (the http:// info) and anywhere you see 'php' written::

        $ cat php.build
        @LSST UPS@ &&
        curl -L \
            http://php.net/get/php-@VERSION@.tar.gz/from/this/mirror
        > @PRODUCT@-@VERSION@.tar.gz &&
        gunzip < @PRODUCT@-@VERSION@.tar.gz | tar -xf - &&
        cd php-@VERSION@ &&
        product_dir=$(eups path 0)/$(eups flavor)/@PRODUCT@/@VERSION@ &&
        ./configure --prefix=$product_dir &&
        make &&
        if [ ! -d $product_dir ]; then
                mkdir -p $product_dir;
        fi &&
        make install &&
        lsst_ups @PRODUCT@ @VERSION@ $product_dir


    * Here's one for sqlalchemy (a Python library).  Again, if you use
      this, edit carefully to replace 'sqlalchemy' references.::

        $ cat sqlalchemy.build
        @LSST UPS@ &&
        curl -L \
            http://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-@REPOVERSION@.tar.gz \
        > @PRODUCT@-@REPOVERSION@.tar.gz &&
        gunzip < @PRODUCT@-@VERSION@.tar.gz | tar -xf - &&
        product_dir=$(eups path 0)/$(eups flavor)/@PRODUCT@/@VERSION@ &&
        python_version=$(python -c "import distutils.sysconfig as ds; print ds.get_python_version()") &&
        if [ ! -d $product_dir ]; then
         mkdir -p $product_dir
         mkdir -p $product_dir/lib/python$python_version/site-packages
        fi &&
        cd SQLAlchemy-@REPOVERSION@ &&
        PYTHONPATH=${product_dir}/lib/python$python_version/site-packages:$PYTHONPATH &&
        python setup.py install --prefix=$product_dir &&
        if [ ! -d $product_dir/lib/python ]; then
           mkdir -p $product_dir/lib/python
        fi &&
        ln -fs $product_dir/lib/python$python_version/site-packages  $product_dir/lib/python &&
        if [ $(eups flavor) = Linux64 -a -d $product_dir/lib64 ]; then
         rm -rf $product_dir/lib
         mv $product_dir/lib64 $product_dir/lib
        fi &&
        lsst_ups @PRODUCT@ @VERSION@ $product_dir

        
#. Create a table file (also in the buildFiles/ directory).  This
   specifies dependencies for the new package and any environment
   variables which must be updated so the package can be used.  Below
   are examples with/without Python::

      # typical table file if no Python is needed
      $ cat php.table    
      pathPrepend(PATH, ${PRODUCT_DIR}/bin)
      envPrepend(LD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
      envPrepend(DYLD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)

      # typical table file if Python *is* needed
      $ cat sqlalchemy.table
      setupRequired(python)
      pathPrepend(PYTHONPATH, ${PRODUCT_DIR}/lib/python/site-packages)
    

#. Test the build and table files.  If the build and table are OK,
   this should install the package on the local system::

      $ cd buildFiles/
      $ EUPS_PKGROOT=dream:. eups distrib install php 5.6.7 --noclean

#. Create the package.  This will take your newly created build,table
   file templates, and produce actual version-specific build files in
   your packages/ directory.  If you don't have a packages/ directory,
   eups will create the directory tree when you run ``eups create``.
   The example below shows an ``eups create`` for PHP version 5.6.7
   (build and tables files are shown above)::

       $ cd buildFiles/
       $ eups distrib create php 5.6.7 -v -s $HOME/public_html/packages -S buildFilePath=$PWD
       
       # you may see a warning (which you can ignore), and a list of skipped dependencies
       WARNING: No usable package repositories are loaded
       Dependency gcc 4.6.4 is already deployed; skipping

   * If you look in packages/build/, you'll now see the
     version-specific build file (e.g. ``php-5.6.7.build``).  The
     various macros (e.g. @LSST UPS@) will have been replaced with
     code.  If you see '@LSST UPS@' has been replaced with 'XXX', your
     startup.py file doesn't contain the 'LSST UPS' macro definition
     and **the build file is broken**.
       
   * If your packages/ directory is in a stable location, you may wish
     to edit ``startup.py`` in the ``cmdHook()`` callback function.
     There you can specify ``opts.serverDir`` to point to your system
     packages/ directory.  If you do this, the ``eups create`` command
     is shorter::

       $ cd buildFiles/
       $ eups distrib create php 5.6.7 -v -S buildFilePath=$PWD

#. You can use this distribution on other machines by specifying
   EUPS_PKGROOT to include the location where you just installed the
   packages/.  Assuming you're now on a separate machine, and you did
   the installation on old.domain.edu in your user public_html/
   directory, you can append to EUPS_PKGROOT using a pipe '|'
   character as a delimiter (Note you need to quote the '|' character
   or the shell will interpret the character as a pipe)::

    $ export EUPS_PKGROOT=$EUPS_PKGROOT'|'http://old.domain.edu/~user/packages/
    $ eups distrib install php 5.6.7


#. Check-in your build/table files, and update the main distribution.
   For HSC, the current location of the buildFiles.git repo is shown::

       $ cd buildFiles/
       $ git ci -m "Added package foo" foo.build foo.table
       $ git push

       $ ssh hsca.ipmu.jp
       $ cd /var/git/repos/buildFiles.git/
       $ git fetch


#. The build files for HSC are currently served from
   hsca.ipmu.jp/sumire/packages/, and you can make your distribution
   generally available to the group by copying (rsync'ish, etc) your
   build and table files to the main packages/ server.

       $ ssh <build_machine>
       $ cd $HOME/public_html/packages/
       $ scp builds/php-5.6.7.build hsca.ipmu.jp:/var/www/html/sumire/packages/builds/
       $ scp tables/php-5.6.7.table hsca.ipmu.jp:/var/www/html/sumire/packages/tables/
       
