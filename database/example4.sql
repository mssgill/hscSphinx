
-- Get objects where Galactic extinction corrected sinc mag of i band brighter than 25.5 mag, 
-- and -0.5 < r - i < 0.5 and g - r < 2.0 and centroid well determined and no error 
-- in measuring sinc fluxes on i-band coadd image.

-- WARNING:
--   --> Remove 'LIMIT 10' for your query
--   --> Edit the schema name 'ssp_s14a0_udeep_20140523a' for your query.
SELECT
    pm.object_id, pm.ra2000, pm.decl2000,
    pm.gmag_sinc - pm.a_g as gmag, pm.gmag_sinc_err,
    pm.rmag_sinc - pm.a_r as rmag, pm.rmag_sinc_err,
    pm.imag_sinc - pm.a_i as imag, pm.imag_sinc_err,
    (pm.gmag_sinc - pm.a_g) - (pm.rmag_sinc - pm.a_r) as g_r,
    (pm.rmag_sinc - pm.a_r) - (pm.imag_sinc - pm.a_i) as r_i
FROM
    ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect pm,
    ssp_s14a0_udeep_20140523a.mosaic_forceflag_i__deepcoadd__iselect iflg 
WHERE
    pm.tract = iflg.tract AND pm.patch = iflg.patch AND pm.pointing = iflg.pointing AND pm.object_id = iflg.object_id 
    AND 
    (pm.imag_sinc - a_i) < 25.5
    AND
    (pm.rmag_sinc - pm.a_r) - (pm.imag_sinc - pm.a_i) between -0.5 and 0.5
    AND
    (pm.gmag_sinc - pm.a_g) - (pm.rmag_sinc - pm.a_r) < 2.0 
    AND 
    iflg.centroid_sdss_flags is not True 
    AND 
    iflg.flux_sinc_flags is not True 
LIMIT 10;

