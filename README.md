# Reusable Skills Repository

This repository contains reusable prompt skills packaged in a simple multi-skill layout for GitHub publishing and future reuse.

## Included Skills

### `general-bioinformatics-teaching-script`

A skill for rewriting or authoring bioinformatics analysis scripts in a beginner-friendly, teaching-oriented style. It emphasizes:

- clear sectioned structure;
- explanations of why each step exists;
- input/output clarity;
- biological meaning;
- reproducibility and handoff readiness.

Location: `general-bioinformatics-teaching-script/SKILL.md`

### `general-bioinformatics-teaching-script-enhanced`

An enhanced version of the bioinformatics teaching-script skill for users who need much more explicit guidance on code syntax, parameters, object structure, debugging steps, and how to read each line while running the script section by section.

Location: `general-bioinformatics-teaching-script-enhanced/SKILL.md`

### `general-project-handoff`

A skill for creating strong project handoff documents that help another AI assistant, future work session, or collaborator continue a complex project without losing critical context.

Location: `general-project-handoff/SKILL.md`

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── general-bioinformatics-teaching-script/
│   └── SKILL.md
├── general-bioinformatics-teaching-script-enhanced/
│   └── SKILL.md
└── general-project-handoff/
    └── SKILL.md
```

## How to Use

You can use this repository in a few simple ways:

1. Read a skill directly on GitHub and paste its instructions into your workflow.
2. Copy a skill folder and reuse its `SKILL.md` in another repository or local skill collection.
3. Use this repository as the source for future skill installation or packaging workflows.

## Publishing To GitHub

Recommended first-push flow:

```powershell
git init
git add .
git commit -m "Initial commit: add two reusable skills"
git branch -M main
git remote add origin https://github.com/<your-name>/<repo-name>.git
git push -u origin main
```

If Git identity is not configured yet:

```powershell
git config --global user.name "Your GitHub Name"
git config --global user.email "your-email@example.com"
```

## License

This repository is released under the MIT License. See `LICENSE` for details.
