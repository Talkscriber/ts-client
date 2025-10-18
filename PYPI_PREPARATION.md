# PyPI Publication Preparation Guide

This document outlines the steps needed to publish the Talkscriber Python Client to PyPI.

## Pre-Publication Checklist

### ✅ Package Configuration
- [x] `pyproject.toml` configured with proper metadata
- [x] `setup.py` updated with correct dependencies
- [x] Version set to `1.0.0` (initial release)
- [x] All dependencies properly specified with version constraints
- [x] License file (`LICENSE.md`) present
- [x] README.md updated for PyPI with proper badges and installation instructions

### ✅ Documentation
- [x] Main README.md updated with PyPI installation instructions
- [x] Examples README files updated to use `pip install talkscriber-client`
- [x] CHANGELOG.md created with version history
- [x] All documentation links verified

### ✅ Code Quality
- [x] All imports working correctly
- [x] CLI tools properly configured
- [x] Test files created and working
- [x] Error handling implemented
- [x] Dependencies properly managed

### ✅ GitHub Integration
- [x] GitHub Actions workflow created (`.github/workflows/publish.yml`)
- [x] Repository structure organized
- [x] All files committed and pushed

## PyPI Account Setup

### 1. Create PyPI Account
1. Go to [PyPI](https://pypi.org/account/register/)
2. Create an account with your email
3. Verify your email address

### 2. Create API Token
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Give it a name (e.g., "talkscriber-client")
5. Set scope to "Entire account" (for first upload)
6. Copy the token (starts with `pypi-`)

### 3. Add Token to GitHub Secrets
1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token

## Testing Before Publication

### 1. Test Package Build
```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the package
twine check dist/*
```

### 2. Test on Test PyPI
```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ talkscriber-client
```

### 3. Test Installation
```bash
# Test in clean environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
pip install talkscriber-client
python -c "import talkscriber; print(talkscriber.__version__)"
```

## Publication Methods

### Method 1: GitHub Actions (Recommended)
1. Create a new release on GitHub
2. Tag it as `v1.0.0`
3. GitHub Actions will automatically build and publish to PyPI

### Method 2: Manual Upload
```bash
# Build the package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Post-Publication

### 1. Verify Publication
- Check [PyPI package page](https://pypi.org/project/talkscriber-client/)
- Test installation: `pip install talkscriber-client`
- Verify all functionality works

### 2. Update Documentation
- Update any hardcoded version numbers
- Update installation instructions if needed
- Test all example code

### 3. Announce Release
- Update GitHub repository description
- Create release notes
- Announce on relevant channels

## Version Management

### Semantic Versioning
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (1.1.0): New features, backward compatible
- **PATCH** (1.0.1): Bug fixes, backward compatible

### Updating Version
1. Update version in `pyproject.toml`
2. Update version in `setup.py`
3. Update `CHANGELOG.md`
4. Create new release on GitHub

## Troubleshooting

### Common Issues

1. **"Package already exists"**
   - Check if package name is already taken
   - Consider using a different name or contacting existing maintainer

2. **"Invalid distribution"**
   - Check `pyproject.toml` syntax
   - Verify all required fields are present

3. **"Authentication failed"**
   - Verify PyPI API token is correct
   - Check token permissions

4. **"Dependencies not found"**
   - Ensure all dependencies are available on PyPI
   - Check version constraints

### Getting Help
- [PyPI Help](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)

## Security Considerations

- Never commit API tokens to code
- Use GitHub Secrets for sensitive information
- Regularly rotate API tokens
- Monitor package downloads and usage
