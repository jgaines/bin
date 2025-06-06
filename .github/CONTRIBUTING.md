# Contributing Guidelines

This document outlines best practices for managing scripts and tools in this
repository, particularly when working with AI assistants like GitHub Copilot.

## File Creation Rules

- Use meaningful names for permanent scripts
- Prefix temporary test scripts with `tmp-`
- Create temporary files in `~/bin/steff` when possible
- Document at the top of each file whether it's permanent or temporary

## Cleanup Protocols

- Remove all temporary scripts after completing the task
- When creating temporary files, track them in a list for later cleanup
- Always clean up test scripts unless explicitly requested to keep them
- Move useful test scripts to a proper location (`~/bin/tests`) if they have lasting value

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

- The repository uses [Jujutsu](https://jj-vcs.github.io/jj/latest/).
- Jujutsu maintains a set of changesets designated by alphabetic codes as
  opposed to the hexadecimal hashes of git.
- An example listing of changesets is:

  ```bash
  ❯ jj log
  @  ykwqrvso john.gaines@netscout.com 2025-06-06 16:24:16 255ab6ca
  │  (no description set)
  ○  uylyqqrt john.gaines@netscout.com 2025-06-06 16:11:00 git_head() b5f34b97
  │  tweak contributing instructions
  ○  mnstnmul john.gaines@netscout.com 2025-06-06 16:07:11 cd372270
  │  contributing instructions for agent
  ○  stmkvpol john.gaines@netscout.com 2025-06-06 16:07:11 55c458cb
  │  clean-bash for agent
  ○  wvwmpozs john.gaines@netscout.com 2025-06-06 12:53:32 35413652
  │  sort-vscode-settings
  ◆  ytunkuyz me@jgaines.com 2025-06-06 01:18:09 master* a5046053
  │  added some security checks to scripts using external files
  ~
  ```

- Your current working set of changesets is the chain of changesets from the one
  flagged git_head() to the one marked with @ in the first character position.
- Before making any changes, you should execute `jj new -m "description"`, where
  you should replace the string description with a short description of the
  changes.
- The commit log can be shown with `jj log`.
- You can examine the details of any changeset by running `jj show ykwqrvso` for
  example to show the contents of the active changeset.
 - You can reset the state of the working folder to any changeset by running `jj edit  
