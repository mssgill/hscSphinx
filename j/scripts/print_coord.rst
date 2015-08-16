
print_coord.py
--------------

スクリプトをダウンロードする :download:`print_coord.py`.

以下では、butler を使って、天体の座標系をどう扱うかを示しています。
座標系は様々な表記系（ICRS, FK5, Galactic, Ecliptic）に変換され、
座標系の各次元は様々な形式で表示されます。

..
	The following demonstrates how to work with Coord objects loaded
	through the butler.  Coords are converted between the various types
	(ICRS, FK5, Galactic, Ecliptic), and the Angle objects used for each
	dimension of the coordinate (i.e. RA and Dec are each Angles) are
	printed in various standard forms.


.. _jp_print_coord:

.. literalinclude:: print_coord.py
   :language: python

