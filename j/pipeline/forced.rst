.. _jp_forced:

=================
Forced Photometry
=================

forced photometry はある band の画像で検出された天体の座標情報を使い、
他 band の画像で天体の測定を行います。具体的には、天体検出の参照画像としてある
filter を指定し（例えば HSC-I）、この filter で検出された天体の座標をもとに
HSC-G, HSC-R など他 band の画像を使って天体の測定が行われます。
他に方法としては、最も深い coadd 画像から検出された天体の座標を参照し、
forced photometry を行う場合もあります。

Pipeline を用いて forced photometry より前の解析処理が終了しているなら、
coadd 画像の測定情報を使って visit, CCD 単位で天体のフラックスやサイズを測り直すことができます。 ::

    $ forcedPhotCcd.py /data/Subaru/HSC --rerun=myrerun --id visit=1234 ccd=0..103 tract=0
