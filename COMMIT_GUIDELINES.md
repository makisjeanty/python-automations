# Commit Message Guidelines

This project follows **Conventional Commits** for clear, organized git history.

## Format

```
<type>: <description>

[optional body]
```

## Types

- **feat**: New feature or script
  - `feat: add api consumer`
  - `feat: improve email reporter with attachments`

- **fix**: Bug fix
  - `fix: handle empty directory in file renamer`
  - `fix: api rate limiting issue`

- **docs**: Documentation changes
  - `docs: update README`
  - `docs: add usage examples`

- **refactor**: Code refactoring (no feature change)
  - `refactor: extract helper functions`
  - `refactor: improve error handling`

- **chore**: Maintenance tasks
  - `chore: update dependencies`
  - `chore: add .env.example`

- **test**: Adding or updating tests
  - `test: add unit tests for file renamer`

## Examples

```bash
# Good commits
git commit -m "feat: add cryptocurrency price tracking"
git commit -m "fix: handle special characters in filenames"
git commit -m "docs: update installation instructions"
git commit -m "refactor: simplify API consumer class"

# Bad commits (avoid these)
git commit -m "update"
git commit -m "fixed stuff"
git commit -m "changes"
```

## Best Practices

1. **Keep it concise** - One line is usually enough
2. **Use imperative mood** - "add" not "added", "fix" not "fixed"
3. **Be specific** - Describe what changed, not why
4. **One logical change per commit** - Don't mix features and fixes

## Current Project History

```
8fce7a4 docs: add comprehensive README with usage examples
94737e6 feat: add email reporter for automated reporting
dca22b0 chore: initial project setup with dependencies and gitignore
```

Clean, professional, and easy to understand! 🚀
