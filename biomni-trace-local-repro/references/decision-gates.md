# Decision Gates

Use this reference when deciding whether to ask the user before acting.

## Must Ask the User

Ask before any decision that changes:

- main analysis path;
- biological candidate definition;
- default TRUE/FALSE runtime switches;
- output filenames or schemas used by downstream scripts;
- whether an old script is deprecated, renamed, split, or removed;
- whether to overwrite, delete, move, or regenerate existing results;
- whether to actually run expensive analysis steps;
- whether to install packages or download large files;
- whether to use any non-local raw/original data source;
- whether to use Biomni outputs as intermediate inputs instead of locally generated files;
- how to resolve a conflict between an older local script and a newer corrected trace.

Ask concise questions and explain the consequence of each option.

## Do Not Ask: Discoverable Facts

Do not ask for facts that can be discovered locally:

- which scripts already exist;
- what files are in the downloaded trace;
- which output names are used by prior scripts;
- whether deprecated terms appear in executable code;
- whether a script parses.

Explore first.

## Usually Safe to Decide

Proceed without asking for small, reversible, or style-level choices:

- adding clearer comments;
- improving beginner explanations;
- adding non-destructive static checks;
- fixing typos;
- making error messages clearer;
- aligning wording with an already-approved local convention.

## How To Ask

Good:

```text
The latest trace changes the candidate definition from 116 to 120 rows, which affects F2C and F2step4 inputs. Do you want me to update downstream scripts to require 120 candidates?
```

Bad:

```text
What should I do?
```
