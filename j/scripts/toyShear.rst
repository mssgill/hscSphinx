
toyShear.py
-----------

スクリプトをダウンロードする :download:`toyShear.py`.

以下の例では、moment を adaptive moment や楕円体に変換するための方法を紹介しています。
例では galaxy-galaxy shear でよく使われるような toy calculation を用いています。
中心の pixel 座標は中心に対して定義された native x, y を用いており、
天体の pixel-moment はこの座標を中心に回転されています。moment 
は様々な楕円体の形（E1, +ve, -ve）に変換されます。

..
	The following demonstrates how to work with moments to convert the
	measured adaptive moments, Ixx/Iyy/Ixy to semi-major and semi-minor
	axes, and how to convert these to ellipticities of various types.  The
	example is meant to represent a toy calculation which might be used in
	computing galaxy-galaxy shear.  A central pixel coordinate is chosen,
	and the pixel-moments of the sources are rotated from the native x,y
	coordinate system to ones defined with respect to the central
	position.  The moments are then converted to various ellipticities,
	with E1 then representing the tangential (+ve) and radial (-ve)
	components.

.. _jp_toyShear:

.. literalinclude:: toyShear.py
   :language: python

