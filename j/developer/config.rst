
====================
設定パラメータ
====================

.. _jp_minipipe_config:

config コードは pex_config モジュールにあります。ここでは、
2 つのファイル内にある主な成分について記述します。

pex_config には、``python/lsst/pex/config/config.py`` と
``python/lsst/pex/config/configurableField.py`` があります。


Field
-----
特定の設定パラメータは Field の中で定義されています。Field にはパラメータの種類、
そのパラメータの簡単な説明、そしてデフォルトの値が含まれます。

	
ConfigMeta
----------
Config クラスを作るために使われる *メタクラス* が ConfigMeta です。ここでは、
python のクラスがどのようにオブジェクトとして扱われるか理解する必要があります。
このトピックについてよく知らない場合は、まずメタクラスの `入門編の解説
<http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example>`_
を読んでみてください。

	
Config
------
全ての Config クラスの元となるクラスのことです。


ConfigurableInstance, ConfigurableField
---------------------------------------
Config クラスがタスクパラメータを参照する時、``ConfigurableField`` で定義された
``ConfigurableInstance`` というデータ型を変数が使われます。


config.py
---------
以下では ``config.py`` の基本的な成分のみ含んでいます。全体の機能は維持されていますが、
このコードではパイプラインで使う上での安定性や正確性は考慮されていません。
ここでは、パイプラインの使用で要求される複雑な成分は除いたシンプルなコードを例示しています。

.. literalinclude:: simpleTools/lsst_pex_config/config.py
   :language: python


configurableField.py
--------------------

.. literalinclude:: simpleTools/lsst_pex_config/configurableField.py
   :language: python
