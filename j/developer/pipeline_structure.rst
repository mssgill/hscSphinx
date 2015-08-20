
=======================
パイプラインの構造
=======================

以下ではパイプラインがどのように各 visit データを処理しているかの概要を示しています。
データ処理の中では多くのタスクを参照しています。もしパイプラインタスクに不慣れな場合は、
まずは :ref:`jp_coreComponents` をざっと読むのをお勧めします。

パイプラインスクリプトは複数の ``task`` が共通のブロックとして読み込まれます。
ある特定のスクリプトでどのような処理が行われているか理解したい場合は、コマンドラインで 
``--show tasks`` の引数を指定すれば、そのスクリプト内で呼び出される全てのタスクと
サブタスクを一覧で表示してくれます。例えば、``hscProcessCcd.py`` 
ではどのようなタスクが呼び出されているか見てみましょう。

.. highlight::
	bash
	
::

    $ hscProcessCcd.py /data/Subaru/HSC --show tasks
    
    <log lines not shown>
    Subtasks:
    calibrate: lsst.pipe.tasks.calibrate.CalibrateTask
    calibrate.astrometry: lsst.obs.subaru.astrometry.SubaruAstrometryTask
    calibrate.detection: lsst.meas.algorithms.detection.SourceDetectionTask
    calibrate.initialMeasurement: lsst.meas.algorithms.measurement.SourceMeasurementTask
    calibrate.initialMeasurement.replaceWithNoise: lsst.meas.algorithms.replaceWithNoise.ReplaceWithNoiseTask
    calibrate.measureApCorr: lsst.meas.algorithms.measureApCorr.MeasureApCorrTask
    calibrate.measurePsf: lsst.pipe.tasks.measurePsf.MeasurePsfTask
    calibrate.measurement: lsst.meas.algorithms.measurement.SourceMeasurementTask
    calibrate.measurement.replaceWithNoise: lsst.meas.algorithms.replaceWithNoise.ReplaceWithNoiseTask
    calibrate.photocal: lsst.meas.photocal.PhotoCal.PhotoCalTask
    calibrate.repair: lsst.pipe.tasks.repair.RepairTask
    deblend: lsst.meas.deblender.deblend.SourceDeblendTask
    detection: lsst.meas.algorithms.detection.SourceDetectionTask
    fakes: lsst.pipe.tasks.fakes.DummyFakeSourcesTask
    isr: lsst.obs.subaru.isr.SubaruIsrTask
    isr.assembleCcd: lsst.ip.isr.assembleCcdTask.AssembleCcdTask
    isr.crosstalk: lsst.obs.subaru.crosstalk.CrosstalkTask
    isr.fringe: lsst.ip.isr.fringe.FringeTask
    measurement: lsst.meas.algorithms.measurement.SourceMeasurementTask
    measurement.replaceWithNoise: lsst.meas.algorithms.replaceWithNoise.ReplaceWithNoiseTask
    qa: hsc.pipe.tasks.qa.QaTask
    qa.seeing: hsc.pipe.tasks.measSeeingQa.MeasureSeeingMitakaTask
    <log lines not shown>

PBS/Torque や Slurm cluster で処理する場合、``reduceFrames.py`` では
ProcessExposureTask を使います。ProcessExposureTask は主に 2 
つの解析成分で構成されています。そのうち多くの解析処理は ``processCcd`` で行われます。
ProcessExposureTask では cluster におけるバッチ処理を実行させます。また、
このタスクでは ``BatchPoolTask`` 内のクラスを継承しています。 ::

    hscPipe.ProcessExposureTask(hscPipe.BatchPoolTask)
    
    - processCcd          built with makeSubTask() ... (see SubaruProcessCcdTask below)
    - photometricSolution built with makeSubTask()


パイプラインにおける CCD ごとの解析は ``ProcessCcdTask`` によって実行されます。
パイプラインではすばるデータ解析用に ``SubaruProcessCcdTask`` というタスクが用意されています。
このタスクは ``ProcessCcdTask`` に、観測されたデータの精度を検証する ``qa`` 
というサブタスクを含んだものとなっています。
以下ではタスク内の階層構造はパイプライン処理の構造を示しています。さらに併せて、
タスク内のパッケージにに関連するネームスペース（例えば、meas_algorithms には ``meas_alg.``）
と、関連するファイル名も紹介しています。これらタスク内のクラス階層構造を UML
（Unified Modeling Language）ダイアグラムを使わずに説明するのは難しいのですが、
以下ではなんちゃってコードを使って説明しています。 ::

    hscPipe.SubaruProcessCcdTask(pipe_tasks.ProcessCcdTask)               (hsc/pipe/processExposure.py)
    
    # SubaruProcessCcdTask が 親タスクである ProcessCcdTask の run() を呼び出す
    pipe_tasks.ProcessCcdTask(self, dataRef).run()

         # ProcessCcdTask は ProcessImageTask
         pipe_tasks.ProcessCcdTask(pipe_tasks.ProcessImageTask)           (pipe/tasks/processCcd.py)

         # サブタスク [makeSubTask() を使って作られたもの]
         --> isr:         ip_isr.IsrTask(Task)                            (ip/isr/isr.py)
         --> calibrate:   pipe_tasks.CalibrateTask(Task)                  (pipe/tasks/calibrate.py)

         # 最後に、多くの処理が ProcessImageTask で実行される
         pipe_tasks.ProcessImageTask(self, dataRef).process()
         
              pipe_tasks.ProcessImageTask(pipe_base.CmdLineTask)          (pipe/tasks/processImage.py)

              # サブタスク [makeSubTask() を使って作られたもの]
              --> detection:     meas_alg.SourceDetectionTask(Task)       (meas/algorithms/detection.py)
              --> deblend:       meas_alg.SourceDeblendTask(Task)         (meas/algorithms/deblend.py)
              --> measure:       meas_alg.SourceMeasurementTask(Task)     (meas/algorithms/measure.py)
                
    # SubaruProcessCcdTask から 'qa' 処理を実行
    --> qa:               hsc_pipe.QaTask(Task)                           (hsc/pipe/qa.py)


Notes:

'isr' = 'Instrument Signature Removal' (つまり、一次処理のこと)
        