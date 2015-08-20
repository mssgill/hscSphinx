
==============
git の使い方
==============

.. highlight::
	bash

ここでは、架空のイシュー（Issue number 1234）を例に、HSC におけるワークフローを掲載します。

* | **イシューを Jira の "In Progress" に投稿する**
  |	他のメンバーとジョブが重複しないように、今あなたが取り組んでいるジョブを周知させる事は重要です。また、Jira にジョブを報告することはメンバーやチームの進捗を知る上でも役立ちます。

* | **git に新しくブランチを作る**
  |	"tickets/HSC-<issue number>" というイシュー番号のブランチを作ります。例えば、master, releases/S14A_0 など、関係する項目下に配置します。 
  
	::

	$ git co master
	$ git co -b tickets/HSC-1234

* | **進捗/変更があったら、このブランチに報告（git commit）する**
  |	進捗は hsc-repo に ``git push`` する。この時点では進捗/変更を反映せる（コミットする）事が重要なので、ブランチ内のデータの clean は最後に行ってかまいません。作成したブランチのイシューが完全に解決するまでは、他のブランチとマージ（git merge）しないようにしてください！

* | **ブランチに報告した内容を "git rebase -i" を使って修正する**
  |	できれば、ブランチにはイシューと関連がある事項をコミットするようにしましょう。コードの bug fix や直接関係ない項目は別のブランチを立ててコミットするのが好ましいです。進捗をコミットする時は、一行程度で内容がわかるようなコミットメッセージを添えましょう。詳細は以下 [Hsc_software 3243] からのメッセージをご覧ください。ローカルで進めたジョブを強制的に master のレポジトリにする時には git push --force を実行してください。 
  
	::

	$ git rebase -i master

  * git rebase -i をすると、デフォルトで使用しているエディターが開き、
    master から分岐させたブランチでのコミット情報が表示されます（古い順）。 ::
      
          pick e32c676 Add fancy feature
          pick 6909422 Add ugly feature
          pick c90ae32 Make useful improvement on fancy feature
          pick 8fe234c Remove ugliness of ugly feature

  * 以下では、ブランチに報告したコミット情報を並べ直し、``pick`` を ``squash`` 
    に置き換えています。このように変更することで、1 つ前（例では 1 つ上）のコミットを、
    ひとつのコミットとしてまとめて master に取り込むことができます。例では、2 
    行目に記載されている 'fancy feature' というコミットを 'Add fancy feature'
    にまとめています。同様に、4 行目に記載されている 'ugly feature' は 3 行目の 
    'Add ugly feature' にまとめられています。（但し書き：エディターでの編集が終わると、
    コミットメッセージの書き換えが要求されます。) ::
    
          pick e32c676 Add fancy feature
          squash c90ae32 Make useful improvement on fancy feature
          pick 6909422 Add ugly feature
          squash 8fe234c Remove ugliness of ugly feature	

  * git log には ``pick`` でラベル付けしたコミットメッセージだけ表示されるようになります
    （コミット ID 番号とメッセージも変更されます）。 ::

          $ git log --oneline
          7bc123e Add fancy feature #2
          f740de0 Add fancy feature #1
          < other log entries >

  * もし、既にメインの git レポジトリに自身で作成したブランチのコミットを登録した後で
    修正を加える必要が生じた場合、``git push --force`` で修正を反映させる必要があります。
    しかし、この操作を行うと、メインリポジトリに蓄えられてきた履歴が上書きされてしまいます。
    そのため、個人のイシューブランチである ``tickets/HSC-1234``  で git push --force
    を行うのは問題ないかもしれません。しかし、**master ブランチ** （または、
    他者と共有しているブランチ）では ``git push --force`` を **絶対に行わないでください!!!!** ::
  
          $ git push --force

* | **イシューを Jira の "In Review" に載せる**
  |	イシューを担当できそうな査読者を選び、自身が投稿したイシューが何のパッケージで何を調べているか伝えましょう。hsc-repo に実際何を登録したか、査読者と一緒にダブルチェックします。コミットの差分を調べる時に一緒にコミット log を投稿しておくと、査読者には査読すべき項目や変更箇所がわかって便利です。以下でその方法を示しています（最後についている '..' で、"master" ブランチをベースのブランチとして置き換えています）。

	::

	$ git --no-pager log --stat --reverse origin/master..

	
* | **もしイシューで API の変更があった場合は査読者以外からもコメントを求める**
  |	コメント（注: RFC "request for comments"）は hsc_software　のメーリングリストに送りましょう。

* | **レビューが終わったらイシューを "Review Complete" にする**
  |	レビューでは、コードの機能、実装されているタスク、ドキュメンテーション、試験、他のコードとの相互作用を調べます。イシューに問題があった場合は、その問題が解決するまで master へイシューリポジトリを統合（merge）しないように、査読者はイシュー投稿者に依頼することができます。

* | **レビューコメントに対応する**
  |	査読者からのコメントに異議を唱えることができますが、レビューコメントの問題が大きい場合は、解決するまで master リポジトリへの merge は控えましょう。変更があればその都度イシューブランチにコミットします。もし変更がマイナーなものであれば、``git commit --fixup`` が使えます。このコマンドでは新たなコミットメッセージをつけずに変更をコミットすることができます。例えば、上記例に登場した 'Add fancy feature #1' のコミット関してマイナーチェンジを行った場合は以下のように行います。

	::

		$ git commit --fixup f740de0
		[dev e449123] fixup! Add fancy feature #1

		# log には '修正した' コミットが表示されます
		$ git log --oneline
		e449123 fixup! Add fancy feature #1
		7bc123e Add fancy feature #2
		f740de0 Add fancy feature #1
    
* | **"tickets/HSC-<issue number>" ブランチを master ブランチに統合（merge）する**
  |	もしうまく merge できない場合、ticket ブランチを修正し、競合している修正があれば対処します。
  
	::

		$ git co master
		$ git merge tickets/HSC-1234
    
* | **イシューの "完了" を投稿する**



コミットメッセージ
---------------------------

（[Hsc_software 3243] から抜粋）

* Please give each commit a summary that makes sense in the context of
  the entire package (not just the issue you're working on).  The
  summary is the first line of the commit message, and is an integral
  part of the git version control system (e.g., "git log --oneline"
  shows only the summary, "git cherry -v" shows only the summary).
  Good summaries allow me to easily identify commits that need to be
  moved between releases.  For more good advice about commit messages,
  see `<http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_	

* Please try to keep git commits self-contained.  As far as possible,
  each feature should be contained within one commit, and each commit
  should contain only one feature.  This simplifies the exchange of
  commits between releases.  A useful tool for this is "git gui"
  (which you may have to install separately from the git core with
  your linux distro's package manager), which allows you to separate
  work into different commits by line or by hunk.  If you're working
  remotely and can't use a GUI, "git add -p" is useful.