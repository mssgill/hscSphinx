
.. _jp_errormessages:

======================
共通の Pipeline エラー
======================

もし Pipeline における処理が失敗した場合、ターミナルに表示されているログから、
Pipeline における処理が失敗した時に何が起こったか調べることができます。このログには、
エラーメッセージ以外に有用な情報がたくさん表示されています。以下に、よく遭遇しうる
エラーを紹介します。ここで紹介されていないようなエラーを見つけた場合は、ぜひご連絡ください。

もし ``stdout`` に関係するトラブルがある場合は、:ref:`Debugging <jp_debugging>`
のページをご覧ください。



``_mapper`` ファイルがない
-----------------------------------------

データリポジトリには、mapper という情報を含んだ ``_mapper`` ファイルがあります。
mapper はデータリポジトリの中でデータの位置情報を記録しています（詳しくは
:ref:`j_data_repo` をご覧ください）。もしデータリポジトリに _mapper 
ファイルがないと、以下のようなエラーメッセージが表示されます。 ::

    RuntimeError: No mapper provided and no _mapper available

この場合、_mapper ファイルを作成し、配置してください。IPMU の``master`` 
システムでの解決策は以下の通りです。 ::

    $ cat /lustre/Subaru/SSP/_mapper
    lsst.obs.hsc.HscMapper


astrometry_net_data がない
--------------------------------------------

デフォルトでは Pipeline は astrometry_net_data カタログの登録を行いません。
登録されていない場合は 'none' というダミーデータが設定されてしまいます。解決するためには、
次のような 2 つの方法があります。 ::

#. 'setup astrometry_net_data <catalog>' を実行する

#. hscPipe をリセットし、astrometry_net_data もリセットする
   
以下のエラーでは何か問題か教えてくれています。 ::

    assert(matches is not None)
    AssertionError

    WARNING: hsc.meas.astrom failed ([Errno 2] No such file or directory: 'none/andConfig.py')

例えば、astrometry_net_data の登録を忘れて hscProcessCcd.py を実行した際に生じるエラーを以下にお見せします。
  
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


    
Ambiguous calibration inputs
----------------------------

When you created calibration inputs, you specified ``--detrendId
calibVersion=XXX``.  If you made multiple detrends (e.g. biases) with
different ``calibVersions``, the pipeline code will find them and will
not know which one to use.  This is currently not configurable, but
should be soon.  The solution to remove the conflicting detrend.  For
e.g. a flat, it will be located in the data repo in
``CALIB/FLAT/<YYYY-MM-DD>/<FILTER>/<unwanted-calib>``.  Scan the final
line of the error traceback to determine which detrend caused the
trouble.  They're all in ``CALIB/`` in your data repo.

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


RuntimeError: No mapper provided and no _mapper available.