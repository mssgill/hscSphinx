
============================
計算機の仕様
============================

このページではある特定の計算機の情報について記述しています。
以下の計算機にアクセスできない人は読み飛ばしてください。

master
------

.. highlight::
	bash

**EUPS のセットアップ** 方法 (bash shell の場合のみ) ::

    $ source /data1a/ana/products2014/eups/default/bin/setups.sh
    
**データリポジトリの場所**。eups の特別なコマンドで（ ``$SUPRIME_DATA_DIR``
という環境変数）で対応できます。 ::

    $ setup -v suprime_data

    $ echo $SUPRIME_DATA_DIR 
    /lustre/Subaru/SSP
    