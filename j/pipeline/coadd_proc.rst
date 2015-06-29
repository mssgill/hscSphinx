

===========================
天体データの重ね合わせ
===========================

このページで紹介する解析は reduceFrames.py による各 CCD の一次処理と天体検出、測光が完了
していることを前提としています。もしまだ完了していない場合は、まず reduceFrames.py を実行してください。
天体データの重ね合わせの処理過程では、全ての天体データを共通の WCS 座標系に変換し、取得された
全ての天体データを重ね合わせて、S/N が改善された最終画像（coadd 画像）を生成します。以下のステップで天体データの
重ね合わせ処理は行われます。:

#. **SkyMap** （coadd 画像に用いられる座標系）を生成する。

#. **mosaic**: 等級原点や座標を決定する。

#. **Warp**: 観測された WCS 座標系から SkyMap の座標系に画像をリサンプルする（warp 画像の生成）。

#. **coadd 画像の生成**: warp 画像の足しあわせ。

#. **Process**: coadd 画像から天体を検出し、カタログを生成する。

以下では各解析ステップについて紹介します。なお、``warp``, ``assemble``, ``process``
は全て ``stack.py`` と呼ばれる 1 つの解析コマンド内で実行されています。


.. _jp_skymap:

Making a SkyMap
---------------

まず最初に SkyMap を生成します。SkyMap は天球面上をタイル、またはモザイク状にしたもので、
最終 coadd 画像で用いられる座標系です。SkyMap で設定される最大の領域は 'Tract' と呼ばれ、
その中には複数の 'Patch' 領域が含まれています。Tract も Patch も隣の
Tract/Patch と重なり合うように設定されます。デフォルトでは、Tract は 1 arcmin、
Patch は 100 pix 重なるよう設定されています（1 Patch は 4000 x 4000 pix）。
各 Tract には異なる WCS が設定されていますが、その中にある Patch には Tract が持つ
WCS に対する offset の値が与えられます。以降の解析で紹介する warp において、
天体データが持つ観測時の WCS の情報は SkyMap による共通の WCS の情報に変換されます。

SkyMap を生成するには 2 つの方法があります: (1) 全天の情報を使って生成する
（個々の PI-type の観測データの解析では **使用しない** かもしれません）、または
(2) 観測データのみを使って生成する。


Full SkyMap
^^^^^^^^^^^

To create a full SkyMap (again, not likely what you want), do the following::
   
    $ makeSkyMap.py /data/Subaru/HSC/ --rerun=cosmos

    
Partial SkyMap
^^^^^^^^^^^^^^

To create a local SkyMap for the region containing your data, use the
``makeDiscreteSkyMap.py``.  Here, you can select specified visits to
be used to define the region of the SkyMap.  In this case the example
shows visits 1000 to 1020 with increment 2 (i.e. every other one, as
is the standard for HSC visit naming).  Because you chose a local
SkyMap, all your data will be within a single Tract, and that Tract
will be defined to have ID 0 (zero).  If you're using a full SkyMap,
the Tracts are a fixed system and you'll have to look-up which tracts
your data live in.

.. todo:: Describe how to lookup tract IDs.

**(probably what you want)**

::

    $ makeDiscreteSkyMap.py /data/Subaru/HSC/ --rerun=cosmos --id visit=1000..1020:2


One of the example scripts (:ref:`showVisitSkyMap.py
<showvisitskymap>`) can be used to display a set of visits on a
SkyMap.  Here it was used to display two visits superimposed on a
discrete (partial) SkyMap.  Only the patches overlapped by the visits
are shown.  Each patch is labeled.

.. image:: ../../images/showVisitSkyMap.png


Making a Custom SkyMap
^^^^^^^^^^^^^^^^^^^^^^

If you have a particular need for your coadds to have a specific WCS,
you can also customize the SkyMap to have a given pixel scale and
tangent point.  This is done by specifying config parameters to
``makeSkyMap.py`` as follows::

    $ cat overrides.config
    root.skyMap = "discrete"
    root.skyMap["discrete"].raList = [149.9]
    root.skyMap["discrete"].decList = [2.3]
    root.skyMap["discrete"].radiusList = [0.35]
    root.skyMap["discrete"].pixelScale = 0.2
    root.skyMap["discrete"].projection = "TAN"
    root.skyMap["discrete"].tractOverlap = 0

    $ makeSkyMap.py /data/Subaru/HSC --rerun=cosmos --configfile overrides.config

.. warning:: untested.

.. _jp_mosaic:

mosaic.py
^^^^^^^^^

Once the single-frame processing is completed and you have a SkyMap,
you can perform an 'ubercal' with mosaic.py.  This will solve for an
improved astrometric and photometric solution for a collection of
visits.  In the ``--id``, you must specify the tract in addition to
the identifiers for your data (i.e. visit, field, filter, etc.).  If
you constructed a partial SkyMap, the tract will be 0.  It's also
useful to specify ccd=0..103.  CCDs 104 to 111 exist but are not used
for science data (4 auto-guide plus 8 auto-focus), and should not be
included.

::
   
    $ mosaic.py /data/Subaru/HSC/ --rerun=cosmos --id tract=0 visit=1000..1020:2 ccd=0..103


.. _jp_stack:    

Coadd Processing with One Command
---------------------------------

If you just want to produce a coadd and run the pipeline on the
coadded image, then ``stack.py`` is the command you should use::

    $ stack.py /data/Subaru/HSC/ --rerun=cosmos --id tract=0 filter=HSC-I --selectId visit=1000..1020:2 --queue small --nodes 4 --procs 6 --job stack
    

In the example, the input visits are specified with ``--selectId``
(even-numbered visits from 1000 to 1020).  The ``--id`` parameter is
now used to specify the tract and patch dataId for the output.  If you
constructed a partial SkyMap with ``makeDiscreteSkyMap.py``, then your
tract number will be 0.  ``stack.py`` distributes jobs over PBS
TORQUE, and the remaining command line arguments shown are related the
batch processing.  See :ref:`TORQUE <jp_back_torque>` for details.
          

Coadd Processing in Steps
-------------------------

If you wish to do your coadd processing in individual steps, you can
forego ``stack.py``, and perform each of its component steps manually.

First, you must resample your single-frame output images to the
coordinate system used for coadds (the SkyMap you just created).  The
process is called 'warping', and will convert your input CCDs to
'patches'.  The corners of a given CCD will almost always lie across
patch borders, as CCDs and patches don't (can't) align perfectly.
Thus, each CCD will contribute to 4 patches.  The part of each patch
which is outside the region of the input CCD contains no data and is
masked in the 'warped' image.

In the second step, the warped images are combined statistically
with ``assembleCoadd.py`` to produce the 'coadd' or 'stack'.

The final part of coadd processing is to run detection and measurement
with ``hscProcessCoadd.py``.

.. _jp_warp:
          
Warping
^^^^^^^
       
The first step is to warp your images to the SkyMap coordinate system
(Tracts and Patches).  This is done with makeCoaddTempExp.py::

    $ makeCoaddTempExp.py /data/Subaru/HSC --rerun cosmos --id tract=9000 patch=1,1 filter=HSC-Y --selectId visit=1000^1002 ccd=0..103

There are now two ``id`` settings required.  ``--id`` refers to the
Tract and Patch that you wish to create, while ``--selectId`` refers
to the *input* visits, CCDs, etc. that you wish warp to the specified
tract and patch.

.. _jp_assemblecoadd:

Coadding
^^^^^^^^

Once your images have been warped on to the SkyMap patches, running
``assembleCoadd.py`` will create the stacked image.  Again, there are
two sets of ``id`` settings: ``--id`` (the destination Tract,Patch),
and ``--selectId`` (the input visits,CCDs).  These should probably be
set to be the same as the settings you used for
``makeCoaddTempExp.py``::

    $ assembleCoadd.py /data/Subaru/HSC --rerun cosmos --id tract=9000 patch=1,1 filter=HSC-Y --selectId visit=1000^1002 ccd=0..103

.. todo::

    Add examples for how to override useful parameters for different
    types of stacks.

    
.. _jp_processcoadd:
        
Coadd Processing (i.e. detection, measurement)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running the pipeline on coadded images cannot be done with
``hscProcessCcd.py`` or ``reduceFrames.py``.  Instead, a separate
process ``hscProcessCoadd.py`` is used.  This example will process the
same Tract,Patch which has been constructed above with
``assembleCoadd.py``::
    
    $ hscProcessCoadd.py /data/Subaru/HSC --rerun cosmos --id tract=9000 patch=1,1 filter=HSC-Y


    
.. todo::
    
   Is hscOverlaps.py still used?
   
.. todo::
   
   Is hscStack.py still used?

