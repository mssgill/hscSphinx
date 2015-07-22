
===================================
観測データの解析ひとまとめ
===================================

ここまでの HSC パイプラインを用いた解析に関するページは全て読み終わっているものとして、
話を進めることにします。このページでは PI 
観測で得たデータをパイプラインを使って解析する際のコマンドを一通りまとめて紹介します。
ここで例として紹介するデータは "COSMOS" フィールドを HSC-I で観測したデータで、
一次処理用データとして Bias, Dark, DomeFlat も含んでいます。
天体データの visit は 100 から 200 とします（つまり visit=100..200:2）。
解析の際には、必ず、 **正しい天体名、visit　番号を指定** してください。また、
使用する計算機ではバッチ処理が可能だという前提で、
``--queue``, ``--nodes``, ``--procs`` らの引数も使用しています。

.. highlight::
	bash

#. セットアップ (詳細は :ref:`jp_back_eups`)::

     $ . /data1a/ana/products2014/eups/defaults/bin/setup.sh
     $ setup -v hscPipe -t HSC
     $ setup -v astrometry_net_data ps1_pv1.2a
    
#. 生データをレジストリに登録する (詳細は :ref:`jp_ingest`)::

     $ mkdir /data/Subaru/HSC
     $ echo lsst.obs.hsc.HscMapper > /data/Subaru/HSC/_mapper
     $ cd /path/to/rawdata/
     $ hscIngestImages.py /data/Subaru/HSC/ --create --mode=link HSCA*.fits

#. 一次処理用データの解析 (詳細は :ref:`jp_detrend`)::

     $ reduceBias.py /data/Subaru/HSC/ --rerun all_bias --queue small --detrendId calibVersion=all --job bias --nodes=3 --procs=12 --id field=BIAS
     $ genCalibRegistry.py --create --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

     $ reduceDark.py /data/Subaru/HSC/ --rerun all_dark --queue small --detrendId calibVersion=all --job dark --nodes=3 --procs=12 --id field=DARK
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12
     
     $ reduceFlat.py /data/Subaru/HSC --rerun dome_flats --queue small --detrendId calibVersion=domeflat --job dflat --nodes=3 --procs=12 --id field=DOMEFLAT
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

     # 天体データを使い Fringe データを生成する
     $ reduceFringe.py /data/Subaru/HSC/ --rerun all_fringe --queue small --detrendId calibVersion=all --job fringe --nodes=3 --procs=12 --id field=COSMOS
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

#. どの天体データを使用して解析するかデータをチェックする。例 全 HSC-I データ (詳細は :ref:`jp_registryinfo`)::

     $ export SUPRIME_DATA_DIR=/data/Subaru/HSC
     $ registryInfo.py --field COSMOS --filter HSC-I
     < visit リスト >
     
#. (オプション) ``registryInfo.py list`` のリストから 1 CCD だけ選んで試しに解析を実行する (詳細は :ref:`jp_hscprocessccd`)::

     $ hscProcessCcd.py /data/Subaru/HSC/ --rerun cosmos --id visit=100 ccd=50
     
#. 天体データの一次処理 (詳細は :ref:`jp_reduceframes`)::

     $ reduceFrames.py /data/Subaru/HSC/ --rerun cosmos --id visit=100..200:2 \
         --queue small --nodes 4 --procs 6 --job redframes
   
#. SkyMap を生成する (観測データから SkyMap を生成する場合) (詳細は :ref:`jp_skymap`)::

    $ makeDiscreteSkyMap.py /data/Subaru/HSC/ --rerun=cosmos --id visit=100..200:2 ccd=0..103

#. mosaic.py の実行 (ubercal) (詳細は :ref:`jp_mosaic`)::

    $ mosaic.py /data/Subaru/HSC --rerun cosmos --id tract=0 visit=100..200:2 ccd=0..103

#. 天体データの重ね合わせ (詳細は :ref:`jp_stack`)::

    $ stack.py /data/Subaru/HSC/ --rerun=cosmos --id tract=0 filter=HSC-I --selectId visit=100..200:2 \
          --queue small --nodes 4 --procs 6 --job stack

#. Multiband の解析 (R,I,Z-band の解析を行うとする。詳細は :ref:`jp_multiband_proc`)::

    $ multiBand.py /data/Subaru/HSC/ --rerun cosmos --id tract=0 filter=HSC-R^HSC-I^HSC-Z \
          --queue small --nodes 4 --procs 6 --job multiband

..     
   #. (optional) Run single-frame QA on some select visits (e.g. visit number 100)::

   $ cat .pqa/dbauth.py
   $ cat .hsc/dbauth.py
   $ mkdir -p /home/you/public_html/qa
   $ export WWW_ROOT=/home/you/public_html/qa
   $ export WWW_RERUN=cosmos
   $ export TESTBED_PATH=/data/Subaru/HSC/rerun
   $ newQa.py -p hsc cosmos
   $ pipeQa.py -d butler -C hsc -v 100 cosmos

