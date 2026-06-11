# Git Branching & Commit Workflow

This document outlines the professional branching strategy and commit conventions for the Sports League API project. By adhering to these standards, we ensure a clean, understandable, and collaborative commit history.

---

## 1. Branching Strategy: GitHub Flow

We use **GitHub Flow** as our branching model. Under this strategy:
- The `main` branch is always stable, production-ready, and deployable.
- All development, fixes, and updates occur on isolated branches.
- No direct commits are allowed on `main`. All changes must be merged via Pull Requests (PRs).

### When to Create a Branch
You must create a new branch off `main` for **any and all modifications** to the codebase, including:
- **Features**: Adding new functionality (e.g., API endpoints, models).
- **Bug Fixes**: Resolving issues, crashes, or logical errors.
- **Dependency Management**: Upgrading, adding, or patching packages.
- **Documentation**: Creating or updating markdown files, guides, or API specifications.
- **Refactoring**: Reorganizing or cleaning up code without changing its external behavior.
- **Testing**: Adding unit or integration tests.

---

## 2. Branch Naming Conventions

To keep the repository organized, all branch names must follow a standard structured pattern.

### Structure
`[type]/[issue-number]-[short-description]`

- **`[type]`**: The category of change. Must be lowercase.
  - `feature/` – New features or capabilities.
  - `bugfix/` or `fix/` – Resolving bugs.
  - `refactor/` – Code cleanup, restructuring, or improvements.
  - `docs/` – Documentation changes.
  - `chore/` – Build configurations, lockfile updates, or repository maintenance.
- **`[issue-number]`**: The numeric ID from the project management tracker (e.g., GitHub Issues).
- **`[short-description]`**: A brief kebab-case description of the task.

### Examples
- `feature/12-add-team-endpoints`
- `fix/42-resolve-null-jersey-error`
- `docs/3-create-git-workflow`
- `chore/55-upgrade-django`

### Rules
1. **All Lowercase**: Branch names must contain only lowercase letters (e.g., use `bugfix/`, not `bugFix/`).
2. **Kebab-Case Only**: Use single hyphens `-` to separate words.
3. **No Trailing Hyphens**: Do not end a branch name with a hyphen.
   - *Bad:* `feature/12-add-login-`
   - *Good:* `feature/12-add-login`
4. **No Consecutive Hyphens**: Avoid double hyphens.
   - *Bad:* `feature/12--add--login`
   - *Good:* `feature/12-add-login`

---

## 3. Commit Message Conventions

We follow the **Conventional Commits** specification. Every commit message must be structured clearly to explain the *what* and *why* of the change.

### Structure
`<type>: <description>`

### Allowed Types
- **`feat`**: A new feature for the application.
- **`fix`**: A bug fix.
- **`docs`**: Documentation-only changes.
- **`style`**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.).
- **`refactor`**: A code change that neither fixes a bug nor adds a feature.
- **`perf`**: A code change that improves performance.
- **`test`**: Adding missing tests or correcting existing tests.
- **`chore`**: Changes to the build process, auxiliary tools, or libraries.

### Rules for Writing Commit Messages
1. **Imperative Mood**: Write the subject line in the imperative present tense (e.g., "Add user authentication" instead of "Added user authentication" or "Adds user authentication"). Think of it as completing the sentence: *"If applied, this commit will..."*
2. **Lowercase Description**: Start the description after the colon with a lowercase letter.
3. **No Trailing Period**: Do not end the subject line with a period.
4. **Character Limit**: Keep the subject line under 50 characters.
5. **Separate Body**: If the change requires context, include a blank line after the subject line followed by a detailed explanatory body wrapped at 72 characters.

### Examples
- `feat: add league retrieval endpoint`
- `fix: prevent duplicate team names in same league`
- `docs: document branch and commit conventions`
- `chore: update requirements.txt with pinned django version`

#### Resources
- https://mumin-ahmod.medium.com/git-conventions-the-developers-guide-to-writing-better-commits-and-workflows-840b5e3b830d
- https://www.conventionalcommits.org/en/v1.0.0/

