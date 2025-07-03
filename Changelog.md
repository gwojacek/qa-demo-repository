## [1.0.0]
### Internal
- version 1.0.0 finally ;)
- detailed BUGS.md document added
- new tests added with cart, shopping_modal and product_details markers
- new page objects and helpers for advanced UI tests
- expanded CI those markers
- docker-compose debug services now set shm_size to 2g - without it the vnc crushed

## [0.9.0]
### Internal 
- fixed logger and print workaround for xdist
- minor code cleaning
- better ci names
- fixed GitHub Pages publishing so all reports persist
- sequential GH Pages upload to avoid push conflicts
- xfail handling for screenshots


## [0.8.1]
### Internal 
-  better intro to readme, tigervnc add


## [0.8.0]
### Internal 
- Added detailed readme file 

## [0.7.1]
### Internal 
- Better naming of runs in ci, reflecting the env on which test are executed like "CI (staging) " 
- updated pyproject

## [0.7.0]
### Internal 
- Refactored GitHub Actions CI to support running against multiple environments (local, staging) 
via environment files and workflow UI selection.

- Added env_type input to workflow; now CI jobs can run against either environment by selecting from the Actions UI, 
or default to local on push and scheduled runs.
- Updated run_tests.sh to accept an -e flag for environment selection, making local and CI runs consistent.

## [0.6.0]
### Internal 
- expected condtions functions for selenium, api requests for dummy site

## [0.5.0]
### Internal 
- cli script for linters, precommit check, ini options to pyproject toml, markers py

## [0.4.0]
### Internal 
- added CI solution for github with workflow_dispatch (manually triggering) and working reports on gh pages 

## [0.3.0]
### Internal 
- changed firefox for opera for easier parallel test executing to work

## [0.2.0]
### Internal 
- added changelog
- added firefox browser
- added automated full screen vnc with -v option

## [0.1.0]
### Internal 
- working repository stack python pytest docker poetry
- working html report with screenshots