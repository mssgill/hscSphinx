----- This is an example for selecting QSO candidates at z ~ 4.5 
----- based on Richards et al. (2002) AJ 123, 2945 
----- including i band based classification of extendedness (PSF-like objects) 
SELECT 
      pm.id, pm.ra2000, pm.decl2000, pm.gmag_kron, pm.gmag_kron_err, 
      pm.rmag_kron, pm.rmag_kron_err, pm.imag_kron, pm.imag_kron_err, 
      pm.zmag_kron, pm.zmag_kron_err, pm.ymag_kron, pm.ymag_kron_err 
FROM ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect pm, 
     ssp_s14a0_udeep_20140523a.mosaic_forcelist__deepcoadd__iselect mfi 
WHERE pm.tract=mfi.tract and pm.patch=mfi.patch and 
      pm.pointing=mfi.pointing and pm.id = mfi.object_id 
  and mfi.filter01='HSC-I' 
  and mfi.classification_extendedness = 0  --- not extended
-----  the follwing constraints are similar to those of Richards et al. (2002) AJ 123, 2945
-----  for selecting QSOs at z ~ 4.5  
  and pm.imag_kron_err < 0.2  --- good measurement in i band Kron photometry  
  and pm.gmag_kron > 25.8     ---  gmag limit
  and (pm.rmag_kron - pm.imag_kron) > 0.6   --- r - i > 0.6
  and (pm.imag_kron - pm.zmag_kron) > -1.0  --- i - z < -1.0
  and (pm.imag_kron - pm.zmag_kron) < 0.52*(pm.rmag_kron - pm.imag_kron) - 0.412 -- i - z < 0.52(r - i) - 0.412
  and pm.imag_kron < 26.6      --- imag limit
  and pm.rmag_kron < 27.5      --- rmag limit
  and pm.zmag_kron < 25.8;     --- zmag limit
