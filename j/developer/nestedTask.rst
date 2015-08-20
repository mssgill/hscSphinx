
==========
nestedTask
==========

.. _jp_nestedtask:

以下では :ref:`simpleTask.py <jp_simpletask>` よりちょっと複雑なタスクの例を紹介しています。
``nestedTask.py`` では NestedTask と呼ばれるメインのタスクが使われています。NestedTask
には ``Step1`` と ``Step2`` と呼ばれる 2 つのサブタスクが含まれています。同様に、``Step2`` 
には ``Step2a`` と ``Step2b`` という 2 つのサブ-サブタスクが含まれています。
このスクリプトをパイプラインコードで使うために、``nestedTask.py`` では simpleTools 
コードを実行しています。また、パイプラインでこのスクリプトを実行するために、
import を以下のように変更してください。 ::

    import lsst.pex.config        as pexConfig
    import lsst.pipe.base         as pipeBase

``nestedTask.py`` スクリプトは以下の方法で実行できます
（このスクリプトを実行した際の出力も示してあります）。 

.. highlight::
	bash

::
	
    $ ./nestedTask.py $PWD -j2 --id visit=100..102:2
	
    Starting the main pipe with:  OrderedDict([('visit', '100')])
    In Step1: OrderedDict([('visit', '100')]) par1 is: 1.0
    In Step2: OrderedDict([('visit', '100')]) par2 is: 2.0
       --> In Sub2a: OrderedDict([('visit', '100')]) par2a is:2.1
       --> In Sub2b: OrderedDict([('visit', '100')]) par2b is:2.2
    Starting the main pipe with:  OrderedDict([('visit', '102')])
    In Step1: OrderedDict([('visit', '102')]) par1 is: 1.0
    In Step2: OrderedDict([('visit', '102')]) par2 is: 2.0
       --> In Sub2a: OrderedDict([('visit', '102')]) par2a is:2.1
       --> In Sub2b: OrderedDict([('visit', '102')]) par2b is:2.2


nestedTask.py
--------------

.. highlight::
	python

.. literalinclude:: simpleTools/nestedTask.py
