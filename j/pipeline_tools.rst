=========================
パイプラインツール
=========================

.. note::
	Jim Bosch（HSCパイプライン開発チーム / Princeton）による
	`HSC Pipeline Outputs <http://hsca.ipmu.jp/notebooks/HSC-Pipeline-Outputs.html>`_
	という IPython のメモも参照のほど。

HSC パイプラインは LSST パイプラインをもとに開発されており、コマンドは python
スクリプトの形式になっています。HSC パイプラインには画像処理のコマンド以外にも python
をベースにした便利なツールがいくつか同梱されています。HSC
パイプラインを通して生成されたカタログを使って研究を行うならば、
パイプラインツールは非常に便利です。また、画像を使って研究を行う場合でも、
パイプラインツールを使って画像データの処理を行うことができます。EUPS 'setup' 
セットアップコマンドで HSC パイプラインをセットアップすれば、Application FrameWork
（'afw'）や他のパイプラインツールもセットアップすることができます。

.. highlight::
	bash

::

    $ setup -v hscPipe <version>

主なパイプラインツールを以下に紹介します。:

#. butler, dataRef: 様々なタイプのデータを検索したりロードすることができるツール

#. Exposures, MaskedImages, Images: 画像を処理するためのツール

#. SourceCatalogs: 検出された天体カタログの座標, フラックス, サイズ, adaptive moment などの情報を一覧にして取り扱うツール

   
.. _jp_tool_butler:
   
butler
----------

butler を使うと、データベースから必要な情報を検索し読み出し、保存することができます。
このチュートリアルではパイプラインの出力データを用いて bulter の使い方を説明します。
ファイルのパーミッションを設定しておけば butler で読み込んだデータを上書きすることはありません。
それでも心配な場合は、上書き/書き出し処理をせずに butler を使用してください。

以下の方法で butler を呼び出すことができます。

.. highlight::
	python
	
::

    import lsst.daf.persistence as dafPersist
    # <snip> #
    dataDir = "/data/Subaru/HSC/rerun/myrerun"
    butler = dafPersist.Butler(dataDir)


``butler`` では ``get()`` と dataId を使って自分が興味があるデータを呼び出すことができます。
以下の例では dataId として 'visit' と 'ccd' を参照しています。もし coadd 
データに対し butler を使用する際には、dataId には 'tract' と 'patch' を指定しましょう。 ::

    dataId = {'visit': 1234, 'ccd': 56}
    bias = butler.get('bias', dataId)


'_filename' 拡張子
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
データそのものではなく、どのデータから読み込まれたファイルか調べる時には、
以下のように ``_filename`` 拡張子を加えることができます。例えば、Bias
データに filename 拡張子をつけたい時には以下の方法があります。 ::
	
    bias_filename = butler.get('bias_filename', dataId)


'_md'（メタデータ）拡張子
^^^^^^^^^^^^^^^^^^^^^^^^^^^

butler で呼び込むデータの多くはメタデータ（ヘッダー等）です。もしメタデータに興味があるなら
``_md`` 拡張子をつけてデータリクエストを行いましょう。また、一次処理用データには、
``calexp_md`` という拡張子をつけることもできます。 ::

    calexp_md = butler.get("calexp_md", dataId)


.. Where should this warning go???    
.. .. warning:: Loading reprocessed data (i.e. inputs from one repo,
..   outputs written to another), may yield unexpected results.  This
..   can occur when coadd outputs have been produced in one repository,
..   and a second coadd has been produced from the same single-frame
..   outputs.  If the butler is unable to find a requested dataset, it
..   will then check the parent repository.  Thus, if a given patch or
..   CCD is produced in the original coadd, but not in the second coadd,
..   the butler will load the data from the original.  If this is a
..   concern (i.e. if you're loading reprocessed coadds), the
..   ``_filename`` suffix can be used as a butler target to get the path
..   and verify which data is being loaded.  Data loaded from the parent
..   repository will include the directory (a symlink) ``_parent`` in
..   the path.  This may actually be exactly what you want (calibration
..   data, single-frame outputs, etc. will all live in the parent repo),
..   but could cause confusion for e.g. deepCoadd_src.

    
.. _jp_tool_dataref:
    
dataRef
^^^^^^^^^^^

butler を使うには ``butler`` と ``dataId`` が必要です。もし同じ dataId
の様々なデータについて調べたい時には、bulter の 'data reference' で参照できます。
同じ dataId の Bias データを調べたい時には以下のようにコマンドを実行しましょう。 ::
    
    import hsc.pipe.base.butler as hscButler
    # <snip> #
    dataId = {'visit': 1234, 'ccd': 56}
    dataRef = hscButler.getDataRef(butler, dataId)
    bias = dataRef.get('bias')




butler でよく使われる検索
--------------------------------------------------

パイプラインを介して生成された様々なデータは butler の ``get()`` 
を使って検索や読み出しができます。ここでは、
よく使用されると思われる検索内容を紹介します（かっこ内にデータの種類を記述しています）。

一次処理用データ (dataId で visit と ccd を指定)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下に一次処理用データのデータタイプをまとめてあります。画像ベースのデータはすべて
``ExposureF`` というデータタイプになります。 :

=========== =========== ================================
Target      Data type   Comment
=========== =========== ================================
**bias**    ExposureF   Bias 画像
**dark**    ExposureF   Dark 画像（1 秒あたり）
**flat**    ExposureF   Flat 画像
**fringe**  ExposureF   Fringe 画像（基本 Y-band のみ）
=========== =========== ================================


一次処理済データ (dataId で visit と ccd を指定)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **postISRCCD** (``ExposureF``): 一次処理済データのことで、
   'ISR' とは 'instrument signature removal' の略語で、
   天体データの一次処理が完了していることを意味します（例えば、Bias 引き、Flat 補正、
   Fringe 補正が完了しているということ）。デフォルトのパイプライン処理では
   postISRCCD データは出力されません。パイプライン処理において出力させるには
   reduceFrames.py において ``isr.doWrite=True`` のパラメータを追加してください。

#. **calexp** (``ExposureF``): background が引かれた postISRCCD データで、
   一次処理済メタデータを意味します。デフォルトのパイプライン処理（reduceFrames.py）では、
   このデータが生成されます（デフォルトでは postISRCCD は　disk に出力されていないため）。

#. **psf** (``Psf``): 画像処理において使用される PSF を意味します。この PSF
   を用いて、自身が指定した dataId のデータの PSF を再現することができます。
   具体的な使い方については ``Psf`` をご覧ください。

#. **src** (``SourceCatalog``): dataId の検索に含まれる全天体の測定結果（カタログ）
   です。カタログ内の天体の情報としては、RA, DEC, フラックス（aperture, PSF 等）,
   adaptive moment などなどがあります。

#. **wcs** と **fcr** (``ExposureI``): 天体データの一次処理が完了したら、
   座標と等級原点を決める ``mosaic`` 処理（uber-calibration）が実行されます。
   'wcs' と 'fcr' には、座標と測光を補正する天体がそれぞれ含まれています。


coadd データ (dataId で tract と patch を指定)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

coadd データを検索する際に必要な引数は一次処理済データの場合と共通ですが、
``deepCoadd_`` という拡張子をつける必要があります。また、coadd データには
'postISRCCD', 'wcs', 'fcr' の引数に相当するデータはありません。
そのため、使える引数は以下です。

==================== ===========================
Single Frame target  Coadd Target
==================== ===========================
calexp               **deepCoadd_calexp**
psf                  **deepCoadd_psf**
src                  **deepCoadd_src**
==================== ===========================


他の butler 引数を調べる
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

もしある特定のデータを調べたかったり、あるデータが butler
内でどのような引数で呼び出されるか知りたい時、butler の別種と言える 'mapper'
を調べてみてください。'mapper' には butler で検索できうる全ての引数の情報を含んだ
configuration ファイルが格納されています。HSC の場合、mapper configuration
ファイルは ``obs_subaru`` EUPS パッケージにあります。ディレクトリは
``$OBS_SUBARU_DIR`` という環境変数で指定されており（:ref:`EUPSの動作の仕組み 
<jp_back_eupsworks>` と :ref:`jp_back_policy` 参照）、その中の HscMapper.paf
ファイルが mapper configuration ファイルです。

.. highlight::
	bash

::

    $ ls $OBS_SUBARU_DIR/policy/HscMapper.paf
    /data1a/ana/products2014/Linux64/obs_subaru/2.0.0/policy/HscMapper.paf

    
では、mapper configuration ファイルの中身を一部抜粋して見てみましょう。 ::
    
    calexp: {
        template:      "%(pointing)05d/%(filter)s/corr/CORR-%(visit)07d-%(ccd)03d.fits"
        python:        "lsst.afw.image.ExposureF"
        persistable:   "ExposureF"
        storage:       "FitsStorage"
        level:         "Ccd"
        tables:        "raw"
        tables:        "raw_visit"
    }

ここで抜粋したのは 'calexp' (calibrated exposure) と呼ばれる引数です。
``template`` は calexp に関係するデータがデータリポジトリ内のどこに配置されているかを、
``python`` は python 内で参照する際のデータの種類を表しています。
それ以外のパラメータは主に開発者用のものです。HscMapper.paf を開いて butler 
内での引数を調べる時には、ファイルそのものを編集しないように気をつけてください。



Exposures, MaskedImage, Images
----------------------------------

``Exposure``, ``MaskedImage``, ``Image`` は、
パイプラインによって生成された画像データを処理するためのツールです。butler 同様、
python 内では拡張子をつけて画像データを読み込んでください。通常は float 'F'
（例 ``ExposureF``）か integer 'I'（例 ``ImageI``）が用いられます。
これら 3 つの画像処理ツールのうちで ``Image`` が最もシンプルで、
ピクセルの 2D 構造を読み込みます。一方、``MaskedImageF`` では 3 つの画像データを読み込み
（ImageF データ, mask ImageI データ, variance ImageF データ）、
``ExposureF`` では ``MaskedImageF`` とそれに附随するメタデータ
（FITS ヘッダー内の情報のこと）を読み込みます。

多くの場合、butler で検索された画像データは ``ExposureF`` のデータタイプで処理されます。
butler 内では、パイプラインで生成された画像データを numpy で処理できる画像形式に変換します。
さらに、画像データに加えて、データに附随するメタデータ（ヘッダー情報）を ``PropertySet``
と呼ばれる変数として格納します。以下に載せるスクリプトの例では 'calexp' を butler
で呼び込み、その中から画像とメタデータを抜き出して matplotlib で画像データを表示し PNG
ファイルの形式で画像を書き出しています。この例は一次処理済の天体データ（visit, ccd）
に対して行っていますが、butler 内の 'deepCoadd_calexp' 引数を使えば
coadd データに対して同様の処理が可能となります。


..	In most cases, any image data you request from the butler will be
	handed to you in the form of an ``ExposureF`` object.  In the form of
	pipeline Image objects, these may be difficult to work with, but the
	images can be converted to more familiar numpy images, if you're more
	comfortable with that format.  In addition to the image data, the
	associated metadata is also present in an object called a
	``PropertySet``.  The following example demonstrates loading a
	'calexp' with the butler and extracting both the image and metadata
	information, and writing a PNG with matplotlib.  This would be used on
	single-frame data (i.e. visit,ccd), while the 'deepCoadd_calexp'
	butler target would be used for coadd data.


.. literalinclude:: ../scripts/ccdplot.py
   :language: python


マスク（mask）
^^^^^^^^^^^^^^^^^

前述の通り、``MaskedImage`` には '画像' と 'variance' と 'mask' 
データが格納されています。mask データには非常に特殊な方法でデータが格納されており、
その扱いには注意が必要です。HSC mask データでは、各ピクセル 16-bit で flag
の情報を格納しています。16-bit のうち 14-bit は以下のリストに載せた mask
される種別の有無の判別に使われ、残り 2-bit でそのピクセルが mask
として検出されるかの判別に使用されます。mask として flag されるピクセルの多くは、
宇宙線やサチった星によるオーバーフローが影響しているような問題あるピクセルです。
それ以外には、検出された天体の footprint の位置につけられる場合もあります。

================= ======================================================================================
Label             意味
================= ======================================================================================
BAD               bad ピクセル（HSC カメラ側の問題）
CR                宇宙線
CROSSTALK         ピクセルのクロストーク
EDGE              端にある CCD 
INTERPOLATED      周囲のピクセルから補間されたカウント値になっているピクセル
INTRP             （INTERPOLATED と同義）
SATURATED         サチっているピクセル
SAT               （SATURATED と同義）
SUSPECT           **ほぼ** サチっているピクセル（非線形性がうまく補正されていないため）
UNMASKEDNAN       ISR 画像でピクセルの値が NaN になっているピクセル

DETECTED          検出された天体の footprint の一部であるピクセル
DETECTED_NEGATIVE 天体の footprint の一部で値が **負** になっているピクセル

CLIPPED           （coadd データのみ）coadd 処理において 1 か 2 というクリップがついたピクセル
NO_DATA           （coadd データのみ）coadd 処理において入力データがないピクセル
================= ======================================================================================

HSC パイプラインでは、ある rerun データ処理中に宇宙線を検出すると、
'CR' として 16-bit の mask データ中に記録します。この mask データは rerun 毎に独立なので、
他の rerun で宇宙線が検出されるかは自明ではありません!
mask の情報や mask 画像を取り扱いたい時には、パイプラインツールを使うと非常に便利です。

ある mask データで mask の bit 情報を使い（例 宇宙線）、
mask した領域の画像を生成するには以下の方法があります。

.. highlight::
	python
	
::

    # maskedImage を呼び込んだ場合 ...
    mask       = maskedImage.getMask()
    crBitMask  = mask.getPlaneBitMask("CR")

    # crImage のコピーを作り、CR bit のみ注目している
    # (マスクしていないピクセルには 0 が、マスクされているピクセルには crBitMask の値が入る)
    crImage = mask.clone()
    crImage &= crBitMask

    
天体カタログ
----------------------------

パイプラインで生成された天体カタログは ``SourceCatalogs`` として格納されます。
``SourceCatalog`` は HSC パイプライン内でのみ参照できる形式のカタログで、
各列には天体が、各行には全天体の測定結果が含まれています。butler を使って検索する際には、
一次処理済データの場合は 'src' という引数で、coadd データの場合は 'deepCoadd_src'
という引数を使用してください。 ::

    sources = butler.get("src", dataId)

カタログ内の変数は変数のタイプに応じて列や行の形式で抽出されます。

* シンプルなタイプの変数（float, int 等）の場合、``sources.get('thing')`` 
  を使って変数を抽出できます。ここで 'thing' は自身が欲しいデータタイプで、
  例えば、'flux.aperture', 'flux.aperture.err' などがあげられます。
  こうした天体の測定値は SourceCatalog の行に格納されているため、
  ``numpy.ndarray`` のようなベクトル処理を使うと便利です。しかし、'coord'
  のようなより複雑な変数の場合、``SourceCatalog`` の列だけ抽出することはできません。

* カタログ内の個々の天体の情報は、index（例 ``s = source[i]``）や、ループ処理
  （例 ``for src in sources``）を使ってアクセスできます。ここでは ``SourceRecord``
  （カタログ内の各天体の全測定結果の情報）を返します。

以下では上記 2 つの検索方法について例示しています。まず、ある dataId のカタログ内の天体数と、
``ndarray`` でそれら天体の PSF フラックスの値を得ています。それから天体全体でループをかけ、
PFS フラックス、'classification.extendedness'（星と銀河を区別するパラメータ）
の値を抽出しています。 ::

    # butler で SourceCatalog を読み込む
    sources = butler.get("src", dataId)

    # カタログ内の天体数と PSF フラックスの値を得る
    n = len(sources)
    psfFlux    = sources.get("flux.psf")

    # 各天体の PSF フラックスと 'extendedness' の値を SourceRecord から抽出
    for i, src in enumerate(sources):
        print i, psfFlux[i], src.get("classification.extendedness")

ユーザーの多くは天体のフラックスよりも等級をを使うことが多く、
そのために原点情報が必要なことがあると思います。各 CCD の原点情報は butler
の ``calexp_md`` という引数から調べることができます。 ::

    metadata  = butler.get("calexp_md", dataId)
    zeropoint = 2.5*numpy.log10(metadata.get("FLUXMAG0"))

または、``mosaic.py`` の実行で得られる uber-calibrated の原点情報も利用可能です。
mosaic.py によって得られた原点等級の値は以下の方法で求められます。 ::

    fcr_md     = butler.get("fcr_md", dataId)
    ffp        = measMosaic.FluxFitParams(fcr_md)
    x, y       = sources.getX(), sources.getY()
    correction = numpy.array([ffp.eval(x[i],y[i]) for i in range(n)])
    zeropoint  = 2.5*numpy.log10(fcr_md.get("FLUXMAG0")) + correction

次のスクリプト例では、カタログ内のフラックス値を等級に直して出力しています。 :

.. literalinclude:: ../scripts/print_mags_from_butler.py
    
``SourceCatalog`` の全測定情報については :ref:`Single-frame Schema <jp_prettyschema_sf>`
と :ref:`Coadd Schema <jp_prettyschema_coadd>` をご覧ください。SourceCatalog
ができたら、``schema`` を使ってカタログ内を検索してみましょう。
上記リンクで表示した測定情報と同様の結果を見ることができます。 ::

    sources = butler.get("src", dataId)
    print sources.schema
    

SourceRecords 内の特別なデータフォーマット
----------------------------------------------------

SourceCatalogs には通常とは異なるデータタイプも含まれています。

Coord と Angle
^^^^^^^^^^^^^^^

``Coord`` には座標情報が格納されています。この中には、RA, DEC, 座標変換の情報と、
``Angle`` と呼ばれる特別なデータタイプが含まれます。Coord には、
ICRS, FK5, Galactic, Ecliptic 系の座標情報が含まれています。今のところ、
ICRS と FK5 は同じものです。Angle では様々な角度のフォーマットが利用可能です:
degrees, radians, arcminutes, arcseconds。以下のスクリプトでは、
基本的な使い方を示します。

.. literalinclude:: ../scripts/print_coord.py
   :language: python


Moment
^^^^^^

adaptive moment も ``Quadrulpole`` や ``Axes`` という特殊なデータタイプとして処理されます。
以下のスクリプトでは、基本的な使い方を示します。

..	Adaptive moments are also handled in special data types,
	``Quadrulpole``, and ``Axes``.  The following example shows the basic
	usage

.. literalinclude:: ../scripts/print_moment.py


ds9 を用いた処理
----------------------------

画像の表示
^^^^^^^^^^^^^^^^^

HSC パイプラインに同梱されている python ツールから ds9 に画像を表示されることができます。
ds9 そのものはパイプラインに含まれていませんので、自身で別途インストールしてください。
ds9 のインストールが完了したら、 ``mtv()`` という関数を使って ds9 
に画像データを表示されることができます。 ::

    exposure = butler.get("calexp", dataId)
    ds9.mtv(exposure)

もし Image を使って画像を表示させると、2D の画像情報のみ表示されます。しかし、
MaskedImage か Exposure を使って画像を表示させると、mask 画像を重ねて表示してくれます。
mask 画像は色付き半透明画像として天体画像の上に表示されます。mask 画像の各色は、
以下の mask 情報に対応しています。

=================  =============
Mask Flag          Color
=================  =============
BAD                RED
CR                 MAGENTA
EDGE               YELLOW
INTERPOLATED       GREEN
SATURATED          GREEN
DETECTED           BLUE
DETECTED_NEGATIVE  CYAN
SUSPECT            YELLOW
=================  =============

``mtv()`` では表示するパラメータを追加することもできます。パラメータとしては、
タイトル, ds9 内での 'scale' パラメータ, grayscale, 拡大率, mask 画像の透明度などです。 ::

    settings = {'scale':'zscale', 'zoom': 'to fit', 'mask' : 'transparency 60'}
    ds9.mtv(exposure, frame=1, title="My Data", settings=settings)

ds9 の画像上にシンボルを重ねて表示することもできます（region file に相当）。
パイプラインでは ``dot()`` という関数で指定します。 ::

    sources = butler.get('src', dataId)
    with ds9.Buffering():
        for source in sources:
            symbol = "o"
            ds9.dot(symbol, source.getX(), source.getY(), ctype=ds9.RED, size=5, frame=1, silent=True)

利用可能なシンボルは '+', 'o', '*', 'x' です。もし楕円体を表示させたい場合は、
以下のように ``symbol`` のパラメータを "@:Ixx,Ixy,Iyy" としてください。 ::
			
    symbol = "@:{ixx},{ixy},{iyy}".format(ixx=source.getIxx(),ixy=source.getIxy(), iyy=source.getIyy())


butler で画像を読み込み、ds9 で画像を表示するまでの全過程のスクリプトが 
:ref:`showInDs9 <jp_showInDs9>` にあるので参考にしてください。