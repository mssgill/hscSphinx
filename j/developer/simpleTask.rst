
==========
simpleTask
==========

.. _jp_simpletask:

以下では、CmdLineTask を用いた最も基本的なスクリプトを紹介します。
このタスクの中ではいくつかのシンプルな設定パラメータを指定し、使用しています。タスクの用途は
``run()`` メソッドにコーディングされています。もう少し上級者用の例は :ref:`nestedTask.py 
<nestedtask>` に紹介しています。

``simpleTask.py`` は simpleTools コードを使って実行することができます。
HSC パイプラインの中で実際このスクリプトを実行するには、``import`` 構文内の
``_`` を ``.`` に変更してください。例えば以下がパイプラインで実行する際の 
``import`` 構文の書き方です。 ::

     import lsst.pex.config       as pexConfig
     import lsst.pipe.base        as pipeBase

このスクリプトにはヘルプコマンドが組み込まれており、``-h`` をつけて実行すると表示されます。

.. highlight::
	bash

::

     $ ./simpleTask.py -h

このスクリプトをパイプラインスクリプトとして実行する時の例は以下の通りです。この例では、
データリポジトリのあるディレクトリは ``/path/to/data``、このリポジトリ下の visit ID
100 から 110 のデータを 2 core を使って並列計算処理をしようとしています。 ::

     $ ./simpleTask.py /path/to/data -j 2 --id visit=100..110:2

次に、このスクリプトの設定パラメータをコマンドライン上で変更する例を示します。 ::

     $ ./simpleTask.py /path/to/data -j 2 --id visit=100..110:2 --config x=2.71828
     
	 
simpleTask.py
--------------	 
	 
.. highlight::
	python
	 
.. literalinclude:: simpleTools/simpleTask.py
