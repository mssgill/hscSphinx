.. highlight::
	bash

======================
予備知識
======================

HSC パイプラインでは、データ処理のいろいろな局面に共通して知っておいた方がよい種々の事項があります。
そのいくつかは開発者と意思疎通するための基本用語であり、
また、パイプラインのコードを有効に使うための情報も含まれます。

.. There are a variety of things which are common to all tasks associated
.. with a processing run.  Some of the things are just basic terminology
.. that you'll need to communicate with developers, while others are of
.. more practical importance for actually running the pipeline code
.. effectively.

.. _jp_back_eups:

EUPS
----
EUPS は、LSST と HSC プロジェクトで利用されている、
プロジェクト内製によるパッケージ管理ソフトウェアです。SDSS サーベイの運用中に
Nikhil Padmanabhan が最初に開発したものをベースに、
LSST と HSC プロジェクトのパッケージ管理のためにプロジェクトにより再度書き直しを行いました。
ここでいう「パッケージ管理」とは、RedHat Linux での `yum`、Debian Linus での `apt-get`、
OSX での `Macports` や `Homebrew` に相当するものです。例えば、
あなたが何らかのソフトウェアパッケージをインストールしたいと思った時に、
他のソフトウェアとの複雑な依存関係がよく問題となりますが、
「パッケージ管理」ソフトウェアがこれを解決をしてくれます。
HSC で EUPS を使う理由は、先の yum などと比べて便利な機能を持つためです。
たとえば、あるソフトウェアの別バージョンを同一システム内で使い分けることが出来ます。
一般的には、システムにとあるバージョンの FFTW をインストールすると、
一貫してそのバージョンを使わなければなりませんが、EUPS を使えば、FFTW 
の複数のバージョンをインストールして、状況に応じて必要なバージョンを選択することが出来ます。
また、異なるユーザ（あるいは同一ユーザでも）が、
異なるバージョンのソフトウェアを同時に使うことも出来ます。

.. EUPS is the in-house package manager used by LSST and HSC.  It was
.. originally developed by Nikhil Padmanabhan during the SDSS survey, and
.. has since been rewritten (and then re-rewritten) to manage the LSST
.. and HSC code.  The term package manager here refers to a system like
.. `yum` (Redhat Linux), `apt-get` (Debian Linux), Macports (OSX), or
.. Homebrew (OSX).  When you wish to install some software package, the
.. required dependencies can be a complicated mess to sort out, and
.. package managers are meant to handle this for you.  The EUPS is used
.. here because it has some additional functionality that the others
.. lack.  Namely, it permits a user to use different versions of the same
.. software.  Rather than installing e.g. FFTW and then having to use
.. that installed version, EUPS lets you install several versions, and
.. choose which one you'd like to work with at a given time.  Different
.. users (or the same user) can all use different versions
.. simultaneously.
..
.. In order to enable EUPS in your current shell, you must source a
.. script appropriate for the shell you're using.  If you're not sure
.. which shell you use, type ``echo $SHELL`` and it will say either
.. ``/bin/bash`` or ``/bin/tcsh``.  Note that you must source the file,
.. not execute it::

EUPS を使うには、作業中のシェル用の初期化スクリプトを "source" します。
もしも使っているシェルの種類が分からなければ、 ``echo $SHELL`` とタイプすれば、
``/bin/bash`` や ``/bin/tcsh`` として利用中のシェルへのパスが表示されます。
初期化スクリプトは "source" するのであって、実行してはいけないことに注意して下さい。 ::

    # bashを使う場合
    $ source ${PRODUCT_DIR}/eups/default/bin/setups.sh

    # cshまたはtcshを使う場合
    $ source ${PRODUCT_DIR}/eups/default/bin/setups.csh


初期化スクリプトはパイプラインを利用するための多種のシェル関数や環境変数を設定します。
新なシェル（端末エミュレータ）を開いて作業する場合には、毎回この初期化を行う必要があるので、
上記のコマンドのエイリアスを `~/.bashrc` や `~/.cshrc` で設定したり、
他の作業と環境変数などが干渉しなければ、その中で初期化スクリプトを source 
してしまうのもよいかもしれません。 ::

    # .bashrc でのエイリアス設定の一例
    alias setupHsc='source /data1a/ana/products2014/eups/default/bin/setups.sh'

上記エイリアスを設定しておけば、次回ログインからは以下のコマンドをタイプすれば初期化が出来ます。 ::

     $ setupHsc


.. Doing this sets a number of shell functions and environment variables
.. that enable eups commands in your current shell.  Since you'll have to
.. do this in every shell where you intend to work, you probably want to
.. create an alias for it in your `~/.bashrc` (or `~/.cshrc`), or simply
.. source the setups.sh file directly there::
..
..     alias setupHsc='source /data1a/ana/products2014/eups/default/bin/setups.sh'
..
.. Then you can enable EUPS on subsequent logins with::
..
..     $ setupHsc
..
     
以下に非常によく使われる eups コマンドを紹介します。
.. Here are the most common eups commands.

#. `help`::
    
     $ eups -h


#. `list` ... システムにインストールされたパッケージをリストアップする::

     # インストールされているすべてのパッケージを表示
     $ eups list

     # インストールされている obs_subaru パッケージのバージョンを表示
     $ eups list obs_subaru
     
     # インストールされている obs_* にマッチするすべてのパッケージを表示
     $ eups list obs_*
     
     # 現在どのパッケージ＋バージョンを利用するように設定（'setup'）されているかを表示 
     $ eups list -s

     
#. `setup` ... 指定したパッケージ＋バージョンを利用するようにその依存関係を含めて設定する::

     # HSCパイプラインのバージョン 2.12.0f_hsc を利用設定 (-v は 'verbose' 「詳細表示」の意味)
     $ setup -v hscPipe 2.12.0f_hsc
     
     # 'HSC'タグ（開発者推薦）の付いているパッケージ ＋ バージョンの組合せでHSCパイプラインを利用設定::
     $ setup -v hscPipe -t HSC
	 
.. note::
	もし ``You are attempting to run "setup" which requires
	administrative privileges, but more information is needed in 
	order to do so.  Authenticating as "root" Password: ``
	というエラーを見かけたなら、それは、``setups.sh`` ファイルを ``source`` 
	し忘れたせいかもしれません。この場合のエラーの回避については
	:ref:`jp_error_setup` をご覧ください。

     
ローカルディレクトリにある開発中コードの利用設定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. Setting up development code in a directory


もしも EUPS によりシステムインストールされていないコード
（たとえば、自分自身が開発しているコードや HSC 開発者向け git 
リポジトリからチェックアウトしてきたコード）を利用設定したい場合には、
``setup -r dir/`` を実行します。 ``dir/`` の部分はカレントディレクトリであることも多いですが、
その場合には、以下のように ``.`` となります。 ::

     $ setup -v -r .

.. If you're working with your own code (or a some checked-out from git)
.. which is not installed in the eups system, you can run ``setup -r
.. dir/`` to set it up.  Often, ``dir/`` is just the current working
.. directory ``.``, e.g.::


ローカルディレクトリのコード利用設定をする時には、しばしばパッケージの依存関係も正しく
``setup`` されているか確認する必要があります。
``setup`` コマンドで何も明示的に指定しなければ、'current' のタグが付けられたパッケージ
＋ バージョンが利用設定されます。どのようなバージョンに 'current' タグが付けられているかは
``eups list`` を見て下さい。それらが必要とするバージョンの組み合わせではないかもしれません。
もしも、あなたが実行しようとしているコードがどのパッケージ ＋
バージョンの組み合わせに対してビルドされるべきか分かっている時には、
まずそのパッケージ ＋ バージョン群を ``setup`` し、次に、
あなたのローカルディレクトリのコードを ``-k`` オプション（keepの意味）付きで ``setup`` します。
このコマンドにより、すでに ``setup`` されたパッケージ ＋ バージョンの利用設定は有効のままで、
ローカルディレクトリのコードが追加で利用可能となります（このオプションを付けなければ、
ローカルディレクトリのコードと依存関係にあるパッケージは、すでに setup 
されているパッケージについても再度 'current' タグの付いたバージョンが設定されてしまいます）。
または、ローカルディレクトリのコードに対して ``-j`` オプション（justの意味）
を付けた ``setup`` を行うことでも同様のことが実現できます。ただし、 ``-j`` の場合には
``-k`` とは異なり、``setup`` されていないパッケージについては、
たとえ依存関係があっても追加の ``setup`` はされません。

.. When you do this, you'll often need to ensure that any dependencies
.. are also setup correctly.  If you specify nothing, you'll get the
.. packages that are tagged 'current' (see ``eups list``).  That may not
.. be the collection of versions you want.  If you know your code needs
.. to build against, e.g. pipeline version 2.12.2a_hsc, then you should
.. first set that up, and then setup your code with ``-k`` to 'keep' the
.. already-setup versions enabled (rather than defaulting to the ones
.. tagged 'current'), or ``-j`` to setup 'just' your working directory.
.. E.g.::

一例::

     # 以下は、すでに行ったバージョンの ``setup`` を維持した状態で、指定した
     # ローカルディレクトリパッケージの利用設定をします。まだ ``setup`` されて
     # いない依存関係のあるパッケージについては 'current' タグの付いたバージョン
     # が設定されます。
     $ setup -v -k -r .

     # 以下は、指定したローカルディレクトリパッケージの利用を追加で設定をする
     # のは同様ですが、上の例とは異なり、他のパッケージについては何も設定され
     # ません。依存関係のあるパッケージについても設定は行われません。
     $ setup -v -j -r .

.. Any dependencies which aren't setup will default to 'current'.
.. Don't even try to setup dependencies, just setup this directory


     
    
パイプラインの実行設定
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. Setting up for a run

一般に、HSC パイプラインを使って作業をする場合には、以下のステップを踏むことになります。

(1) EUPS を初期化して使える状態にする
(2) パイプラインを ``setup`` で設定する
(3) 位置・等級較正用のカタログを ``setup`` で設定する（詳細はパイプラインの項を参照）

.. In general, in order to do most things with the HSC pipeline, you'll
.. want to do the following: (1) enable EUPS, (2) setup the pipeline,
.. and (3) setup a calibration catalog (described more in the pipeline
.. section)::

コマンド例::

    $ setupHsc
    $ setup -v hscPipe -t HSC
     
* 較正用のカタログを一つ選びます。 ``setup`` コマンドによる設定では、最後に設定したカタログが有効になります::

    # SDSS-DR8 カタログを使う場合（一般）
    $ setup -v astrometry_net_data sdss-dr8

    # PS1 カタログを使う場合（SSPの場合）
    $ setup -v astrometry_net_data ps1_pv1.2a
    

.. For the calibration catalog, CHOOSE ONLY ONE!  A `setup` command will override it's predecessor!::
    
.. _jp_back_eupsworks:    
    
.. How EUPS works

EUPS の動作の仕組み
^^^^^^^^^^^^^^^^^^^^^

ユーザの皆さんは EUPS の実装の詳細にはおそらく興味がないでしょう。しかし、EUPS を使う際には、
お使いのシェルの環境変数が何がしか変更されることに気付くと思います。
いくつかの重要な環境変数の値が変更されたり、新しい環境変数が設定されたりします。

.. The details of EUPS's implementation probably won't be of interest to
.. you as a user.  However, you may notice certain things about your
.. shell environment have changed when EUPS is enabled.  Some of your
.. most important environment variables will have been changed, and many
.. new ones will appear.

なんらかのコマンドを実行する際には、お使いのシェル（おそらく ``/bin/bash`` ）
が実行可能なコマンドを ``$PATH``  変数から調べます。EUPS を使うと、
複数のバージョンのインストール済プログラムの中から、
希望するバージョンの実行コマンドを ``PATH`` 変数に設定することができます。
たとえば、EUPS に対して ``setup foo 2.1.0`` と指示すれば、EUPS は `` foo`` 
パッケージのバージョン 2.1.0 がどこにインストールされているかを検索し、
``foo/2.1.0/bin`` に対する適切な実行パスを ``PATH`` 環境変数に追加してくれます。
同時に、``foo`` パッケージのほかのバージョンのコマンドパスが ``PATH`` 
変数の中に混在していないかを確認してくれます。これにより、
異なるシェルで異なるバージョンのコードを使い分けることが出来ます。

.. When you run a command, your shell (probably ``/bin/bash``), will
.. check your ``$PATH`` variable to look for executable commands.  EUPS
.. allows you to have multiple versions of a program installed by
.. specifying the path for the desired version in your ``PATH`` variable.
.. When you tell EUPS to ``setup foo 2.1.0``, EUPS will look-up where the
.. ``foo`` package version 2.1.0 is installed, and add the corresponding
.. ``foo/2.1.0/bin/`` directory to your ``PATH``.  It will also make sure
.. that any other versions of ``foo`` aren't simultaneously present in
.. your ``PATH``.  So, you should be able to work on two different code
.. versions in two different shells, and everything will be fine.

ただし、HSC パイプラインには 90 ほどのモジュール（主として Python コードで
呼び出されて実行されるソフトウェア）が含まれるため、EUPS はあなたの``PATH``
変数に大量のパスを追加することになります。同様に、``LD_LIBRARY_PATH`` や
``PYTHONPATH`` にも見慣れないほど多数のパスが追加されますので驚かないで下さい。

.. However, because there are several different modules in the pipeline
.. (about 90), EUPS will be adding a lot to your ``PATH`` variable.
.. Similarly, you can expect both ``LD_LIBRARY_PATH``, and ``PYTHONPATH``
.. to be much more extensive than you're likely to have seen before.

.. warning::

   万が一、PATH 環境変数の中身がおかしいと感じる場合には、
   手動で修正するのはやめた方が無難かもしれません -- 効を奏すことが少ないです。
   それよりは、単純に新しいシェル（端末エミュレータ）を開きなおし、
   必要な EUPS 管理下のパッケージについて ``setup`` をやり直す方がおそらく有効です。

.. If you suspect that one of your PATH variables has been corrupted,
.. don't attempt to fix it by editing manually and re-exporting the
.. variable.  Such efforts aren't likely to be successful, and you're
.. almost certainly better off to open a new shell and re-``setup``
.. the EUPS package your interested in.

EUPS は、既存の環境変数を操作するほかに、EUPS が HSC パイプラインの
各パッケージを管理するための専用の環境変数を新たに追加します。
ユーザの皆さんがよく目にすると思われるのは、 ``$PACKAGE_DIR`` 
のような形式の変数です。ここで、 ``PACKAGE`` の部分には、EUPS 
管理下の各種パッケージ名が入ります。これらの ``*_DIR`` 変数は、
それぞれのパッケージコードがインストールされているディレクトリを指し示しています。
この変数をユーザが意識する必要はほとんどありませんが、
時々、特定のパッケージがどこに置かれているのか、あるいは、
今自分が実行しているのはどこに置かれたパッケージか、
などを知りたい時に参照するとよいでしょう。例えば、 ``AFW_DIR``
（現在使っているアプリケーションフレームワークのコードの在処）や
``OBS_SUBARU_DIR``
（現在使っている、すばるのデータ解析に固有の操作を行うソフトウェアの在処）など。

.. In addition to manipulating your existing environment variables, EUPS
.. will also create new variables for each module it manages.  The only
.. one you're likely to encounter has the form ``$PACKAGE_DIR``, where
.. PACKAGE is the name of an EUPS-managed package.  These ``*_DIR``
.. variables refer to the directories where the corresponding code is
.. installed.  You'll rarely, if ever, need to use them, but
.. occassionally you may need to know where a specific package lives.
.. Examples include ``AFW_DIR`` (where the application framework code
.. lives), and ``OBS_SUBARU_DIR`` (where the Subaru-specific software
.. lives).

.. warning::

   ``*_DIR`` 以下に置かれたファイルを絶対に直接編集してはいけません。
   これらはインストールされた（共有の）コードです。

..    You must never (never never) try to edit any of the files you find
..    in a ``*_DIR`` directory.  These files are installed code.
    
.. _jp_back_torque:

PBS/TORQUE
-------------

HSC パイプラインのいくつかのコマンドは、TORQUE 
と呼ばれるバッチ処理システムと組み合せて使うことが出来るように実装されています。
TORQUE は、PBS（Portable Batch System）
という商用バッチシステムから派生して開発されている無償で利用できるバッチシステムです。
TORQUE は、複数の PC ノード上で分散並列処理を行うジョブのスケジュールとキュー管理を行います。
ジョブの状態確認やキャンセルといった、少しの TORQUE コマンドを知っておけば、
TORQUE を使って HSC パイプラインを実行するのには困らないでしょう。

.. Our batch processing is handled with a system called TORQUE, which is
.. a popular variant of PBS (Portable Batch System).  The system handles
.. job scheduling and queue management for parallel jobs being run on
.. distributed compute nodes.  For the purposes of running the HSC
.. pipeline, there are only a handful of commands you'll need to concern
.. yourself with, mainly checking the status of your job, and possibly
.. cancelling it.  An example of each is shown below.

あなたの使う TORQUE システム上には、複数の 'キュー' が作られているかもしれません。
各々のキューは、それぞれ別個のリソース利用の制限（ジョブで指定できる最大ノード数など）
が設定されています。`qstat -Q` コマンドや `qstat -Q -f` コマンド（全ての情報を表示）
でシステム上のキューの設定を確認することが出来ます。一般的に、
使えるノード数の多いキューでは少数のジョブしか同時に実行できず、
ノード数が少ないキューではより多数のジョブを実行することが出来るように設定されています。
TORQUE にジョブをサブミットする時には、
あなたが必要とする最小のキューに対してサブミットするように注意して下さい。
（この段落はシステム設定の一般論です。三鷹や onsite 系には現在 default キューしかありません）

.. There may be various 'queues' defined on a Torque system, with each
.. having different levels of access to resources (i.e. the max number of
.. nodes you can request that your job gets to run on).  The `qstat -Q`
.. command will show you the currently defined queues on the system, and
.. `qstat -Q -f` will show full information.  In general, we've set
.. queues with large node limits to allow fewer jobs to run, while those
.. with small node limits will allow many jobs to run.  When you submit a
.. job, please submit to the smallest queue you think you can afford to
.. use.
        
qstat
^^^^^

.. Use 'qstat' to check the status of a job.  The '-a' option provides a
.. bit more info.  Much more info is available in 'man qstat', but this
.. simple example should give the basic idea.  The example shows a single
.. job in the queue.  It's run by the user 'you' and is running in the
.. quene named 'small'.  It uses 3 nodes, and is currently running 'R'::

ジョブの状態を確認するには、'qstat'コマンドを使います。
'-a' オプションは少しだけ詳細な情報を返します。詳しくは 'man qstat' を参照して下さい。
以下に、基本的な使い方の一例として、キューに入っている単一ジョブの状態の確認方法を記します。
このジョブは、ユーザ 'you' によって、'small' というキューで実行されています。
3 ノードを使って実際に処理が行われています（状態 'R'）。 ::

    $ qstat -a
    master: 
    .                                                                Req'd    Req'd       Elap
    Job ID        Username    Queue    Jobname   SessID  NDS   TSK   Memory   Time    S   Time
    ------------- ----------- -------- --------- ------ ----- ------ ------ --------- - ---------
    374.master    you         small    myjob        --      3     36    --   01:06:40 R  00:00:02


.. For reference, here are the job status codes::

S の欄には、下記のジョブの状態コードのいずれかが表示されます。 ::
  
    C -  ジョブは実行のあと完了(complete)した
    E -  ジョブは実行のあと終了(exit)した
    H -  ジョブは依存関係により保留状態
    Q -  ジョブはキューで待機状態（eligible to run or routed）
    R -  ジョブは実行中（run）
    T -  ジョブは新しい場所へ移行中
    W -  ジョブは実行時間待ちで待機状態
         (-a option) to be reached.
    S -  (Unicos only) ジョブはサスペンド状態


.. Here are the most popular options used with `qstat`::

以下に `qstat` コマンドのうち、よく使われるオプションを記します。 ::

    $ qstat -q          すべてのキューを表示
    $ qstat -Q          すべてのキューについてより詳細を表示
    $ qstat -Q -f       すべてのキューについて全ての情報を表示
    $ qstat -a          すべてのジョブを表示
    $ qstat -au userid  useridが所有するすべてのジョブを表示
    $ qstat -r          現在処理中のジョブを表示
    $ qstat -f job_id   job_idで指定されたジョブの全ての情報を表示
    $ qstat -Qf queue   queueで指定されたキューの全ての情報を表示
    $ qstat -B          ジョブサーバの状態のサマリ表示
    $ qstat -n          ジョブプロセスが割り当られているノード名を表示
    
qdel
^^^^

.. Occassionally, something goes wrong with a job.  Perhaps you submit
.. with the wrong command line arguments, or the job is just taking too
.. long to finish; whatever the reason, `qdel` can be used to kill the
.. job.  Use qstat to determine the job ID, and then kill it as follows
.. (assuming the job ID from the above example)::

時々ジョブには問題が起きることがあります。たいていは、TORQUE 
サブミットしたコマンドに与えた引数が間違っていたり、
予想に反して延々と処理が終わらなかったりといったことです。こうした場合、
``qdel`` コマンドを使ってジョブを殺すことが出来ます。
`qstat` コマンドを使ってジョブ ID を調べ、
次のようにしてその ID のジョブを殺して下さい（以下では上の例のジョブID = 374を仮定します）。 ::

    $ qdel 374

.. More info is available with `man qdel`.

詳細は `man qdel` を参照して下さい。


.. Pipeline TORQUE-related arguments

TORQUE 制御の HSC パイプラインコマンドのオプション
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. The pipeline tasks which use TORQUE (e.g. ``reduceFrames.py``, and
.. ``stack.py``) allow you to specific how your job will make use of the
.. system resources; specifically, which queue, how many nodes, how many
.. cores per node.  When you start running any of the
.. ``reduce<thing>.py`` commands (``reduceBias.py``, ``reduceFlat.py``,
.. ``reduceFrames.py``, etc., you'll be able to use the following
.. arguments to control TORQUE's behaviour:

TORQUE を利用する HSC パイプラインのコマンド（``reduceFrames.py``、``stack.py`` など） は、
どのように計算機リソースを使って実行するか（キューの種類、ノード数、コア数など）を
TORQUE に対して指定するためのコマンドオプションを提供します。``reduce*.py`` 
と名付けられたコマンド（``reduceBias.py``, ``reduceFlat.py``, ``reduceFrames.py`` など）
は一般にこの TORQUE インターフェースを持ちます。これらのコマンドでは TORQUE 
のジョブ管理方法を指定する以下のオプションを使うことが出来ます。 :

``--job``

    ジョブに付ける名前で、 ``qstat`` コマンドの結果に現れます。
    TORQUE がジョブプロセスの標準出力＋標準エラー出力を書き出すログファイルの名前にも使われます。

..    This is the name of the job, as you want it to appear in ``qstat``
..    commands.  It will also be used in the name of the log files that
..    TORQUE writes containing the ``stdout`` from your job.

``--queue``

    ジョブをサブミットすべきキュー名です。お使いのシステム上に複数のキューが存在する場合には考慮します。
    どのようなキューが存在するのかは以下のコマンドで確認できます。 ::

    $ qmgr -c 'print server'

..    The name of the queue you're submitting your job to.  There may be
..    multiple queues on the system you're using.  You can see which
..    ones there are with::


``--nodes``

    ジョブのプロセスに割り当てるノード数です。
    キューが許すより多数のノード数を指定するとエラーになりますので注意して下さい。
    最大の許容ノード数は、``qmgr -c 'print server'`` コマンドで表示される
    ``resources_max.nodes`` の値で知ることが出来ます。

..    Specify the number of nodes you want your process to use.  Note
..    that if you ask for too many, you'll get an error message telling
..    you so.  The maximum number of nodes you're allowed to request
..    from a given queue is listed in the output of ``qmgr -c 'print
..    server'`` with label ``resources_max.nodes``.

``--procs``

    各ノードで起動するプロセス数です。ノード数の場合と同様に、
    キューが指定する最大プロセス数を超えてはいけません。 最大プロセス数を確認するには、
    ``qmgr -c 'print server'`` コマンドにより表示される ``resources_max.ncpus`` 
    の値を確認します。``procs`` x ``nodes`` (つまりジョブが要求するCPUコアの総数）
    が ``resources_max.ncpus`` を超えないように指定して下さい。

..    Specify the number of processes on each node you want your process
..    to use.  Again, you'll have to be careful not to exceed the
..    specifications for the queue you've requested.  Check ``qmgr -c
..    'print server'`` to find ``resources_max.ncpus``, and make sure
..    that ``procs`` times ``nodes`` (i.e. the total number or CPUs
..    you're asking for) isn't larger than ``resources_max.ncpus``.

``--time``

    ジョブの処理にかかる見込みの処理時間を調整します。TORQUE は、
    この時間を超えたジョブを時間切れとして強制終了させます。
    長時間の処理が必要な場合は、このオプションで適宜調整してください。

..    Use this to adjust the expected execution time for each element.
..    TORQUE may time-out your job if it takes longer than expected, so
..    this allows you to increase the limit.
    
``--do-exec``

    このオプションを指定すると、ジョブを TORQUE のキューにサブミットするのではなく、
    現在のシェル上でジョブが実行されます。
    個別の問題の調査には役立ちますが（1 ノードの計算リソースしか使えませんので
    時間がかかります）、大きなジョブは TORQUE にサブミットするのがよいでしょう。

..    This will cause the system to run the code in the current shell,
..    rather than submitting to TORQUE system.  It can be very useful
..    for debugging specific problems, but shouldn't ever be used for a
..    large job (it would just take too long!).
    
``--pbs-output``

    ジョブプロセスの標準出力＋標準エラー出力の書き出し先ディレクトリを指定します。
    無指定の場合は、ジョブをサブミットした作業ディレクトリか、
    TORQUE サーバ側で設定されたディレクトリに書き出されます。

..    .. todo::    I haven't played with this.  Paul? What does it do?

Reruns（リラン）
------------------

.. The term ``rerun`` originated in SDSS.  It simply refers to a single
.. processing run, performed with a specified version of the reduction
.. code, and with a specific set of configuration parameters.  The
.. assumption is that within a given 'rerun', the data have been handled
.. in a homogeneous way.

``rerun`` はもともと SDSS のデータ解析運用で使われた概念で、HSC パイプラインでも使われます。
``rerun`` は、単一のデータ処理作業（data processing run）を表します。単一とは、
その処理作業の中では、ある決まったバージョンの組み合わせのコードをある決まった設定パラメータ
（configuration） で走らせて解析する、という意味です。この定義のもと、ある 'rerun' の中では、
データ処理は均質に扱われることを意図します。

.. todo::

    This is repeated in the glossary.  Are both places needed?  It's
    short, and won't change.

    
.. _jp_back_dataId:

DataId (データID)
---------------------

.. A 'dataId' is a unique identifier for a specific data input.  The two
.. forms you most likely need to familiarize yourself with are the
.. 'visit','ccd' identifiers used to refer to a specific CCD in a
.. specific exposure (called a 'visit'); and 'tract','patch' identifiers
.. which refer to the coordinate system used in coadded images.  Other
.. important keys in a dataId might include:

.. * field (name you gave your target in the FITS header 'OBJECT' entry)
.. * dateObs (the date of observation from the FITS header 'DATE-OBS' entry)
.. * filter  (again from the FITS header ... 'FILTER' entry)

'dataId'（データID）は、入力データを特定するためのユニーク ID です。
特に覚えておかなければならないのは、'visit' と 'ccd' です。この 2 つのキーワードは、
特定の積分（ショット；HSC パイプラインでは 'visit' と呼ばれます）の特定の CCD データ
を指定するために使われます。
'tract' と 'patch' は、coadd 画像を指定するために使われます。他に重要なキーワードとして、
以下のものが上げられます。 ::

 * field (観測ターゲット名。FITS ヘッダの OBJECT に相当。)
 * dateObs (観測日 UT。FITS ヘッダの DATE-OBS に相当。)
 * filter  (フィルター名。FITS ヘッダの FILTER01 に相当。)
 ただし、HSC パイプラインでは上記はすべて大文字に変換され、特殊文字はアンダースコアで置換して扱われます。

.. In almost any pipeline command you can specify which data you wish to
.. process with ``--id <dataID>``, e.g.::

ほとんどすべてのHSCパイプラインコマンドでは、どのデータを処理するのかを
``--id <dataId>`` のオプション記法で指定することが出来ます。例えば ::

    # visit 1000, CCD 50 を処理
    $ hscProcessCcd.py /data/ --id visit=1000 ccd=50

    # 2015-01-15 に HSC-I バンドで取得した OBJECT = M87 のすべてのデータを処理
    $ hscProcessCcd.py /data/ --id field=M87 filter=HSC-I dateObs=2015-01-15

    # HSC-I バンドの coadd 画像のうち、tract 0 patch 1,1 に位置するデータを処理
    $ hscProcessCoadd.py /data/ --id tract=0 patch=1,1 filter=HSC-I

.. Only a few of the dataId components are ever needed to uniquely
.. specify a given data input or output.  For example, the observatory
.. will never reuse the number assigned as a 'visit', so it's impossible
.. to have the same visit with a different filter or dateObs.  Once you
.. specify the visit, the other values are almost all redundant.  This isn't
.. true for tracts and patches, though!  A tract,patch refers to a
.. location on the sky and can have multiple filters or dateObs values.

CCD 画像を指定する場合には、ほんの 2, 3 のdataId 
キーワードで入出力データをユニークに特定できることが多いかもしれません。例えば、
HSC（すばる）では、複数の積分に対して同じ 'visit' が割り当てられることはありませんので、
'visit' だけを指定すれば、他の filter や dateObs 
などのキーワードは冗長であることがほとんどです。ただし、coadd 画像の指定時の tract と
patch についてはこの限りではありません! tract と patch は、
coadd 画像の天域を指定しますので、一つの（tract, patch）の組に対して複数の filter や
dateObs の組み合わせを取り得ます。

.. Ranges and Multiple ``--id`` values

``--id`` オプションの範囲指定と複数指定 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. A dataId will also let you specify a range of values, or a set of
.. separate discrete values.  Pay careful attention to the ``:`` (step
.. size) notation as HSC visit numbers are incremented by 2 (always
.. even).

'dataId' を使って、入出力データを範囲で指定したり、
個々のデータを複数同時に指定することが出来ます。HSC データでは、積分ごとに
visit は 2 ずつ増えますので、``:`` （刻み幅）の記法を用いることに注意して下さい。


.. * ``..`` denotes are range of values.  E.g. visit 1000 with all CCDs
..   between 40 and 60, inclusive::

 * ``..`` は値の範囲を指定します。例えば、visit = 1000 のデータのうち、ccd = 40 と 60 を含むその間の範囲の全 CCD を指定するには次のように指定します::

    --id visit=1000 ccd=40..60

.. * ``^`` separates discrete values.  E.g. visit 1000 and 1004::

 * ``^`` は個々の値を繋いで同時に指定します。例えば、visit = 1000 と 1004 の 2 つの visit のデータを同時に指定するには::

    --id visit=1000^1004

.. * ``:`` specifies a step to use for a range, and thus is only ever
..  used with ``..``.  E.g. even-numbered visits 1000 to 1010::

* ``:`` 値の範囲指定をする際の刻み幅です。常に ``..`` と一緒に使います。例えば、visit = 1000 と 1010 を含むその間の visit のうち、偶数のデータだけを指定するには::

    --id visit=1000..1010:2   # 範囲の中で、2 visitずつ増加します


.. Configuration Parameters

.. _jp_back_config:

設定パラメータ (config)
----------------------------------------

HSC パイプラインのコマンドは、コマンドライン引数に設定パラメータを与えたり、
設定パラメータをファイルとして与えることで、その様々な箇所の動作を制御することが出来ます。
その設定パラメータ（'Config'）の全てを並べると、一見とてつもない数のパラメータがあるのですが、
ユーザにとってはそのごく一握りだけが重要でしょう。参考までに、2 つのコマンドについて、
デフォルトの config パラメータを表示します（
:ref:`reduceFrames.py <reduceframes_config_defaults>`,
:ref:`stack.py <stack_config_defaults>` ）。こうした無数の config パラメータのうち、
コマンド実行時に使用できるパラメータやキーワードを知りたい時は以下のように調べることができます。

.. highlight::
	bash
	
::

	# hscProcessCcd.py というコマンドのパラメータのうち
	# '*background*' という文字列が含まれるパラメータを config パラメータから検索する
	$ hscProcessCcd.py /path/to/data/ --show config="*background*"

Config パラメータ は階層構造を持っています。それぞれのパラメータは
'タスク' と呼ばれるパイプラインの一部を成す特定の解析を行うコード（モジュール）
の中で定義されています。さらにそのタスクに属する 'サブタスク'（タスクから派生した解析コード）
でも固有の config パラメータが定義されており、それらにはピリオドで繋げた形式でアクセスできます。
たとえば、'instrument signature removal'（ISR; Bias 引きや Flat 補正などを行う） 
という 'タスク' は、config パラメータ ``doFringe`` を持ち、
それには以下のような記法でアクセス出来ます。 ::

    isr.doFringe=True

すべての config パラメータはデフォルト値を持ち、たいていのユーザが必要とする値に設定されています。
しかし、それらを変更して実行したい場合には 2 つの指定方法があります:
一つは、コマンドライン引数で config パラメータの値を指定する方法、もう一つは、
ファイルとして config パラメータの値を与える方法です。2 つを組合せることも出来ます。

* コマンドラインで config パラメータをオーバーライドする場合には、
  ``--config name=value`` （ ``-c name=value`` も同じ意味）のように指定します。 ::

    --config isr.doFringe=False

* ファイルを読み込ませて config パラメータをオーバーライドする場合には、
  プレインテキスト形式のファイルに 1 行あたり 1 パラメータの値の設定を書き、 
  ``--configfile filename`` （ ``-C filename`` も同じ意味）のように指定します。
  
.. _jp_back_policy:  
  
Policy (.paf) ファイル
^^^^^^^^^^^^^^^^^^^^^^

.. You won't likely encounter policy files, but there mentioned here just
.. in case you happen to find one.  'Policy' was the predecessor of
.. 'Config', and they were used to store configuration parameters.  The
.. files have suffix ``.paf``, and are plain ascii text.  They are quite
.. easy to read, and contain heirarchical structures of data.  For
.. example, an excerpt from the camera characterization shows information
.. about the first amplifier in CCD 0 (the other amps aren't shown)::

'Policy' はすでに古い設定パラメータ形式であり、
ユーザの皆さんが目にする機会はほとんどないかもしれません。しかし、
もしも御目にかかった場合の予備知識として記載しておきます。'Policy' は、
以前は上で説明した 'Config' の代わりに設定パラメータを保持する目的で使われていましたが、
現在はほとんどの解析タスクが config 形式に移行しています。'Policy' の設定ファイルは
``.paf`` という拡張子の名前を持つプレインテキスト形式のファイルです。階層構造を持ち、
可読性に優れます。一例として、以下はカメラの CCD 特性の設定の一部抜粋です。 ::

    Ccd: {
        name: "1_53"
        ptype: "default"
        serial: 0
        Amp: {
            index: 0 0
            gain: 3.5118
            readNoise: 1.56
            saturationLevel: 52000.0
        }
        <snip>
    }

.. However, the policy files are being phased out for the most part, and
.. eventually they'll disappear completely.  But, for now, they still
.. exist in a few places.

Policy ファイルはパイプラインコードのほとんどの箇所で使われなくなっており、
規定路線ではいずれは完全になくなります。しかし、今のところは、
いくつかの限られた
場所でまだ使われています。
