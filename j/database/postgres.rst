
.. _jp_postgres_intro:

============================
PostgreSQL の基本情報
============================

まずはじめに
---------------

IPMU にある PostgreSQL サーバーは hscdb.ipmu.jp の 5432 ポートで動いています。
データベースに接続するためには、``psql`` クライアントを、
自身の計算機環境にインストールしなくてはいけません。``psql`` クライアントは、
Mac OSX では macports や homebrew を使って簡単にインストールできます。また、
Redhat をベースにした Linux では（例 CentOS）、yum 
リポジトリを指定してインストールする方法があります（詳細は `こちら
<http://yum.postgresql.org/>`_ をご覧ください）。
``psql`` クライアントのインストールができたら、以下の方法でデータベースにアクセスできます。

.. highlight::
	bash

::

   $ psql -h hscdb.ipmu.jp -U kensaku -d dr_early -p 5432

   # -h ホストサーバー
   # -U ユーザー名（read-only）. 例では 'kensaku'
   # -d データベース名
   # -p ポート番号
   
..
   If you're logging in using your own account, you can change your password with the following command::

   > ALTER USER username WITH PASSWORD 'secret';

   .. warning:: Do not ever change the password while logged in as user ``kensaku``.
  

データベースシステムのユーザーアクセスのデフォルトは read-only です。ユーザー名
``kensaku`` （日本語では '調べる' という意味）は、
基本的な HSC のログイン情報を使えばデータベースの中身にアクセスすることができます。


ヘルプ
^^^^^^^^^^^^^

postgreSQL におけるナビゲーションや表示のコマンドはメタコマンドと呼ばれており、
``\`` （バックスラッシュ）と一緒に使います。
メタコマンドの一覧は次のコマンドで呼び出すことができます。 ::

  > \?

また、あるメタコマンドのヘルプ情報を表示させるには ``\h`` を使います。 
例えば、``SELECT`` コマンドのヘルプ情報が知りたい場合は以下の通りです。 ::

  > \h SELECT

特定のメタコマンドを指定せずに ``\h`` を実行した場合は、
``\h`` でヘルプ情報が表示できる全てのメタコマンドの一覧が表示されます。


データベース、スキーマ、テーブルに関する情報を表示する
------------------------------------------------------
  
* データベースの一覧を表示する（小文字の 'L'） ::

    > \l

* 特定のデータベースに接続する。例えば、``dr_early`` というデータベースに接続するには以下 ::

    > \c dr_early

* どのデータベースに接続しているか確認する ::

    > SELECT current_database();
    
* スキーマの一覧を表示する ::

    > \dn

* あるスキーマをデフォルトで使用するように設定する（例では、SSP wide の初期リリースデータの場合） ::

    > set search_path to ssp_s14a0_wide_20140523a;
    
* テーブルとスキーマの一覧を表示（ここでは既に上記 ``search_path`` を設定しているものとする） ::

    > \dt

    # + をつけると表示される情報が増える
    > \dt+

    # 'search_path' で設定したスキーマと異なるスキーマを使用したい場合
	# 新たに使用したいスキーマを正しく指定する必要がある（例では SSP UD の初期リリースデータ）
    > \dt ssp_s14a0_udeep_20140523a.*
  
* テーブル内のカラムを表示（例 テーブルの 'frame' カラムを表示させる） ::

    > \d frame

    
シェルコマンド
--------------

postgreSQL 内で bash のシェルコマンドを使用したい時には、
以下のメタコマンドで実行できます（例 ``ls`` を使用したい時）。 ::

    > \! ls

    
データベースへのクエリ
-------------------------

SQL を用いたデータベースへのクエリ（検索）では 'SELECT' の命令文が用いられます。
ここでは SQL クエリの概略の説明し、さらにクエリの実行例をいくつか紹介します。
このページ以外にも web 上にはたくさんの SQL のチュートリアルがあるので、
そちらを参考になります（例えば、`PostgreSQL Tutorial
<http://www.postgresqltutorial.com/postgresql-select/>`_.）。

SQL で使用されるキーワード文は慣例的に大文字で書くことになっています。
キーワードを大文字で書く慣例はクエリ文を読みやすくするためであり、必須項目ではありません。
そのため、``SELECT`` を ``select`` と書いてクエリを実行しても、``psql``
クライアントはそのクエリを認識してくれます。
ここで紹介しているクエリの実行例は読みやすいようにキーワード文字毎に改行しています。
しかし、``psql`` クライアントでは単一の長いコマンドが実行されます。そのため、
以下に掲載している 2 つのクエリ実行例のどちらでも同じ検索結果が返ってきます。 ::

    > SELECT
         ra2000, decl2000, imag_psf
      FROM
         photoobj_mosaic__deepcoadd__iselect
      WHERE
         imag_psf < 23.0;

         
    > select ra2000, decl2000, imag_psf from photoobj_mosaic__deepcoadd__iselect where imag_psf < 23.0;

デフォルトでは、クエリを実行すると、ターミナル上に検索結果が返されます。
クエリを設定する段階では、ターミナルに返される検索結果の上限値を入れておくと良いかもしれません
例えば、20 エントリーだけ検索結果を返したい場合は、自身のクエリに ``LIMIT 20`` 
を追加して実行してください。 ::

    > SELECT imag_psf FROM  photoobj_mosaic__deepcoadd__iselect LIMIT 20;


クエリ実行結果をファイルに出力する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``psql`` クライアントを介してクエリを実行し、
その結果を自身の計算機環境にファイルとして出力するには、``\o file.dat``
というメタコマンドで検索結果の出力先をターミナルから ``file.dat`` に変更します
（この場合、検索結果は ascii ファイルとして出力されます）。クエリを実行し、
ファイルを出力した後は、引数がない ``\o`` メタコマンドを実行して出力をデフォルト
（ターミナル）に戻しましょう。 ::
	
    > \o imag.dat
    > SELECT imag_psf FROM  photoobj_mosaic__deepcoadd__iselect LIMIT 20;
    > \o
    
      
スクリプトでクエリを実行する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``psql`` 環境外からスクリプトベースでクエリを実行することができます
（emacs では、``.sql`` のファイル内の SQL 
構文をデフォルトでハイライト表示してくれます）。スクリプトは、``psql`` 
コマンドにスクリプト名を指定する ``-f file.sql`` という引数を追加すると実行できます。 ::

    $ cat file.sql
    set search_path to ssp_s14a0_wide_20140523a;
    \o imag.dat
    SELECT imag_psf FROM  photoobj_mosaic__deepcoadd__iselect LIMIT 20;
    \o

    $ psql -h hscdb.ipmu.jp -U kensaku -d dr_early -p 5432 -f file.sql

もしスクリプト内に ``\o file.dat`` の設定を含めない場合、全出力は ``stdout`` 
となります（例えば、ターミナル出力）。出力先の変更はここから行ってください。

