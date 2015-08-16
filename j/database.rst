
======================
データベース
======================

このページでは、HSC データベースにおける検索を例としながら
PostgreSQL について簡単に紹介していきます。もしあなたが既に PostgreSQL
に詳しい場合は、以下のテーブルから必要な情報へ辿ってください。

.. toctree::
   :maxdepth: 3

   database/postgres
   database/tables
   database/stored_function
   database/queries
   database/schema_browsing
   database/cloning

このページ以外にも、NAOJ の `スキーマブラウザー
<https://hscdata.mtk.nao.ac.jp:4443/schema_browser2/schema_browser.html>`_
に PostgreSQL について掲載されていますので、そちらもご覧ください。

データベース接続情報::

   # ほぼ変更しない内容
   User: kensaku
   Pass: The HSC standard one (you probably typed it to see this webpage)
   Port: 5432
   Host: hscdb.ipmu.jp

   # 新たなデータリリース毎に変更される内容
   Database: dr_early
   Schemas:
       ssp_s14a0_wide_20140523a
       ssp_s14a0_udeep_20140523a
