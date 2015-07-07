
.. _jp_multiband_proc:

====================
Multiband の解析
====================

multiband の解析では、異なる filter の coadd 画像で共通の天体カタログを作成します。
coadd 画像をもとにした天体カタログとその天体の多波長の測光データが必要な場合は、
以下のステップが基本となります。

この解析処理におけるオリジナルの概念は HSC wiki に掲載されているので、
詳細を知りたい人は次のページをご覧ください: 
`coadd 画像による multiband 解析処理について
<http://hscsurvey.pbworks.com/w/page/87953929/Coadd%20Multi-Band%20Processing>`_ 。


multiband 解析を改めて行う必要性
-------------------------------------------------------------------------

Pipeline における stack.py でも coadd 画像をもとに天体カタログが生成されるため、
もし 1 band の天体カタログを使った研究をする場合はこのカタログファイルで事足りるでしょう。
しかし多波長データの測光情報など multiband の天体カタログが必要な場合、
各 band で生成された天体カタログを合わせて使用すると様々な問題を生じてしまいます。
例えば、ある band では検出されるけれど他の band では検出されない天体があるとすると、
この天体の color の情報は利用できません。また、銀河のフラックスを多波長で測定する場合、
stack.py によるカタログのみでは全 band で共通の銀河モデルを使って測光できていないという問題が生じえます。


Forced Photometry
^^^^^^^^^^^^^^^^^

複数の band における天体検出と測定は 'forced photometry' というタスクで処理されます。
forced photometry はある band の画像で検出された天体の座標を使い、
他 band の画像で天体の測定を行います。具体的には、天体検出のための画像として filter を指定し
（例えば HSC-I）、この filter で検出された天体の座標から HSC-G, HSC-R
など他画像を使って天体の測定が行われます。このような解析処理が行われるのは、
あまりに暗いためある filter で検出できない天体のフラックスを測定するためです。例えば、
HSC-I では検出で HSC-R では未検出の天体があった場合、forced photometry によって
HSC-I で得られた天体の座標と同じ位置の HSC-R におけるフラックスを測定することができるということです。
forced photometry を実行することで、限界等級よらず、HSC-I で検出した全天体の
G, R, I, Z, Y band の測定データを得ることが可能となります。


使用する銀河モデルに関する問題
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

多波長にわたる銀河からのフラックスを整合的に測定するためには、全ての filter 
で共通の銀河モデル（exponential, de Vaucouleur など）を使う必要があります。
``stack.py`` による出力データには異なるパラメータの銀河モデルに基づいた測光結果が含まれており、
これら測光結果を用いて得られた color の測定結果は正しくありません。


The multiband solution
^^^^^^^^^^^^^^^^^^^^^^

上記のような問題を解決するするため、全ての band で検出された天体カタログを集め、
同一のfootprint、天体を分離する（deblending）ためのパラメータ、
銀河モデルが全ての band における天体の測定で使用されているか確認するための処理が行われます。

:ref:`coadd processing <jp_coadd_proc>` と同様に、multiband の解析は
``multiBand.py`` というコマンド内で 1 タスクの計算として処理されます。


1 patch 1 プロセス 3 filter の multiband 解析
------------------------------------------------------------------

multiband における測光のみ行って、それ以外の中間計算処理はスキップしてしまいたい場合は
``multiBand.py`` を実行してください。以下に載せている実行例では単一 tract/patch (0/1,1) 
での multiband 解析を 3 band（HSC-R, HSC-I, HSC-Z）に対し行っています。
ここでは既に ``stack.py`` によって coadd 画像が 'myrerun' という rerun 
下に生成されているものとします。今 1 patch の multiband 解析を行っているだけなので、
--nodes, --procs は 1 にしていますが、実際は各計算機環境に応じて適宜してしてください。
例えばこのような 1 プロセスのバッチ処理で 1 patch に対して 3 filter の
multiband 解析を IPMU の計算機で実行した場合、約 2 時間かかります。3 filter の場合と
core を 3 つ使った場合はほぼ同様の時間となります。

::

    $ multiBand.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z --nodes 1 --procs 1 --mpiexec='-bind-to socket' --time 1000 --job multiband

上記コマンド実行例のうち ``--job`` は PBS に投げる job 名で、
``--mpiexec='bind-to socket'`` オプションにより PBS のシステムのパフォーマンスが向上されます。


mutlband 解析によって生成されたカタログファイルを別の rerun に出力する場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

coadd 画像の生成時同様に、multiband 解析による出力データは入力データの rerun
ディレクトリとは別の rerun に出力することが可能です。詳しくは
:ref:`異なる rerun に coadd 画像を出力するには <jp_coadd_rerun_change>` 
をご覧ください。

    
Multiband 解析における処理過程
--------------------------------------------------

multiband 解析における計算処理を処理過程毎に実行する場合のコマンドを、
処理過程毎に簡単な説明をつけながら紹介します。

    
detectCoaddSources.py
^^^^^^^^^^^^^^^^^^^^^

.. note:: detectCoaddSources.py は :ref:`stack.py <stack>` の一部として実装されています。もし ``stack.py`` を使い coadd 画像を生成している場合、既に指定したディレクトリ下に出力データが生成されています。

1 band の coadd 画像から天体を検出し、background のモデルを生成する（1 分程度） ::

    $ detectCoaddSources.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z


mergeCoaddDetections.py
^^^^^^^^^^^^^^^^^^^^^^^


全 band の検出天体から footprint, ピーク座標の情報を集めて 1 つの共通の天体リストを作る（1 分程度） ::

    $ mergeCoaddDetections.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z



measureCoaddSources.py
^^^^^^^^^^^^^^^^^^^^^^

deblending と全 band 共通の footprint, ピーク情報を含む天体リストをもとにした、
各 band の coadd 画像に対する天体の測定（約 60 分） ::

    $ measureCoaddSources.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z



mergeCoaddMeasurements.py
^^^^^^^^^^^^^^^^^^^^^^^^^

各 band の coadd 画像をもとにした天体測定結果を集める（約 2 分）。この処理過程では、
どの band の測定結果を最終天体測定の際に採用するか決める（つまり、最終天体リストを作成する）。 ::

    $  mergeCoaddMeasurements.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z



forcedPhotCoadd.py
^^^^^^^^^^^^^^^^^^

各 band の coadd 画像に対して最終天体リストをもとに天体の測定を行う。この段階での計算処理は
``measureCoaddSources.py`` に非常に似ているが、``mergeCoaddMeasurements.py`` 
において採用された *参照 band* で得られたパラメータ（中心座標、銀河モデル、楕円率等）
で固定して全ての band で天体測定を行う点が異なっている（約 35 分）。 ::

    $ forcedPhotCoadd.py /data/Subaru/HSC/ --rerun myrerun --id tract=0 patch=1,1 filter=HSC-R^HSC-I^HSC-Z
