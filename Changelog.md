# Changelog


## 1.1.0 (2025-07-08)

### Feat

- **add-commitizen-for-release-mgmt**: conventional commits , release mgmt

### Docs
- **readme-license-pyproject**: Add license, update readme, fix linters

### Fix
- **incremented-entrances-for-changelog**: now commitizen adds new, dont change earlier entrances in changelog
- **commitizen-tool-changelog-file-fix**: commitizen uses Changelog.md now for bumps

### Refactor

- **delete-.cz.toml**: go back to default commitizen in pyproject, for questions form to work

## [1.0.0]

### Added
- New tests added with `cart`, `shopping_modal` and `product_details` markers  
- Detailed `BUGS.md` document added  
- New page-objects and helpers for advanced UI tests  
- Expanded CI to cover those new markers

### Internal
- Bumped version to 1.0.0 ;)  
- Docker-compose debug services now set `shm_size` to `2g` (avoids VNC crashes)  

---

## [0.9.0]

### Fixed
- Fixed logger/print workaround for `xdist`  
- Fixed GitHub Pages publishing so all reports persist  
- `xfail` handling improved for screenshot tests

### Internal
- Minor code cleanup  
- Better CI job names  
- Sequential GH Pages upload to avoid push conflicts

---

## [0.8.1]

### Added
- Improved README introduction  
- Added TigerVNC support

---

## [0.8.0]

### Added
- Added detailed README file

---

## [0.7.1]

### Internal
- Better naming of CI runs (e.g. “CI (staging)”)  
- Updated `pyproject.toml`

---

## [0.7.0]

### Added
- Added `env_type` input to GitHub Actions workflow (select local or staging)  
- Updated `run_tests.sh` to accept `-e` flag for environment selection

### Internal
- Refactored GitHub Actions CI to support multiple environments via env-files and UI selection

---

## [0.6.0]

### Added
- Expected-conditions helpers for Selenium and API requests on dummy site

---

## [0.5.0]

### Added
- CLI script for linters and pre-commit checks  
- INI options in `pyproject.toml` and pytest markers

---

## [0.4.0]

### Added
- GitHub CI solution with `workflow_dispatch` and functioning reports on GitHub Pages

---

## [0.3.0]

### Internal
- Switched from Firefox to Opera for easier parallel test execution

---

## [0.2.0]

### Added
- Initial `CHANGELOG.md`  
- Firefox browser support  
- Automated full-screen VNC with `-v` option

---

## [0.1.0]

### Added
- Working repository stack: Python, pytest, Docker, Poetry  
- HTML report with screenshots
