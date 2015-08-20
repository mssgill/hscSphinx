
===============================================
パイプラインのコマンドに関する共通情報
===============================================

HSC パイプラインは、Bias や Flat を結合する、1 ショットの観測データを解析する、
coadd データを生成するなど、ある関数の実行に特化したコマンドの集合です。
あるコマンドは複数のツールコマンドの組み合わせでできており、
その中には全てのコマンドに共通するパラメータがあります。
このページではこうしたコマンドのパラメータについて紹介します。ここでは、
例として 1 ショットの解析で使用されるコマンドである ``hscProcessCcd.py`` を使いますが、
他のコマンドでも共通のパラメータになっています。

ヘルプ
--------

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
        ヘルプ用のパラメータ。コマンド毎にヘルプの結果は多少異なります。
    
    --calib RAWCALIB    
		一次処理データリポジトリへの入力パス。
		特別指定しなくてもパイプラインでの解析は実行されます。
		パイプラインによる :ref:`一次処理 <jp_detrend>` に従う限りでは、
		一次処理用データは適切なレポジトリに生成されます。
                            
    --output RAWOUTPUT
		出力データ用リポジトリへのパス（リポジトリがない場合は必須）。
		ある rerun における出力データを他のディレクトリやリポジトリ配下に
		置きたい場合に、このパラメータが有効となります。例えば、
		:ref:`jp_coadd_rerun_change` をご覧ください。
		        
    --rerun [INPUT:]OUTPUT
		rerun 名: OUTPUT か ROOT/rerun/OUTPUT を設定する; オプションとして
		ROOT か ROOT/rerun/INPUT を設定する。基本的に rerun の設定は
		1 つの解析ランにおいて 1 rerun が用いられます。全てのデータは自身が指定した
		rerun から入力データと呼び込まれ、出力データとして書き出されます。
		``:OUTPUT`` オプションを追加すると、同じデータリポジトリ内の異なる
		rerun にデータが出力されます。詳しくは
		:ref:`jp_coadd_rerun_change` をご覧ください。

    -c [NAME=VALUE [NAME=VALUE ...]], --config [NAME=VALUE [NAME=VALUE ...]]    
		ある config パラメータを無効にするパラメータで、例えば
		``-c foo=newfoo bar.baz=3`` のように使います。
		もし変更したい config パラメータが大量にある場合は、
		自身で config ファイルを準備し、``-C`` で読み込ませるという方法もあります。

    -C [CONFIGFILE [CONFIGFILE ...]], --configfile [CONFIGFILE [CONFIGFILE ...]]
		ある config ファイルないのパラメータにデフォルトの config 
		パラメータを置き換えてコマンドを使う時のパラメータ。config 
		ファイルには 1 行 1 パラメータを書き込んでください。
		詳細は :ref:`こちら <jp_back_config>` をご覧ください。
        
    -L LOGLEVEL, --loglevel LOGLEVEL    
		ログメッセージのレベルを特定する。ログ内のおかしなメッセージを調べたければ
		``DEBUG`` を、デフォルト設定時の基本的なコマンドの情報は ``INFO`` を、
		警告情報のみ見たければ ``WARN`` を、
		パイプラインのタスクの失敗箇所のみ調べたければ ``FATAL`` を追加してください。

    -T [COMPONENT=LEVEL [COMPONENT=LEVEL ...]], --trace [COMPONENT=LEVEL [COMPONENT=LEVEL ...]]
		'Trace' ログはある特定のラベルと関係があるメッセージを調べます
		（例えば、主に processCcd.isr のようなパッケージ。
		パイプライン内で広く使用されているログメッセージではありません）。
		``LEVEL`` は整数で、自身で設定したレベル **以下** のtrace レベルのメッセージです。
		そのため、trace レベルを高く設定すれば、より多くの trace
		メッセージを調べることができます。
	        
    --debug
		可能なデバッグ出力。
    
    --doraise    
		エラーでの例外を取り上げるパラメータ。エラーメッセージのデバッグ用に、
		ログメッセージ全体から例外だけ取り出して処理したい時に使用できます。
        
    --logdest LOGDEST    
		ログメッセージを自身で設定した場所にコピーしたい時に指定します
		（解析中のログメッセージそのものはターミナルにも出力されます）。
        
    --show [{config,data,tasks,run} [{config,data,tasks,run} ...]]
		自身で指定した情報のみを表示するパラメータ。最も使用しうるパラメータは
		``--show config`` です。このパラメータを使用すると、全ての config 
		パラメータの情報をターミナルに表示することができます。
		さらに ``--show config`` することで config
		パラメータ中のある特定のキーワードだけ抜き出して検索することも可能です。
		例えば、'*background*' という文字が含まれるパラメータだけ抜き出して表示するには
		``--show config=*background*`` と設定することができます。
		この他に有用なパラメータは ``--show tasks`` です。
		このパラメータでは、使用するコマンド内で用いられるタスクをターミナルに出力してくれます。
         
    -j PROCESSES, --processes PROCESSES
		使用するプロセスの数を指定します。このパラメータを追加すると
		1 ノード上で Python マルチプロセスが実行され、
		複数のプロセスを発生させることができます。
                            
    -t PROCESSTIMEOUT, --process-timeout PROCESSTIMEOUT
		マルチプロセスの処理時間（最大経過時間）を指定。単位は秒です。
                            
    --clobber-output    
		既存の出力ディレクトリを消去して新たに作り直すパラメータ。
		-j を付加した際にはマルチプロセスが実行する前にこのパラメータで指定される処理がはたらくため、
		マルチプロセスは安全に実行されます。
                            
    --clobber-config
		コマンドが保持している config パラメータと EUPS バージョン情報をバックアップし、
		古い config ファイルを上書きするためのパラメータ。
		HSC パイプラインでは、コマンドが実行される度に、全ての config
		パラメータと EUPS バージョン（パイプラインバージョン）の情報が保存されます。
		ある rerun においてパラメータを変更して一度実行したコマンドを改めて実行すると、
		パイプラインはそのコマンドによる解析を拒否する場合があります。
		パラメータが均一なデータを生成するためには、パイプラインによるこの処理は有効ですが、
		単にデータのテストを行いたい場合には不要な処理です。そこで、
		``--clobber-config`` パラメータを追加により、パイプラインは実行しようとしているコマンドの
		config パラメータと EUPS バージョン情報のバックアップを行い
		（<data_repo>/config/ のファイルが <foo> --> <foo>~1 に変更される）、
		古い confing ファイルを上書きしてくれます。
	
    --id [KEY=VALUE1[^VALUE2[^VALUE3...] [KEY=VALUE1[^VALUE2[^VALUE3...] ...]]
		解析を実行したいデータ ID を指定します。例えば
		``--id visit=12345 ccd=1,2`` のように使用できます。詳しくは 
		:ref:`data ID <jp_back_dataId>` をご覧ください。
