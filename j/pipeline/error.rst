
.. _jp_errormessages:

==================================
共通のパイプラインエラー
==================================

もしパイプラインにおける解析処理が失敗した場合、
処理失敗時に何が起こったかターミナルに表示されているログから調べることができます。
このログにはエラーメッセージ以外にも有用な情報がたくさん表示されています。
ここでは、よく遭遇しうるエラーを紹介します。
もしここで紹介されていないようなエラーを見つけた場合は、ぜひご連絡ください。

また ``stdout`` に関係するトラブルは、:ref:`jp_debugging`
のページをご覧ください。


.. _jp_error_setup:

EUPS ``setup`` の際に root パスワードを要求される
--------------------------------------------------------------

新しく計算機にパイプラインやパッケージをインストールしようとした際に、
まれに次のようなメッセージを見かける時があるかもしれません。

.. highlight::
	bash
	
::

    $ setup -v hscPipe 3.3.3
    You are attempting to run "setup" which requires administrative
    privileges, but more information is needed in order to do so.
    Authenticating as "root"
    Password:

このようなメッセージが表示された場合、EUPS の ``setup.sh`` ファイルを
``source`` し忘れたのかもしれません。詳細は :ref:`EUPS <jp_back_eups>` 
をご覧いただくとして、以下に回避方法を紹介します。 ::

    # bash シェルユーザーの場合
    $ source /data1a/ana/products2014/eups/default/bin/setups.sh

    # csh (or tcsh) シェルユーザーの場合
    $ source /data1a/ana/products2014/eups/default/bin/setups.csh

Linux にもシステムの設定を管理する ``setup`` コマンドがあります。上記のように
``setups.sh``　（または ``setups.csh`` ）ファイルを ``source`` すると、
EUPS は ``PATH`` 変数に新しいディレクトリを追加し、システムの ``setup`` 
コマンドを隠してくれます。


``_mapper`` ファイルがない
-----------------------------------------

データリポジトリには、mapper という情報を含んだ ``_mapper`` ファイルがあります。
mapper はデータリポジトリの中でデータの位置情報を記録しています（詳しくは
:ref:`j_data_repo` をご覧ください）。もしデータリポジトリに _mapper 
ファイルがないと、以下のようなエラーメッセージが表示されます。 ::

    RuntimeError: No mapper provided and no _mapper available

このエラーに遭遇した場合は _mapper ファイルを作成しデータリポジトリ内に配置してください。
IPMU の``master`` システムにおける解決策は以下の通りです。

.. highlight::
	bash
	
::

    $ cat /lustre/Subaru/SSP/_mapper
    lsst.obs.hsc.HscMapper


astrometry_net_data がない
--------------------------------------------

パイプラインのデフォルトの設定では astrometry_net_data カタログの登録は行われません。
登録されていない場合は 'none' というダミーデータが設定されてしまいます。解決するためには、
次のような 2 つの方法があります。 

#. 'setup astrometry_net_data <catalog>' を実行する

#. hscPipe をリセットし、astrometry_net_data もリセットする
   
以下のエラーでは何か問題か教えてくれています。 ::

    assert(matches is not None)
    AssertionError

    WARNING: hsc.meas.astrom failed ([Errno 2] No such file or directory: 'none/andConfig.py')

例えば、astrometry_net_data の登録を忘れて hscProcessCcd.py を実行すると、
以下のようなエラーが生じます。 ::
  
	2014-04-01T01:16:53: processCcd.calibrate: Fit and subtracted background
    2014-04-01T01:16:53: processCcd.calibrate.measurement: Measuring 101 sources
    2014-04-01T01:16:54: processCcd.calibrate.astrometry: Applying distortion \
         correction: HscDistortion derived class
    2014-04-01T01:16:54: processCcd.calibrate.astrometry: Solving astrometry
    2014-04-01T01:16:54: processCcd.calibrate.astrometry WARNING: hsc.meas.astrom \
         failed ([Errno 2] No such file or directory: 'none/andConfig.py')
    2014-04-01T01:16:54: processCcd.calibrate WARNING: Unable to perform astrometry \
         (Unable to solve astrometry for 50, 1_12): attempting to proceed
    2014-04-01T01:16:54: processCcd FATAL: Failed on dataId={'taiObs': '2014-04-01', \
         'pointing': 001, 'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
         'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 200.0}: 
    Traceback (most recent call last):
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/cmdLineTask.py", line 223, in __call__
       result = task.run(dataRef, **kwargs)
    File "/data1a/ana/products2014/Linux64/hscPipe/2.12.0i_hsc/python/hsc/pipe/tasks/processCcd.py", line 53, in run
       result = ProcessCcdTask.run(self, sensorRef)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
       res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/processCcd.py", line 82, in run
       result = self.process(sensorRef, postIsrExposure)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
       res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/processImage.py", line 156, in process
       calib = self.calibrate.run(inputExposure, idFactory=idFactory)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
       res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/calibrate.py", line 269, in run
       assert(matches is not None)
    AssertionError


    
一次処理データの異なるバージョンで生じる入力エラー
--------------------------------------------------------------

一次処理用データを作る際に ``--detrendId calibVersion=XXX``を指定し、
複数の Bias データを異なる ``calibVersions`` で生成していたとします。
しかし、現在のパイプラインバージョンではどの ``calibVersions``
の一次処理データを使用するのか指定することができませんし、
どの ``calibVersions`` のデータを使えばよいか自分で判断することもできません。
そのような場合、パイプラインは以下のようなエラーメッセージを表示します。
例えば、Flat データが ``CALIB/FLAT/<YYYY-MM-DD>/<FILTER>/<unwanted-calib>``
というデータリポジトリに配置されているとします。
以下のエラーメッセージのうち最後の一行でどの一次処理データがエラーを生じているかわかります。
このエラーを回避するには、``CALIB/`` 
以下に配置されている全ての一次処理データを解析に使用するのもだけにすることです。

::

    2014-04-01T01:42:26: processCcd FATAL: Failed on dataId={'taiObs': '2014-04-01', \
             'pointing': 100, 'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
             'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 240.0}: \
             Unable to retrieve fringe for {'taiObs': '2014-04-01', 'pointing': 100, \
             'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
             'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 240.0}: \
             No unique lookup for ['calibDate', 'calibVersion'] from {'taiObs': '2014-04-01', \
             'pointing': 100, 'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
             'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 200.0}: 2 matches
    Traceback (most recent call last):
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/cmdLineTask.py", line 223, in __call__
    	result = task.run(dataRef, **kwargs)
    File "/data1a/ana/products2014/Linux64/hscPipe/2.12.0i_hsc/python/hsc/pipe/tasks/processCcd.py", line 53, in run
        result = ProcessCcdTask.run(self, sensorRef)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
        res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/processCcd.py", line 77, in run
        postIsrExposure = self.isr.run(sensorRef).exposure
    File "/data1a/ana/products2014/Linux64/obs_subaru/HSC-2.17.0b_hsc/python/lsst/obs/subaru/isr.py", line 236, in run
        self.fringe.run(ccdExposure, sensorRef)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
        res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/ip_isr/HSC-2.4.2c_hsc/python/lsst/ip/isr/fringe.py", line 84, in run
        fringes = self.readFringes(dataRef, assembler=assembler)
    File "/data1a/ana/products2014/Linux64/ip_isr/HSC-2.4.2c_hsc/python/lsst/ip/isr/fringe.py", line 113, in readFringes
        raise RuntimeError("Unable to retrieve fringe for %s: %s" % (dataRef.dataId, e))
    RuntimeError: Unable to retrieve fringe for {'taiObs': '2014-04-01', 'pointing': 815, \
        'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', 'field': 'ALIENHOMEWORLD', \
        'ccd': 50, 'expTime': 240.0}: No unique lookup for ['calibDate', 'calibVersion'] from \
        {'taiObs': '2014-04-01', 'pointing': 815, 'visit': 999, 'dateObs': '2014-04-01', \
        'filter': 'HSC-Y', 'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 200.0}: 2 matches


.. _jp_no_raw_skytile:

raw_skytile というテーブルがない
-------------------------------------------------

表記にあるエラーは、例えば、butler で coadd データを読み込もうとしているのに、
butler に十分な ``dataId`` 情報を与えないような時に見られます。以下に、
このエラーを生じるようなスクリプト例を載せます。

.. code-block:: python

    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'tract': 0, 'patch': '5,5'}
    calexp = butler.get("deepCoadd", dataId)

これを実行すると、次のようにしてスクリプトは失敗します。 ::    
    
    Traceback (most recent call last):
      File "./foo.py", line 13, in <module>
        main()
      File "./foo.py", line 10, in main
        calexp = butler.get("deepCoadd", dataId)
      File "/data1/hsc/products/Linux64/daf_persistence/HSC-3.1.0b_hsc/python/lsst/daf/persistence/butler.py", line 224, in get
        location = self.mapper.map(datasetType, dataId)
      File "/data1/hsc/products/Linux64/obs_subaru/HSC-3.10.1/python/lsst/obs/hsc/hscMapper.py", line 142, in map
        return super(HscMapper, self).map(datasetType, copyId, write=write)
      File "/data1/hsc/products/Linux64/daf_persistence/HSC-3.1.0b_hsc/python/lsst/daf/persistence/mapper.py", line 120, in map
        return func(self.validate(dataId), write)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/cameraMapper.py", line 285, in mapClosure
        return mapping.map(mapper, dataId, write)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/mapping.py", line 118, in map
        actualId = self.need(self.keyDict.iterkeys(), dataId)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/mapping.py", line 201, in need
        lookups = self.lookup(newProps, newId)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/mapping.py", line 170, in lookup
        where, self.range, values)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/registries.py", line 170, in executeQuery
        c = self.conn.execute(cmd, values)
    sqlite3.OperationalError: no such table: raw_skytile

この例の場合では、coadd データを指定するのに 'filter' の情報が必要であるにも関わらず、
``dataId`` で指定していないために失敗しています。この場合、
スクリプトを次のように書き換えればエラーは回避されます（黄色でハイライトしている箇所参照）。

.. code-block:: python
   :emphasize-lines: 2
   
    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'tract': 0, 'patch': '5,5', 'filter': 'HSC-I'}
    calexp = butler.get("deepCoadd", dataId)



.. _jp_column_view:

カタログファイル内の coord がカラム型に変換できない
-----------------------------------------------------------

この種のエラーは butler を使って non-native-type 
の変数をカラムの表記で表示させようとする時に生じるエラーです。SourceCatalogs
は ``int`` と ``float`` 型のカラムを返します。しかし、non-native-type
（例えば 'coord'）ではカラム型に変換されません。例えば、以下のような butler 
コードを用意したとします。

.. code-block:: python

    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'visit': 1236, 'ccd': 50}
    sources = butler.get("src", dataId)
    coords = sources.get('coord')

すると、このコードを実行すると以下のようなエラーが吐き出されます。 ::

    Traceback (most recent call last):
      File "./foo.py", line 15, in <module>
        main()
      File "./foo.py", line 11, in main
        coords = sources.get('coord')
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 8717, in get
        return self[k]
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 8649, in __getitem__
        return self.columns[k]
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 2955, in __getitem__
        return self[self.schema.find(args[0]).key]
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 2958, in __getitem__
        return _tableLib.BaseColumnView___getitem__(self, *args)
    lsst.pex.exceptions.exceptionsLib.LsstCppException: 0: lsst::pex::exceptions::LogicErrorException thrown at python/lsst/afw/table/specializations.i:405 in void lsst_afw_table_BaseColumnView___getitem____SWIG_1(const lsst::afw::table::BaseColumnView*, const lsst::afw::table::Key<lsst::afw::coord::Coord>&)
    0: Message: Cannot get column view to Coord field.

このエラーを回避するには、コード内の source 変数をループし、各 coord 変数を
``get()`` で読み込むという方法があります（ハイライト箇所）。

.. code-block:: python
    :emphasize-lines: 4

    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'visit': 1236, 'ccd': 50}
    sources = butler.get("src", dataId)
    coords = [src.get("coord") for src in sources]
    