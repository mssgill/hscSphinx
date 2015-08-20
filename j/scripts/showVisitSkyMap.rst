

showVisitSkyMap.py
------------------

スクリプトをダウンロードする :download:`showVisitSkyMap.py`.

ここではあるデータセットにおける SkyMap と CCDs の表示方法を紹介します。
スクリプトは非常に単純です。

.. warning::

	HSC カメラに関するコードは HSC パイプライン開発者らによって既に準備されています。
	自身でコードをいじって使用する際は、
	パイプラインが最新のバージョンかどうかチェックして使用してください。
	
	
..	The camera-related code has already been rewritten in the LSST
	fork of the pipeline, and the new implementation will eventually
	be imported into the HSC fork.  We will naturally update the
	documentation accordingly when that happens, but please be aware
	that if you develop new code based on what you see here, it too
	will have to be updated.

.. _jp_showvisitskymap:

.. literalinclude:: showVisitSkyMap.py
   :language: python


スクリプトを実行させるには、

.. highlight::
	bash
	
::

    $ python skymap.py /data2b/work/bick/HSC/rerun/cosmos 0 902^904 -p

出力
^^^^^^

.. image:: ../images/showVisitSkyMap.png
