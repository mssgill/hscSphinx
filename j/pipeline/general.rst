
====================================
Pipeline のコマンドに関する共通情報
====================================

Pipeline は、bias や flat を結合する、1 観測ショットの解析を実行する、
coadd を構築し実行するなど、ある関数の実行に特化したコマンドの集合です。
ある Pipeline コマンドは複数の tool コマンドの組み合わせでできており、
その中には全てのコマンドで共通のあるコマンドオプションがあります。このページでは
こうしたコマンドオプションについて紹介します。ここでは、例として 1 ショットの
解析コマンドである ``hscProcessCcd.py`` を使いますが、他のコマンドでも
共通のオプションになっています。

ヘルプ
------

ヘルプを呼び込むにはコマンドの後に ``--help`` または ``-h`` を追加します。
例えば、``hscProcessCcd.py`` のヘルプを呼び込むと以下のような中身が返されます。::

    $ hscProcessCcd.py -h
    usage: hscProcessCcd.py input [options]

    positional arguments:
      ROOT                  path to input data repository, relative to
                            $PIPE_INPUT_ROOT

    optional arguments:
      -h, --help            show this help message and exit
      --calib RAWCALIB      path to input calibration repository, relative to
                            $PIPE_CALIB_ROOT
      --output RAWOUTPUT    path to output data repository (need not exist),
                            relative to $PIPE_OUTPUT_ROOT
      --rerun [INPUT:]OUTPUT
                            rerun name: sets OUTPUT to ROOT/rerun/OUTPUT;
                            optionally sets ROOT to ROOT/rerun/INPUT
      -c [NAME=VALUE [NAME=VALUE ...]], --config [NAME=VALUE [NAME=VALUE ...]]
                            config override(s), e.g. -c foo=newfoo bar.baz=3
      -C [CONFIGFILE [CONFIGFILE ...]], --configfile [CONFIGFILE [CONFIGFILE ...]]
                            config override file(s)
      -L LOGLEVEL, --loglevel LOGLEVEL
                            logging level
      -T [COMPONENT=LEVEL [COMPONENT=LEVEL ...]], --trace [COMPONENT=LEVEL [COMPONENT=LEVEL ...]]
                            trace level for component
      --debug               enable debugging output?
      --doraise             raise an exception on error (else log a message and
                            continue)?
      --logdest LOGDEST     logging destination
      --show [{config,data,tasks,run} [{config,data,tasks,run} ...]]
                            display the specified information to stdout and quit
                            (unless run is specified).
      -j PROCESSES, --processes PROCESSES
                            Number of processes to use
      -t PROCESSTIMEOUT, --process-timeout PROCESSTIMEOUT
                            Timeout for multiprocessing; maximum wall time (sec)
      --clobber-output      remove and re-create the output directory if it
                            already exists (safe with -j, but not all other forms
                            of parallel execution)
      --clobber-config      backup and then overwrite existing config files
                            instead of checking them (safe with -j, but not all
                            other forms of parallel execution)
      --id [KEY=VALUE1[^VALUE2[^VALUE3...] [KEY=VALUE1[^VALUE2[^VALUE3...] ...]]
                            data ID, e.g. --id visit=12345 ccd=1,2

.. glossary:: 

    ROOT
        :ref:`データリポジトリ <j_data_repo>` への入力パス。

    -h, --help
        ヘルプオプション。コマンド毎にヘルプの結果は多少異なります。
    
    --calib RAWCALIB    
		一次処理データリポジトリへの入力パス。特別指定しなくても Pipeline での
		解析は実行されます。Pipeline による :ref:`一次処理 <j_detrend>`
		に従う限りでは、一次処理用データは適切なレポジトリに生成されます。
                            
    --output RAWOUTPUT
		出力データ用リポジトリへのパス（リポジトリがない場合は必須）。
		ある rerun における出力データを他のディレクトリやリポジトリ配下に
		置きたい場合に、このオプションが有効となります。例えば、
		:ref:`異なる rerun リポジトリに coadd データを出力する場合 <j_coadd_rerun_change>`.
		をご覧ください。
		        
    --rerun [INPUT:]OUTPUT
		rerun 名: OUTPUT か ROOT/rerun/OUTPUT を設定する; オプションとして
		ROOT か ROOT/rerun/INPUT を設定する。基本的に rerun の設定は
		1 つの解析ランにおいて 1 rerun が用いられます。全てのデータは自身が
		指定した rerun から入力データと呼び込まれ、出力データとして書き出されます。
		``:OUTPUT`` オプションを追加すると、同じデータリポジトリ内の
		異なる rerun にデータが出力されます。詳しくは
		:ref:`異なる rerun リポジトリに coadd データを出力する場合 <coadd_rerun_change>`
		をご覧ください。

    -c [NAME=VALUE [NAME=VALUE ...]], --config [NAME=VALUE [NAME=VALUE ...]]    
		ある config パラメーターを無効にするオプションで、例えば
		``-c foo=newfoo bar.baz=3`` のように使います。
		もし変更したい config パラメーターが大量にある場合は、
		自身で config ファイルを準備し、 ``-C`` で読み込ませるという方法もあります。

    -C [CONFIGFILE [CONFIGFILE ...]], --configfile [CONFIGFILE [CONFIGFILE ...]]
		ある config ファイルないのパラメーターにデフォルトの config パラメーターを
		置き換えてコマンドを使う時のオプション。config ファイルには
		一行一パラメーターを書き込むようにする。
		詳細は :ref:`こちら <j_back_config>` をご覧ください。
        
    -L LOGLEVEL, --loglevel LOGLEVEL    
		ログメッセージのレベルを特定する。ログ内のおかしなメッセージを調べたければ
		``DEBUG`` を、デフォルト設定時の基本的なコマンドの情報は ``INFO`` を、
		警告情報のみ見たければ ``WARN`` を、Pipeline のタスクの失敗箇所のみ
		調べたければ ``FATAL`` を追加してください。

    -T [COMPONENT=LEVEL [COMPONENT=LEVEL ...]], --trace [COMPONENT=LEVEL [COMPONENT=LEVEL ...]]
		'Trace' ログは Pipeline 内で広く使用されているログメッセージでは
		ありませんが、ある特定のラベルと関係があるメッセージを調べます
		（例えば、主に processCcd.isr のようなパッケージ）。``LEVEL`` は
		整数で、自身で設定したレベル **以下** のtrace レベルのメッセージです。
		そのため、trace レベルを高く設定すれば、より多くの trace メッセージを
		調べることができます。
	        
    --debug
		可能な debug 出力。
    
    --doraise    
		エラーでの例外を取り上げるオプション。エラーメッセージを debug するために
		ログメッセージ全体から例外だけ取り出して処理したい時に使用できます。
        
    --logdest LOGDEST    
		ログメッセージを自身で設定した場所にコピーしたい時に指定します
		（解析中のログメッセージそのものはターミナルにも出力されます）。
        
    --show [{config,data,tasks,run} [{config,data,tasks,run} ...]]
		自身で指定した情報のみを表示するオプション。最も使うであろうオプションは
		``--show config`` です。このオプションを使用すると、全ての config 
		パラメーターの情報をターミナルに表示することができます。さらに有用なのは、
		config パラメーター中のある特定のキーワードだけ抜き出して検索することも
		可能な点です。例えば、'*background*' という文字が含まれるパラメーター
		だけ抜き出して表示するには ``--show config=*background*`` と
		設定することで実行されます。この他に有用なオプションは ``--show tasks`` です。
		このオプションでは現在自身が使用している Pipeline コマンドで用いられる  
		のタスクをターミナルに出力してくれます。
         
    -j PROCESSES, --processes PROCESSES
		使用するプロセスの数を指定します。このオプションでは、1 ノード上で
		複数のプロセスを発生させるために Python マルチプロセスを使用します。
                            
    -t PROCESSTIMEOUT, --process-timeout PROCESSTIMEOUT
		マルチプロセスの処理時間を指定; 最大経過時間で、秒で指定します。
                            
    --clobber-output    
		既存の出力ディレクトリを消去したり再生成するオプション
		（-j をつけて実行したほうが安全です）。
/*		(safe with -j, but not all other forms of parallel execution). */
                            
    --clobber-config
		Pipeline が実行される度に全ての config パラメーターと ``setup`` パッケージ
		の EUPS バージョンは保存されます。これら解析のパラメーターと EUPS の
		バージョンは、ある rerun における解析の度に Pipeline 内で調べられます。
		もし何かパラメーターを変更した場合、データが不均一となるため Pipeline では
		そのコマンドの実行を拒否します。最終データを生成する上時にデータの均一性を
		保つために Pipeline のこの処理は有効ですが、単にデータのテストを行い
		たい場合には不要です。そこで、``--clobber-config`` を特定すると、
		Pipeline コマンドでは現在使用している config パラメーターと
		EUPS バージョン情報のバックアップを行い
		（<data_repo>/config/ のファイルが <foo> --> <foo>~1 に変更される）、
		古い cifing　ファイルを上書きします。
	
    --id [KEY=VALUE1[^VALUE2[^VALUE3...] [KEY=VALUE1[^VALUE2[^VALUE3...] ...]]
		解析を実行したいデータ ID を指定します。例えば ``--id visit=12345
         ccd=1,2`` のように使用できます。詳しくは 
		 :ref:`data ID <j_back_dataId>` をご覧ください。
