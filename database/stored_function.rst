.. _stored_function:

================
Stored Functions
================
For making user's search more convenient, the stored functions are prepared 
for use. Additional to standard aggregate and other types of functions which 
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
   
   * - weighted_mean(values, q-value or array of q-values)
     - numeric
     - same as argument data type
     - the weighted mean of all input values

   * - mean
     - double precision 
     - same as argument data type
     - the mean of all input values 

   * - variance
     - double precision 
     - same as argument data type
     - the variance of all input values 

   * - stddev 
     - double precision 
     - same as argument data type
     - the standard deviation of all input values 

   * - kurtosis 
     - double precision 
     - same as argument data type
     - the kurtosis of all input values 

   * - skewness 
     - double precision 
     - same as argument data type
     - the skewness of all input values 

example of qmedian::
   
      -- calculate median of seeing values in frame table of UDEEP CCD data

      SELECT qmedian(seeing) from ssp_s14a0_udeep_20140523a.frame;

example of quantile::

      -- calculate 30% quantile of seeing values in frame table of UDEEP CCD data

      SELECT quantile(seeing, 0.3) from ssp_s14a0_udeep_20140523a.frame;    
      
      -- calculate quantile (30, 50 and 70%) of seeing values in frame table of UDEEP CCD data

      SELECT quantile(seeing, array[0.3, 0.5, 0.7]) from ssp_s14a0_udeep_20140523a.frame;    

example of weighted_mean::

      -- calculate weighted_mean of Sinc magnitudes with weight by error of Sinc magnitudes 
      -- Caution!! only numeric input is allowed currently and cast to numeric is essential

      SELECT weighted_mean(mag_sinc::numeric, 1.0/mag_sinc_err::numeric)     -- cast inputs to numeric type
        FROM ssp_s14a0_udeep_20140523a.frame_forcephoto__deepcoadd__iselect 
       WHERE tract=0 and id=207876417126408 and mag_sinc_err > 0.0;

example of mean, variance & stddev::

      To be coming soon....


example of kurtosis & skewness::

      To be coming soon....



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
  

example of f_getobj_rectangle(ra, dec, delta_ra, delta_dec, table_name)::

      -- get objects' tract, patch, pointing, id, ra2000, decl2000, cx, cy, cz, xxyyzz, distance 
      -- within 2 x 2 arcsec centered at (RA,DEC)=(150.403189,1.485288) in frame_forcelist of UDEEP CCD 
      -- RA and DEC are in degrees.  

      SELECT * from f_getobj_rectangle(150.403189, 1.485288, 2.0, 2.0, 'ssp_s14a0_udeep_20140523a.frame_forcelist__deepcoadd__iselect');
      
