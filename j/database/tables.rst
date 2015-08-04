.. _jp_tables_intro:

===================================
HSC SSP データベースのテーブル
===================================

はじめに
---------------
HSC データには 2 種類のデータベーステーブルがあります。
1 つは画像データのメタ情報を含むデータベースで、データベースには、
パイプラインの解析で生成された 'calexp' や 'deepCoadd_calexp'
のような画像データの観測時間、filter 名、WCS 座標、
画像の測定結果（seeing、原点等級など）が格納されています。一方、もう 1 
つのデータベースは天体のカタログ情報を含むデータベースで、
'src-' や 'match-' fits ファイルのように、
パイプライン解析で生成された FITS BINTABLE から情報が抽出されています。

以下で HSC データベースに含まれているテーブルの中身を紹介します。


画像メタデータのテーブル
-------------------------
テーブルの中身は、各データの FITS ヘッダーから読み出されています。テーブルは FITS
フォーマットの形式で、観測日（date-obs）、filter 名、露出時間、WCS 座標、
seeing、原点等級など、データベースから FITS データを探す際の情報が記述されています。

================= =========== ============================================== ====== =====
Table Name        FITS Data   Description                                     Mng   HPX11
================= =========== ============================================== ====== =====
**frame**         CORR        Reduced CCD image                                O      O
**calibframe**    CALEXP      Mosaic Corrected Reduced CCD image               O      O
**exposure**      metaQaExp   Exposure meta information                        O
**wcs**           wcs         wcs file output by mosaicking                    O
**fcr**           fcr         flux correction by mosaicking                    O
**warped**        warp        warped image for one exposure(visit) per patch   O      O
**mosaic**        calexp      coadd image                                      O      O 
**mosaicframe**               set of (visit,ccd) which consist of coadd                  
================= =========== ============================================== ====== =====

..	================= =========== ============================================== ====== =====
	テーブル名          FITS データ  コメント                                        Mng	HPX11
	================= =========== ============================================== ====== =====
	**frame**         CORR        一次処理済 CCD 画像                               O      O
	**calibframe**    CALEXP      mosaic 処理済（等級原点、座標決定済） CCD 画像       O      O
	**exposure**      metaQaExp   1 ショットメタ情報                                O
	**wcs**           wcs         mosaic.py で生成される WCS 補正ファイル             O
	**fcr**           fcr         mosaic.py で生成されるフラックス補正ファイル         O
	**warped**        warp        1 patch 1 ショット（visit）の warp 画像            O      O
	**mosaic**        calexp      coadd 画像                                      O      O 
	**mosaicframe**               coadd 画像に含まれる (visit,ccd) セット                  
	================= =========== ============================================== ====== =====

どのテーブルにも 'mng' テーブルというファイル管理情報（ファイルパス、
プロポザール ID、データ転送日等）を含んだテーブルファイルが添付されています。
例えば、'frame' テーブルの管理情報テーブルは 'frame_mng' です。また、
'**frame**', '**calibframe**', '**warped**', '**mosaic**' 
テーブルには 'hpx11' テーブルというテーブルファイルも添付されます。
'hpx11' テーブルファイルには観測天域をカバーするような HEALPix の 11 
次の変数リストが含まれます。例えば '**frame**' テーブルの 'hpx11' テーブルは 
'**frame_hpx11**' です。これらテーブルは、観測天域、seeing、transparency、
filter 名、観測日等の様々なメタ情報をもとにした FITS データの検索に使われます。


カタログデータのテーブル (2014.07.01 現在)
-----------------------------------------
カタログ情報を含むデータベースは、FITS BINTABLE にある全てのカラムの値を抽出し、
データベースに同じ名前のカラムとして格納するよう設計されています。この設計により、
データベースでのカラム名を変えたり短くしたりすることで生じうる FITS BINTABLE
とデータベース間のカラムの混同を避けることができます。
FITS データ内のいくつかのアレイはデータベース内で複数のカラムに分けられます
（例 天球面座標）。また、FITS データで bits 形式で格納されていた flag 情報は
boolean 型のカラム（true/false の 2 値をとるデータ型）としてデータベースに格納されます。

=========================== ============== ====================================================== ===== =====
Table Name                  FITS Data      Description                                            Photo Coord
=========================== ============== ====================================================== ===== =====
**frame_sourcelist**        SRC            SourceCatalog for each reduced CCD                       O     X
**frame_icsourcelist**      ICSRC          Bright SourceCatalog for each reduced CCD                O     X
**frame_matchlist**         ML             Match list for each reduced CCD                          O     X
**frame_forcelist**         FORCEDSRC      Forced photometry Catalog for each reduced CCD           O     X
**calibframe_sourcelist**   CALSRC         Mosaic calibrated SourceCatalog for each reduced CCD     O     X
**mosaic_sourcelist**       src            SourceCatalog for each coadd image                       O     X
**mosaic_icsourcelist**     icSrc          Bright SourceCatalog for coadd image                     O     X
**mosaic_matchlist**        srcMatchFull   Match list for each coadd image                          O     X
**mosaic_forcelist**        forced_src     Forced photometry object Catalog for each coadd image    O     X
**mosaic_forceflag**        (forced_src)   All flags accompanied to each measurement on coadd 

**photoobj_mosaic**                        Summary table for coadd forced sources
**photoobj_frame**                         Summary table for reduced CCD forced sources
=========================== ============== ====================================================== ===== =====

ある FITS データのカタログテーブルには、FITS BINTABLE、
パイプラインで検出されたある天体の測定結果の全ての情報が含まれます。全てのテーブルには
'**photo**' と '**coord**' テーブルが添付されます。これらのテーブルには、
様々な測定で得られた天体の等級、フラックス [erg/cm^2/Hz/sec]、中心（RA, DEC）
座標が含まれています（ただし、S14A0 リリースでは '**coord**'
テーブルは実装さていません）。
これらのテーブルにはそれぞれプライマリーキー制約が設定されています。
例えば '**frame_*list**' テーブルの場合 FRAME_ID がプライマリーキーですが、
'**mosaic_*list**' テーブルのプライマリーキーは 'tract', 'patch',
'filter', 'poinitng', 'id' です。'**frame_forcelist**' や 
'**frame_forcephoto**', '**mosaic_forcelist**' , 
'**mosaic_forcephoto**' テーブルでは、'id' が　'object_id'
と同じ意味で使用されています。

force_photo や force_coord から一次処理済データや 
coadd データに対するサマリーテーブルが生成されます。'**Photoobj_mosaic**' 
テーブルは '**mosaic_force_photo**' テーブルや '**mosaic_force_coord**' 
テーブルにある、ある天体の全カタログ情報を集めて 1 つのテーブルにまとめたものです。
'**Photoobj_frame**' テーブルは '**calibframe_source_photo**' 
テーブルや '**calibframe_source_coord**' テーブルにある、
ある天体の全情報を集めたテーブルです。どちらのサマリーテーブル内の測定情報も filter
毎に格納されています。平均や標準偏差といった統計量は、
様々な等級測定法に対して見積もられ、新しいカラムとして追加されます。


データベーステーブルの命名法
-----------------------------------
データベースを管理するために、PostgreSQL はデータベース、スキーマ、テーブルの
3 層構造になっています。HSC パイプラインでは、さらに以下の 2 層
（mos_rerun と cat_rerun）が追加されています。 ::

      (Database)     (Schema)             (Table)                           (mos_rerun)      (cat_rerun)
      ##########   #############   ################################   ###################  #################

       Database  |--- Schema 1   | -----  Table 1 (Frame)
                 |               | -----  Table 2 (Mosaic)          |-------- deepcoadd
                 |               |                                  |-------- bestseeing
                 |               |                                  |-------- ..........
                 |               |                              
                 |               | -----  Table 3 (Mosaic_Forcelist)|-------- deepcoadd  |--- iselect
                 |               |                                  |                    |
                 |               |                                  |                    |--- rselect....
                 |               |                                  |
                 |               |                            
                 |               |                                  |-------- bestseeing |--- iselect
                 |               |                                  |                    |
                 |               |                                  |                    |--- rselect....
                 |               |
                 |               |                                  |-------- .......... |--- iselect
                 |               |                                  |                    |
                 |               |                                  |                    |--- rselect.....
                 |               | -----  Table 4 (Photoobj_Mosaic)
                 |               | -----  .......
                 |               | -----  .......
                 |
                 |--- Schema 2   | -----  Table 1 (Frame)
                 |               | -----  Table 2 (Mosaic)
                 |               | -----  Table 3 (Photoobj_Mosaic)
                 |               | -----  .......
                 |               | -----  .......
                 |
                 |--- Schema 3   | -----  Table 1 (Frame)
                                 | -----  Table 2 (Mosaic)
                                 | -----  Table 3 (Photoobj_Mosaic)
                                 | -----  .......
                                 | -----  .......

S14A0 のデータリリースでは、データベースは 'dr_early'、
スキーマは 'ssp_s14a0_udeep_20140523a' か 'ssp_s14a0_wide_20140523a' で、
パイプライン中の 'rerun' に対応しています。mosaic の方法や forced measurements
で用いる参照 filter に応じて異なるカタログが生成されるため、
追加のテーブルを検討する必要があります。例えば、今、
パイプラインで基本的に用いられている mosaic の方法は 'deepCoadd' で、
'全ての' CCD データに対し mosaic と coadd が実行されます。一方で、良い seeing
の CCD データだけ使って coadd を実行する 'bestSeeing' という mosaic/coadd 
の方法もあり、この方法で作られた天体カタログは 'deepCoadd' 
の方法で作られたカタログと異なります。そこで、'mos_rerun' （mosaic rerun の意味）
というテーブルが新たなテーブルとして HSC パイプラインによるデータベースに追加されました。
また、異なる filter を参照して検出された天体カタログ（例えば、i-band selected、
r-band selected など）も別のカタログとして扱う必要があります。
このような場合のテーブルとして、HSC データベースには
'cat_rerun'（カタログ rerun の意味）が用意されています。
全てのテーブルを含んだフルテーブル名は
**schema_name.table_root_name__(mos_rerun)__(cat_rerun)** となります
（ただし、mos_rerun と cat_rerun は不要な場合は除外することもできます）。
例えば、S14A0 リリースデータの UDEEP 領域で 'deepCoadd' の方法で作られた
i-band selected の '**mosaic_forcelist**' テーブルは、
'**ssp_s14a0_udeep_20140523a.mosaic_forcelist__deepcoadd__iselect**'
となります。このままでは非常に名前が長いので、以下に紹介するように alias
を使ってテーブル名を短くすると良いかもしれません。


coadd 画像における flag を確認する
-----------------------------------------------------
各 filter の **mosaic_forceflag** テーブルの全記録から、
**mosaic_forceflag_filter** を定義することができます。S14A0
のデータリリースにおける各 filter の view 名は以下の通りです。

========================== ======================================== ===== ====
View Name                  Description                              UDEEP WIDE
========================== ======================================== ===== ====
mosaic_forceflag_g         g-band flags for coadd forced measurents   O    
mosaic_forceflag_r         r-band flags for coadd forced measurents   O
mosaic_forceflag_i         i-band flags for coadd forced measurents   O    O
mosaic_forceflag_z         z-band flags for coadd forced measurents   O
mosaic_forceflag_y         y-band flags for coadd forced measurents   O    O
========================== ======================================== ===== ====

これら view 名は coadd のサマリーテーブル（**photoobj_mosaic**）
から 各 filter における flag 情報を使い天体を選択する時に用いられます。


自身で用意したクエリにテーブルを '結合' する方法
-------------------------------------------------------
検出された天体の情報やパイプライン中の異なる解析方法で得られた天体の測定情報は、
データベース管理を簡易化と見易さのために、異なるテーブルに格納されます。一方で、
ユーザーがデータベース内のある天体を検索し測定量を得るためのクエリは共通です。
そこで、関係するデータベーステーブルを '結合' する方法が用いられています。
SQL を用いてテーブルを '結合' するにはいくつか方法がありますが、
ここではそのうちいくつかの方法のみ紹介します。また、
以下では HSC SSP データベース内のテーブルに特化して、いくつか実行例を紹介します。
さらなる実行例を :ref:`HSC クエリの例 <jp_database_queries>` に掲載していますので、
興味がある人はそちらもご覧ください。


CCD 画像単位で検出＆測定された天体を探す
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
COSMOS UDEEP データの visit=300, ccd=1 の CCD 画像（CORR-0000300-001.fits）
で検出された天体の id, RA, DEC, psf 等級と誤差情報を検索する。

.. highlight::
	bash
	
::

   SELECT  
        fs.id, fs.ra2000, fs.decl2000, fp.mag_psf, fp.mag_psf_err 
   FROM
        ssp_s14a0_udeep_20140523a.frame_sourcelist fs,  -- 'frame_sourcelist' テーブルの alias を fs と設定
        ssp_s14a0_udeep_20140523a.frame_sourcephoto fp, -- 'frame_sourcephoto' テーブルの alias を fp と設定
	ssp_s14a0_udeep_20140523a.frame ft              -- 'frame' テーブルの alias を ft と設定
   WHERE
            fs.frame_id = fp.frame_id and fs.id = fp.id -- fs と fp を結合
        and 
            fs.frame_id = ft.frame_id                   -- fs と ft を結合
        and 
            ft.visit=300 and ft.ccd=1                   -- ft 内の visit と ccd を指定

上記クエリ実行例では、SQL 構文内でテーブル名の alias を設定し、'**frame_sourcelist**', 
'**frame_sourcephoto**', '**frame**' の 3 つのテーブルを結合しています。
テーブルを結合するためには、'where' の後ろにプライマリーキーを使わなくてはいけません。
上記クエリ例では、'frame_id' と 'id' が fs と fp テーブルの結合に用いられ、
'frame_id' が fs と ft テーブルの結合に用いられています。
テーブルの結合で必要となるプライマリーキーは NAOJ が提供している
`スキーマブラウザー <https://hscdata.mtk.nao.ac.jp:4443/schema_browser2/schema_browser.html>`_ 
ページの 'DB keys' カラムで確認できます。'**frame**' テーブルには、
ある CCD 画像を特定するための 'visit' と 'ccd' の値も格納されており、
上記クエリ例でも用いられています。もし、ある CCD の frame_id
（'HSCA00030154' に相当）そのものが既知の場合、
'**frame**' テーブルは結合する必要はありません。


coadd 画像単位で検出＆測定された天体を探す
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
COSMOS UDEEP データの tract=0, patch=4,4, filter=HSC-I の
coadd 画像（calexp-HSC-I-0-4,4.fits）で検出された天体の id, RA, DEC, 
i-band psf 等級と誤差情報を検索する。 ::

   SELECT  
        ms.id, ms.ra2000, ms.decl2000, mp.mag_psf, mp.mag_psf_err 
   FROM
        ssp_s14a0_udeep_20140523a.mosaic_sourcelist__deepcoadd ms,  -- 'mosaic_sourcelist' テーブルの alias を ms と設定 
        ssp_s14a0_udeep_20140523a.mosaic_sourcephoto__deepcoadd mp  -- 'mosaic_sourcephoto' テーブルの alias を mp と設定
   WHERE
            ms.tract = mp.tract and ms.patch = mp.patch and ms.filter01 = mp.filter01  -- ms に mp を結合
            and ms.pointing = mp.pointing and ms.id = mp.id                            -- ms に mp を結合 
        and 
            ms.tract=0 and ms.patch='4,4' and ms.filter01 = 'HSC-I'                    -- ms 内の tract, patch, filter を指定

上記クエリ実行例では、'**mosaic_sourcelist**' と '**mosaic_sourcephoto**'
テーブル内の 'tract', 'patch', 'filter01', 'pointing', 'id' 
を組み合わせたプライマリーキーが使用されています。ゆくゆくは、'id' 
だけがプライマリーキーとして使用されるようになるでしょう。


coadd サマリーテーブル（多色 coadd テーブル）で検出＆測定された天体を探す
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
i-band 画像で centroid の測定がよく決まっており、
psf 等級も 24.0 等より明るいデータから作られた coadd サマリーテーブル
（**photoobj_mosaic**）の天体の id, RA, DEC, g,r,i,z,y-band での
psf 等級と誤差情報を検索する。 ::

   SELECT  
        pm.object_id, pm.ra2000, pm.decl2000, pm.gmag_psf, pm.gmag_psf_err, pm.rmag_psf, pm.rmag_psf_err,  
		pm.imag_psf, pm.imag_psf_err, pm.zmag_psf, pm.zmag_psf_err,  pm.ymag_psf, pm.ymag_psf_err
   FROM
        ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect pm,     -- 'photoobj_mosaic' テーブルの alias を pm と設定 
        ssp_s14a0_udeep_20140523a.mosaic_forceflag_i__deepcoadd__iselect mff  -- 'mosaic_forceflag_i' テーブルの alias を mff と設定 
   WHERE
            pm.tract = mff.tract and pm.patch = mff.patch                     -- pm と mff を結合
            and pm.pointing = mff.pointing and pm.object_id = mff.object_id   -- pm と mff を結合
	    and pm.imag_psf < 24.0 and mff.centroid_sdss_flags is not True    -- 限界等級と flag filtering を追加

'**photoobj_mosaic**' と '**mosaic_forceflag**' 
テーブルには共通のプライマリーキー（tract, patch, pointing, object_id）
があり、上記クエリ実行例ではこれらのプライマリーキーを使いテーブルを結合しています。
将来的には 'tract' と 'patch' のプライマリーキーは取り除かれるようになるでしょう。




