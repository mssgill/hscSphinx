
========================
パイプラインの成分
========================

.. _jp_coreComponents:

パイプラインのコマンドで実行される基本的な成分を task（タスク）と言います。
タスクには、天体の検出や測定など解析の諸段階で用いられる計算処理が含まれています。
どのタスクにも多くの設定パラメータがあり、これらのパラメータは ``Config`` 
クラスの中で定義されています。``Config`` クラスのコードを理解することは非常に難しいのですが、
単にパイプラインを理解して使うだけならコードの中身まで理解する必要はありません。
こうした ``Config`` クラスを使って自分で ``task`` コマンドを書くためには ``CmdLineTask`` 
を理解することが一番重要かもしれません。

ここでは、タスクの成分がどのように機能するか簡単に説明し、2-3 の簡単なタスクを紹介します。
もし、タスクをどう書くか興味がある場合は、以下をスキップして :ref:`タスクの例 <simpleExamples>`
まで進んでください。

.. warning:: 
	ここでは、パイプラインの成分のうち最も重要な ``Config`` クラスを簡単に紹介します。
	コード自体を調べたい時の具体的な調べ方も説明します。
	これから記述する概説で、パイプライン成分の主な概念を理解してもらえたら嬉しいです。

Download tarball :download:`simpleTools.tar`

.. toctree::
   :maxdepth: 2

   task
   cmdLineTask
   config
   argumentParser


CmdLineTask の実行方法
---------------------------------

.. _jp_runCmdLineTask:

.. highlight::
	bash

CmdLineTask を書いてタスクを実行したい時、そのスクリプトは数行ですみます。以下では
``yourScript.py`` というスクリプトの中身を紹介しています。このスクリプトでは 
``YourCmdLineTask`` （恐らく ``CmdLineTask`` をベースに改変したもの） 
と自身で設定した ``yourModule`` を取り込んでいます。 ::

    #!/usr/bin/env python
    import yourModule
    yourModule.YourCmdLineTask.parserAndRun()

simpleTools コードで作ったスクリプト（simpleTask.py）は以下のように実行します。HSC 
パイプラインの中で使われているコードはもっと多くのコマンドオプションが呼び込まれています。
中でも最も重要なものを以下に表示しました。では、まずこのスクリプトのヘルプを見てみましょう。 ::

    $ simpleTask.py -h
    usage: simpleTask.py input [options]
    
    positional arguments:
      ROOT                  path to input data repository
    
    optional arguments:
      -h, --help            show this help message and exit
      -c [NAME=VALUE [NAME=VALUE ...]], --config [NAME=VALUE [NAME=VALUE ...]]
                            config override(s), e.g. -c foo=newfoo bar.baz=3
      -j PROCESSES, --processes PROCESSES
                            Number of processes to use
      --id [KEY=VALUE1[^VALUE2...] [KEY=VALUE1[^VALUE2...] ...]]
                            id parameters

``ROOT`` は解析リポジトリのディレクトリ構造の元となるディレクトリです。``-c`` または
``--config`` はコマンドライン上で設定パラメータを上書きさせる時のパラメータです。``--id`` 
パラメータを使うと、解析に使用したいデータを特定することができ、visit や CCD 番号を入力し、
スクリプトを実行します。例えば、``A..B:C`` と設定した場合は、A から B まで C 
飛ばしの番号を指定しています。また、連続しない番号を選択したい時は ``^`` を使って ``--id``
を指定することができます。``-j N`` は並列して計算処理ための core 数（N）を指定します。
``--id`` で指定したデータの解析処理はそれぞれ独立に実行されます。以下の例では
``/path/to/data`` にある、visit 100, 102, 104 の CCD ID 40, 60 のデータの処理を行います。
このデータ処理は 2 core を使った並列計算で行われます。 ::

     $ simpleTask.py /path/to/data --id visit=100..104:2 ccd=40^60 -j 2

``simpleTask.py`` ではデータを探すわけではなく、自身が設定したタスクをループし、
その結果をターミナル上に出力してくれます。

   
CmdLineTask の簡単な例
---------------------------

.. _jp_simpleExamples:

以下では ``CmdLineTask`` スクリプトをゼロから書く方法を例示しています。
これらのタスクではパイプラインにおける天体の測光タスクを模倣しています。具体的には、
シンプルな計算処理を行い、その結果をターミナル上に出力してくれます。``simpleTask.py``
スクリプトでは、最小限のデータ一覧が表示されます。また、``nestedTask.py`` スクリプトでは
``CmdLineTask`` の使用例を示しています。

``simpleTask.py`` も ``nestedTask.py`` も次の tarball に含まれています
（:download:`simpleTools.tar`）。


.. toctree::
   :maxdepth: 1
   
   simpleTask
   nestedTask