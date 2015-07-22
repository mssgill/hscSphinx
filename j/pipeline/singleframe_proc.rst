
============================
天体データへの一次処理
============================

パイプラインでは、自身の解析ニーズに応じて、天体データへの一次処理には
``reduceFrames.py`` と ``hscProcessCcd.py`` の 2 つのコマンドが用意されています。
``hscProcessCcd.py`` は、ある特定の visit, CCD データに対して、一次処理（Bias 引き、
Flat 補正等）と天体検出, 測光を行います。``reduceFrames.py`` では、ある visit の全ての
CCD に対して一次処理を実行します。いずれにコマンドでも :ref:`データ ID <jp_back_dataId>`
を指定する必要があります: ``--id <identifiers>`` という形式で、データの指定方法（identifiers）は、
``visit``, ``ccd``, ``field``, ``dateObs``, ``filter`` などがあります。

詳しいパラメータの情報は ``--help`` か ``-h`` で検索できます。

.. _jp_reduceframes:

reduceFrames.py
---------------

``reduceFrames.py`` で用いられる様々なコマンドタスクはバッチ処理に対応しています。
そのうちいくつかをここで紹介します。さらなる詳細は :ref:`jp_back_torque` をご覧ください。

**例 1**

.. highlight::
	bash

::
   
   $ reduceFrames.py /data/Subaru/HSC --rerun cosmos --queue small --job cosmos --nodes 2 --procs 12 --id field=COSMOS filter=HSC-I dateObs=2016-02-02

* ``/data/Subaru/HSC``      データの配置場所。
* ``--rerun cosmos``        出力データの rerun 名。
* ``--id``                  データ ID。例では COSMOS data, HSC-I filter, 2016年2月2日に取得されたデータを指定している。
* ``--queue default``       PBS torque 名。
* ``--job cosmos``          実行している PBS job 名 (``qstat`` で表示される job 名)。
* ``--nodes 2``             2 ノードを指定。
* ``--procs 12``            各ノードで 12 プロセスの解析を実行。

.. _jp_hscprocessccd:

hscProcessCcd.py
----------------
  
**例 1**


ここでは、デフォルトの設定ではなく、ある config ファイル（``tmp.config``）を用いて
hscProcessCcd.py を実行した場合について記述します。以下の例では、
単に config ファイルを読み込むだけではなく、コマンドラインベースで Frige 
データの補正を行わないことも指定しています。もし config 
ファイルを自身で用意してコマンドを実行する際は、自分の解析に適したパラメータを準備してください。

::

   # confing ファイルの中身を確認する（例では cmodel を用いた天体の測光は行わない設定になっている）
   
   $ cat tmp.config
   root.measurement.algorithms.names=['flux.psf', 'flags.pixel', 'focalplane', 'flux.aperture',
   'flux.naive', 'flux.gaussian', 'centroid.naive', 'flux.sinc', 'shape.sdss', 'jacobian',
   'flux.kron', 'correctfluxes', 'classification.extendedness', 'skycoord']
   root.measurement.slots.modelFlux='flux.gaussian'

   # -C パラメータで使用する config ファイルを指定し、コマンドラインで追加する config パラメータは --config 以下で指定する
   $ hscProcessCcd.py /data/Subaru/HSC --rerun cosmos --id visit=1000 ccd=50 --clobber-config -C tmp.config --config isr.doFringe=False

   
* ``/data/Subaru/HSC``            データの配置場所。
* ``--rerun cosmos``              全入出力データの配置場所（rerun 名）。
* ``--id``                        データ ID。例では visit 1000, ccd 50 の天体データを指定。
* ``-C tmp.config``               config パラメータが記入された config ファイルを指定（中身は上記 tmp.config のもの）。
* ``--config isr.doFringe=False`` コマンドラインで追加する config パラメータ。ここでは Fring データの補正は行わないことを指定している。なお。Fringe データの補正は基本的に HSC-Y バンドのみで実行される。
* ``--clobber-config``            もし同じ rerun 名で一度解析を実行したことがあり、config パラメータを変更して新たに解析を実行する場合に必要になるパラメータ。

.. warning::

	--clobber-config は、ある既存の rerun に対して異なる config
	パラメータで解析を実行するか、
	異なるパイプラインのバージョンを用いて解析を実行する場合に必要になるパラメータです。
	一度このオプションを設定すると、解析されたデータのパラメータは同一の rerun 
	で不均一であるとみなされます。

