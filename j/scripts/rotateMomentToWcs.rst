
rotateMomentToWcs.py
--------------------

スクリプトをダウンロードする :download:`rotateMomentToWcs.py`.

以下のスクリプトでは、adaptive moments の取り扱いの中でも、
pixel 座標系で測定された moment を arcsec 単位に変換する方法を紹介しています。

..
	The following demonstrates how to work with adaptive moments,
	specifically how to convert moments measured in the pixel coordinate
	system having a known WCS to moments in units of arcseconds, with
	position angle theta aligned to the axis of Right Ascension.

.. _jp_rotateMomentToWcs:

.. literalinclude:: rotateMomentToWcs.py
   :language: python

