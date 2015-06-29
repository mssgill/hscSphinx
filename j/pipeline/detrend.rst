.. role:: red
.. raw:: html
         
   <style> .red {color:red} </style>


.. _jp_detrend:
      
===================================================
一次処理用データの生成
===================================================

全一次処理解析における共通概念
-------------------------------

以下では Bias, Flat, Dark, Fringe データの生成コマンドを紹介します。ここで紹介して
いるコマンドは、IPMU の解析コンピューター ``master`` で試験しています。そのため IPMU 
の ``master`` では Pipeline コマンドの実行は可能なはずですが、解析を実行する際は、
各自データへのパスなどのパラメーター情報に注意してください。また、コマンドのオプションなど
調べたい場合はヘルプオプションを使用してください（ '--help' または '-h'）::

   $ reduceFlats.py -h

   
一次処理用データレジストリの生成
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

デフォルトでは全ての一次処理用データは ``CALIB/`` ディレクトリに生成されます
（``CALIB/BIAS/``, ``CALIB/DARK``, など）。しかし、各一次処理用コマンドの実行後には
*必ず* ``genCalibRegistry.py`` コマンドを実行し、新しく生成された一次処理データを
登録してください。なお、``genCalibRegistry.py`` を初めて実行する際には ``--create`` 
オプションを追加して一次処理用の新しいレジストリを登録してください（``calibRegistry.sqlite``
という sqlite データベースファイルが生成されます）。例えば、各一次処理コマンドの後に
以下のように実行します。::

   $ reduce<Calib>.py [必要なオプション]
   
   # NOTE: 一番最初に calibRegistry.sqlite を生成する時のみ --create オプションが必要
   $ genCalibRegistry.py --create --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

``--root`` オプションはデータリポジトリ内の ``CALIB/`` を直接指定します。また、
``--validity`` オプションによって生成された一次処理用データが使用可能な日数を指定します。
ここでは例として 12 日としていますが、データによってはもっと長い日数を指定する必要があります。
自身のデータに適切な日数を指定してください。

一次処理データのバージョン
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bias, Flat, Fringe といった一次処理データには ``calibVersion`` というラベルを
つけることができます。以下の例では、全てのケースで 'all' というラベルをつけています。
例えば flat データにおいては  'dome' や 'twilight' というラベルをつけることも可能です。

   
Bias データ
-------------

Bias データは ``reduceBias.py`` を使って生成されます。コマンド実行時には複数の
オプションが必要となります。Bias データは filter に依存しないものですが、
reduceBias.py の出力には filter 情報が参照されています。この filter の情報は、
Bias データと取得時に filter 交換機構内で参照していた filter に起因するもので、
Bias データの生成に filter 情報は不要です。

Bias データ生成例 その1
^^^^^^^^^^^^^^^^^^^^^^

::
  
    $ reduceBias.py /data/Subaru/HSC --rerun my_biases --queue small \
        --detrendId calibVersion=all --job bias --nodes 2 --procs 12 \
        --id field=BIAS dateObs=2013-11-04
        
    $ genCalibRegistry.py --create --root /data/Subaru/HSC/CALIB --camera HSC --validity 12
    
オプション詳細:

* ``/data/Subaru/HSC`` データリポジトリの場所
* ``--rerun my_biases``  入出力データを配置する rerun 名 (トリム平均, バイアス引き済データが配置される)
* ``--detrendId calibVersion=all``  最終出力データには ``calibVersion`` が ``all`` と名付けられる
* ``--id``  入力データを指定する
* PBS Torque オプション
  * ``--queue small``  PBS キューの名前
  * ``--job domeI``    ``qstat`` コマンドで参照した際に見られる job 名
  * ``--nodes 2``      2 ノードを使用
  * ``--procs 12``     各ノードで 12 プロセス実行


もし job が途中で失敗しリスタートする場合、または、既存の rerun に新しくデータを
追加しようとする場合、処理パラメーターが異なる出力が生成されるとして Pipeline は
警告を発します。これはパラメーターが不均一なデータが生成されないようにするためです。
もしパラメーターが不均一なデータの生成を気にしないのであれば、コマンドに ``--clobber-config``
オプションを追加することでこの警告を回避することができます。


   
Dark データ
-----------
  
Dark データは ``reduceDark.py`` を用いて生成されます。コマンドの実行に必要な
オプションは基本的には Bias データ生成時と同じです。そのため、オプションの詳細は
上記 Bias データ生成例をご覧ください。

Dark データ生成例 その1
^^^^^^^^^^^^^^^^^^^^^

::
  
    $ reduceDark.py /data/Subaru/HSC --rerun my_darks --queue small \
        --detrendId calibVersion=all --job darks --nodes 2 --procs 12 \
        --id field=DARK dateObs=2013-11-04

    $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

    
Flat データ
-----------

Flat データは ``reduceFlat.py`` コマンドで生成されます。コマンドの実行に必要な
オプションは基本的には Bias データ生成時と同じですので、オプションの詳細は上記
Bias データ生成例をご覧ください。Flat データ生成に関して特記する点は、reduceFlat.py
は各 filter 毎に実行するという点です。以下の例では HSC-I filter の Flat データ生成
に関してのみ紹介します。

          
Flat データ生成例 その1
^^^^^^^^^^^^^^^^^^^^^^

::
  
    $ reduceFlat.py /data/Subaru/HSC --rerun my_dome_i_flats --queue small \
        --detrendId calibVersion=all --job domeI --nodes 2 --procs 12 \
        --id field=DOMEFLAT filter=HSC-I dateObs=2013-11-04 expTime=6.0

    $ reduceFlat.py ... [他 filter]
    $ reduceFlat.py ... [また他の filter]
        
    $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

    
Fringe データ
-------------
  
Fringe データは ``reduceFringe.py`` コマンドによって生成されます。コマンドの実行に
必要なオプションは基本的には Bias データ生成時と同じですので、オプションの詳細は上記
Bias データ生成例をご覧ください。Fringe データに関して特記すべき点を以下にあげます。

#. Fringe データは Y-band データにのみ必要です。現時点では、他の filter では深刻な Fringe の影響は見受けられません。

#. Fringe データ用に別途データを取得する必要はありません。Fringe データは天体データ
   を用いて生成されます。天体データに Fringe の影響が見られなければ、Fringe データの
   影響は少ないと考え、別途解析処理を実行しなくてもよいでしょう。以下の例では MYTARGET 
   という仮想のデータを用いて Fringe データの生成を行っています。
   処理済みの Fringe データは rerun 以下に指定したディレクトリに生成され、
   生成された Fringe データの FITS ヘッダーの OBJECT には MYTARGET という情報が
   登録されます。

   
Fringe データ生成例 その1
^^^^^^^^^^^^^^^^^^^^^^^^

::
  
    $ reduceFringe.py /data/Subaru/HSC --rerun my_fringe --queue small \
        --detrendId calibVersion=all --job fringe --nodes 2 --procs 12 \
        --id field=MYTARGET dateObs=2013-11-04 filter=HSC-Y
        
    $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

