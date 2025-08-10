# CocoLedger Development Workflow

## Branch Strategy

- **`main`**: Production-ready code only
- **`develop`**: Active development branch
- **`feature/*`**: Feature-specific branches (optional)

## Daily Development Process

### 1. Start Development

```bash
# Switch to develop branch
git checkout develop

# Pull latest changes
git pull origin develop

# Start coding...
```

### 2. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add coconut calculation service"

# Push to develop
git push origin develop
```

### 3. Before Merging to Main

#### Prerequisites Checklist:

- [ ] All features are complete and tested
- [ ] Backend API is fully functional
- [ ] Frontend UI is working correctly
- [ ] No critical bugs exist
- [ ] Application runs without errors
- [ ] All tests pass (when implemented)

#### Testing Commands:

```bash
# Test Backend
cd backend
source venv/bin/activate
python -m pytest  # (when tests are added)
uvicorn app.main:app --reload

# Test Frontend
cd frontend
npm run build
ng serve

# Manual testing of all features
```

## Merging to Main Branch

### Option 1: Pull Request (Recommended)

1. Create Pull Request from `develop` to `main`
2. Review all changes
3. Merge after approval

### Option 2: Direct Merge (Local)

```bash
# Only when everything is tested and working
git checkout main
git pull origin main
git merge develop
git push origin main
```

## Emergency Fixes

For critical production fixes:

```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-fix

# Make fix
git add .
git commit -m "fix: critical production issue"

# Merge to both main and develop
git checkout main
git merge hotfix/critical-fix
git push origin main

git checkout develop
git merge hotfix/critical-fix
git push origin develop
```

## Git Aliases (Optional)

Add to your `~/.gitconfig`:

```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    dev = checkout develop
    main = checkout main
    pushdev = push origin develop
```

## Protected Branch Rules

The main branch is protected to prevent accidental pushes. Always develop in the `develop` branch and merge to `main` only when the application is complete and tested.
