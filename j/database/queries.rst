.. _jp_database_queries:

=================================
HSC データにおけるクエリ実行例
=================================

初めて SQL を実行しようとしている人は、まず最初に :ref:`jp_postgres_intro`
を読んでください。 

また、NAOJ が提供している `スキーマブラウザー
<https://hscdata.mtk.nao.ac.jp:4443/schema_browser2/schema_browser.html>`_
も合わせてお読みください。

例 1
^^^^^^^^^
Download :download:`example1.sql`


.. literalinclude:: example1.sql
   :language: sql


例 2
^^^^^^^^^

Download :download:`example2.sql`

.. literalinclude:: example2.sql
   :language: sql

例 3
^^^^^^^^^

Download :download:`example3.sql`

.. literalinclude:: example3.sql
   :language: sql


例 4
^^^^^^^^^

Download :download:`example4.sql`

.. literalinclude:: example4.sql
   :language: sql


例 5
^^^^^^^^^

high-z 天体を探すためのクエリ実行例。限界等級はデータの質に応じて調整してください。

Download :download:`example5.sql`

.. literalinclude:: example5.sql
   :language: sql

例 6
^^^^^^^^^

ある特定の天域周囲にいる天体をカラーで制限をつけて検索する。

Download :download:`example6.sql`

.. literalinclude:: example6.sql
   :language: sql

例 7
^^^^^^^^^

ある CCD において forced measurement で検出された天体の shape 情報をもとに
WCS 座標を得る。

Download :download:`example7.sql`

.. literalinclude:: example7.sql
   :language: sql