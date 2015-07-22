.. _j_data_repo:

.. highlight::
	bash

====================================================
データリポジトリ -- 解析するデータの置き場所
====================================================

HSC パイプラインでデータを解析するためには、
最初にすべてのデータを決まったディレクトリツリーの配下に置かなければなりません
（ **超重要！** ）。

このデータ配置の構造は、データリポジトリと呼ばれます。
この構造は、パイプラインのバージョンに依存して変更される可能性もあるので、
自身でディレクトリを作成するよりは、
パイプラインに同梱されるコマンドを使ってリポジトリを設定するほうが安全です。

データレポジトリという構造や概念は、あくまでも HSC パイプラインを用いて解析する際に必要なデータの設置方法で、
ファイルのパスを直接指定してデータ解析をするスクリプトを自身で準備する場合には必要ありません。


.. _jp_data_format:

データフォーマット
---------------------

1 ショットの HSC データには 2048 × 4176 (trimmed) ピクセルの CCD が 112 枚含まれており、
うち 8 枚はフォーカス合わせ用、残り 104 枚がサイエンスユース用となっています。

生データの名前
^^^^^^^^^^^^^^^^^^

すばる望遠鏡で取得されたは生データには 4 文字 + 8 数字 で構成される **FRAMEID**
と呼ばれるデータ名を付ける慣習があります。HSC で取得されたの各 CCD 生データは
``HSC<1-文字><8-数字コード>.fits`` という名前の fits データとして出力されます。
1-文字系列は現在 'A' が割り当てられていますが、将来的には 'B', 'C' と変化していきます。
8-数字コードは以下のようなルールのもとに命名されています。

* 下 2 桁は CCD 番号を表す。 ``00 - 99`` では 112 枚の CCD 分を対応できないため、HSC カメラは 56 個の '偶数' と '奇数' 番号のデバイスに分けられている（:ref:`CCD のレイアウト <jp_hsc_layout>` か、国立天文台の `CCD 配置図 <http://www.naoj.org/Observing/Instruments/HSC/CCDPosition_20140811.png>`_ を参照）。

* 生データの CCD ID は ``00`` から ``57`` の 56 枚割り当てられている。ただし、ID 49, 50 はない（生データ ID 49, 50 の位置には読み出し系統が異なるオートガイダー用 CCD が配置されている）。

* 下 3 桁目の数（偶数/奇数）は、カメラ面内でどこのデバイス上にいるかを表している。

* HSC のショット数（LSST の解析システム内では 'visit' ）は偶数番目で表す。

例えば、100, 102 という visit 番号の生データのファイル名は次のようになります。::

     Visit 100 偶数:  HSCA00010000.fits - HSCA00010057.fits
     Visit 100 奇数:  HSCA00010100.fits - HSCA00010157.fits
     
     Visit 102 偶数:  HSCA00010200.fits - HSCA00010257.fits
     Visit 102 奇数:  HSCA00010300.fits - HSCA00010357.fits

これら生データがリポジトリの中に配置されると、``HSC-<7-数字 visit>-<3-数字 CCD>.fits`` 
という新しいファイル名が付与されます。例えば、上記の生データは以下のような名前に置き換えられます。::

    Visit 100 偶数と奇数:  HSC-0000100-000.fits - HSC-0000100-111.fits 
    Visit 102 偶数と奇数:  HSC-0000102-000.fits - HSC-0000102-111.fits

データ名が生データとリポジトリ内で変更することや、生データが visit +
偶数/奇数の組み合わせになっていることを覚えておくと、
今後データを整理する際に役立つでしょう。


データ量
^^^^^^^^^^

生データの 1 ピクセルには 16 bit のデータが格納されているため、
1 CCD の生データは約 18 MB のデータ量になります。CCD は 112 枚あるので、
1 ショットで約 2 GB のデータ量となります。処理済み画像データの 1 ピクセルには
32-bit の整数データと 32-bit の画像データ、16-bit の flag 画像データが含まれており、
1 ピクセルの容量は 80-bit になります。最終的に、1 CCD の解析データは約 82 MB、
1 ショットの解析データは約 11 GB にもなります。
どの程度のディスク容量が HSC パイプラインの処理で必要になるかを以下に簡単にまとめます。


========================   ==================
Data                       Size
========================   ==================
1 raw CCD                  18 MB
1 raw exposure             2 GB  (112 CCDs)
1 processed CCD            82 MB
1 processed Exposure       11 GB (104 CCDs)
1 CCD's catalog            ~10MB - 30MB
1 exposure's catalogs      1-2 GB
**1 CCD (raw+proc+cat)**   **100 MB**
**1 exp (raw+proc+cat)**   **13 GB**
========================   ==================

.. =====================================  ==================
   データ                               サイズ
   =====================================  ==================
   生データ 1 CCD                       18 MB
   生データ 1 ショット                 2 GB  (112 CCDs)
   解析処理後 1  CCD                   82 MB
   解析処理後 1 ショット              11 GB (104 CCDs)
   1 CCD のカタログファイル            ~10MB - 30MB
   1 ショットのカタログファイル      1-2 GB
   **1 CCD (生＋処理済＋カタログ)**  **100 MB**
   **1 exp (生＋処理済＋カタログ)**  **13 GB**
   ====================================   ==================

   
.. _jp_ingest:

データレポジトリの作成とデータの配置
--------------------------------------------

HSC パイプラインには、データレポジトリ作成用のコマンドが同梱されています。
このコマンドは ``HSC*.fits`` ファイルを収集して、
パイプライン指定のディレクトリ配下に移動し、
sqlite3のデータベースに情報を格納するまでを一度に行います。
また、ファイルをコピーすることによるディスク容量の圧迫を防ぐため、
シンボリックリンクによるファイル配備にも対応しています。
コマンドの実行方法は以下の通りです。ただし、HSC パイプラインの実行に必要な 
EUPS `setup` （S14A_0ならば、setup hscPipe 2.12.4d_hsc）は完了しているとします。::

    # データリポジトリのためのディレクトリの作成（raw data のための root directory のようなもの）
    $ mkdir /data/Subaru/HSC

    # '_mapper' という名前のファイルをデータリポジトリディレクトリに作成
	# ファイル中には以下の文字列を記述する（解析対象の装置を指定しているが、通常はHSCです）
    $ echo lsst.obs.hsc.HscMapper > /data/Subaru/HSC/_mapper

    # データリポジトリに初めてデータ配置する
	# 例では、ファイルを移動するのでなくシンボリックリンクを作成している
    $ hscIngestImages.py /data/Subaru/HSC --create --mode=link /path/to/rawdata/HSCA*.fits

    # データリポジトリにデータを配置する（2 回目以降）
	# すでに配置されたデータがある場合を想定
    $ hscIngestImages.py /data/Subaru/HSC --mode=link /path/to/rawdata/HSCA*.fits

    
上記のコマンドを実行すると、/data/Subaru/HSC/ 以下に `_mapper` ファイル
と生データの fits ファイルが置かれたのが分かるでしょう。各データは、FITS ヘッダの OBJECT 
キーワードにもとづいて決められた名前のディレクトリ以下に置かれます（例 M87）。また、
その下に、DATE-OBS と FILTER01 から得られた値を元に、それぞれ pointing と filter
と呼ばれるディレクトリ階層が作られます。
ここで、ファイル名が少し変更を受けているのに気づくと思います。
この変更は、パイプライン内でのファイルの取り扱いの都合によるもので、
'HSC-%07d-%03d.fits' というフォーマットになっています。ここで、`%07d` の部分は
visit（ショット番号）を表します。STARS　内のオフィシャルの生データは 'HSCA%08d.fits' 、
つまり `HSCA` という接頭子を持ちますが、実はこの最後の `A` は将来的に
8 桁の数字を使い切った後、`B`,`C`, ... とインクリメントする可能性が高いため、
パイプライン内のファイル名では予めこの状況に対応するため、`%07d` の先頭一桁目を 
`A-->0`, `B-->1`, ... のように整数を割り当てています。最後の `%03d` の部分は、
CCD 番号を表しており、FITS ヘッダの DET-ID と完全に一致するものです。
最後に、このディレクトリに置かれた sqlite3 ファイル、つまり sqlite3 
のデータベースファイルのことを、'registry'（レジストリファイル）と呼んでいます。

生データを配置した直後の様子は以下のようになっています。::

    $ tree /data/Subaru/HSC
    /data/Subaru/HSC/
    |-- M87
    |   `-- 2015-12-21
    |       `-- 00999
    |           `-- HSC-I
    |               `-- HSC-0001000-055.fits -> /data/work/rawdata/HSCA09870000.fits
    |-- _mapper
    `-- registry.sqlite3


ほとんどのユーザーにとってはここまでで述べたお膳立てが重要です。もう少し細かく説明すると、
hscIngestImages.py が行う操作は 2 ステップに分かれています。:
(1) 生データを指定のデータリポジトリ配下にコピーする（またはリンクを作る）。
(2) レジストリファイルにそれらファイルの情報を登録する。  
つまり、(2) のレジストリファイルの DB エントリーだけを追加したいのであれば、
``--mode=skip`` というオプションを追加することで実現出来ます。
以下では、OBJECT=``M31`` というデータがすでにリポジトリディレクトリにある場合のコマンドです。::

    # レジストリファイルへのDB登録だけ行う
    $ hscIngestImages.py /data/Subaru/HSC/ --mode=skip /data/Subaru/HSC/M31/2013-03-21/00100/HSC-I/HSC-*fits

.. _jp_registryinfo:

レジストリに含まれる情報
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

レジストリ（データベース）ファイルには、
その 1 行ごとに投入された生データについての情報が含まれています。その情報には、
``registryInfo.py`` コマンドを使ってクエリ（検索）を投げることが出来ます。
パイプラインの多くの解析ステージで、入力データを同定するために、
visit 番号であったり frameId を知る必要がありますが、 ``registryInfo.py``
を使うとこのような詳細な情報を探すことが出来ます。 ::

    # 例）HSC-Iで取られた全てのCOSMOSデータリストを得る    
    $ registryInfo.py /data/Subaru/HSC/registry.sqlite3 --field COSMOS --filter HSC-I
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112
    ...
    
第一引数のリポジトリのあるディレクトリへのパスを省略するために、
SUPRIME_DATA_DIR という環境変数に予め値を入れておく方法もあります::

    $ export SUPRIME_DATA_DIR=/data/Subaru/HSC

    # こうしておくと、registryInfo.py は、第一引数がない場合にこの変数値を registry.sqlite3 のあるディレクトリとみなす

    $ registryInfo.py --field COSMOS --filter HSC-I
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112
    ...

    $ registryInfo.py --visit 1234
    
    filter  field                   dataObs expTime pointing  visit nCCD
    HSC-I   COSMOS               2015-01-20   240.0     0001   1234  112

    
Rerun ディレクトリの構造
----------------------------------------

解析を進めるには、結果ファイルを探すためにディレクトリ階層について
知る必要があります。
予備知識の節で述べたように、HSCパイプラインでは、データ処理の各バッチの単位を
``rerun`` と呼んでいます。新しい rerun は、データリポジトリ配下に、
既存のものとは別の ``rerun`` ディレクトリとして作られます。  
フル解析の流れはいくつものステージで構成されますが、おおまかには
シングルフレーム処理（visit単位の解析）と coadd処理（モザイク-Coadd 以降）
に分かれます。
それぞれの処理の結果ファイルの一部は、それぞれの処理の次の入力としても使われます。


処理結果ファイル
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. coaddも載せてあり、英語版と少し変えている。

ここでは、``test`` という名前の rerun の例について、
シングルフレームおよび coadd の処理結果ファイルをリストアップしてみます。
ここでは、リストを明解にするために、フィルターやトラクト、パッチといった階層の
例をひとつだけを示していますが、実際には、複数のフィルターなどのディレクトリやファイルが並びます::

    /data/Subaru/HSC/rerun/test/ rerunディレクトリ   
    |
    |- _parent --> /data/Subaru/HSC リポジトリディレクトリへのリンク
    |
    |- config/ 解析パラメータ
    |    |- processExposure.py 解析パラメータ
    |    |- mosaic.py          
    |    |- stacker.py
    |    |- forcedPhotCoadd.py
    |    |- forcedPhotCcd.py
    |    |- eups.versions      解析ソフトバージョン
    |    |
    |
    |- schema/ カタログ構造定義
    |    |- src.fits           カタログスキーマ
    |    |- icSrc.fits         カタログスキーマ
    |    |
    |
    |- 00817/ 観測エポック（MJD相当）
    |    |- HSC-I/ フィルター
    |         |- thumbs/ CCDサムネイル画像用
    |         |    |- oss-0000999-[000-103].png
    |         |    |- flattened-0000999-[000-103].png
    |         |
    |         |- output/ CCDカタログ出力用
    |         |    |- ICSRC-0000999-[000-103].fits  較正に使う浅い天体カタログ
    |         |    |- MATCH-0000999-[000-103].fits  較正に使うマッチリスト
    |         |    |- ML-0000999-[000-103].fits     MATCHの内容をカラムに展開したもの
    |         |    |- SRC-0000999-[000-103].fits    CCD単体で検出した最終カタログ
    |         |    |- SRCMATCH-0000999-[000-103].fits SRCと較正に使った外部カタログをマッチしたもの
    |         |    |- SRCML-0000999-[000-103].fits    SRCMATCHの内容をカラムに展開したもの
    |         |    |
    |         |    |- 9369/ Tract番号
    |         |    |    |- CALSRC-0000999-[000-103].fits モザイクによるwcs, fcrをSRCに反映したもの
    |         |
    |         |- qa/  CCDデータ評価用
    |         |    |- magHist-0000999-[000-103].png  シーイング用星選択に使う天体個数分布
    |         |    |- seeingRough-0000999-[000-103].png  シーイング測定途中経過
    |         |    |- seeingRobust-0000999-[000-103].png シーイング測定図
    |         |    |- seeingMap-0000999-[000-103].png    星状天体のFWHM天体ごと
    |         |    |- fwhmGrid-0000999-[000-103].png     星状天体のFWHMグリッドごと
    |         |    |- ellipseMap-0000999-[000-103].png   星状天体の伸び具合の楕円天体ごと
    |         |    |- ellipseGrid-0000999-[000-103].png  星状天体の伸び具合の楕円グリッドごと
    |         |    |- ellipticityMap-0000999-[000-103].png  whisker plot
    |         |    |- ellipticityGrid-0000999-[000-103].png 上記のグリッドごと 
    |         |    |- ellPaGrid-0000999-[000-103].fits   星状天体の伸びの方向グリッドごと
    |         |    |- psfSrcGrid-0000999-[000-103].fits  グリッドごとの星状天体スタック 
    |         |    |- psfModelGrid-0000999-[000-103].fits グリッドごとのPSFモデル
    |         |    |- psfSrcGrid-0000999-[000-103].png   上記のpng版
    |         |    |- psfModelGrid-0000999-[000-103].png 上記のpng版
    |         |    |- seeingMap-0000999-[000-103].txt    星状天体の測定結果リスト 
    |         |    |- seeingGrid-0000999-[000-103].txt   星状天体の測定結果グリッドごと
    |         |
    |         |- corr/ 1ショット1CCD単位での処理済画像およびモザイクのCCDごとの結果用
    |         |    |- BKGD-0000999-[000-103].fits スカイ引きパターン
    |         |    |- CORR-0000999-[000-103].fits  較正済CCD画像
    |         |    |
    |         |    |- 9369/ トラクトごとのモザイク結果
    |         |    |    |- wcs-0000999-[000-103].fits  モザイクにより決まったWCS
    |         |    |    |- fcr-0000999-[000-103].fits  モザイクにより決まったflux scaleと補正パターン
    |         |         |- CALEXP-0000999-[000-103].fits モザイクによるwcs, fcrをCORRに反映したもの
    |         |
    |         |- processExposure_metadata/ CCD解析途中の出力（サイエンスには不要）
    |         |    |- 0000999.boost 
    |         |
    |         |- tract9369/ トラクトごとのforced photometry
    |         |    |- FORCEDSRC-0000999-[000-103].fits モザイクカタログ位置でのCCD画像のforced photometry
    |         |    |- forcedPhotCcd_metadata/ 通常不要
    |         |         |- 0000999-[000-103].boost  forced CCD測定のメタ情報
    |  
    |- deepCoadd/ warpとcoadd画像
    |    |
    |    |- skyMap.pickle トラクトの定義
    |    |
    |    |- HSC-I/ フィルター
    |    |    |- 9369/ トラクトごとのcoadd
    |              |- 0,8/ パッチごとのワープ
    |              |    |- warp-HSC-I-9369-0,8-999.fits パッチごとのワープ画像
    |              |
    |              |- 0,8.fits パッチごとのcoadd画像
    |     
    |- metadata/ トラクトのメタ情報
    |    |- metadata/deep_makeSkyMap.boost トラクト作成のメタ情報
    |    | 
    |
    |- deepCoadd-results/ coaddカタログと関連ファイル
    |    |- HSC-I/ フィルター
    |    |    |- 9369/ Tract番号
    |              |- 0,8/ パッチごとのカタログ作成処理結果
    |              |    |- icSrc-HSC-I-9369-0,8.fits   マッチングに使う浅い天体カタログ
    |                   |- icMatch-HSC-I-9369-0,8.fits icSrcと位置較正カタログをマッチしたもの
    |                   |- bkgd-HSC-I-9369-0,8.fits    スカイ引きパターン
    |                   |- calexp-HSC-I-9369-0,8.fits  スカイ引き済のカタログ生成用coadd画像
    |                   |- srcMatch-HSC-I-9369-0,8.fits srcとマッチングに使った外部カタログをマッチしたもの
    |                   |- src-HSC-I-9369-0,8.fits     singleバンドcoaddで検出した天体カタログ
    |                   |- srcMatchFull-HSC-I-9369-0,8.fits SRCと位置較正カタログをマッチしたもの
    |                   |- forced_src-HSC-I-9369-0,8.fits referenceバンドのcoaddカタログの各ソースの
    |                                                     位置で測定した天体カタログ
    |
    |- deepCoadd_forcedPhotCoadd_metadata/ 通常不用force測定のメタ情報
    |    |- HSC-I/ 
    |    |    |- 9369/ Tract番号
    |              |- 0,8.boost forced Coadd測定のメタ情報
    |

..    /data/Subaru/HSC/rerun/test/    
..   \ |-- 00100                                         The pointing （epochに相当; MJDから生成）
..    |   `-- HSC-I                                     The filter 
..    
..    |       |-- corr                                  Corrected frames
..    |       |   |-- BKGD-0000999-050.fits             The background (not easily readable)
..    |       |   `-- CORR-0000999-050.fits             The corrected image
..    
..    |       |-- output                                Output data (i.e. measurements)
..    |       |   |-- ICSRC-0000999-050.fits                
..    |       |   |-- MATCH-0000999-050.fits            Objects matched to catalog sources
..    |       |   |-- ML-0000999-050.fits                   
..    |       |   |-- SRC-0000999-050.fits              Measurements on sources
..    |       |   |-- SRCMATCH-0000999-050.fits             
..    |       |   `-- SRCML-0000999-050.fits
..    
..    |       |-- processCcd_metadata                   pipeline internals
..    |       |   `-- 0000999-050.boost
..    
..    |       |-- qa                                    Quality Assurance data and figures
..    |       |   |-- ellPaGrid-0000999-050.fits
..    |       |   |-- ellipseGrid-0000999-050.png
..    |       |   |-- ellipseMap-0000999-050.png
..    |       |   |-- ellipticityGrid-0000999-050.fits
..    |       |   |-- ellipticityGrid-0000999-050.png
..    |       |   |-- ellipticityMap-0000999-050.png
..    |       |   |-- fwhmGrid-0000999-050.fits
..    |       |   |-- fwhmGrid-0000999-050.png
..    |       |   |-- magHist-0000999-050.png
..    |       |   |-- psfModelGrid-0000999-050.fits
..    |       |   |-- psfModelGrid-0000999-050.png
..    |       |   |-- psfSrcGrid-0000999-050.fits
..    |       |   |-- psfSrcGrid-0000999-050.png
..    |       |   |-- seeingGrid-0000999-050.txt
..    |       |   |-- seeingMap-0000999-050.png
..    |       |   |-- seeingMap-0000999-050.txt
..    |       |   |-- seeingRobust-0000999-050.png
..    |       |   `-- seeingRough-0000999-050.png
..    |       `-- thumbs                                Thumbnail figures
..    |           |-- flattened-0000999-050.png
..    |           `-- oss-0000999-050.png
..    
..   \ |-- _parent -> /data/Subaru/HSC                   A link back to the root of the data repo
..    
..   \ |-- config                                        Parameters specific to this rerun
..    |   |-- eups.versions                             Package versions (file~1 contains clobbered versions)
..    |   `-- processCcd.py                             Configuration parameters (file~1 contains clobbered parameters)
..    
..    `-- schema
..       \ |-- icSrc.fits
..        `-- src.fits
..
..
..
.. The Coadd outputs
.. ^^^^^^^^^^^^^^^^^


mosaic 処理の出力
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

reduceFrames.py による各 CCD の一次処理の後で、``mosaic.py``
によって全ショットに対するより精密な座標決めや原点等級決め（'uber-calibration'）
が行われます（詳細は :ref:`jp_mosaic` 参照）。この過程では各 tract 内の各 CCD 
に新たに 2 つのファイルが追加されます。これらのファイルは ``corr/<TRACT>`` 
ディレクトリ下に生成されます。例えば、'0000' の tract で、1236, 1238 の visit
番号のデータに mosaic 処理を実行したとします。
その場合のコマンド実行後のディレクトリ構造は以下の通りです。::

    /data/Subaru/HSC/rerun/test/
    `-- 00100                                         # ポインティング
        `-- HSC-I                                     # フィルター名
            `-- corr
                `-- 0000
                    |-- fcr-0001236-050.fits          # 全 visit から見積もられた測光情報の補正ファイル
                    |-- fcr-0001238-050.fits
                    |-- wcs-0001236-050.fits          # 全 visit から見積もられた座標決めファイル
                    `-- wcs-0001238-050.fits


Coadd による出力
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

coadd 出力は ``stack.py`` によって生成されます（:ref:`Coadd Processing <coadd_proc>` 参照）。
出力データはリポジトリ内の ``deepCoadd/`` と ``deepCoadd-results/``
ディレクトリ下に生成されます。以下に、この 2 つのディレクトリ構造をお見せします。
coadd による解析は ``stack.py`` の中で処理されていますが、
その中のサブプロセスの解析過程は独立に実行され、各解析過程でデータが出力されます。

以下の例では HSC-I の 1228, 1238 の visit 番号の HSC SSP データに対する
``stack.py`` の実行結果を示しています。ここでは、1,1 というある patch 
データの出力を示していますが、他全ての patch に対し同様の形式でデータが生成されます
（基本的には patch ID は 10,10 までですが、SkyMap で定義した tract
のサイズによって patch の数は変わります）。

coadd における最初の処理は SkyMap を生成することです。SkyMap 
は入力した画像の座標系を最終 coadd 処理のために使用する座標系に変換する（warp）
ために用いられます。この処理での出力は ``deepCoadd/`` ディレクトリに格納されます。
 
::

    $ tree /data/Subaru/HSC/rerun/myrerun/deepCoadd/
    /data/Subaru/HSC/rerun/myrerun/deepCoadd/
    |-- HSC-I
    |   `-- 0
    |       |-- 1,1
    |       |   |-- warp-HSC-I-0-1,1-1228.fits        # visit ID 1228 のデータを tract/patch = 0/1,1 用に座標変換したデータ
    |       |   `-- warp-HSC-I-0-1,1-1238.fits        # visit ID 1238 のデータを tract/patch = 0/1,1 用に座標変換したデータ
    |       `-- 1,1.fits                              # 全 tract/patch = 0/1,1 の warp 画像を coadd 処理したデータ
    `-- skyMap.pickle                                 # skymap
 
coadd 処理によって生成された画像（上記ディレクトリ構造例の ``1,1.fits`` 画像）
のカタログファイルは ``deepCoadd-results/`` ディレクトリに格納されています。
メインの天体カタログは ``src-HSC-I-0-1,1.fits`` です。

::

    $ tree /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    `-- HSC-I
        `-- 0
            `-- 1,1
                |-- src-HSC-I-0-1,1.fits              # tract/patch 0/1,1 内のカタログファイル
                |-- srcMatch-HSC-I-0-1,1.fits
                `-- srcMatchFull-HSC-I-0-1,1.fits


マルチバンド解析の出力
^^^^^^^^^^^^^^^^^^^^^^^^^^^

異なる filter での coadd の結果から、全 filter で一致したカタログを生成するコマンドが
``multiBand.py`` です。以下では HSC-I と HSC-R のディレクトリを示しています。

``stack.py`` と同様に、``multiBand.py`` の中でも各処理段階毎に異なるプロセスが走っています
（:ref:`jp_multiband_proc` 参照）。各処理は独立に実行され、
その段階毎に中間生成ファイルが出力されます。以下ではその全てのファイルを表示しています。
もし ``multiBand.py`` をデフォルトのパラメーターで実行すると、
以下の例にある ``detectMD-*`` と ``measMD-`` ファイルは生成されませんのでご注意ください。

::

    $ tree /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    /data/Subaru/HSC/rerun/myrerun/deepCoadd-results/
    |-- HSC-I
    |   `-- 0
    |       `-- 1,1
    |           |-- bkgd-HSC-I-0-1,1.fits             # detectCoaddSources.py
    |           |-- det-HSC-I-0-1,1.fits              # detectCoaddSources.py
    |           |-- detectMD-HSC-I-0-1,1.boost        # detectCoaddSources.py      (multiBand.py ではない)
    |           |-- forced_src-HSC-I-0-1,1.fits       # forcedPhotCoadd.py
    |           |-- meas-HSC-I-0-1,1.fits             # measureCoaddSources.py
    |           |-- measMD-HSC-I-0-1,1.boost          # measureCoaddSources.py     (multiBand.py ではない)
    |           `-- srcMatch-HSC-I-0-1,1.fits         # measureCoaddSources.py
    |-- HSC-R
    |   `-- 0
    |       `-- 1,1
    |           |-- bkgd-HSC-R-0-1,1.fits             # detectCoaddSources.py
    |           |-- det-HSC-R-0-1,1.fits              # detectCoaddSources.py
    |           |-- detectMD-HSC-R-0-1,1.boost        # detectCoaddSources.py      (multiBand.py ではない)
    |           |-- forced_src-HSC-R-0-1,1.fits       # forcedPhotCoadd.py
    |           |-- meas-HSC-R-0-1,1.fits             # measureCoaddSources.py
    |           |-- measMD-HSC-R-0-1,1.boost          # measureCoaddSources.py     (multiBand.py ではない)
    |           `-- srcMatch-HSC-R-0-1,1.fits         # measureCoaddSources.py
    `-- merged
        `-- 0
            `-- 1,1
                |-- mergeDet-0-1,1.fits               # mergeCoaddDetections.py
                `-- ref-0-1,1.fits                    # mergeCoaddMeasurements.py



