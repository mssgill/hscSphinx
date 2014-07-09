
=====================
The Data Repository
=====================

The HSC pipeline requires that its data be handled in a very
particular way.  To complicate matters, the developers make no
promises about how the data model might change in the future.  This
summary give a short description of the structure of the data
repository, but please keep in mind that the layout shouldn't be
relied upon.  If, for example, you write a script which happens to
look for a file in the pipeline data repo, it's quite possible that
the file's location may change in later versions of the pipeline.  It
may even disappear entirely!  Feel free to poke around, but keep in
mind that the data repo is intended to be written-to and read-from
only by the pipeline tools.


.. _ingest:

Creating a Data Repo and Ingesting Data
---------------------------------------

The pipeline code includes a program to take a collection of
``HSCA*.fits`` files and import (or rather 'ingest') them into a
pipeline-friendly directory tree.  To avoid doubling the disk space
used by your raw data, this ingest step can be done with symlinks.

To create an HSC data repo, and ingest your raw data into it (assuming
you already EUPS `setup` the pipeline)::

    # make the directory where you want the data repo to live
    $ mkdir /data/Subaru/HSC

    # add a '_mapper' file to tell the pipeline which camera the data came from
    $ echo lsst.obs.hsc.HscMapper > /data/Subaru/HSC/_mapper

    # ingest the HSCA*.fits files.  The first time you do this, use '--create'
    $ hscIngestImages.py /data/Subaru/HSC --create --mode=link /path/to/rawdata/HSCA*.fits

You'll now see a newly created data repository in /data/Subaru/HSC/.
In addtion to the `_mapper` file you just created, it also contains a
directory tree named according the OBJECT entry in the FITS header
(M87 here), the DATE-OBS, the pointing, and the filter name.  The FITS
symlink itself has a name slightly different from the original raw
data file.  The format is HSC-VVVVVVV-CCC.fits, where V is a seven
digit 'visit' number, and 'C' is a 3 digit CCD number.  Lastly,
there's a sqlite database called the 'registry'.


Here's what it looks like with a single files ingested::

    $ tree /data/Subaru/HSC
    /data/Subaru/HSC/
    |-- M87
    |   `-- 2015-12-21
    |       `-- 00999
    |           `-- HSC-I
    |               `-- HSC-0001000-055.fits -> /data/work/rawdata/HSCA09870000.fits
    |-- _mapper
    `-- registry.sqlite3


The ingest step does two things: (1) copy (or symlink) the files into
the repo, and (2) make an entry in the registry database.  If you have
files which are already in place, and you just want to make an entry
into the registry database, use ``--mode=skip``.  Here's an example
registering ``M31`` data which is already in place in the repo.  (a
real example where the 2013-03-21/ directory was a symlink to use data
stored in another data repo::

    # register data which is already in place
    $ hscIngestImages.py /data/Subaru/HSC/ --mode=skip /data/Subaru/HSC/M31/2013-03-21/00100/HSC-I/HSC-*fits

.. _registryinfo:

Registry Information
^^^^^^^^^^^^^^^^^^^^

The registry file contains one entry for every file ingested, and it
is possible to query it with the ``registryInfo.py`` command.  Many
stages of pipeline processing require you to use visit numbers
(i.e. frameID) to specify the input data, and ``registryInfo.py``
makes it straightforward to find out various details about the
ingested files::

    # get a listing of all COSMOS data taken in filter HSC-I
    $ registryInfo.py /data/Subaru/HSC/registry.sqlite3 --field COSMOS --filter HSC-I
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112
    ...
    
To avoid having to type the path to the registry file, you can specify
the data repository directory in the SUPRIME_DATA_DIR environment
variable::

    $ export SUPRIME_DATA_DIR=/data/Subaru/HSC

    # now registryInfo.py can find the registry.sqlite3 file on its own
    $ registryInfo.py --field COSMOS --filter HSC-I
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112
    ...
    
On systems where the ``suprime_data`` EUPS package exists, the
SUPRIME_DATA_DIR is best setup with ``setup suprime_data``.  The
manager of the system should have configured that package to point to
the most up-to-date data set.  If multiple versions of
``suprime_data`` are present (check ``eups list suprime_data``), the
version names should indicate which data they contain::

    $ setup suprime_data
    $ registryInfo.py --visit 1234
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112

    
The Structure of a Rerun Directory
----------------------------------

Eventually, you may need to snoop around looking for your output data.
Each processing batch is referred to as a rerun, and new reruns will
appear in a ``rerun`` directory within your data repository.  A full
processing run takes place in multiple stages, but can loosely be
lumped together as single-frame processing, and coadd processing.
There are different outputs associated with each.


The single-frame outputs
^^^^^^^^^^^^^^^^^^^^^^^^

Here's a short look at the structure of a single-frame rerun called
``test``.  In this example, for clarity only one HSC CCD was processed
(CCD 50), but a full HSC rerun would contain 112 (104 on-sky + 8
focus) CCDs for each visit processed::

    /data/Subaru/HSC/rerun/test/    
    |-- 00100                                         The pointing
    |   `-- HSC-I                                     The filter
    
    |       |-- corr                                  Corrected frames
    |       |   |-- BKGD-0000999-050.fits             The background (not easily readable)
    |       |   `-- CORR-0000999-050.fits             The corrected image
    
    |       |-- output                                Output data (i.e. measurements)
    |       |   |-- ICSRC-0000999-050.fits                
    |       |   |-- MATCH-0000999-050.fits            Objects matched to catalog sources
    |       |   |-- ML-0000999-050.fits                   
    |       |   |-- SRC-0000999-050.fits              Measurements on sources
    |       |   |-- SRCMATCH-0000999-050.fits             
    |       |   `-- SRCML-0000999-050.fits
    
    |       |-- processCcd_metadata                   pipeline internals
    |       |   `-- 0000999-050.boost
    
    |       |-- qa                                    Quality Assurance data and figures
    |       |   |-- ellPaGrid-0000999-050.fits
    |       |   |-- ellipseGrid-0000999-050.png
    |       |   |-- ellipseMap-0000999-050.png
    |       |   |-- ellipticityGrid-0000999-050.fits
    |       |   |-- ellipticityGrid-0000999-050.png
    |       |   |-- ellipticityMap-0000999-050.png
    |       |   |-- fwhmGrid-0000999-050.fits
    |       |   |-- fwhmGrid-0000999-050.png
    |       |   |-- magHist-0000999-050.png
    |       |   |-- psfModelGrid-0000999-050.fits
    |       |   |-- psfModelGrid-0000999-050.png
    |       |   |-- psfSrcGrid-0000999-050.fits
    |       |   |-- psfSrcGrid-0000999-050.png
    |       |   |-- seeingGrid-0000999-050.txt
    |       |   |-- seeingMap-0000999-050.png
    |       |   |-- seeingMap-0000999-050.txt
    |       |   |-- seeingRobust-0000999-050.png
    |       |   `-- seeingRough-0000999-050.png
    |       `-- thumbs                                Thumbnail figures
    |           |-- flattened-0000999-050.png
    |           `-- oss-0000999-050.png
    
    |-- _parent -> /data/Subaru/HSC                   A link back to the root of the data repo
    
    |-- config                                        Parameters specific to this rerun
    |   |-- eups.versions                             Package versions (file~1 contains clobbered versions)
    |   `-- processCcd.py                             Configuration parameters (file~1 contains clobbered parameters)
    
    `-- schema
        |-- icSrc.fits
        `-- src.fits



The Coadd outputs
^^^^^^^^^^^^^^^^^

