
.. _jp_showbackground:

showBackground.py
-----------------

スクリプトをダウンロードする :download:`showBackground.py`.

以下のスクリプトでは、一次処理済データを読み出すもので、:ref:`ccdplot.py <jp_ccdplot>` 
と非常によく似たものとなっています。しかし、この例では、一次処理済データで既に引かれている
background の取り扱いについても追加しています。一次処理済データでは既に background
が引かれていますが、中には自分で background 引きを行いたいという人がいるかもしれません。
そんな人たち用に、background 画像を読み出し、一次処理済データに戻す場合も例示します。


.. literalinclude:: showBackground.py
   :language: python

