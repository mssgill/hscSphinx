

-- Simple area search based on the range of RA and DEC getting all object
-- with r band Kron magnitudes are smaller than 25.5, and in the area in
-- the range RA J2000 between 210.0 and 215.0 degrees and DEC J2000 2.3
-- and 2.31 degrees.

-- WARNING:
--   --> Remove 'LIMIT 10' for your query
--   --> Edit the schema name 'ssp_s14a0_udeep_20140523a' for your query.

SELECT
        object_id, ra2000, decl2000,
        imag_kron, imag_kron_err,
        ymag_kron, ymag_kron_err,
        imag_kron - ymag_kron AS i_y
FROM
        ssp_s14a0_wide_20140523a.photoobj_mosaic__deepcoadd__iselect
WHERE
        ra2000 BETWEEN 210.0 AND 215.0       
        AND
        decl2000 BETWEEN 0.3 AND 2.31
        AND
        imag_kron < 25.5
LIMIT 10;
        