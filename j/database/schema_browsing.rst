.. _jp_schema_browsing:

=====================================================
HSC SSP データベースのスキーマブラウザー
=====================================================

NAOJ が提供するオンラインスキーマブラウザー
----------------------------------------------------
オンラインスキーマブラウザーが NAOJ により提供されています:
`スキーマブラウザー 
<https://hscdata.mtk.nao.ac.jp:4443/schema_browser2/schema_browser.html>`_ 。
スキーマブラウザーには、カラム名, データベースの形式, コメント, カラムの値の形式, 
単位系, DB 内のキーワードと HSC パイプラインにおけるキーワード名が表示されています。
ターゲットテーブルはデータベーススキーマにあるテーブル名をクリックすると切り替わります。
例えば、'ssp_s14a0_udeep_20140523a'（UDEEP COSMOS のカタログテーブル）
をクリックするとターゲットテーブルが表示されます。スキーマテーブルの詳細な使い方は
`スキーマブラウザー 
<https://hscdata.mtk.nao.ac.jp:4443/schema_browser2/schema_browser.html>`_ 
ページ冒頭の説明箇所をお読みください。


hscDb パッケージ内のスクリプト
-----------------------------------------
HSC パイプラインをインストールすると、hscDb パッケージが利用できます。この
hscDb パッケージにはデータベースのテーブル情報を閲覧するための
2 つのスクリプトがあります。1 つ目は '**getHscTableName.py**' で、
ある特定のデータベーススキーマの全テーブルを表示してくれます。2 つ目は
'**getHscTableInfo.py**' で、インデックスの情報や定義を含む、
ある特定のデータベーステーブルのスキーマを表示してくれます。

テーブル名一覧を表示する::

    getHscTableName.py --dbname=database --dbhost=host_name or address --dbschema=schema_name
                -U kensaku -p password_for_kensaku_user

    ex) getHscTableName.py --dbname=dr_early --dbhost=192.168.0.1 --dbschema=ssp_s14a0_udeep_20140523a 
                -U kensaku -p password_for_kensaku_user

テーブルスキーマ一覧を表示する::

    getHscTableInfo.py --dbname=database_name --dbhost=host_name or address --dbschema=schema_name 
                       -U kensaku -p password_for_kensaku_user table_name 

    ex) getHscTableInfo.py --dbname=dr_early --dbhost=192.168.0.1 --dbschema=ssp_s14a0_udeep_20140523a 
                       -U kensaku -p password_for_kensaku_user mosaic__deepcoadd 

データベース管理者に、ユーザー名 'kensaku' のパスワードを聞いてから実行してください。


psql を使う
---------------------
:ref:`jp_postgres_intro` で説明したように、データベースにアクセスするために
'psql' コマンドを使い、テーブルの情報やインデックスを閲覧するために '\dt+', 
'\dv+', '\di+' コマンドを使うのは簡単です。
