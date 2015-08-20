
==============
ArgumentParser
==============

パイプラインで使われている引数の解析（argumentParser）は、もとは、python の 
``argparse`` という引数解析のクラスから求められます。コマンドラインの引数の多くは、
ほとんど全てのパイプラインタスクで必要となります。argumentParser を使う多くのタスクでは、
通常パイプラインで使うコマンドラインの引数を利用可能にします。中でも最も便利な引数は
``--id`` で、HSC データを指定する際に使用されるコマンドラインの引数です。

以下の例では argumentParser.py 内の基本成分だけ掲載しています。このコードのオリジナルは
``pipe_base`` モジュールの中にあります。


argumentParser.py
-----------------

.. literalinclude:: simpleTools/lsst_pipe_base/argumentParser.py
