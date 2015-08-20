
=========================================
EUPS: 新しいパッケージとリリースに関して
=========================================

.. contents::
   :local:
   :depth: 2

   
新しいパッケージを作る
-----------------------------
以下の方法で新しいパッケージをディストリビューションに加えることができます。まず最初は、
プロダクトの構造を定義します。例えば、以下のような ``products/`` ディレクトリをインストールします。

..
	If you wish to add a package to a distribution, these are the steps to
	follow.  The necessary steps are shown first with no explanation as a
	quick reference, and this is followed by complete instructions.  There
	are two examples shown, and both are for external packages.

	Your installed ``products/`` directory tree probably looks something like this::

.. highlight::
	bash
	
::

    $ tree /path/to/products/
    |-- EupsBuildDir                 # パッケージをビルドする仮ディレクトリ
    |-- Linux64                      # パッケージをインストールするディレクトリ
    |   `-- <many product dirs>
    |-- eups
    |   |-- default -> master/       # master/ へのシンボリックリンク
    |   `-- master                   # eups コード (バージョン 'master')
    |-- site
    |   |-- manifest.remap           # 
    |   `-- startup.py               # eups が行うシステム全体にわたるコード (hooks, macros, globals, とか)
    `-- ups_db                       # eups のデータベース情報
        `-- <many product dbs>


startup.py
^^^^^^^^^^

:download:`startup.py`

ここで提供されているようなパッケージを使うためには、
``startup.py`` というパラメータファイルが必要となります。このパラメータファイルは
``eups distrib create`` を実行するために必須のファイルです。**もしディレクトリを作らない場合は、
パラメータファイルによる設定は不要です。**

``startup.py`` は次の 2 箇所に置いてください。**既にこのファイルがあれば、
このコードがファイル内に記載されているか確認してください。** ::

    # システム全体に対する設定を行うパラメータファイル:
    /path/to/products/site/startup.py

    # または、ユーザーレベルのパラメータファイル:
    /home/username/.eups/startup.py
    
    
クイックスタート
^^^^^^^^^^^^^^^^^^^^^^^
'php' のバージョン 5.6.7 というソフトウェアをインストールする例を以下に示します。

::

    $ git clone ssh://gituser@hsc-repo.mtk.nao.ac.jp:10022//home/gituser/repositories/buildFiles.git
    $ cd buildFiles
    # < ビルドファイル、テーブルファイルを作る（以下の例を参照） >

    # ディレクトリからインストールし、ビルドファイルとテーブルファイルをテストする
    $ EUPS_PKGROOT=dream:. eups distrib install php 5.6.7 --noclean

    # ディストリビューションを作る（packages/ ディレクトリ内にバージョン固定のビルドファイル、テーブルファイルを作る）
    $ eups distrib create php 5.6.7 -v -s $HOME/public_html/packages -S buildFilePath=$PWD

    # 他の計算機にソフトウェアをインストールする
    $ ssh some.other.machine.edu
    $ . /path/to/products/eups/default/bin/setups.sh
    $ export EUPS_PKGROOT=$EUPS_PKGROOT'|'http://old.domain.edu/~user/packages/
    $ eups distrib install php 5.6.7

    # ビルドファイルにソフトウェアをチェックインすることを忘れずに!!
    
    
新しいパッケージのインストール（詳細）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. buildFiles.git リポジトリをダウンロードする。 ::

    # buildFiles.git リポジトリをダウンロード
    $ git clone ssh://gituser@hsc-repo.mtk.nao.ac.jp:10022//home/gituser/repositories/buildFiles.git
    $ cd buildFiles
    

#. | ビルドファイルを buildFiles/ ディレクトリに作る。
   |	以下では PHP（python は不要）と SQLAlchemy（python が必要）をインストール
    	場合を例として示しています。どのようなソフトウェアをインストールしビルドする場合も、
    	だいたい以下の例のように行ってください。buildFiles/ パッケージの中には、
    	ビルドファイルの設定に使う多くのパッケージが同梱されています。		

    * ダウンロードしたいパッケージの http 情報と、
      そのパッケージによってできるディレクトリにパッケージ名がついているか確認してください。
      例では 'php' です。 ::
	
        $ cat php.build
        @LSST UPS@ &&
        curl -L \
            http://php.net/get/php-@VERSION@.tar.gz/from/this/mirror
        > @PRODUCT@-@VERSION@.tar.gz &&
        gunzip < @PRODUCT@-@VERSION@.tar.gz | tar -xf - &&
        cd php-@VERSION@ &&
        product_dir=$(eups path 0)/$(eups flavor)/@PRODUCT@/@VERSION@ &&
        ./configure --prefix=$product_dir &&
        make &&
        if [ ! -d $product_dir ]; then
                mkdir -p $product_dir;
        fi &&
        make install &&
        lsst_ups @PRODUCT@ @VERSION@ $product_dir


    * 以下では sqlalchemy（python ライブラリ）をインストールする場合の例です。
      ディレクトリ等が 'sqlalchemy' という名前で参照されているか確認しましょう。 ::
	
        $ cat sqlalchemy.build
        @LSST UPS@ &&
        curl -L \
            http://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-@REPOVERSION@.tar.gz \
        > @PRODUCT@-@REPOVERSION@.tar.gz &&
        gunzip < @PRODUCT@-@VERSION@.tar.gz | tar -xf - &&
        product_dir=$(eups path 0)/$(eups flavor)/@PRODUCT@/@VERSION@ &&
        python_version=$(python -c "import distutils.sysconfig as ds; print ds.get_python_version()") &&
        if [ ! -d $product_dir ]; then
         mkdir -p $product_dir
         mkdir -p $product_dir/lib/python$python_version/site-packages
        fi &&
        cd SQLAlchemy-@REPOVERSION@ &&
        PYTHONPATH=${product_dir}/lib/python$python_version/site-packages:$PYTHONPATH &&
        python setup.py install --prefix=$product_dir &&
        if [ ! -d $product_dir/lib/python ]; then
           mkdir -p $product_dir/lib/python
        fi &&
        ln -fs $product_dir/lib/python$python_version/site-packages  $product_dir/lib/python &&
        if [ $(eups flavor) = Linux64 -a -d $product_dir/lib64 ]; then
         rm -rf $product_dir/lib
         mv $product_dir/lib64 $product_dir/lib
        fi &&
        lsst_ups @PRODUCT@ @VERSION@ $product_dir

        
#. | buildFiles/ ディレクトリ下にテーブルファイルを作る。
   |	テーブルファイルによって新しいパッケージと環境変数の依存関係を特定します。
    	以下では python の有無による設定方法を例示しています。 

	::

	  # typical table file if no Python is needed
	  $ cat php.table    
	  pathPrepend(PATH, ${PRODUCT_DIR}/bin)
	  envPrepend(LD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
	  envPrepend(DYLD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)

	  # typical table file if Python *is* needed
	  $ cat sqlalchemy.table
	  setupRequired(python)
	  pathPrepend(PYTHONPATH, ${PRODUCT_DIR}/lib/python/site-packages)
    

#. | ビルドファイルとテーブルファイルの動作確認をする
   |	もし作成したビルドファイルとテーブルファイルの動作確認ができたら、
    	ローカルの計算機にパッケージをインストールする。

	::

	  $ cd buildFiles/
	  $ EUPS_PKGROOT=dream:. eups distrib install php 5.6.7 --noclean


#. | パッケージを作る。
   |	ここでは新しくビルドファイル、テーブルファイルのテンプレートを作り、packages/
    	ディレクトリ下にバージョン指定のビルドファイルを生成します。もし packages/
    	ディレクトリがない場合は、``eups create`` を実行する際に eups が packages/
    	ディレクトリを生成します。以下の例では PHP バージョン 5.6.7 を　``eups create``
    	で生成しています（ビルドファイル、テーブルファイルは上で示したものです）。
		
	::

	  $ cd buildFiles/
	  $ eups distrib create php 5.6.7 -v -s $HOME/public_html/packages -S buildFilePath=$PWD
       
	  # もしかすると警告文が表示されるかもしれません（とはいえ通常は無視して先に進みますが）
	  # この警告文にはスキップされた依存関係が一覧として表示されます
	  WARNING: No usable package repositories are loaded
	  Dependency gcc 4.6.4 is already deployed; skipping

   * packages/build/ ディレクトリを見ると、バージョン指定のビルドファイルが確認できます
     （例えば ``php-5.6.7.build``）。パッケージ名やバージョンが eups が置換してくれますが、
     マクロ（例 @LSST UPS@）は必ず自分で指定しないといけません。指定し忘れると eups 
     は 'XXX' と置換してしまい、エラーメッセージが表示されることもなく
     **ビルドは失敗します。**
       
   * ``startup.py`` の ``cmdHook()`` を使うと、自身で関数を設定することができます。
     例えば、packages/ ディレクトリにある ``opts.serverDir`` を指定したい時は、
     以下のように ``eups create`` を使います。 ::

       $ cd buildFiles/
       $ eups distrib create php 5.6.7 -v -S buildFilePath=$PWD

#. packages/ ディレクトリをインストールするディレクトリを含めた EUPS_PKGROOT を指定すると、
   このディストリビューションを他の計算機でも使用できるようになります。例えば、別の計算機
   old.domain.edu に php インストールしたいた時、eups ではパイプ '|' 
   を使って EUPS_PKGROOT を新たに追加することができます。ここで '|' は *or* の意味を持っており、
   以下の例では EUPS_PKGROOT という変数に、既存の EUPS_PKGROOT ディレクトリに 
   old.domain.edu を追加しています。 ::

    $ export EUPS_PKGROOT=$EUPS_PKGROOT'|'http://old.domain.edu/~user/packages/
    $ eups distrib install php 5.6.7


#. | ビルド・テーブルファイルをチェックインし、メインのディストリビューションを更新する。
   |	HSC では、buildFiles.git リポジトリは以下のようになっています。
   
	::

	  $ cd buildFiles/
	  $ git ci -m "Added package foo" foo.build foo.table
	  $ git push

	  $ ssh hsca.ipmu.jp
	  $ cd /var/git/repos/buildFiles.git/
	  $ git fetch


#. ビルドファイルは現在 hsca.ipmu.jp/sumire/packages/ にあり、自身のビルドファイル、
   テーブルファイルを main packages/ サーバーにコピーすれば、
   自身で用意したディストリビューションを make することができます。 ::


       $ ssh <build_machine>
       $ cd $HOME/public_html/packages/
       $ scp builds/php-5.6.7.build hsca.ipmu.jp:/var/www/html/sumire/packages/builds/
       $ scp tables/php-5.6.7.table hsca.ipmu.jp:/var/www/html/sumire/packages/tables/
       