@echo off
setlocal
set PYTHONPATH=%CD%\backend;%CD%
python -m pytest tests\agent -q
python tests\scripts\run_agent_tests.py
pause
