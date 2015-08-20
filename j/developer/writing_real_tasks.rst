
==================
タスクを編集する
==================

ここでは、いくつかの難易度レベルで ``CmdLineTasks`` を編集する方法を掲載しています。
これらのコード例では既存のパイプラインのタスクをを使って、
実際の解析で使えそうないくつかの処理を紹介します。

このように、既存のタスクを活用しながら新たにタスクを編集したい理由として :

* パイプライン既存の dataId を指定する引数やバッチ処理タスクを活かしたい
* デフォルトとはかなり異なる方法でパイプラインを実行したい

などがあげられるでしょう。

CmdLineTask から引き継いでいるタスクの一般的な形式を以下に載せています。以下の例では、
None を返すために 3 つの ``_get<>Name()`` メソッドをオーバーロードしています。
通常パイプライン内では、このメソッドは設定パラメータとパイプラインパッケージのバージョンを
トラックするために使われています。タスクを実行する上ではこのメソッドは必要ですが、
単に ``None`` を返すだけなので、気にせず実行してください。 ::

    #!/usr/bin/env python
    import lsst.pipe.base as pipeBase
    import lsst.pex.config as pexConfig
    
    class MyTask(pipeBase.CmdLineTask):
        _DefaultName = 'mytask'
        ConfigClass = pexConfig.Config()
        
        def run(self, dataRef):

            ################################
            # dataRef に関して何か処理を行う
            ################################
            
            return
            
        # CmdLineTask からタスクを引き継いでいるなら _get<>Name() をオーバーロードする
        def _getConfigName(self):
            return None
        def _getEupsVersionsName(self):
            return None
        def _getMetadataName(self):
            return None
            
    if __name__ == '__main__':
        MyTask.parseAndRun()

以下の例では、パイプラインを使って解析したデータに対して非常に単純な処理をするために、
基本的なタスクを使っています。


.. toctree::
   :hidden:

   findTract
   detectFewer
   
:ref:`findTract.py <jp_findtract>`

	このスクリプトでは、ある visit, CCD データから　tract を調べるために CmdLineTask 
	を作ります。

:ref:`detectFewer.py <jp_detectFewer>`

	この例では、パイプラインタスクを上書きし、そのタスクの振る舞いを変えるような
	タスクの編集方法を紹介しています。このスクリプトはパイプラインの SourceDetectionTask
	タスクを、検出数を少なくするような天体検出タスクに置き換えています。これにより、
	パイプラインのスクリプトの実行速度が速くなります。


    
    
.. findTract
.. runAFew
.. runPostISRCCD