


==============
Git Workflow
==============

The following outlines the HSC (borrowed from LSST) workflow for a
fictional issue being developed (which will be Issue number 1234) by a
fictional user ``jdoe``.


* **Put the issue into "In Progress" in Jira**.  This is important, as
  it tells others what you're working on so that work isn't
  duplicated.  It also helps with the accumulation of statistics that
  inform our progress.

* **Create a Git branch** "u/<username>/HSC-<issue number>" from the
  appropriate place (e.g., master, releases/S14A_0)::

      $ git co master
      $ git co -b u/jdoe/HSC-1234

* **Commit changes to this branch as you work**.  Push them to
  hsc-repo.  These changes may not be particularly clean --- the
  principal focus is on getting the substance in --- you can clean up
  later.  Do not merge other branches into your issue branch unless it
  is required to fulfill the purpose of the issue.

* **Use "rebase -i" on the branch to clean up the commits** when
  ready.  As far as it is possible, there should be a one-to-one
  relationship between features and commits.  Try to separate bug
  fixes made in distinct parts of the code.  Try to separate features
  that aren't directly related.  The tests should pass for each
  commit.  There should be a helpful commit message as part of each
  commit, with a concise summary on the first line.  Reasons for this,
  along with more details are attached below, from message
  [Hsc_software 3243].  Push with --force to hsc-repo::

       $ git rebase -i master

  * this will open your default editor and show you the commits since
    branching from master (oldest at top)::
      
          pick e32c676 Add fancy feature
          pick 6909422 Add ugly feature
          pick c90ae32 Make useful improvement on fancy feature
          pick 8fe234c Remove ugliness of ugly feature

  * You can reorder the commits, and changing ``pick`` to ``squash``
    will cause the 'squashed' commit to be combined with the one
    before (above) it.  Here the 2nd 'fancy feature' commit is moved
    to follow the 'Add fancy feature' commit, and is squashed onto it.
    The same is done for 'ugly feature'. (Note: you'll be asked to
    rewrite the commit message when this step is done)::
    
          pick e32c676 Add fancy feature
          squash c90ae32 Make useful improvement on fancy feature
          pick 6909422 Add ugly feature
          squash 8fe234c Remove ugliness of ugly feature

  * Git log will now show only the picked commits (note the hashes and
    messages have changed)::

          $ git log --oneline
          7bc123e Add fancy feature #2
          f740de0 Add fancy feature #1
          < other log entries >

  * If you rebase a branch which has already been pushed to the
    main Git repo, you will need ``--force`` to push the rebased
    working copy.  Note that doing this will rewrite the history in
    the main Git repository.  It's fine to do this on your personal
    ``u/jdoe/HSC-1234`` branch, but **you should never use** ``--force``
    **on the master branch** (or any branch which is shared with other
    developers).::

          $ git push --force

          
* **Put the issue into "In Review" in Jira.** Choose a suitable
  reviewer (don't need to change the assignee).  Be sure to tell them
  what branch to look at, and what packages.  Double-check that you
  actually pushed everything to hsc-repo.  It would be helpful if you
  could post the commit logs along with the diff stats so they know
  exactly what they're being asked to review and they can compare that
  with what they have in their git.  The command for this is::

      # note that that's two dots only at the end of the line
      # replace "master" with the base of the branch as appropriate
      $ git --no-pager log --stat --reverse origin/master..

* **Send an RFC if the issue introduces an API change** in anything
  that might possibly be used by anyone.  The RFC ("request for
  comments") should be sent to the hsc_software list.

* **The reviewer should put the issue into "Review Complete"** and
  post the review.  The review should cover the suitability of the
  feature, implementation, documentation and tests; code and commit
  style; and any concerns about interaction with other components.
  The reviewer may request holding off merging until some problem is
  resolved.

* **Deal with the review comments.** You are permitted to disagree
  with the reviewer, but if the disagreement is anything more than
  tiny you should hold off merging until the disagreement is resolved.
  Commit any changes into your issue branch.  The concern to keep the
  history clean still applies here.  If the changes are minor, you
  could use "commit --fixup", which will make it easier to clean up.
  E.g. assuming you fix something related to the commit 'Add fancy
  feature #1' above::

     $ git commit --fixup f740de0
     [dev e449123] fixup! Add fancy feature #1

     # the log will show the fixup which you can easily 'rebase'
     $ git log --oneline
     e449123 fixup! Add fancy feature #1
     7bc123e Add fancy feature #2
     f740de0 Add fancy feature #1

     
* **Create branch "tickets/HSC-<issue number>"** from your "u/"
  personal issue branch.  This is your last chance to clean up your
  commits to keep the history clean.  If you have any "fixup" commits,
  do a "rebase -i" to squash them into the original.  Push the branch
  to hsc-repo::

      $ git co u/jdoe/HSC-1234
      $ git co -b tickets/HSC-1234
      $ git rebase -i master
    
* **Merge the "tickets/HSC-<issue number>" branch to master** (or the
  desired location).  If it doesn't merge cleanly, I suggest rebasing
  the ticket branch and dealing with any conflicts there, rather than
  as part of the merge (otherwise the merge is more than just a
  merge)::

      $ git co master
      $ git merge tickets/HSC-1234
    
* Put the issue into **"Done".**



Commit Messages
---------------

(From [Hsc_software 3243])

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
