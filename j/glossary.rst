

========
用語集
========

こちらでは、パイプラインで使用する用語に関して、
その概念や詳細な情報を調べるためのリンクを簡単に紹介します。

.. glossary::

    amplifier
		HSC の 1 CCD は 4 つのアンプを介してデータを読み出しています。
		アンプは CCD のピクセル列にそってデータを読み出しており、1 CCD
		（2048 x 4096）には 4 つの 512 x 4096 アンプ領域がついています。
		各アンプの電子的な挙動はわずかに異なります。そのため、各アンプが読み込む
		4 つの CCD の領域の gain と非線形性もわずかに異なっています。
		:ref:`レイアウト <jp_hsc_layout>` は各 CCD のアンプ 1 の位置を図示しています。
    
    aperture flux
    aperture photometry
		HSC パイプラインでは様々なアルゴリズム（aperture, PSF, cmodel）
		で天体のフラックスを測定します。通常、'aperture flux' は、
		天体周囲のある 'aperture' か指定した半径（通常円形）
		内の全ピクセルのカウントの積算値として導出されます。HSC 
		パイプラインでは、基本的に同じ概念のもとピクセルのカウント値を Sinc 
		関数で補間してフラックスを計算します（Sinc アルゴリズムと言い、
		もとは SDSS で開発されたコード）。詳細は :term:`Sinc photometry <sinc flux>` 
		をご覧ください。
    
    background matching
		coadd 画像を作る際に遭遇しうる困難は、各画像の sky background 
		が全く異なる（異なる観測日による月の位置など）という点です。伝統的には 
		background をモデル化し（通常は、大きな smoothing kernel 
		で画像をなまして background 画像を作る）、coadd 画像を作る前に
		background を差し引いています。しかし、モデルの代わりに 'reference' 
		画像を用意し、background と入力画像の差を調べるという方法も考えられます。
		この方法によって入力画像の background を 'reference' 画像に一致させ、
		画像の重ね合わせを行うと、coadd 画像の S/N 比は高いけれど background は 
		0 ではないという現象が起こりえます。ゆえに、coadd の前に background
		をより正確に測定し差し引くことが重要です。    

    brighter-fatter
    brighter-fatter effect
		波長が長い側の photon の感度を上げるために、HSC で使われている CCD
		は一世代前のデバイス（~15-25 um）より厚くなっています（200 um、ちなみに
		1 ピクセルは 15 x 15 um の大きさです）。CCD デバイス中には電場が生じているのですが、
		ある CCD ピクセルのデバイスの底付近に光電子が溜まってしまうとこの電場がゆがみ、
		新たに入ってくる光電子が隣のピクセルに到着してしまうことがあります。
		この現象は明るい星で特に顕著で、brighter-fatter effect と呼ばれ、**明るい** 
		星は系統的に広い（つまり、**'フラットな'**）な PSF を持つようになります。

    Butler
		入出力データの読み出し/書き出しをパイプライン内で行うには、'butler' という tool 
		が用意されています。パイプラインで生成されたデータのリポジトリにおける場所がわからなくても、
		butler を使うと簡単にデータを読み出して情報を表示してくれます。読み込みたいデータまでの
		path、ファイル名、パイプライン内でのデータを呼び出すための構文がなくとも、
		butler の 'get' とデータを特定する dataId（frame, CCD, など）
		を使えばデータの情報を簡単に呼び込むことができます。例えば、Bias データを呼び出す時:
    
        ``biasImg = butler.get('bias', dataId)``
    
        
    CAS
    Catalog Archive Server
		この項目は SDSS で系統的に使われているもので、SDSS 
		データを取得するためにコミュニティが利用していた
		オンラインデータベースシステムを参照しています。
		このシステムを通して利用出来るデータは天体の測定結果（RA, Dec, ugriz 等級など）で、
		画像ではありません（データベースにおける画像データについては :term:`DAS`
		を参照してください）。
    
    .. todo:: perhaps a link here?
    
    ccd
		CCD は正式には charge-couple device（電荷結合素子）と言います。
		パイプラインにおける CCD は、生データか一次処理解析において参照されます。
		コマンドタスクにおける ccd の参照方法は :term:`DataId` をご覧ください。
        
    cmodel
		編集中
    
    .. todo:: ask Jim.
            
    CoaddPsf
		編集中
    
    .. todo:: ask Jim.
    	        
    DAS
    Data Archive Server
		この項目は SDSS で系統的に使われているもので、画像データを取得するための
		オンラインデータリポジトリを参照しています。パイプラインの出力（RA, Dec, ugriz 
		等級など）については :term:`CAS` をご覧ください。
        
    dataId
		観測された各ショットは 'visits' や 'frames' 名で参照されます（
		その次に参照されるのは CCD で、LSST では 'sensors' として参照されます）。
		しかし、coadd データは別の dataId で参照されます。それは 'tracts'
		（観測天域を HSC カメラの 1 視野サイズに分割したもの）と 'patches' 
		（tract を分割したもので、ほぼ 1 CCD サイズに相当）です。つまり、
		生データや一次処理用データでは 'visit' や 'CCD' が参照され、coadd データでは
		'tract' や 'patch' が参照されます。これ以外でも dataId では field 名
		（field）、観測日（dateObs）、filter 名（filter）を指定することができます。    
        
    deblend
		パイプラインで検出された天体の中には複数の天体が混合していたり、
		重なっていたりする場合があります。混合している個々の天体のフラックスを測定するためには、
		検出された天体（'親'）を '子' 天体に分離する必要があります。
    
    .. todo:: add link to explanation of deblend algorithm.
    
    deep survey
    	編集中
		
    .. todo:: 
    
    double-Gaussian
		星の PSF は 2D ガウス関数に非常によく似ていますが、外側の半径の '裾野'
		に相当する部分に多くのフラックスが検出されます。つまり、1 ガウス関数で PSF
		をモデル化するのは不十分ということです。そこで、ガウス関数を 2
		つ掛け合わせたような関数を考えてみます。1 つ目のガウス関数は PSF の中心に、
		2 つ目のガウス関数は裾野側をフィットするように配置します（典型的には、
		幅 2x、振幅 0.1x）。このようなダブルガウス関数 PSF はパイプラインでも利用できますが、
		ある redun で生成されるデータの PSF には使用できません。
    
    differencing
        編集中
    
    doxygen
		doxygen はソフトウェアグループで使用されているコードドキュメンテーションシステムです。
		ソースコードから記述されたコメントから自動的にドキュメントを生成してくれるシステムで、
		ドキュメントには開発されているコードの構造や定義などが書かれています。
		特にソフトウェア開発者用のページで、HSC の doxygen は `こちら 
		<http://hsca.ipmu.jp/doxygen/>`_ にあります。
		
    EUPS
		EUPS はソフトウェアグループで利用されているパッケージ管理システムです。EUPS
		はパイプラインのバージョンをトラックし、新しいバージョンをインストールしてくれます。
		詳細は :ref:`jp_back_eups` をご覧ください。
		        
    extendedness (classification.extendedness)
		extendedness はパイプライン内で測定される天体の測定値の 1 つです。
		出力される値は float 型で、星/銀河を分離するための flag で利用されています
		（0 = 星、1 = 銀河 ... 銀河のほうが星より '広がって' いる）。
    
    flag
		パイプラインで生成される測定値や、問題のあるピクセルや測定値は 'flag'
		としてパイプラインから出力されるカタログに記録されています。例えば、こうした flag
		情報は ``flags_pixel_edge`` や ``flags_pixel_interpolated_any``
		としてカタログ内に記載されています。出力データに含まれるパラメータを
		`こちら <http://hsca.ipmu.jp/hscsoft/datainfo.php>`_ に一覧にしていますので、
		ご覧ください。        
        
    footprint
		検出された天体を占めるピクセル領域をソフトウェアグループでは 'footprint'
		と呼んでいます。footprint 内のピクセルが天体の測定に使われます。
    
    forced measurement
		coadd 画像では、入力した coadd 画像や他の filter の coadd 画像において
		5σ 限界より暗い天体を検出することができます。例えば、i-band の coadd 
		画像で検出された天体があったとします。他 band では天体が検出されていなくても、
		この天体と同じ位置でフラックスを測定すればいいわけです。このような解析をパイプラインでは
		'forced measurement' と呼んでいます。
    
    frame
		全 CCD を含んだ全ショットを frame と言います。これは観測所で EXP-ID
		として登録されます。ソフトウェアグループでは LSST の慣習を倣って 'visit' 
		と呼んでいます。

    FRAMEID
		すばる望遠鏡で使用される 1 ショットの名前で、``<4-char><8-digit>``
		という形式で使用されています。詳細は :ref:`jp_data_format` をご覧ください。

    healpix
		HealPix は天文業界でよく利用されている天域を分割する方法です。
    
    .. todo:: We support this, but I don't know of anywhere where we're currently using it.
    
	
    HSM
    Hirata-Seljak-Mandelbaum
		HSM は、Chris Hirata, Uros Seljak, Rachel Mandelbaum によって作られた
		天体の形を測定するアルゴリズムをコード化しまとめたパッケージです。パッケージには
		'KSB' (HSM_KSB), 'regaussianization' (HSM_REGAUSS), 'Bernstein-Jarvis'
        (HSM_BJ), 'linear' (HSM_LINEAR), 小さな形をもとにしたアルゴリズム
        (HSC_SHAPELET) などが含まれています。これは HSC 
		パイプラインのデフォルトで測定されています。
    
    Kron flux
        編集中
              
    .. todo:: write this.
    
    KSB
        編集中
        
    .. todo:: Do we need this?  Out of scope for this glossary?
    
    
    mosaic
		mosaic は HSC パイプラインの中における uber-calibration を行う mosaic.py 
		と同じ意味で、異なる visit での測光を同一の測光システムにして処理することを言います。
    
    multifit
        編集中
    
    .. todo:: ask jim.
    
    multishapelet
        編集中
    
    .. todo:: ask jim.
    
    object
		ソフトウェアグループでは、特に、自分たちが測定したい天体を object と呼んでいます。
		一方 'source' はある object がある観測時間での場合を言います。例えば、星は
		'object' ですが、この星の 2 ショット分のデータからは 2 つの 'sources' が得られます。
    
    patch
        :term:`DataId` をご覧ください。
    
    
    peak
		:term:`天体の分離 <deblend>` 過程では、個々の天体は :term:`footprint`
		として認識されます。footprint のうち最もカウント値が大きなピクセルは、
		各 '子' 天体のピークになります。        
    
    Petrosian flux
        編集中
        
    .. todo:: ask rhl.
    
    pipeline
		入力データを解析処理するコードを集めたソフトウェア。最終的には、
		画像データと出力カタログを生成されます。
        
    PSF
    point spread function
		PSF とは '点源' やデルタ関数に対する応答関数のことです。この関数には、
		大気、望遠鏡、カメラによる影響が含まれます。PSF は画像における位置の関数で、
		時間で変動します。
    
    PSF flux
    PSF photometry
		aperture photometry ではある天体周囲の積算したフラックスで計算されますが、
		PSF photometry は画像内の天体周囲の PSF を重みとした *重み付き* フラックスです。
		もし測定したい天体自体が点源（例えば星）であった場合、この測定方法は非常に適しているでしょう。
    
    PSF-Ex
		Emmanuel Bertin によって開発された PSF モデルライブラリ。HSC
		パイプラインの中では PSF-Ex が PSF flux の測定で使用されています。
    
    raft
		'raft' は LSST カメラの CCD 構造の 1 セットの呼び名です。
		LSST カメラ（HSC *ではありません*）は 3 x 3 の 9 個の CCD を 1 セットとした
		'raft' が 21 個集まった構造をしています（つまり、CCD の枚数は 9 x 21 = 189 枚）。
		HSC カメラの構造は LSST と全く異なりますが、パイプラインは LSST 
		パイプラインをベースにしているので、raft という言葉を聞く機会はあるかもしれません。
		    
    rerun
		``rerun`` という概念はもともと SDSS のデータ解析で使用されていたものです。
		単純には、同じパラメータセット, パイプラインのバージョンでのデータ処理を 1 つの
		rerun とみなします。ある 'rerun' では、一連解析方法でデータを取り扱うことを意味します。    
    
    schema
		schema（スキーマ）はデータベースの構造のことで、データがどのように格納されているかを記す
		青写真のようなものです。どの field がどの table に格納されていて、
		どのような種類のデータが含まれているか、スキーマの中には記述されています。

		HSC データベースでは PostgreSQL を使用しており、postgreSQL における
		'スキーマ' は特別な意味を持っています。PostgreSQL では、
		1 データベース内の論理データベースを 'スキーマ' と呼んでいます。
            
    sensor
		'sensor' は LSST カメラの 'raft' 内の 1 CCD を指します。つまり、
		1 raft をなす 9 個の CCD が 'sensor' です。
    
    sinc flux
    sinc photometry
        編集中
    
    skymap
        編集中
    
    Sloan swindle
        編集中
        
    source
        編集中
        
    SSP
        :term:`Strategic Survey Proposal (SSP)` をご覧ください。
    
    stack
		（HSC パイプラインでは）パイプラインで coadd, warp 
		を行うタスクの総称のことを stack と言います。
	
    stack
		（画像の重ね合わせでは）coadd の別名のことを stack と言います。
    
    Strategic Survey Proposal (SSP)
        編集中
        
    TAN-SIP
        編集中
        
    Task
		各パイプラインの解析処理が含まれるソフトウェアのクラスを 'Task' と言います。
    
    tract    
        :term:`DataId` をご覧ください。
    
    uber-calibration
		uber-calibration は、元々、SDSS 
		のデータ解析において全観測データを単一の測光システムにするために開発された解析手法です。
		この手法は、複数のショットで同じ天体を撮るような観測に有効です。uber-calibration
		における補正項は異なる観測ショットの天体の測定結果を比較して調整される。HSC
		パイプラインにおける uber-calibration は 'mosaic' で実行されます。
    
    .. todo:: put a ref to Nikhil's paper.
        
    ultra-deep survey
        編集中
    
    
    visit
        :term:`DataId` をご覧ください。
    
    warp
		stack データ（coadd 画像）を生成するには、
		全ての入力画像は共通のピクセルグリッドにリサンプルしなくてはいけません。
		この解析処理過程は warping と呼ばれています。
	
    WCS
    World Coordinate System
        編集中
    
    wide survey
        編集中
    
    
    
    
    
    
    
    
    
    
    
    
