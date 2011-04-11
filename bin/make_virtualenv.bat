@echo off

:: This script exists because my project dir is synched between my home and
:: work machines using Dropbox, and a virtualenv created on one machine doesn't
:: work on the other. (because they have have Python installed at different
:: locations (because %SystemDrive% isn't C: on one of them)) So I have to
:: create a new virtualenv whenever I switch between them. This script
:: automates that. It shouldn't affect anything that is checked into the repo.
:: -Jonathan

:: An alternative approach would presumably be to create the virtualenv and
:: then run 'virtualenv --relocatable .', but this doesn't work on Windows.

:: eradicate whatever existing virtualenv is here
virtualenv --clear .
call scripts\deactivate

:: create a new virtualenv
virtualenv --distribute --no-site-packages .
call Scripts\activate
pip install pyglet PyOpenGL

