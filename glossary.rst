
========
Glossary
========

The idea here is to give you a two or three sentence explanation of a
concept, and (possibly) a link to where you can find more
information.

.. glossary::


    amplifier
        Each CCD in the HSC camera is read-out through 4 separate
        amplifiers (amps).  The pixel regions read through a given
        amplifier are along the columns; thus each 2048 x 4096 CCD has
        four 512 x 4096 amps.  Each amp behaves slightly differently
        electronically, so each of the four CCD regions corresponding
        to the amps has a slightly different gain, and non-linearity.
        The :ref:`HSC camera layout <hsc_layout>` shows the locations
        of amp1 for each CCD in the camera.
    
    aperture flux
    aperture photometry
        The HSC pipeline measures source flux with various algorithms
        (aperture, PSF, cmodel).  The 'aperture flux' has traditionally
        referred to a straight sum of the counts in all pixels within an
        'aperture' or specified (usually circular) region around the
        source.  What the HSC pipeline uses is conceptually exactly the
        same thing, except that it uses a Sinc interpolation algorithm
        (developed originally in SDSS) to handle the partial pixels
        correctly.  See :term:`Sinc photometry <sinc flux>` for details.
    
    background matching
        One difficulty encountered in creating a coadd stack of images is
        that the sky background present in each image can be very
        different (observed on different nights, with different moon
        position/phase, etc).  The solution has traditionally been to
        model the background (usually by smoothing the image with a large
        smoothing kernel) and subtract it prior to making the coadd.
        However, a better approach may be to choose one image as a
        'reference', and instead model the difference between its
        background and that of the other input images.  In this way, the
        input image backgrounds are matched to the reference and stacked.
        The result is that the coadd has a non-zero background (that of
        the reference image), but its signal-to-noise ratio is higher and
        it can therefore be measured and subtracted more accurately than
        it could have been prior to co-addition.
    

    brighter-fatter
    brighter-fatter effect
        To gain sensitivity to red photos, the CCDs used in the HSC camera
        (and many modern astronomical camera) are thicker than the
        previous generation of devices (200 um versus ~15-25 um).  The
        pixels have physical dimensions of 15x15 um, and so each can be
        thought of as having the aspect ratio of a sky-scraper.
        Photo-electrons are released in the higher floors of the silicon
        sky scraper and are pulled by an electric field down to the
        PN-junction in the basement where they're stored until read-out.
        However, as more photo-electrons accumulate in the basement, their
        presence tends to deflect some of the newly arriving
        photo-electrons into the neighbouring pixels.  The concequence of
        this is that **brighter** stars have a systematically wider
        (i.e. **'fatter'**) point spread function (PSF).

    Butler
        Rather than having different modules of the pipeline keep track of
        where and how they read/write their inputs/outputs, a software
        tool called the 'butler' does this.  If you go to an expensive
        restaurant, the 'valet' will park your car for you.  You don't
        need to know where the garage is when you arrive, and you don't
        need to remember where you parked when you leave.  This is what the
        butler does for the input/output operations of the pipeline.
        Rather than hard-coding the paths, filenames, and loading/writing
        syntax for various data inputs and outputs throughout the pipeline
        code; you simply make a call to the butler to 'get' the thing you
        want for a specific dataId (frame, CCD, etc).  For example,
        loading a bias image looks like this:
    
        ``biasImg = butler.get('bias', dataId)``
    
        
    CAS
    Catalog Archive Server
        This term is inherited from SDSS and refers to the online
        database system which is used by the community as one of the
        main ways to obtain SDSS data.  The data available through
        this system are the output measurements of the sources (right
        ascension, declination, ugriz magnitudes, etc), but not the
        images (see :term:`DAS` for that).
    
        .. todo:: perhaps a link here?
    
    ccd
        A charge-couple device, of course, but also used to refer to data
        from a CCD in a raw data image or in single-frame data products.
        See also :term:`DataId`.
        
    cmodel
        todo
    
    .. todo:: ask Jim.
    
        
    CoaddPsf
        todo
    
    .. todo:: ask Jim.
    
        
    DAS
    Data Archive Server
        This term is inherited from the SDSS and refers to the online data
        repository where data products such as images can be obtained.
        The pipeline outputs (RA, Dec, magnitudes, etc) are provided by
        the :term:`CAS`.
    
    
    dataId
        Individual exposures are refered to either as 'visits' or
        'frames', and their sub-components are the CCDs in the camera
        (note that LSST refers to these as 'sensors').  However, when
        making a coadd, the celestial sphere is broken into a set of fixed
        regions called 'tracts', which are similar in size to the field of
        view of the HSC camera.  The tracts are composed of sub-regions
        called 'patches'.  Each patch is about the size of a CCD.  Thus,
        'visit' and 'CCD' are used to refer to raw data or single-frame
        data products, while 'tract' and 'patch' refer to coadd data.  A
        dataId also includes such things as field name (field), date of
        observation (dateObs), and filter.
    
        See also :ref:`DataId <back_dataId>`
    
        
    deblend
        Sources which are detected in the pipeline are often found to be a
        group of multiple blended/overlapping sources.  In order to
        measure each of the contributing sources separately, the detected
        source (called a 'parent') must be 'deblended' into its
        'children'.  The algorithm use is decribed in
    
        .. todo:: add link to explanation of deblend algorithm.
    
    deep survey
        todo
    
    double-Gaussian
        The point spread function of a star is quite similar to a 2D
        Gaussian, but has too much flux present in the extended 'wings'.
        However, while one Gaussian is a poor model, two Gaussians does
        quite a good job.  One Gaussian models the center of the PSF,
        while the second Gaussian (typically 2x the width and 0.1x
        amplitude) models the wings.  A double-Gaussian PSF is available
        in the pipeline software, but is not used as a PSF for production
        reruns.
    
    differencing
        todo
    
    doxygen
        Doxygen is a code documentation system used by the software group.
        The system uses specially formatted comments in the code to
        construct a web-based navigable tool which is useful for
        developers.  The HSC doxygen is served `here
        <http://hsca.ipmu.jp/doxygen/>`_.
    
        
    EUPS
        EUPS is the package management system used by the software group.
        It's used to install and generally keep track of different
        versions of the software pipeline modules.  For specific details,
        see the :ref:`EUPS page <back_eups>`
        
    extendedness (classification.extendedness)
        This is an output value associated with each source measured by
        the pipeline.  It's stored as a float, but is currently used as a
        flag for star/galaxy separation (0 = star, 1 = galaxy ... a galaxy
        is more 'extended' than a star).
    
    flag
        In any measurement that the pipeline makes, any concerns
        associated with the pixels or the measurement will be recorded in
        the catalog outputs in parameters with names including the word
        'flag'.  Examples include ``flags_pixel_edge``,
        ``flags_pixel_interpolated_any`` ... you can guess what these
        mean.  The full list is included in the `data products document
        <http://hsca.ipmu.jp/hscsoft/datainfo.php>`_.
        
        
    footprint
        Within the software group, the region of pixels occupied by a
        source (which we want to measure) is called the source's
        'footprint'.  The pixels within the footprint are used for the
        measurement, the ones outside are not.
    
    forced measurement
        In our stacked images, we're able to detect faint sources which
        would be below our 5-sigma thresholds in any of the input images,
        or in the coadds from different filters.  However, once we know
        that a source is detected in e.g. a deep i-band stack, we can then
        measure it at the location we expect it to be in another image
        where it wasn't detected.  This is called a 'forced measurement'.
    
    frame
        A full exposure including all CCDs.  It's assigned a number by the
        observatory (called a frameID).  The software group tends to use
        the word 'visit' to mean the same thing.
    
    healpix
        There are various ways you can break up the celestial sphere into
        discrete regions (called tesselation).  HealPix is a popular one
        in the astronomy community.
    
        ..todo:: We support this, but I don't know of anywhere where we're currently using it.
    
    HSM
    Hirata-Seljak-Mandelbaum
        This refers to a collection of shape measurement algorithms
        coded-up, bundled together, and made public by Chris Hirata,
        Uros Seljak, and Rachel Mandelbaum.  The package includes 'KSB'
        (HSM_KSB), 'regaussianization' (HSM_REGAUSS), 'Bernstein-Jarvis'
        (HSM_BJ), 'linear' (HSM_LINEAR), and a shapelet-based algorithm
        (HSC_SHAPELET).  It is enabled by default in the HSC pipeline.
    
    Kron flux
        todo
              
    .. todo:: write this.
    
    KSB
        todo
        
    .. todo:: Do we need this?  Out of scope for this glossary?
    
    
    mosaic
        Mosaic is the name of the HSC software module which performs a
        photometric uber-calibration, in which the photometry measured in
        different visits is tied together into the same self-consistent
        photometric system.
    
    multifit
        todo
    
    .. todo:: ask jim.
    
    multishapelet
        todo
    
    .. todo:: ask jim.
    
    object
        This is a common word, but has a somewhat specific meaning in the
        software group.  It refers to a celestial object whose properties
        we'd like to measure.  It should not be confused with a 'source',
        which is a specific exposure instance of an object.  For example,
        a star is an 'object', but two exposures of it will yield two
        'sources'.
    
    patch
        See :term:`DataId`.
    
    
    peak
        During :term:`deblending <deblend>`, individual components are
        identified in the parent source's :term:`footprint`.  The
        highest pixel in each candidate child is it's peak.
        
    
    Petrosian flux
        todo
        
    .. todo:: ask rhl.
    
    pipeline
        The collection of data processing steps which run autonomously to
        take the raw input data and produce the final catalog output
        measurements.
        
    PSF
    point spread function
        The response function of an imaging system to a 'point source', or
        delta function.  This includes the atmosphere plus the telescope
        plus the camera.  The PSF is a function of position across the
        field of an image, and is also varies over time.
    
    PSF flux
    PSF photometry
        While aperture photometry measures the sum of the integrated flux
        within a synthetic aperture around a source; PSF photometry
        measures the *weighted* sum of the flux, where the weight function
        is the local PSF at the sources position in the image.  If the
        source is itself a point source (i.e. a star), then the
        measurement is optimal.
    
    PSF-Ex
        A PSF model library developed by Emmanuel Bertin.  PSF-Ex is used
        for PSF flux measurement in the HSC pipeline.
    
    raft
        The LSST camera (*not* HSC) is subdivided into 21 square
        platforms, with 9 CCDs mounted 3x3 on each one (total 189
        CCDs).  The 21 square platforms are called 'rafts'.  The HSC
        camera is not structured this way, but you may occassionally hear
        the term as the pipeline code is shared with the LSST project.
    
    rerun
        The term ``rerun`` originated in SDSS.  It simply refers to a
        single processing run, performed with a specified version of the
        reduction code, and with a specific set of configuration
        parameters.  The implication is that within a given 'rerun', the
        data have been handled in a homogeneous way.
    
    
    schema
        (w.r.t. database) The schema of a database is its structure.
        It refers to the coded blueprint which describes how the data
        are to be stored with respected to one another.  Which fields
        will appear in which tables, and what types of data they will
        contain are described in a database's schema.
    
        Note also, that the HSC database system uses PostgreSQL, and the
        term 'schema' has a specific meaning in the context of postgreSQL.
        Separate logical databases within a single PostgreSQL database are
        called 'schema'.
    
        
    sensor
        See :term:`DataId`.
    
    
    sinc flux
    sinc photometry
        todo
    
    skymap
        todo
    
    Sloan swindle
        todo
        
    source
        todo
        
    SSP
        See Strategic Survey Proposal
    
    stack
        (w.r.t. the data reduction pipeline) A slang term for the
        complete set of software packages which make up the pipeline
        code.
        
    stack
        (w.r.t. image coaddition) A synonym for coadd.
    
    Strategic Survey Proposal (SSP)
        todo
        
    TAN-SIP
        todo
        
    Task
        Each step in the pipeline processing is contained within a
        software class called a 'Task'.
    
    tract    
        See :term:`DataId`.
    
    uber-calibration
        Uber-calibration was originally developed in SDSS to tie all
        observations onto a single consistent photometric system.  The
        method relies on repeated observations of the same objects in
        multiple exposures.  The calibration terms can then be adjusted to
        allow measurements in the different exposures to be compared
        meaningfully.  The HSC uber-calibration process is called 'mosaic'.
    
    .. todo:: put a ref to Nikhil's paper.
        
    ultra-deep survey
        todo
    
    
    visit
        See :term:`DataId`.
    
    warp
        In order to produce a stack, the input images must all be
        resampled onto a common pixel grid. The process is referred to as
        warping.
    
    WCS
    World Coordinate System
        todo
    
    wide survey
        todo
    
    
    
    
    
    
    
    
    
    
    
    
