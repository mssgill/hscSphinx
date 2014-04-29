
=====================
The Data Repository
=====================

The HSC pipeline requires that its data be handled in a very
particular way.  To complicate matters, the developers make no
promises about how the data model might change in the future.
Fortunately, however, the pipeline code includes a program to take a
collection of `HSCA*.fits` files and import (or rather 'ingest') them
into a pipeline-friendly directory tree.  To avoid doubling the disk
space used by your raw data, this ingest step can be done with
symlinks.

To create an HSC data repo, and ingest your raw data into it (assuming
you already EUPS `setup` the pipeline)::

    # make the directory
    $ mkdir /data/Subaru/HSC

    # add a '_mapper' file to tell the pipeline which camera the data came from
    $ echo lsst.obs.hsc.HscMapper > /data/Subaru/HSC/_mapper

    # ingest the HSCA*.fits files.  The first time you do this, use '--create'
    $ hscIngestImages.py /data/Subaru/HSC --create --mode=link /path/to/rawdata/HSCA*.fits

    
You'll now see a newly created data repository in /data/Subaru/HSC/.
In addtion to the `_mapper` file you just created, it also contains a
directory tree named according the OBJECT entry in the FITS header
(M87 here), the DATE-OBS, the pointing, and the filter name.  The FITS
symlink itself has name slightly different from the original raw data
file.  The format is HSC-VVVVVVV-CCC.fits, where V is a seven digit
'visit' number, and 'C' is a 3 digit CCD number.  Lastly, there's a
sqlite database called the 'registry'.

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

    
As mentioned earlier though, please don't rely on the directory tree
keeping this structure specifically.  If, for example, you write a
script which happens to look for a file in the pipeline data repo,
it's quite possible that the file's location may change in later
versions of the pipeline.  It may even disappear entirely!  Feel free
to poke around, but keep in mind that the data repo is intended to be
written-to and read-from only by the pipeline tools.

