
==============================
パイプラインのインストール
==============================

このページは
PBWorks `wiki <http://hscsurvey.pbworks.com/w/page/64515753/Pipeline%20Installation>`_
のHSCパイプラインのインストールガイドのコピーです。

HSCパイプラインはLSSTパイプラインをベースにしているため、
`LSSTパイプラインインストールページ <https://dev.lsstcorp.org/trac/wiki/Installing>`_ 
が役立つかもしれません。全てLSSTパイプラインと同じというわけではありませんが、
まず最初に以下を試して、何かトラブルが生じた時はLSSTパイプラインのインストールページを
参照するとよいかもしれません。もしそれでも解決しない場合は、エラーメッセージを
google で検索してみるか、`パイプライン開発グループにメール <mailto:hsc_software@astro.princeton.edu>`_
してください。

まず、LSSTパイプラインインストールマニュアルの
`事前準備事項 <https://dev.lsstcorp.org/trac/wiki/Installing/Summer2012>`_ 
をチェックしましょう。必要なパッケージが全てインストールされているか確認してください。
さらに、git も自身の計算機にインストールされていることを確認しましょう。
もし git に不慣れな場合は、`LSSTによる git の紹介ページ <https://dev.lsstcorp.org/trac/wiki/GitDemoAndTutorial>`_ 
をご覧ください（基本がわかればよいので、全てを理解する必要はありません）。
ちなみに、git プロトコルのために open port 9148 が必要となります。
もし、この port が自身が所属する機関でブロックされている場合は、この port を open にするように
機関に申請するか、ssh tunnel を使用してください。もし、使用している計算機が
クラスターで `PBS/Torque <www.adaptivecomputing.com/products/open-source/torque/>`_
を使用している場合は、以下のようにインストールしてください。
:ref:`PBS/Torque の使用について <jp_back_torque>` はこちらのページをご覧ください。

`EUPS <https://github.com/RobertLuptonTheGood/eups>`_ はパイプラインによるプロダクト
の管理ツールです。EUPS については様々な説明ページがありますので、そちらをご覧ください：
`LSST wiki <https://dev.lsstcorp.org/trac/wiki/Eups>`_ 、:ref:`本サイト内EUPSページ <jp_back_eups>`。
EUPSはその他パイプラインに関連するパッケージをインストールする前に、最初にインストールしてください。
パイプラインで使用する全てのソフトは root 権限がなくてもインストールできる仕様になっています。
sudo や root にならずに local の環境に /install ディレクトリを作るなどして
インストールを行ってください。
 
::

    mkdir -p /install
    cd /work
    git clone git://github.com/RobertLuptonTheGood/eups.git
    cd eups
    ./configure --prefix=/install/eups/default/ --with-eups=/install/
    make install
 
インストールが終了したら、~/.bashrc に以下の内容を書き足してください。::
 
    source /install/eups/default/bin/setups.sh
    export NCORES=$((sysctl -n hw.ncpu || (test -r /proc/cpuinfo && grep processor /proc/cpuinfo | wc -l) || echo 2) 2>/dev/null)
    export MAKEFLAGS="-j $NCORES"
    export SCONSFLAGS="-j $NCORES --setenv"

もし csh か tcsh を使用している場合は、 ~/.cshrc か ~/.tcshrc に上記に相当する
内容を書き足してください。::
 
    source /install/eups/default/bin/setups.csh
 
.bashrc が編集できたら、EUPS環境を設定し、環境変数の設定を反映させます。

環境設定が完了したら、パイプラインのインストールを開始しましょう。::
 
    # bash の場合
    export EUPS_PKGROOT=http://hsca.ipmu.jp/sumire/packages/
	
    # (t)csh の場合
    setenv EUPS_PKGROOT http://hsca.ipmu.jp/sumire/packages/
    eups distrib install hscPipe <version>
 
<version> はパイプラインのバージョンを指定します。自身が使用する適切なバージョンを
指定しましょう（もしバージョンがわからない場合は、``eups distrib list hscPipe`` を試してみてください）。

 
Gotchas
-------

mpich
^^^^^

もし `mpich <www.mpich.org>`_ が自身の計算機の
/usr/include と /usr/lib にない場合、以下の環境変数を設定しましょう。:

* PBS_INCLUDE_DIR: トルクの include ディレクトリを設定する（tm.h header ファイルを探す）
* PBS_LIB_DIR: トルクの lib ディレクトリを設定する（libtorque.so ファイルを探す）
* PBS_DIR: トルクの include と lib ディレクトリを設定する; PBS_INCLUDE_DIR=$PBS_DIR/include と PBS_LIB_DIR=$PBS_DIR/lib ディレクトリを設定するのと同義

 
Mac OSX (10.7 以降)
^^^^^^^^^^^^^^^^^^^^^^^^

gcc ではなく clang コンパイラを使うために、追加のフラグ設定が必要です: SCONSFLAGS+=" cc=clang"

加えて、EUPS に使用する "system" のバージョンを追加する必要があります。::
  
   cd /work
   git clone git://hsca.ipmu.jp/repos/devenv/buildFiles.git
   eups declare python system -r none -m none -L buildFiles/python/python.cfg
   eups declare libjpeg system -r none -m none -L buildFiles/libjpeg/libjpeg.cfg
 
次に 以下を ~/.eups/manifest.remap に配置すれば、EUPSが以下のシステムにアクセスできるようになります。::

    python  system
    gmp     None
    mpfr    None
    mpc     None
    gcc     None
    libjpeg system

    
Ubuntu 12
^^^^^^^^^

Ubuntu 11.04 (Natty Narwhal) とそれ以降のバージョンでは、
環境変数にいくつかのフラグを追加する必要があります
（`LSST's ubuntu-specific setup <https://dev.lsstcorp.org/trac/wiki/Installing/Winter2013#Ubuntu12.04specificstep>`_ 
も参照のこと）。::

    export LDFLAGS+=" -Wl,--no-as-needed"
    SCONSFLAGS+=" LINKFLAGS='-Wl,--no-as-needed'"
 
 
Mac OSX から Redhat 搭載の計算機へのアクセス
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

少なくともいくつかの Redhad 搭載の計算機では、Mac OSX の計算機からターミナル経由でパイプラインを
インストールする時（特に、TERM=xterm-256color を使用している時）、python のバージョンを
決定しているプロセスでエスケープコードが生じるという python/readline に関するバグが発生します。
この問題に関しては `stackoverflow
<http://stackoverflow.com/questions/15760712/python-readline-module-prints-escape-character-during-import>`_
でも紹介しています。回避方法としては以下の通りです。 ::

    export TERM=vt100
 
 
SSL 認証エラー
^^^^^^^^^^^^^^^^^^^^^^

もし build log 内に SSL 認証エラーを見つけたら、以下を試した後に
EUPS distribution のインストールを行ってください。::

    curl () { /usr/bin/curl -k "$@"; } export -f curl

    
Intel Math Kernel Library (MKL)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

mosaic.py は MKL を使ってコンパイルしない限り非常に長い時間がかかります
（MKL は有料です）。MKL の設定は、バージョン毎、
計算機毎にインストール方法が異なっているため少々厄介です。いろいろ試してみてください。
もしうまくいかない場合は、パイプライン開発チームにご連絡ください。

MKL を設定するには、buildFiles を持ってきて以下のように行います。::

    git clone git://hsca.ipmu.jp/repos/buildFiles.git
    cd buildFiles

MKL のインストール用のディレクトリ MKL_SYSTEM_DIR を設定します
（LD_LIBRARY_PATH も正しく設定してください）。その後以下のようにEUPSを実行します。::
	
    eups declare mkl VERSION -M mkl.table -r none -L mkl/mkl.cfg
    
以下のファイルを  ~/.eups/manifest.remap に配置します。::

    mkl    VERSION

（適切な MKL のバージョン名に VERSION 箇所を置換してください）

上記 MKL の設定によって meas_mosaic が再構築されることはありません。もし再構築したい場合は、
次のコマンドを実行してください。::

    git clone git://hsca.ipmu.jp/repos/meas_mosaic.git
    cd meas_mosaic
    setup hscPipe <LATEST_VERSION> # replace with the appropriate version
    setup -j -r .
    setup -j mkl VERSION
    scons opt=3
    
meas_mosaic の適切なバージョンは以下のように置換されます。::

    setup meas_mosaic <LATEST_VERSION>
    setup -j mkl VERSION
    eups distrib install -jF meas_mosaic <LATEST_VERSION>
    

"This Intel <math.h> is for use with only the Intel compilers"
という文言のエラーメッセージが出た場合は、mkl.cfg 内の CPPFLAGS をいじってみてください
（例えば entry を消去するなど）。


AstronometryNetData カタログ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

HSCパイプラインで使用される astrometry_net_data はプレースホルダーで、真の座標較正用カタログ
ではありません。パイプライン内で適切な解析が行われるように、適切な astrometry_net_data を入手・登録し、
パイプラインで使用できるように設定する必要があります。

**入手**:

もし astrometry_net_data を既にもつ計算機にアカウントがある場合（例 IPMU クラスター計算機）、
自身の解析環境下にディレクトリをコピーすれば完了です。::

	eups list -d astrometry_net_data

もしコピーできない場合は、2mass カタログを
`astrometry.net <http://broiler.astrometry.net/~dstn/4200/HSC/>`_ から入手しましょう。
その際、andConfig.py と呼ばれる以下のような追加ファイルが必要になります。::

    root.defaultMagColumn = "j_mag"      # Default column name to use for magnitudes
    root.magColumnMap = { 'J': 'j_mag' } # Mapping from filter to magnitude column name
    root.magErrorColumnMap = {}          # Mapping from filter to magnitude error column name
    root.indexFiles = ['index-130202000-00.fits',
                       'index-130202000-01.fits',
                       # Etc, listing all the index files
                      ]
				
または、SDSS DR8 カタログを `ここ <http://hsca.ipmu.jp/sumire/astrometry_net_data/sdss-dr8/>`_.
からダウンロードして使用することもできます。

**登録**:

自身がダウンロードした astrometry_net_data ディレクトリに対し、以下のコマンドを実行してください。::

    eups declare astrometry_net_data <version> -r /path/to/astrometry_net_data/<version> -m none
    
もしディレクトリが複数に及ぶ場合、以下の方法もあります。::

    cd /path/to/astrometry_net_data
    for d in *; do eups declare astrometry_net_data $d -r $d -m none; done
    
**設定**:

EUPSに使用したいカタログが登録できたら、パイプラインで使用できるように設定します。::

    setup -j astrometry_net_data <version>
  
    # 例;
    setup -j astrometry_net_data sdss-dr8
    
``-j`` フラグは ``setup`` の時にだけ使用します。このフラグなしでは例えば
``gcc`` や ``python`` との依存性を設定してくれません。

この ``astrometry_net_data`` の ``setup`` は新しい計算機環境を設定する度に必ず毎回行ってください。

