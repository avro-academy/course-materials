ADVANCED GIT & GITHUB: starter files
Avro Academy · Advanced Git & GitHub: Work Like a Pro Team

pay-calculator/   A practice Git repo with 12 commits and a v1.0 tag (Modules 1-4).
                  It was made with fixed dates and names, so its commit IDs are
                  exactly the ones in the lessons (40bd88b, be19a4a and so on).
                  Start each module from a freshly unzipped copy: commands that
                  change history (amend, reset, rebase) change the IDs after them.
                  Module 7: run  git switch leaked-key  to see a commit where
                  someone forced a .env file with an API key into the repo
                  (the key is made up).
                  Run the tests with:  python test_pay.py   (python3 on Mac/Linux)
                  They fail on main on purpose. Module 4 shows you how to find
                  the commit that broke them.

shift-swap/step-6-final/
                  The finished Shift Swap app from the Flask course, with
                  17 tests (Module 6: put it in its own repo and add CI).

ci-files/.github/ Ready-made GitHub files to copy into a repo:
                    workflows/tests.yml        runs the tests on every PR
                    dependabot.yml             weekly update pull requests
                    pull_request_template.md   fills in every new PR
                    CODEOWNERS                 who reviews what
                  The folder starts with a dot, so it may be hidden. In
                  Windows File Explorer: View > Show > Hidden items. On a Mac,
                  press Cmd + Shift + . in Finder.
