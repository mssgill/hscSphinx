---- get objects' id, ra, dec, mags and mags_err on g,r,i,z,y bands and distance from the search center in arcsec  
---- which are within 30 arcsec radius from (RA, DEC) = (150.93, 1.93) in degrees  
---- and with good sinc magnitude measurement in r and i band 
---- and have (r - i) >= 2.0 in Sinc magnitudes.  

SELECT 
      pm.object_id, pm.ra2000, pm.decl2000, pm.gmag_sinc, pm.gmag_sinc_err, pm.rmag_sinc, pm.rmag_sinc_err, 
      pm.imag_sinc, pm.imag_sinc_err, pm.zmag_sinc, pm.zmag_sinc_err, pm.ymag_sinc, pm.ymag_sinc_err, obj.distance
FROM f_getobj_circle(150.93, 1.93, 30.0, 'ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect') obj,
     ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect pm, 
     ssp_s14a0_udeep_20140523a.mosaic_forceflag_i__deepcoadd__iselect mfi, 
     ssp_s14a0_udeep_20140523a.mosaic_forceflag_r__deepcoadd__iselect mfr  
WHERE obj.object_id=pm.object_id and obj.tract=pm.tract and obj.patch=pm.patch and obj.pointing = pm.pointing 
  and obj.object_id=mfi.object_id and obj.tract=mfi.tract and obj.patch=mfi.patch and obj.pointing = mfi.pointing 
  and obj.object_id=mfr.object_id and obj.tract=mfr.tract and obj.patch=mfr.patch and obj.pointing = mfr.pointing 
  and mfi.flux_sinc_flags is False and mfr.flux_sinc_flags is False 
  and pm.rmag_sinc - pm.imag_sinc >= 2.0 
ORDER by obj.distance;

