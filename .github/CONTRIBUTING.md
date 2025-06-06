# Contributing Guidelines

This document outlines best practices for managing scripts and tools in this
repository when working with AI assistants like GitHub Copilot.

## File Creation Rules

- Use meaningful names for permanent scripts
- Prefix temporary test scripts with `tmp-`
- Create temporary files in `~/bin/steff` when possible
- Document at the top of each file whether it's permanent or temporary

## Cleanup Protocols

- Remove all temporary scripts after completing the task
- When creating temporary files, track them in a list for later cleanup
- Always clean up test scripts unless explicitly requested to keep them
- Move useful test scripts to a proper location (`~/bin/tests`) if they have
  lasting value

## Organization Practices

- Keep `~/bin` uncluttered - only permanent, useful scripts belong there
- Use `~/bin/tests` for test scripts that need to be preserved
- Follow the established naming conventions in each directory

## Documentation

- Add clear comments explaining what each script does
- Include usage examples in script headers
- Update README.md when adding permanent scripts to `~/bin`
- Don't use notebook format anywhere

## Best Practices

- Follow shell scripting best practices for the target shell (zsh, bash, etc.)
- Make scripts executable and include appropriate shebangs
- Include error handling in scripts that could fail
- Use consistent formatting and style across all scripts
- Test scripts thoroughly before marking them as permanent

## Source Control

- The repository uses [Jujutsu](https://jj-vcs.github.io/jj/latest/) in
  colocated mode on top of a git repo.
- Jujutsu maintains a list of changesets designated by alphabetic codes as
  opposed to the hexadecimal hashes of git.
- To view the commit log, run: `jj log`.
- An example listing of changesets is:

  ```bash
  ❯ jj log
  @  tzswroox john.gaines@netscout.com 2025-06-06 17:04:20 1534ffcc
  │  agent contributing guide
  ○  stmkvpol john.gaines@netscout.com 2025-06-06 16:43:09 git_head() 269a50f5
  │  clean-bash for agent
  ○  wvwmpozs john.gaines@netscout.com 2025-06-06 12:53:32 35413652
  │  sort-vscode-settings
  ◆  ytunkuyz me@jgaines.com 2025-06-06 01:18:09 master?? master@bborigin master@git master@origin a5046053
  │  added some security checks to scripts using external files
  ~
  ```

- The changeset with the @ in the first character is the current set, any
  changes made in the project folder will get automatically added to the current
  changeset.
- A changeset with a ○ in the first column has not been commited to the remote
  repository yet so can be manipulated.
- A changeset with a ◆ in the first column has been pushed to a remote so should
  not be changed.
- Your current working set of changesets is the list of changesets from the one
  with the ◆ to the one with the @.
- Before making any changes, you should execute `jj new -m "description"`, where
  you should replace the string description with a short description of the
  changes.  That will create a new changeset from the current @ changeset, which
  any new changes will get placed in.
- You can examine the details of any changeset by running `jj show tzswroox` for
  example to show the contents of the active changeset.
