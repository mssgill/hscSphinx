
-- Get an object where sinc mag of r band smaller than 25.5 mag, and -0.5
-- < r - i < 0.5 and g - r < 2.0.

-- WARNING:
--   --> Remove 'LIMIT 10' for your query
--   --> Edit the schema name 'ssp_s14a0_udeep_20140523a' for your query.
SELECT
    id, ra2000, decl2000,
    gmag_sinc, gmag_sinc_err,
    rmag_sinc, rmag_sinc_err,
    imag_sinc, imag_sinc_err,
    gmag_sinc - rmag_sinc as g_r,
    rmag_sinc - imag_sinc as r_i
FROM
    ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect
WHERE
    imag_sinc < 25.5
    AND
    rmag_sinc - imag_sinc between -0.5 and 0.5
    AND
    gmag_sinc - rmag_sinc < 2.0
LIMIT 10;

