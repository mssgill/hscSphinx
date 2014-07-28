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
The most contents of these tables are coming from FITS header of each corresponding 
data. They are information on FITS format, date-obs, filter name, exposure time, WCS 
keywords, seeing, magnitude zero point and so on, which are used for constraints on 
searching the user's necessary FITS data from database.  

================= =========== ============================================== ====== =====
Table Name        FITS Data   Description                                     Mng   HPX11
================= =========== ============================================== ====== =====
**frame**         CORR        Reduced CCD image                                O      O
**calibframe**    CALEXP      Mosaic Corrected Reduced CCD image               O      O
**exposure**      metaQaExp   Exposure meta information                        O
**wcs**           wcs         wcs file output by mosaicking                    O
**fcr**           fcr         flux correction by mosaicking                    O
**warped**        warp        warped image for one exposure(visit) per patch   O      O
**mosaic**        calexp      coadd image                                      O      O 
**mosaicframe**               set of (visit,ccd) which consist of coadd                  
================= =========== ============================================== ====== =====

Each table will be accompanied by 'mng' table, in which some information 
for file management (file path, proposal IDs, data transfer dates etc.). 
For 'frame' table, management table is named as 'frame_mng'. 
'**frame**', '**calibframe**', '**warped**' and '**mosaic**' tables are also accompanied 
by 'hpx11' tables, which are the list of HEALPix order 11 indeces for 
covering the sky area of corresponding images. For '**frame**' table, 
this type table is named as '**frame_hpx11**'. 
Those tables are assumend to be used for searching the place of FITS data on 
file systems based on various meta information like covering sky area, seeing 
and transparency (zero point per second, for example), and more basics like 
filter names, observational dates and so on.  

Table for catalog data (as of 2014.07.01)
-----------------------------------------
Our basic concept of producing catalog database is to extract all columns' values of FITS BINTABLE file and 
store them into the database columns with the same names. It is for avoiding the confusion caused by the 
shortened column names. There are some expansion of arrays in FITS data into seperate database columns, for 
example, on sky coordinates. The flags stored as bits in FITS data will be expanded to each boolean column 
in database in current implementation.   

=========================== ============== ====================================================== ===== =====
Table Name                  FITS Data      Description                                            Photo Coord
=========================== ============== ====================================================== ===== =====
**frame_sourcelist**        SRC            SourceCatalog for each reduced CCD                       O     X
**frame_icsourcelist**      ICSRC          Bright SourceCatalog for each reduced CCD                O     X
**frame_matchlist**         ML             Match list for each reduced CCD                          O     X
**frame_forcelist**         FORCEDSRC      Forced photometry Catalog for each reduced CCD           O     X
**calibframe_sourcelist**   CALSRC         Mosaic calibrated SourceCatalog for each reduced CCD     O     X
**mosaic_sourcelist**       src            SourceCatalog for each coadd image                       O     X
**mosaic_icsourcelist**     icSrc          Bright SourceCatalog for coadd image                     O     X
**mosaic_matchlist**        srcMatchFull   Match list for each coadd image                          O     X
**mosaic_forcelist**        forced_src     Forced photometry object Catalog for each coadd image    O     X
**mosaic_forceflag**        (forced_src)   All flags accompanied to each measurement on coadd 

**photoobj_mosaic**                        Summary table for coadd forced sources
**photoobj_frame**                         Summary table for reduced CCD forced sources
=========================== ============== ====================================================== ===== =====

The tables with corresponding FITS data contain all records of FITS BINTABLE, one record per one 
measurements for the object.  
Each table will be accompanied by '**photo**' and '**coord**' tables, in which various types of magnitudes, 
fluxes(in erg/cm^2/Hz) or (RA, DEC) coordinates of centroids ('**coord**' tables have not been implemented 
for S14A0 release, yet). Those tables consist of a set, with common primary keys. For '**frame_*list**', 
FRAME_ID is the primary key, while 'tract', 'patch', 'filter', 'poinitng' and 'id' are those for 
'**mosaic_*list**' tables. In near future, primary key will be set only for 'id'. 

Summary tables are produced from force_photo and force_coord for CCD (frame) or Coadd (mosaic). 
'**Photoobj_mosaic**' table compile all records for an object (for about some filters) in '**mosaic_force_photo**' 
and '**mosaic_force_coord**' tables into one record. '**Photoobj_frame**' table assemble all records for an 
object (for multiple visits and filters) in '**calibframe_source_photo**' and  '**calibframe_source_coord**' into 
one record. Each measurement is stored in an array on each filter. Some statistical values like means, standard 
deviation etc. are calculated for various magnitude types and added as individual columns.  

The naming rules of database tables
-----------------------------------

PostgreSQL has 3 layers for managing the database. They are database, schema and table. Additionally as described 
in the following document, we define 2 layers (mos_rerun and cat_rerun) as shown in the following. ::

      (Database)     (Schema)             (Table)                           (mos_rerun)      (cat_rerun)
      ##########   #############   ################################   ###################  #################

       Database  |--- Schema 1   | -----  Table 1 (Frame)
                 |               | -----  Table 2 (Mosaic)          |-------- deepcoadd
                 |               |                                  |-------- bestseeing
                 |               |                                  |-------- ..........
                 |               |                              
                 |               | -----  Table 3 (Mosaic_Forcelist)|-------- deepcoadd  |--- iselect
                 |               |                                  |                    |
                 |               |                                  |                    |--- rselect....
                 |               |                                  |
                 |               |                            
                 |               |                                  |-------- bestseeing |--- iselect
                 |               |                                  |                    |
                 |               |                                  |                    |--- rselect....
                 |               |
                 |               |                                  |-------- .......... |--- iselect
                 |               |                                  |                    |
                 |               |                                  |                    |--- rselect.....
                 |               | -----  Table 4 (Photoobj_Mosaic)
                 |               | -----  .......
                 |               | -----  .......
                 |
                 |--- Schema 2   | -----  Table 1 (Frame)
                 |               | -----  Table 2 (Mosaic)
                 |               | -----  Table 3 (Photoobj_Mosaic)
                 |               | -----  .......
                 |               | -----  .......
                 |
                 |--- Schema 3   | -----  Table 1 (Frame)
                                 | -----  Table 2 (Mosaic)
                                 | -----  Table 3 (Photoobj_Mosaic)
                                 | -----  .......
                                 | -----  .......

In the S14A0 release, Database is 'dr_early', Schema is 'ssp_s14a0_udeep_20140523a' or 'ssp_s14a0_wide_20140523a', 
corresponding to 'rerun' in pipeline. 
Additionally the tables, which contain records based on the mosaicking and forced measurement must be considered, 
because there are some branching according to mosaicking methods and or reference filter for forced measurements. 
For example, the most basic mosaicking is currently named 'deepCoadd' in pipeline, meaning 'all' CCD images to be 
mosaiced and coadded. On the other hand, some special mosaicking/coadding like 'bestSeeing' which will use only 
CCD images taken under good seeing conditions can be considered and coadd images and relating object catalogs are 
different from 'deepCoadd' based one. So 'mos_rerun' (meaning mosaic rerun) is considered to separate the relating table names. 
It is also essential to consider different source catalog tables based on different reference filter coadd images (i-band 
selected and r-band selected, for example), and we define 'cat_rerun'(meaning catalog rerun) for specifying the 
database tables. Therefore, the full name of the tables will be **schema_name.table_root_name__(mos_rerun)__(cat_rerun)**, 
although (mos_rerun) and/or (cat_rerun) will be omitted if unnecessary. 
For example, the name of '**mosaic_forcelist**' table in S14A0 release for UDEEP, based on 'deepCoadd' mosaicking and i-band 
selected is '**ssp_s14a0_udeep_20140523a.mosaic_forcelist__deepcoadd__iselect**'. The name is currently so long and we 
strongly recommend to use alias for these tables to get shorter names, as described in the following section.   

Views for flags of coadd measurements on each filter 
-----------------------------------------------------
By selecting the all records from **mosaic_forceflag** table on each filter, the views '**mosaic_forceflag_filter** 
are defined. The current list of views are as follows, on S14A0 release. 

========================== ======================================== ===== ====
View Name                  Description                              UDEEP WIDE
========================== ======================================== ===== ====
mosaic_forceflag_g         g-band flags for coadd forced measurents   O    
mosaic_forceflag_r         r-band flags for coadd forced measurents   O
mosaic_forceflag_i         i-band flags for coadd forced measurents   O    O
mosaic_forceflag_z         z-band flags for coadd forced measurents   O
mosaic_forceflag_y         y-band flags for coadd forced measurents   O    O
========================== ======================================== ===== ====

These views are assumed to be used for selecting objects in the coadd summary table (**photoobj_mosaic**) by 
using some flags of each band measurements.  

How to 'join' the tables for your queries
-----------------------------------------

As mentioned above, the information for objects, measured in various phase 
of the pipeline processing, is stored in several separate tables, for ease 
of database management, and visualization of the tables. On the other hand, 
it is common for the user to do the query using multiple parameters(database 
columns) separated in multiple tables as the constraints for the search, 
or get values from multiple tables for the objects. 
For the purpose, it is reasonable to use 'join' in the relational database, 
like PostgreSQL, we are using for the HSC SSP database. 
Here are some examples specific for the tables in HSC SSP database. 
Please see the :ref:`HSC Query Examples <database_queries>` section for more examples. 
There are several ways to enable the 'join' in SQL of PostgreSQL, and only limited 
numbers of samples are shown here.   


Searching objects measured in CCD images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Getting id, RA, DEC, psf magnitudes and their errors measured in the CCD image with visit=300 and ccd=1
(CORR-0000300-001.fits) file in UDEEP(COSMOS) data.  ::

   SELECT  
        fs.id, fs.ra2000, fs.decl2000, fp.mag_psf, fp.mag_psf_err 
   FROM
        ssp_s14a0_udeep_20140523a.frame_sourcelist fs,  -- alias fs for 'frame_sourcelist' table
        ssp_s14a0_udeep_20140523a.frame_sourcephoto fp,  -- alias fp for 'frame_sourcephoto' table
	ssp_s14a0_udeep_20140523a.frame ft               -- alias ft for 'frame' table
   WHERE
            fs.frame_id = fp.frame_id and fs.id = fp.id    -- joining fs with fp 
        and 
            fs.frame_id = ft.frame_id                  -- joining fs with ft 
        and 
            ft.visit=300 and ft.ccd=1                  -- specifying visit and ccd in ft 

As easily imagined, we can use aliasing of the tables for shorter table name in SQL, 
we are using 3 tables '**frame_sourcelist**', '**frame_sourcephoto**' and '**frame**' 
for joining. For joining the tables, common primary keys should be used after 'where' clause. 
In this example, 'frame_id' and 'id' are used for joining fs and fp tables, instead only 'frame_id' 
for fs and ft. Primary keys can be identified in the NAOJ online 
`Schema Browser <https://hscdata.mtk.nao.ac.jp:4443/schema_browser/hsc/hsc_online_schema_tableonly.html>`_ 
by the column 'DB keys' set to 'P'. 
As values of 'visit' and 'ccd' for identifying the CCD image is only stored 
in '**frame**' table, it is also joined for this example. If you know the frame_id like 
'HSCA00030154' for the CCD, you need not to join '**frame**' table. 


Searching objects measured in Coadd images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Getting id, RA, DEC, i-band psf magnitudes and their errors measured in the Coadd image with tract=0, patch=4,4 and 
filter=HSC-I (calexp-HSC-I-0-4,4.fits) file in UDEEP(COSMOS) data.  ::

   SELECT  
        ms.id, ms.ra2000, ms.decl2000, mp.mag_psf, mp.mag_psf_err 
   FROM
        ssp_s14a0_udeep_20140523a.mosaic_sourcelist__deepcoadd ms,  -- alias ms for 'mosaic_sourcelist' table
        ssp_s14a0_udeep_20140523a.mosaic_sourcephoto__deepcoadd mp  -- alias mp for 'mosaic_sourcephoto' table
   WHERE
            ms.tract = mp.tract and ms.patch = mp.patch and ms.filter01 = mp.filter01  -- joining ms with mp 
            and ms.pointing = mp.pointing and ms.id = mp.id                            -- joining ms with mp 
        and 
            ms.tract=0 and ms.patch='4,4' and ms.filter01 = 'HSC-I'                    -- specifying tract, patch, filter in ms 

The primary keys currently set to the combination of 'tract', 'patch', 'filter01', 'pointing' and 'id' in the 
'**mosaic_sourcelist**' and  '**mosaic_sourcephoto**' tables. In the future, only 'id' may become the primary key. 


Searching objects in coadd summary table(multi-color coadd table)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Getting id, RA, DEC, psf magnitudes and their errors for g,r,i,z,y bands in coadd summary (**photoobj_mosaic**) table 
with good centroid measurement in i-band image and i-band psf magnitude brighter than 24.0. ::

   SELECT  
        pm.id, pm.ra2000, pm.decl2000, pm.gmag_psf, pm.gmag_psf_err, pm.rmag_psf, pm.rmag_psf_err,  
	pm.imag_psf, pm.imag_psf_err, pm.zmag_psf, pm.zmag_psf_err,  pm.ymag_psf, pm.ymag_psf_err
   FROM
        ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect pm,  -- alias pm for 'photoobj_mosaic' table
        ssp_s14a0_udeep_20140523a.mosaic_forceflag_i__deepcoadd__iselect mff  -- alias mff for 'mosaic_forceflag_i' view 
   WHERE
            pm.tract = mff.tract and pm.patch = mff.patch                              -- joining pm with mff 
            and pm.pointing = mff.pointing and pm.id = mff.id                          -- joining pm with mff
	and pm.imag_psf < 24.0 and mff.centroid_sdss_flags is not True                 -- magnitude limit and flag filtering 

'**photoobj_mosaic**' and '**mosaic_forceflag**' tables have the common primary keys (tract, patch, pointing, id), then 
use these columns for joining them. 'tract' and 'patch' will be eliminated from primary keys in the future. 


