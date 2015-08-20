

======
PipeQA
======

.. contents::
   :local:
   :depth: 2


はじめに
------------------------

パイプラインには、天体データの一次処理や重ね合わせを行った出力データの精度を評価するためのデータ評価システム（pipeQA）が用意されています。このシステムは 2 つのパッケージで構成されています: ``testing_displayQA`` （ウェブベースで結果を表示するツール） ``testing_pipeQA`` （図や評価結果の値をパイプラインベースで出力してくれるツール）。 pipeQA の使用には様々なオプションが利用可能なウェブサーバーとデータベースが必要です（詳細は以下）。


計算機の環境に依存した pipeQA の設定
---------------------------------------------

もしデータベースのサイズが大きいデータに対して pipeQA を実行したい場合、
Apache + PostgreSQL を用いた環境で pipeQA を実行すると、
速く安定して計算処理を行うことができます。しかし、もし小容量のデータに対して pipeQA
を実行したいか、使用している計算機環境では Apache か PostgreSQL が使用できないか
インストールしたくない場合、PHP か Sqlite を使って pipeQA を実行することも可能です。

Apache + PostgreSQL（インストールは難しいが、実行速度は速い）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pipeQA の基本的なインストール方法を紹介します。pipeQA による並列計算によって、
PostgreSQL ではデータベースの複数のデータに対して処理を行うことができます。
ここでは Apache と PostgreSQL のインストールを紹介します。

.. highlight::
	bash

* apache のインストールと起動

    * php, php-pdo, php-pgsql のインストール（例：redhad 系で yum を使う場合） ::

        $ yum install php
        $ yum install php-pdo
        $ yum install php-pgsql

* postgresql のインストールと起動

    * createdb ...
    * create user ... (set privileges for create table)


PHP + Sqlite（インストールは簡単だが、処理は遅い）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

もし root 権限がないか、Apache, PostgreSQL を自身の計算機にインストールしたくない場合;
パイプラインに含まれる Sqlite と最新の PHP (> 5.4) を使い簡易サーバーを設置する方法があります。

最新の PHP のバージョンは `PHP <http://php.net/downloads.php>`_
にて見つけられます。多くの Linux マシンではデフォルトで PHP 5.3 のバージョンが使用されていますが、
これはウェブサーバーでは使用されていませんので、最新のものを使用してください。

.. highlight::
	bash

* PHP バージョン > 5.4 をインストールする。最新の PHP は $HOME/usr ディレクトリにインストールされるため、既存の PHP を干渉しない。設定方法は以下。 ::

   $ tar xvzf php-tarball.tar.gz
   $ cd php/
   $ ./configure --prefix=$HOME/usr
   $ make
   $ make install

* 簡易ウェブサーバーの起動（localhost:8000/ から閲覧可能）。 ::

   # サーバーディレクトリに移動
   $ cd $HOME/directory/to/serve/

   # ポート番号 1024 以上でサーバーを起動（例ではポート 8000 を使用）
   $ ~/usr/bin/php -S localhost:8000 -t .


クイックスタート
------------------------------

まず最初に (1) Apache + PHP + PostgreSQL か (2) PHP > 5.4
をインストール/設置してください。

Apache + PostgreSQL
^^^^^^^^^^^^^^^^^^^^^^

::

    # データベースの接続設定を確認する
    $ cat ~/.pqa/db-auth.py
    host = "postgresdb.master.ipmu.jp"
    port = "5432"
    user = "username"
    password = "secret"
    dbsys = "pgsql"

    # 環境変数を設定し、pipeQA を実行する rerun ディレクトリを作る
    $ export WWW_ROOT=$HOME/public_html/qa
    $ mkdir $WWW_ROOT
    $ export WWW_RERUN=cosmos
    $ export PGPASSWORD=secret

    # pipeQA の rerun ディレクトリを作成し、pipeQA を実行する
    $ newQa.py -c green -p hsc $WWW_RERUN
    $ hscPipeQa.py /data/Subaru/HSC --rerun cosmos --id visit=1000..1020:2 ccd=0..103 -j 20

    # http://master.ipmu.jp/~username/qa/cosmos/ にいき pipeQA による評価結果を調べる

PHP + Sqlite
^^^^^^^^^^^^^^^

::

    # 設定を確認する
    $ cat ~/.pqa/db-auth.py
    dbsys = "sqlite"

    # 環境変数を設定し、pipeQA を実行する rerun ディレクトリを作る
    $ export WWW_ROOT=$HOME/public_html/qa
    $ mkdir $WWW_ROOT
    $ export WWW_RERUN=cosmos

    # pipeQA の rerun ディレクトリを作成し、pipeQA を実行する
    $ newQa.py -c green -p hsc $WWW_RERUN
    $ hscPipeQa.py /data/Subaru/HSC --rerun cosmos --id visit=1000^1002 ccd=0..103 -j 2

    # ローカル環境で PHP サーバーを起動する
    $ cd ~/public_html/
    $ php -S localhost:8000 -t .
    
    # http://localhost:8000/qa/cosmos/ にいき pipeQA による評価結果を調べる


設定
-------------

pipeQA を実行するためにはデータベースへの接続情報が必要となります。そしてこの接続情報は、
自身のディレクトリ ``~/.pqa/db-auth.py`` のパラメーターファイルに格納されます。
IPMU の master（master.ipmu.jp）における例を以下に載せます。 ::

    $ cat ~/.pqa/db-auth.py
    host = "postgresdb.master.ipmu.jp"
    port = "5432"
    user = "username"
    password = "secret"
    dbsys = "pgsql"

Sqlite を使用する際には、host, port, user, password の情報は不要ですが、
``dbsys = 'sqlite'`` の登録が必要となります。 :: 

    $ cat ~/.pqa/db-auth.py
    dbsys = "sqlite*


.. ::
    * ~/.hsc/db-auth.paf (db where pipeQA loads data from [currently not enabled])::

    database: {
        authInfo: {
            host: "157.82.237.169"
            port: "5432"
            user: "kensaku"
            password: "secret"
        }
    }

pipeQA は 2 つの環境変数を使用します: ``WWW_ROOT`` と ``WWW_RERUN`` です。
もし PostgreSQL を使用する場合には 3 つ目の環境変数 ``PGPASSWORD`` を使うと便利です。
この ``PGPASSWORD`` では自身が使用しているデータベースへのパスワードを保存してくれます
（データベースへのパスワードが環境変数として保存されます）。 ::

    # pipeQA を実行する rerun ディレクトリを指定
    $ export WWW_ROOT=$HOME/public_html/qa

    # pipeQA の評価結果を格納する rerun ディレクトリ $WWW_ROOT/$WWW_RERUN を指定
	# もし PostgreSQL を使用している場合は、newQa.py により生成されたデータベースは pqa_<WWW_RERUN> と呼ばれる
    $ export WWW_RERUN=cosmos

    # (PostgreSQL の場合のみ) 未設定だと、newQa.py を実行する際に要求される
    $ export PGPASSWORD=secret
    

newQa.py で pipeQA の rerun ディレクトリを生成する
------------------------------------------------------

pipeQA を実行する前に、``newQa.py`` で評価結果の閲覧用ウェブサイトを
生成する必要があります。 ::

    $ newQa.py -c green -p hsc $WWW_RERUN

このコマンドによって WWW_ROOT ディレクトリ下に pipeQA 用の rerun 
ディレクトリが生成されます。このウェブサイトでは green CSS スタイルを使用しています。
もし PostgreSQL を使用している場合には、pqa_<WWW_RERUN> という新しいデータベースも
生成されます。``newQa.py`` で使用できる引数を以下にまとめます。 ::

    -c {blue,green,red,brown}, --color {blue,green,red,brown}
                          スタイルの色を指定
    -f, --force           pipeQA がある場合は強制的に再インストール
    -F, --forceClean      pipeQA による評価が行われている場合は、データを削除して再インストール
    -r ROOT, --root ROOT  WWW_ROOT を上書き
    -n, --noquery         Don't query about options ... user knows what user is
                          doing.
    -p {lsst,hsc,sc}, --project_icons {lsst,hsc,sc}
                          プロジェクトを特定するためのアイコンを設定する
						 


pipeQA の実行
-----------------------------

pipeQA の実行方法は様々あります。最もよく使われる方法は、rerun ディレクトリ下の
出力データに対し pipeQA を実行し、さにティーチェックを行う方法です。この方法で pipeQA
を実行した場合、評価結果はカタログの値と比較することで得られます。しかし、他のデータと
自身のデータを比較したい場合（例えば、同じ観測領域で撮られた異なる visit データ）、
同じデータを用いて解析された異なる 2 つの rerun 内のデータを比較したい場合
（例えば、異なるパラメータで解析されたデータ）は、別の方法を使って pipeQA を実行します。


通常の pipeQA の使い方
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ここではまず、ある rerun での出力データの精度を評価するというような、
pipeQA の通常の使い方を説明します。

**Python 並列処理を用いる**

**Sqlite で多くの core を使用するようなことはしないでください!**
  Sqlite では並列処理は適しておらず、pipeQA の実行に時間がかかります。
  PostgreSQL では約 20 の並列処理が可能であるので、このような問題は起こりません。

* 一次処理済天体データに対する pipeQA（-j 20 で 20 CPU core を使うことを指定） ::

    $ hscPipeQa.py /data/Subaru/HSC --rerun my_rerun --id visit=1234..1240:2 ccd=0..103 -j 20

* coadd データに対する pipeQA（-j 2 で 2 CPU core を使うことを指定） ::

    $ hscCoaddQa.py /data/Subaru/HSC --rerun my_rerun --id tract=0 patch=5,4^5,5 filter=HSC-I -j 2

    
**Batch 処理を行う**

* 一次処理済天体データに対する pipeQA, 1 process あたり 8 node で 4 node 使用する（NOTE: コマンドのパフォーマンスを向上するために --mpiexec='-bind-to socket' を実行） :: 

    $ poolPipeQa.py /data/Subaru/HSC --rerun my_rerun --id visit=1234..1240:2 ccd=0..103 --job=poolqa --nodes=4 --procs=8 --mpiexec='-bind-to socket'

* coadd データに対する pipeQA, 1 process あたり 8 node で 4 node 使用する（NOTE: コマンドのパフォーマンスを向上するために --mpiexec='-bind-to socket' を実行） :: 

    $ poolCoaddQa.py /data/Subaru/HSC --rerun my_rerun --id tract=0 filter=HSC-I --job=poolcoadd --nodes=4 --procs=8 --mpiexec='-bind-to socket'


pipeQA による評価結果の比較法
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ここでは 2 つのデータの pipeQA による評価結果を比較する方法について紹介します。
2 つのデータを比較するためのタスクは Python の並列処理でのみ実行され、
バッチ処理は行えません。

**visit 同士の比較の場合**

同じ rerun にある 2 つの visit データを比較する（以下で選んでいる CCD は同じ天域を観測しているものとします） ::

    $ hscPipeCompare.py /data/Subaru/HSC --rerun=cosmos --id visit=1236 ccd=0..103 --refVisit=1238

**rerun 同士の比較の場合（一次処理済データ）**

解析パラメータが異なる 2 つの rerun 内のデータを比較する（例えば、パイプラインのパラメータを変更した際の影響を比較したい場合） ::

    $ hscPipeCompare.py /data/Subaru/HSC --rerun=cosmos --id visit=1236 ccd=0..103 --refRerun=cosmos2

**rerun 同士の比較の場合（coadd データ）**

coadd データを比較する時、rerun 同士の比較のみが可能です（visit とは異なり、coadd データは完全に同じ領域をカバーしています） ::

    $ hscCoaddCompare.py /data/Subaru/HSC --rerun=cosmos --id tract=0 patch=5,5 filter=HSC-I --refRerun=cosmos2

**coadd　データと一次処理済データの場合**

coadd データと 一次処理済データ（visit 単位）の比較を行うこともあるかもしれません。
その場合は、以下の方法が使えます。 ::

    $ hscCoaddCompare.py /data/Subaru/SSP --rerun=cosmos --id tract=0 patch=5,5 filter=HSC-I --refVisit=1236



delQa.py を用いてある rerun の visit か tract を削除する
-----------------------------------------------------------------------------

基本的な使い方 ::

    $ delQa.py $WWW_RERUN <group> -p [-n]

    # -n データの情報をレポートする
    # -p データの情報をレポートする（詳細）

``<group>`` で参照される引数で visit か tract を定義します。一次処理済データの場合
'1234-i'（visit 番号 1234 の I-band データ）という形で指定し、coadd データの場合
'9375-HSC-I-i'（HSC-I で取得された tract 番号 9375）という形で指定します
（どちらの場合も 'i' は filter を意味します）。

もし、どのデータをデータリポジトリから削除し、レジストリから削除するか調べたい場合、
``-n`` の引数をつけてパイプラインを実行してください。この引数によって、データを削除せずに、
その情報をレポートしてくれます。

``-p`` を使うとさらに詳細にデータの情報をレポートしてくれます。

例えば、coadd データの評価結果からある tract のデータを削除したいとします。
ウェブ上の pipeQA サイトを見て、データの名前を確認します。今回は、 ``mergetest``
という rerun ディレクトリにある HSC-I の tract 番号 9375 のデータを削除するとします。 ::
    
    $ delQa.py mergetest 9375-HSC-I-i -p


