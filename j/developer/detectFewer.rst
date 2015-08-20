
.. _jp_detectFewer:

detectFewer.py
--------------

このコードは ``meas_algorithms.SourceDetectionConfig`` と
``meas_algorithms.SourceDetectionTask`` から引き継いだ Config とタスククラスを作ります。
このコードでは通常のパイプラインタスクである ``SourceDetectionTask`` 
の代わりに新たなタスクを書き込んで解析処理を実行させています。この例でのポイントは、
パイプラインデフォルトのタスクを、ユーザー定義のタスクに置換する方法です。

コード例は非常にシンプルです。footprint を検出する数を指定する設定パラメータを ``nObjects`` 
で定義しています（ちなみに、デフォルトでは 400 で設定されています）。この設定によって、
パイプライン解析の処理が速くなります。

もとの SourceDetectionTask/Config から Config クラスを引き継ぐことで、
元のタスクにおける処理機能が使えるようになります。パイプラインの SourceDetectionTask
では、天体を検出しカタログを作成するための ``makeSourceCatalog()`` メソッドを使っています。
``detectFewer.py`` では ``nObject`` で検出する天体数を定義します。そして、
デフォルトのタスクの代わりに自身で設定したタスクを使うようにパイプラインに命令するために、
設定パラメータを新しく定義する必要があります。

設定パラメータの新定義は ``my-fast-overrides.config`` というファイルの中で定義されています
（パイプラインの中で天体検出は 2 度呼び出されており、その両方で設定パラメータを再定義する必要があります）。 

.. highlight::
	bash

::

	$ cat my-fast-overrides.config
	
	import detectFewer
	root.calibrate.detection.retarget(detectFewer.FewerSourceDetectionTask)
	root.detection.retarget(detectFewer.FewerSourceDetectionTask)

新たに定義した設定パラメータファイルを使って ``hscProcessCcd.py`` を実行します。

.. highlight::
	bash

::

    $ hscProcessCcd.py /path/to/data/ --rerun=myrerun --id visit=100 ccd=50 -C my-fast-overrides.config
    
``detectFewer.py`` のコードを以下に掲載します。このタスクでは 3 つの ``get<>Name()`` 
メソッドは上書きしません。このスクリプトの中では CmdLineTask からタスクを引き継いで使用します。
このタスクはパイプラインの中で ``SourceDetectionTask`` の代わりに用いられるので、
``get<>Name()`` メソッドは ``hscProcessCcd.py`` において処理されます。 

.. highlight::
	python

::

    import random
    import lsst.pex.config as pexConfig
    import lsst.pipe.base as pipeBase
    import lsst.afw.table as afwTable
    import lsst.meas.algorithms as measAlg

    class FewerSourceDetectionConfig(measAlg.SourceDetectionConfig):
        nObjects = pexConfig.Field(doc="Number of sources to select", dtype=int, optional=False, default=400)

    class FewerSourceDetectionTask(measAlg.SourceDetectionTask):
        """This task serves only to cull the source list and make measurement faster"""

        ConfigClass = FewerSourceDetectionConfig

        def makeSourceCatalog(self, table, exposure, doSmooth=True, sigma=None, clearMask=True):
            if self.negativeFlagKey is not None and self.negativeFlagKey not in table.getSchema():
                raise ValueError("Table has incorrect Schema")
            
            # detect the footprints as usual
            fpSets = self.detectFootprints(exposure=exposure, doSmooth=doSmooth, sigma=sigma,
                                           clearMask=clearMask)

            # shuffle the footprints to ensure they're random across the frame
            n = self.config.nObjects
            fpPos = fpSets.positive.getFootprints()
            random.shuffle(fpPos)

            # delete the excess footprints, and the negative footprints
            del fpPos[n:]
            fpSets.numPos = n
            if fpSets.negative:
                del fpSets.negative.getFootprints()[0:]
                fpSets.negative = None

            # make sources
            sources = afwTable.SourceCatalog(table)
            table.preallocate(fpSets.numPos)
            if fpSets.positive:
                fpSets.positive.makeSources(sources)

            return pipeBase.Struct(sources=sources, fpSets=fpSets)