.. _tables_intro:

==========================
Tables of HSC SSP database
==========================

Introductions
---------------
There are two types of database tables for the HSC data. 
One is for storing meta information of image data, such as 
time, filters, wcs, some measured stats like seeing, magnitude 
zero point and so on for each image like 'calexp' and 'deepCoadd_calexp' 
in the pipeline. Another one is for storing catalog information, 
which are extracted from FITS BINTABLE produced by the pipeline, 
such as SourceCatalogs like 'src', 'match' and so on.   

The following list shows the tables for HSC database. 


Table for image meta data
-------------------------

============== =========== ==============================================
Table Name     FITS Data   Description
============== =========== ==============================================
**frame**      CORR        Reduced CCD image 
**calibframe** CALEXP      Mosaic Corrected Reduced CCD image
**exposure**   metaQaExp   Exposure meta information 
**wcs**        wcs         wcs file output by mosaicking 
**fcr**        fcr         flux correction by mosaicking
**warped**     warp        warped image for one exposure(visit) per patch
**mosaic**     calexp      coadd image 
============== =========== ==============================================

Each table will be accompanied by 'mng' table, in which some information 
for file management (file path, proposal IDs, data transfer dates etc.). 
For 'frame' table, management table is named as 'frame_mng'. 
'frame', 'calibframe', 'warped' and 'mosaic' tables are also accompanied 
by 'hpx11' tables, which are the list of HEALPix order 11 indeces for 
covering the sky area of corresponding images. For 'frame' table, 
this type table is named as 'frame_hpx11'. 
Those tables are assumend to be used for searching the place of FITS data on 
file systems based on various meta information like covering sky area, seeing 
and transparency (zero point per second, for example), and more basics like 
filter names, observational dates and so on.  

Table for catalog data
----------------------

=========================== ============== ======================================================
Table Name                  FITS Data      Description
=========================== ============== ======================================================
**frame_sourcelist**        SRC            SourceCatalog for each reduced CCD 
**frame_icsourcelist**      ICSRC          Bright SourceCatalog for each reduced CCD 
**frame_matchlist**         ML             Match list for each reduced CCD 
**frame_forcelist**         FORCEDSRC      Forced photometry Catalog for each reduced CCD 
**calibfarme_sourcelist**   CALSRC         Mosaic calibrated SourceCatalog for each reduced CCD 
**mosaic_sourcelist**       src            SourceCatalog for each coadd image
**mosaic_icsourcelist**     icSrc          Bright SourceCatalog for coadd image
**mosaic_matchlist**        srcMatchFull   Match list for each coadd image
**mosaic_forcelist**        forced         Forced photometry object Catalog for each coadd image 
**mosaic_forceflag**                       All flags accompanied to each measurement on coadd 

**photoobj_mosaic**                        Summary table for coadd sources
**photoobj_frame**                         Summary table for reduced CCD sources
=========================== ============== ======================================================

The tables with corresponding FITS data contain all records of FITS BINTABLE, one record per one 
measurements for the object.  
Each table will be accompanied by 'photo' and 'coord' tables, in which various types of magnitudes, 
fluxes(in erg/cm^2/Hz) or (RA, DEC) coordinates of centroids ('coord' tables have not been implemented 
for S14A0 release, yet). Those tables consist of a set, with common primary keys. For 'frame_*list', 
FRAME_ID is the primary key, while 'tract', 'patch', 'filter', 'poinitng' and 'id' are those for 
'mosaic_*list' tables. In near future, primary key will be set only for 'id'. 

Summary tables are produced from force_photo and force_coord for CCD (frame) or Coadd (mosaic). 
Photoobj_mosaic tables compile all records for an object (for about some filters) in 'mosaic_force_photo' 
and 'mosaic_force_coord' tables into one record. Photoobj_frame tables assemble all records for an 
object (for multiple visits and filters) in 'calibframe_source_photo' and  'calibframe_source_coord' into 
one record. Each measurement is stored in an array on each filter. 

  
