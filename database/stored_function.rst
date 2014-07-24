.. _stored_function:

================
Stored Functions
================
For making user's search more convenient, the stored functions (in other relational database, may be called
Stored Procedure) are prepared for use. Additional to standard aggregate and other types of functions which
are `originally implemented in PostgreSQL server <http://www.postgresql.org/docs/9.3/static/functions-aggregate.html>`_,
some user defined functions are available on NAOJ HSC database server for HSC SSP data.
More functions are planned to be added in near future, for example, coordinate string converter to degrees
(hh:mm:ss.s,+/-dd:mm:ss.s -> degrees), and magnitude to/from flux density converters.

Aggregate Functions
^^^^^^^^^^^^^^^^^^^
.. list-table:: **User Defined Functions(Aggregate)**

   * - **Functions**
     - **Argument Type(s)**
     - **Return Type**
     - **Description**

   * - qmedian(expression)
     - int, bigint, numeric, double precision
     - same as argument data type
     - the median of all input values

   * - quantile(expression)
     - int, bigint, numeric, double precision
     - same as argument data type
     - the quantile of all input values

   * - weighted_mean(values, weight_values)
     - set of double precision
     - double precision
     - the weighted mean of all input values

   * - mean
     - double precision
     - same as argument data type
     - the mean of all input values

   * - variance
     - double precision
     - same as argument data type
     - the (unbiased) variance of all input values

   * - stddev
     - double precision
     - same as argument data type
     - sqrt of the unbiased variance

   * - skewness
     - double precision
     - same as argument data type
     - the skewness of all input values: κ\ :sub:`3`\ /κ\ :sub:`2`\ :sup:`3/2` where κ\ :sub:`i` denotes the unbiased i-th cumulant

   * - kurtosis
     - double precision
     - same as argument data type
     - the kurtosis of all input values: κ\ :sub:`4`\ /κ\ :sub:`2`\ :sup:`2` where κ\ :sub:`i` denotes the unbiased i-th cumulant

example of qmedian::

      -- calculate median of seeing values in frame table of UDEEP CCD data

      SELECT qmedian(seeing) from ssp_s14a0_udeep_20140523a.frame;

example of quantile::

      -- calculate 30% quantile of seeing values in frame table of UDEEP CCD data

      SELECT quantile(seeing, 0.3) from ssp_s14a0_udeep_20140523a.frame;

      -- calculate quantile (30, 50 and 70%) of seeing values in frame table of UDEEP CCD data

      SELECT quantile(seeing, array[0.3, 0.5, 0.7]) from ssp_s14a0_udeep_20140523a.frame;

example of weighted_mean::

      -- calculate weighted_mean of Sinc magnitudes with weight by error of Sinc magnitudes (mag_sinc_err)^{-2}
      -- Caution!! only double precision input is allowed currently and cast to numeric is essential

      SELECT weighted_mean(mag_sinc, (1.0/mag_sinc_err)*(1.0/mag_sinc_err))     
        FROM ssp_s14a0_udeep_20140523a.frame_forcephoto__deepcoadd__iselect
       WHERE tract=0 and id=207876417126408 and mag_sinc_err > 0.0;

example of mean, variance & stddev::

      -- calculate the mean of mag_sinc_err that are valid,
      -- the variance of mag_gaussian that are valid,
      -- and the standard deviation of flux_cmodel that are not NaN
      -- in the UDEEP CCD frame table

      SELECT mean(mag_sinc_err, '>', 0), variance(mag_gaussian, '<', 99.99), stddev(flux_cmodel, '==', flux_cmodel)
        FROM ssp_s14a0_udeep_20140523a.frame_forcephoto__deepcoadd__iselect
        WHERE tract=0;

example of skewness & kurtosis::

      -- calculate the skewness of mag_sinc that are valid,
      -- and the kurtosis of mag_gaussian that are valid

      SELECT skewness(mag_sinc, '<', 99.99), kurtosis(mag_gaussian, '<', 99,99),
        FROM ssp_s14a0_udeep_20140523a.frame_forcephoto__deepcoadd__iselect
        WHERE tract=0;

Function for spatial searches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table:: **User Defined Functions(Spatial Search)**

   * - **Functions**
     - **Description**

   * - f_getobj_circle(ra, dec, radius, table_name)
     - get object in circle defined by radius from the central coordinate(ra, dec) on the specified table

   * - f_getobj_rectangle(ra, dec, delta_ra, delta_dec, table_name)
     - get object in rectangle defined by delta_ra and delta_dec centered at the coordinate(ra, dec) on the specified table


example of f_getobj_circle(ra, dec, radius, table_name)::

      -- get objects' tract, patch, pointing, id, ra2000, decl2000, cx, cy, cz, xxyyzz, distance
      -- within 2 arcsec radius centered at (RA,DEC)=(150.403189,1.485288) in frame_forcelist of UDEEP CCD
      -- RA and DEC are in degrees.

      SELECT * from f_getobj_circle(150.403189, 1.485288, 2.0, 'ssp_s14a0_udeep_20140523a.frame_forcelist__deepcoadd__iselect');

      -- get object's id, ra, dec, sinc magnitudes of g,r,i,z,y bands and distance from the central coordinates specified.
      -- the cone search is for objects within 3 arcsec from the coordinate (RA,DEC)=(150.403189,1.485288).
      -- Joining the query result of cone search with photoobj_mosaic table.
      -- distance in arcsec

      SELECT pm.id, pm.ra2000, pm.decl2000, pm.gmag_sinc, pm.rmag_sinc, pm.imag_sinc, pm.zmag_sinc, pm.ymag_sinc, obj.distance
      FROM f_getobj_circle(150.93, 1.93, 3.0, 'ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect') obj,
           ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect pm
      WHERE obj.id=pm.id and obj.tract=pm.tract and obj.patch=pm.patch and obj.pointing = pm.pointing
      ORDER by obj.distance;

example of f_getobj_rectangle(ra, dec, delta_ra, delta_dec, table_name)::

      -- get objects' tract, patch, pointing, id, ra2000, decl2000, cx, cy, cz, xxyyzz, distance
      -- within 2 x 2 arcsec centered at (RA,DEC)=(150.403189,1.485288) in frame_forcelist of UDEEP CCD
      -- RA and DEC are in degrees.

      SELECT * from f_getobj_rectangle(150.403189, 1.485288, 2.0, 2.0, 'ssp_s14a0_udeep_20140523a.frame_forcelist__deepcoadd__iselect');


Functions for utils 
^^^^^^^^^^^^^^^^^^^
Some utility functions for handling HSC information are prepared. They are (visit, ccd) <-> FrameId conversion etc. 

.. list-table:: **User Defined Functions(Utils)**

   * - **Functions**
     - **Argument Type(s)**
     - **Return Type**
     - **Description**   

   * - frameid2visitccd
     - text 
     - set of integer
     - transform of FrameId to (visit, ccd)

   * - visitccd2frameid
     - set of integer
     - text
     - transform of (visit, ccd) to FrameId 

   * - hms2deg
     - text (hh:mm:ss.sss)
     - double precision
     - transform RA in hh:mm:ss.sss to degree unit

   * - deg2hms
     - double precision
     - text (hh:mm:ss.sss)
     - transform RA in degree to hh:mm:ss.sss

   * - dms2deg
     - text (+/-dd:mm:ss.ss)
     - double precision
     - transform DEC in +/-dd:mm:ss.ss to degree unit

   * - equ2gal
     - set of double precision (ra, dec) J2000
     - set of double precision (gallon, gallat) 
     - transform equatrial coordinates in degree to galactic coordinates in degree (based on SLALIB 2.5-4)

   * - gal2equ
     - set of double precision (gallon, gallat)
     - set of double precision (ra, dec) J2000
     - transform galactic coordinates in degree to equatrial coordinates in degree (based on SLALIB 2.5-4)

   * - date2mjd
     - text (date string: YYYY-MM-DD)
     - integer (mjd in integer)
     - transform date-obs to MJD

   * - datetime2mjd
     - text (datetime string: YYYY-MM-DDThh:mm:ss.sss)
     - double precision (mjd)
     - transform date-obs + UT to MJD
 
   * - datetime2mjd
     - set of text (date string: YYYY-MM-DD, time string hh:mm:ss.sss)
     - double precision (mjd)
     - transform date-obs + UT to MJD

   * - mjd2date
     - integer (MJD in integer)
     - text (date string: YYYY-MM-DD)
     - transform MJD to date string

   * - mjd2datetime
     - double precision (MJD)
     - text (datetime string: YYYY-MM-DDThh:mm:ss.sss)
     - transform MJD to string DATE-OBJ + UT

   * - mjd2datetime2
     - double precision (MJD)
     - set of text (date string: YYYY-MM-DD, time string: hh:mm:ss.sss)
     - transform MJD to string DATE-OBJ + UT

example of frameid2visitccd and  visitccd2frameid::

      SELECT frameid2visitccd('HSCA00000301');
      return (2,27)

      SELECT visitccd2frameid(2, 27);
      return 'HSCA00000301'

example of hms2deg and dms2deg::

      SELECT hms2deg('12:12:12.345');
        return 183.0514375

      SELECT dms2deg('-01:00:12.00');
        return -1.00333333333333

example of deg2hms and deg2dms::

      SELECT deg2hms(183.051416666667);
        return 12:12:12.34

      SELECT deg2dms(83.0514375);
        return +83:03:05.18

example for getting coordinates with hh:mm:ss.sss and +/-dd:mm:ss.ss rather than degree::

      SELECT deg2hms(ra2000) as ra, deg2dms(decl2000) as dec 
      FROM ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect 
      LIMIT 10;

example for getting objects' id, coordinates in degree and hms/dms formats which are within 20 arcsec from the center at 
(RA, DEC) = (10:03:45.000, +02:00:00.00) in photoobj_mosaic table of UDEEP survey. ::

      SELECT id, ra2000, decl2000, deg2hms(ra2000) as ra, deg2dms(decl2000) as dec 
      FROM f_getobj_circle(hms2deg('10:03:45.000'), dms2deg('+02:00:00.00'), 20.0, 'ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect');

example of equ2gal and gal2equ::

      SELECT equ2gal(120.0, 30.0);

      SELECT gal2equ(230.0, 20.0);

      -- get the objects' id, ra, dec and galactic coordinates which are within 20 arcsec from the center at 
      -- (RA, DEC) = (10:03:45.000, +02:00:00.00) in photoobj_mosaic table of UDEEP survey. 

      SELECT pm.id, pm.ra2000, pm.decl2000, e2g.l as gallon, e2g.b as gallat 
      FROM 
         f_getobj_circle(hms2deg('10:03:45.000'), dms2deg('+02:00:00.00'), 20.0, 'ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect') pm, 
         equ2gal(pm.ra2000, pm.decl2000) e2g
      ;


example of date2mjd and mjd2date::

      SELECT date2mjd('2014-07-17');

      SELECT mjd2date(56855);

example of datetime2mjd and mjd2datetime, mjd2datetime2::

      SELECT datetime2mjd('2014-07-17T12:12:12.000');
      
      SELECT datetime2mjd('2014-07-17', '12:12:12.000');

      SELECT mjd2datetime(56855.5084722222);

      SELECT mjd2datetime2(56855.5084722222);

Setting Stored Functions in your own Database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to run the stored functions in your own database servers, you should
do install and set-up the functions.
All functions described in this document available in the latest **hscDb** package
(version later than 2014.07.04), under 'python/hsc/hscDb/pgfunctions' directories.

For C and C++ functions, you should run Makefile first, then do make install as
root user, then run 'create extension [function_name]' in psql command. ::

     # For example on qmedian

     % cd pgfunctions/c/qmedian
     % make
     % su <-- switch to root user
     % make install

     % /usr/local/pgsql/bin/psql -U hscana -d dr_early -h your_db_host

     psql> create extension qmedian;

Please see README file in each package directory.

For PL/pgSQL functions, you should run all SQL scripts under the plpgsql directory.::

     % /usr/local/pgsql/bin/psql -U hscana -d dr_early -h your_db_host -f f_arcsec2radian.sql
     % /usr/local/pgsql/bin/psql -U hscana -d dr_early -h your_db_host -f ......
     % ..........................

**Caution**

As the stored functions are set up to each database instance, you should run 'create extension'
or 'create function' command when you newly create the database instance with 'create database'
or createdb command.

You can see the set-up functions by using '**\\df**' command on psql prompt.

