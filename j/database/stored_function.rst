.. _jp_stored_function:

=====================================================
ユーザーによる定義関数（ストアドファンクション）
=====================================================
データベースがより使いやすくなるように、ユーザー定義の関数
（ストアドファンクション）を使用することができます。
`PostgreSQL に元々実装されている基本的な関数
<http://www.postgresql.org/docs/9.3/static/functions-aggregate.html>`_
に加え、HSC SSP データ用に天文台が公開している HSC データベースでは、
いくつかのユーザー定義の関数が利用できます。将来的には、
座標変換（hh:mm:ss.s,+/-dd:mm:ss.s -> degrees）
や等級・フラックス変換などの関数も装備されていくでしょう。

統計量を調べる関数一覧
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table:: **ユーザー定義の関数（統計量）**

   * - **関数**
     - **Argument Type(s)**
     - **Return Type**
     - **コメント**

   * - qmedian(expression)
     - int, bigint, numeric, double precision
     - same as argument data type
     - 全入力値の median

   * - quantile(expression)
     - int, bigint, numeric, double precision
     - same as argument data type
     - 全入力値の分位点

   * - weighted_mean(values, weight_values)
     - set of double precision
     - double precision
     - 全入力値の weighted mean

   * - mean
     - double precision
     - same as argument data type
     - 全入力値の mean

   * - variance
     - double precision
     - same as argument data type
     - 全入力値の分散（unbiased）

   * - stddev
     - double precision
     - same as argument data type
     - 分散（unbiased）の平方根（標準偏差）

   * - skewness
     - double precision
     - same as argument data type
     - 全入力値の歪度: κ\ :sub:`3`\ /κ\ :sub:`2`\ :sup:`3/2` where κ\ :sub:`i` i-th キュムラント

   * - kurtosis
     - double precision
     - same as argument data type
     - 全入力値の尖度: κ\ :sub:`4`\ /κ\ :sub:`2`\ :sup:`2` where κ\ :sub:`i` i-th キュムラント

.. highlight::
	sql

qmedian の実行例::

      -- UDEEP CCD データのフレームテーブルから seeing の median を計算する

      SELECT qmedian(seeing) from ssp_s14a0_udeep_20140523a.frame;

quantile の実行例::

      -- UDEEP CCD データのフレームテーブルから seeing の 30% 分位点を計算する

      SELECT quantile(seeing, 0.3) from ssp_s14a0_udeep_20140523a.frame;

      -- UDEEP CCD データのフレームテーブルから seeing の（30, 50, 70）% 分位点を計算する

      SELECT quantile(seeing, array[0.3, 0.5, 0.7]) from ssp_s14a0_udeep_20140523a.frame;

weighted_mean の実行例::

      -- Sinc 等級エラー（mag_sinc_err^{-2}）で重み付けした Sinc 等級の weighted mean を計算する
      -- !!注意!! weighted_mean では計算したい変数を倍精度浮動小数点数（double precision）の形で入力しないといけません。

      SELECT weighted_mean(mag_sinc, (1.0/mag_sinc_err)*(1.0/mag_sinc_err))
        FROM ssp_s14a0_udeep_20140523a.frame_forcephoto__deepcoadd__iselect
        WHERE tract=0 and id=207876417126408 and mag_sinc_err > 0.0;

..	  Caution!! only double precision input is allowed currently and cast to numeric is essential

mean, variance, stddev の実行例::

      -- UDEEP CCD データのフレームテーブルから
      -- mag_sinc_err の mean, mag_gaussian の分散,
      -- flux_cmodel（NaN ではない）の標準偏差を計算する

      SELECT mean(mag_sinc_err, '>', 0), variance(mag_gaussian, '<', 99.99), stddev(flux_cmodel, '==', flux_cmodel)
        FROM ssp_s14a0_udeep_20140523a.frame_forcephoto__deepcoadd__iselect
        WHERE tract=0;

skewness, kurtosis の実行例::

      -- mag_sinc の歪度と
      -- mag_gaussian の尖度を計算する

      SELECT skewness(mag_sinc, '<', 99.99), kurtosis(mag_gaussian, '<', 99,99),
        FROM ssp_s14a0_udeep_20140523a.frame_forcephoto__deepcoadd__iselect
        WHERE tract=0;


領域検索で用いられる関数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table:: **ユーザー定義の関数（領域検索）**

   * - **関数**
     - **コメント**

   * - f_getobj_circle(ra, dec, radius, table_name)
     - 中心座標 (ra, dec), 半径 radius の同心円内にいる天体を書き出す

   * - f_getobj_rectangle(ra, dec, delta_ra, delta_dec, table_name)
     - 中心座標 (ra, dec), ra 方向の長さ delta_ra, dec 方向の長さ delta_dec の長方形にいる天体を書き出す

f_getobj_circle(ra, dec, radius, table_name) の実行例::

      -- UDEEP CCD データの frame_forcelist の
      -- 中心座標 (RA,DEC)=(150.403189,1.485288), 半径 2" の同心円内にいる天体の
      -- tract, patch, pointing, id, ra2000 [deg], decl2000 [deg], cx, cy, cz, xxyyzz, distance を書き出す	  

      SELECT * from f_getobj_circle(150.403189, 1.485288, 2.0, 'ssp_s14a0_udeep_20140523a.frame_forcelist__deepcoadd__iselect');

      -- 中心座標 (RA,DEC)=(150.403189,1.485288), 半径 3" の同心円内いる天体の
      -- id, ra, dec, g- r- i- z- y-band の sinc 等級, 指定した中心座標からの距離 ["] を書き出し、
      -- photoobj_mosaic の検索結果と合わせる

      SELECT pm.id, pm.ra2000, pm.decl2000, pm.gmag_sinc, pm.rmag_sinc, pm.imag_sinc, pm.zmag_sinc, pm.ymag_sinc, obj.distance
      FROM f_getobj_circle(150.93, 1.93, 3.0, 'ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect') obj,
           ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect pm
      WHERE obj.id=pm.id and obj.tract=pm.tract and obj.patch=pm.patch and obj.pointing = pm.pointing
      ORDER by obj.distance;

f_getobj_rectangle(ra, dec, delta_ra, delta_dec, table_name) の実行例::

      -- UDEEP CCD データの frame_forcelist の
      -- 中心座標 (RA,DEC)=(150.403189,1.485288), 2' x 2' の長方形にいる天体を書き出す
      -- tract, patch, pointing, id, ra2000 [deg], decl2000 [deg], cx, cy, cz, xxyyzz, distance を書き出す

      SELECT * from f_getobj_rectangle(150.403189, 1.485288, 2.0, 2.0, 'ssp_s14a0_udeep_20140523a.frame_forcelist__deepcoadd__iselect');


utility 用の関数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
HSC の情報を取り扱ういくつかの utility 関数も用意されています。例えば、
(visit, ccd) と FrameId の変換などがあります。

.. list-table:: **ユーザー定義の関数（utility）**

   * - **関数**
     - **Argument Type(s)**
     - **Return Type**
     - **コメント**

   * - frameid2visitccd
     - text
     - set of integer
     - FrameId から (visit, ccd) への変換

   * - visitccd2frameid
     - set of integer
     - text
     - (visit, ccd) から FrameId への変換

   * - hms2deg
     - text (hh:mm:ss.sss)
     - double precision
     - RA [hh:mm:ss.sss] から [degree] への変換

   * - deg2hms
     - double precision
     - text (hh:mm:ss.sss)
     - RA [degree] から [hh:mm:ss.sss] への変換

   * - dms2deg
     - text (+/-dd:mm:ss.ss)
     - double precision
     - DEC [+/-dd:mm:ss.ss] から [degree] への変換

   * - equ2gal
     - set of double precision (ra, dec) J2000
     - set of double precision (gallon, gallat)
     - equatrial coordinates [degree] から galactic coordinates [degree] への変換 (SLALIB 2.5-4 をもとに計算)

   * - gal2equ
     - set of double precision (gallon, gallat)
     - set of double precision (ra, dec) J2000
     - galactic coordinates [degree] から equatrial coordinates [degree] への変換 (SLALIB 2.5-4 をもとに計算)

   * - date2mjd
     - text (date string: YYYY-MM-DD)
     - integer (mjd in integer)
     - date-obs を MJD へ変換

   * - datetime2mjd
     - text (datetime string: YYYY-MM-DDThh:mm:ss.sss)
     - double precision (mjd)
     - date-obs + UT を MJD へ変換（秒を含む）

   * - datetime2mjd
     - set of text (date string: YYYY-MM-DD, time string hh:mm:ss.sss)
     - double precision (mjd)
     - date-obs + UT を MJD へ変換（秒は別扱い）

   * - mjd2date
     - integer (MJD in integer)
     - text (date string: YYYY-MM-DD)
     - MJD を string 型の日付表記に変換

   * - mjd2datetime
     - double precision (MJD)
     - text (datetime string: YYYY-MM-DDThh:mm:ss.sss)
     - MJD を string 型の日付表記 (DATE-OBJ + UT) に変換 

   * - mjd2datetime2
     - double precision (MJD)
     - set of text (date string: YYYY-MM-DD, time string: hh:mm:ss.sss)
     - MJD を string 型の日付表記 (DATE-OBJ + UT) に変換 

   * - mag2flux
     - double precision (AB magnitude)
     - double precision (flux in erg/s/cm^2/Hz)
     - AB 等級から flux [erg/s/cm^2/Hz] への変換

   * - mag2fluxJy
     - double precision (AB magnitude)
     - double precision (flux in Jansky)
     - AB 等級から flux [Jy] への変換

   * - flux2mag
     - double precision (flux in erg/s/cm^2/Hz)
     - double precision (AB magnitude)
     - flux [erg/s/cm^2/Hz] から AB 等級への変換

   * - fluxJy2mag
     - double precision (flux in Jansky)
     - double precision (AB magnitude)
     - flux [Jy] から AB 等級への変換

   * - flux_cgs2Jy
     - double precision (flux in erg/s/cm^2/Hz)
     - double precision (flux in Jansky)
     - flux [erg/s/cm^2/Hz] から flux [Jy] への変換

   * - flux_Jy2cgs
     - double precision (flux in Jansky)
     - double precision (flux in erg/s/cm^2/Hz)
     - flux [Jy] から flux [erg/s/cm^2/Hz] への変換

frameid2visitccd と visitccd2frameid の実行例::

      SELECT frameid2visitccd('HSCA00000301');
      return (2,27)

      SELECT visitccd2frameid(2, 27);
      return 'HSCA00000301'

hms2deg と dms2deg の実行例::

      SELECT hms2deg('12:12:12.345');
        return 183.0514375

      SELECT dms2deg('-01:00:12.00');
        return -1.00333333333333

deg2hms と deg2dms の実行例::

      SELECT deg2hms(183.051416666667);
        return 12:12:12.34

      SELECT deg2dms(83.0514375);
        return +83:03:05.18

天体の座標を hh:mm:ss.sss and +/-dd:mm:ss.ss で取得する例::

      SELECT deg2hms(ra2000) as ra, deg2dms(decl2000) as dec
      FROM ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect
      LIMIT 10;

UDEEP の photoobj_mosaic カタログ内、(RA, DEC) = 
(10:03:45.000, +02:00:00.00) を中心に 20" 以内にある天体の 
id, 座標 [degree], 座標[hms/dms] を取得する例 ::

      SELECT id, ra2000, decl2000, deg2hms(ra2000) as ra, deg2dms(decl2000) as dec
      FROM f_getobj_circle(hms2deg('10:03:45.000'), dms2deg('+02:00:00.00'), 20.0, 'ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect');

equ2gal と gal2equ の実行例::

      SELECT equ2gal(120.0, 30.0);

      SELECT gal2equ(230.0, 20.0);

      -- UDEEP の photoobj_mosaic カタログ内
      -- (RA, DEC) = (10:03:45.000, +02:00:00.00) を中心に 20" 以内にある天体の
      --  id, ra, dec, galactic coordinates

      SELECT pm.id, pm.ra2000, pm.decl2000, e2g.l as gallon, e2g.b as gallat
      FROM
         f_getobj_circle(hms2deg('10:03:45.000'), dms2deg('+02:00:00.00'), 20.0, 'ssp_s14a0_udeep_20140523a.photoobj_mosaic__deepcoadd__iselect') pm,
         equ2gal(pm.ra2000, pm.decl2000) e2g
      ;


date2mjd と mjd2date の実行例::

      SELECT date2mjd('2014-07-17');

      SELECT mjd2date(56855);

datetime2mjd, mjd2datetime, mjd2datetime2 の実行例::

      SELECT datetime2mjd('2014-07-17T12:12:12.000');

      SELECT datetime2mjd('2014-07-17', '12:12:12.000');

      SELECT mjd2datetime(56855.5084722222);

      SELECT mjd2datetime2(56855.5084722222);

mag2flux と flux2mag の実行例::

      -- データベースにある天体の flux と等級の比較
      SELECT iflux_sinc, mag2flux(imag_sinc), imag_sinc, flux2mag(iflux_sinc)
      FROM ssp_s14a0_wide_20140523a.photoobj_mosaic__deepcoadd__iselect
      LIMIT 10;

flux_Jy2cgs と fluxJy2mag の実行例::

      -- 1e-6 Jy より明るい天体を選択
      SELECT iflux_sinc
      FROM ssp_s14a0_wide_20140523a.photoobj_mosaic__deepcoadd__iselect
      WHERE iflux_sinc > flux_Jy2cgs(1e-6)
      LIMIT 10;

      -- または、以下の表記も可能
      SELECT imag_sinc
      FROM ssp_s14a0_wide_20140523a.photoobj_mosaic__deepcoadd__iselect
      WHERE imag_sinc < fluxJy2mag(1e-6)
      LIMIT 10;


WCS テーブルをもとにした座標変換の関数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pixel 座標と天球座標の座標変換がデータベース内で利用できます。現在この座標変換には、
mosaic で生成される wcs*.fits をもとに作られる 'wcs' テーブルが使われます。
そのため、pixel 座標と天球座標の座標変換は mosaic 処理が終了した 
CCD データにだけ適応されます。

.. list-table:: **ユーザー定義の関数（WCS 座標系に関するもの）**

   * - **関数**
     - **Argument Type(s)**
     - **Return Type**
     - **コメント**

   * - sky2pix
     - set of double precision, text and integer (ra, dec, schema, tract, frame-id) [ra and dec in degree]
     - set of double precision (x, y)
     - ある画像データを天球座標から pixel 座標へ変換

   * - pix2sky
     - set of double precision, text and integer (x, y, schema, tract, frame-id)
     - set of double precision (ra, dec) in degree
     - ある画像データを pixel 座標から天球座標へ変換

   * - shape_sky2pix
     - set of double precision, text and integer (shape_array, ra, dec, schema, tract, frame-id) [shape_array (I_xx, I_yy, I_xy), ra and dec in degree]
     - array of double precision (Is_xx, Is_yy, Is_xy) in pixel^2
     - shape パラメータ [arcsec^2] を pixel 座標へ変換

   * - shape_pix2sky
     - set of double precision, text and integer (shape_array, x, y, schema, tract, frame-id)[shape_array (Is_xx, Is_yy, Is_xy)]
     - array of double precision (I_xx, I_yy, I_xy) in arcsec^2
     - shape パラメータ [pixel^2] を天球座標へ変換

   * - shape_err_sky2pix
     - set of double precision, text and integer (err_array, ra, dec, schema, tract, frame-id) [err_array is covariance of (I_xx, I_yy, I_xy) arranged as (xx-xx, xx-yy, yy-yy, xx-xy, yy-xy, xy-xy), ra and dec in degree]
     - array of double precision (xx-xx, xx-yy, yy-yy, xx-xy, yy-xy, xy-xy) in pixel^4 that is the covariance of (Is_xx, Is_yy, Is_xy)
     - shape パラメータの共分散 [arcsec^4] を pixel 座標へ変換

   * - shape_err_pix2sky
     - set of double precision, text and integer (err_array, x, y, schema, tract, frame-id)[err_array is covariance of (Is_xx, Is_yy, Is_xy) arranged as (xx-xx, xx-yy, yy-yy, xx-xy, yy-xy, xy-xy)]
     - array of double precision (xx-xx, xx-yy, yy-yy, xx-xy, yy-xy, xy-xy) in arcsec^4 that is the covariance of (I_xx, I_yy, I_xy)
     - shape パラメータの共分散 [pixel^4] を天球座標へ変換

   * - f_enum_frames_containing
     - set of double precision and text (ra2000, decl2000, schema) [ra,decl in degree]
     - set of text, integer and double precision (frame_id, tract, x, y) [x,y in pixel coord]
     - 一次処理済画像から、ある特定の座標をもつ天体の frame_id を書き出す

   * - f_enum_mosaics_containing
     - set of double precision and text (ra2000, decl2000, schema) [ra,decl in degree]
     - set of text, integer and double precision (frame_id, tract, x, y) [x,y in pixel coord]
     - coadd 画像から、ある特定の座標をもつ天体の frame_id を書き出す

sky2pix と pix2sky の実行例::

      -- tract 0, frame_id 'HSCA00188753' 内の
      -- (RA,DEC)=(150.5 deg, 1.5 deg) の pixel 座標を取得する

      SELECT sky2pix(150.5, 1.5,'ssp_s14a0_udeep_20140523a', 0, 'HSCA00188753');

      -- tract 0, frame_id 'HSCA00188753' 内の
      -- (x,y)=(1750.325,359.630) の天球座標を取得する

      SELECT pix2sky(1750.325,359.630,'ssp_s14a0_udeep_20140523a', 0, 'HSCA00188753');


shape_sky2pix と shape_pix2sky の実行例::

      SELECT shape_pix2sky(shape_sdss, centroid_sdss_x, centroid_sdss_y, 'ssp_s14a0_wide_20140523a', tract, frame_id)
      FROM ssp_s14a0_wide_20140523a.frame_forcelist__deepcoadd__iselect
      limit 10;

      SELECT shape_sdss, shape_sky2pix(shape_pix2sky(shape_sdss, centroid_sdss_x, centroid_sdss_y, 'ssp_s14a0_wide_20140523a', tract, frame_id),  ra2000, decl2000, 'ssp_s14a0_wide_20140523a', tract, frame_id)
      FROM ssp_s14a0_wide_20140523a.frame_forcelist__deepcoadd__iselect
      limit 10;

f_enum_frames_containing の実行例::

      --- UDEEP データの 一次処理済データから 
      --- (RA,DEC)=(150.0,2.0) という座標を含む　frame_ids (CCD's id) を取得する
      select f_enum_frames_containing(150.0, 2.0, 'ssp_s14a0_udeep_20140523a')

      select frame_id, tract, x, y from f_enum_frames_containing(150.0, 2.0, 'ssp_s14a0_udeep_20140523a');

      ---
      --- f_enum_frames_containing は以下のプロセスで実行されます。
      ---
      --- 1. 最初に、指定した (ra, dec) に対応する healpix index を取得します。
      --- 2. 次に、frame のリストを取得するために "frame_hpx11" テーブルを調べます。
      --- 3. (2) で得た "frame_id" が含まれる "frame" テーブルと "wcs" テーブルを結合します。
      --- 4. 最後に、(3) で結合したテーブルから該当する frame_id を選択する。

f_enum_mosaics_containing の実行例::

      --- UDEEP データの coadd データから
      --- (RA,DEC)=(150.0,2.0) という座標を含む (tract, patch, filter) を取得する

      select f_enum_mosaics_containing(150.0, 2.0, 'ssp_s14a0_udeep_20140523a');

      select tract, patch, filter01, x, y from f_enum_mosaics_containing(150.0, 2.0, 'ssp_s14a0_udeep_20140523a');


自身のデータベースでユーザー定義の関数を設定する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
もし自身のデータサーバでユーザー定義の関数を実行したいなら、様々な関数をインストールし、
ご自身で設定しなくてはいけません。このページで紹介している全ての関数は、
'python/hsc/hscDb/pgfunctions' 下にある最新の **hscDb** 
パッケージで利用可能です（2014.07.04 現在）。

C や C++ を使うために、まず最初に Makefile を実行してください。その後 root 
ユーザーで make install を実行し、pqsl コマンド内の
'create extension [function_name]' を実行してください。

.. highlight::
	bash

::

     # 例えば qmedian の実行例

     % cd pgfunctions/c/qmedian
     % make
     % su <-- switch to root user
     % make install

     % /usr/local/pgsql/bin/psql -U hscana -d dr_early -h your_db_host

     psql> create extension qmedian;

まずはじめに、各パッケージディレクトリにある README ファイルを読んでください。

PL/pgSQL を使うために、plpgsql ディレクトリにある全ての SQL 
スクリプトを実行しなくてはいけません。 ::

     % /usr/local/pgsql/bin/psql -U hscana -d dr_early -h your_db_host -f f_arcsec2radian.sql
     % /usr/local/pgsql/bin/psql -U hscana -d dr_early -h your_db_host -f ......
     % ..........................

**注意**

各データベースでユーザー定義の関数を設定するには、'create database' か
createdb コマンドでデータベースを新たに作る時に 'create extension' か
'create function' コマンドを実行しなくてはいけません。

psql において '**\\df**' コマンドを使ってセットアップ関数を調べることができます。
