---- get objects' id, ra, dec, x, y, tract, frame_id, visit, ccd, shape_sdss and sky-based shape_sdss 
---- from the ccd forced photometry table of EDR WIDE data, on the data with (visit, ccd)=(380, 30)
---- The result will be ordered by output id.  

SELECT ff.object_id, ff.ra2000, ff.decl2000, ff.centroid_sdss_x, ff.centroid_sdss_y, ff.tract, ff.frame_id, cf.visit, cf.ccd, ff.shape_sdss, 
       shape_pix2sky(ff.shape_sdss, ff.centroid_sdss_x, ff.centroid_sdss_y, 'ssp_s14a0_wide_20140523a', ff.tract, ff.frame_id) 
FROM ssp_s14a0_wide_20140523a.frame_forcelist__deepcoadd__iselect ff, 
     ssp_s14a0_wide_20140523a.calibframe__deepcoadd cf 
WHERE ff.tract=cf.tract and ff.frame_id=cf.frame_id 
  and cf.visit=380 and cf.ccd=30 
ORDER BY ff.object_id;

