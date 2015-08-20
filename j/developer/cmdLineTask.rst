
===========
CmdLineTask
===========

パイプラインではどのように解析が実行されているか理解するためには、
パイプライン成分の中でも最も重要な ``CmdLineTask`` と ``TaskRunner`` 
を理解するのが良いかもしれません。``CmdLineTask`` には ``Task`` からその機能を引き継ぎつつ、
さらに追加のコードが含まれています。``CmdLineTask`` にはパイプラインの ``ArgumentParser`` 
と ``TaskRunner`` が含まれており、これらのパイプライン成分によって
パイプラインスクリプトと同様の実行可能なスクリプトを構築することができます。


TaskRunner
----------

``TaskRunner`` はコマンドラインから dataId で指定されるデータを分け、python の
``multiprocessing`` モジュールで並列処理させるための Config クラスです。


CmdLineTask
-----------

``CmdLineTask`` は ``task`` から導出された特殊な Config クラスです。``CmdLineTask`` 
から導出されたクラスの ``run()`` メソッド内に自身で作成したコードを含めることで、
``YourCmdLineTask`` 内の ``parseAndRun()`` メソッドを呼び出すことで、
実行可能なスクリプトを簡単に作成することができます。

.. highlight::
	bash
	
::

    #!/usr/bin/env python
    import yourModule
    yourModule.YourCmdLineTask.parseAndRun()
    

cmdLineTask.py
--------------

.. highlight::
	python
	
.. literalinclude:: simpleTools/lsst_pipe_base/cmdLineTask.py
