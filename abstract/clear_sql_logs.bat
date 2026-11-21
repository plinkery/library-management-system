@echo off
echo ============================================================
echo   Resetting live_dbms_transactions.sql to clean state...
echo ============================================================
(
echo -- ===================================================================
echo -- LIVE DBMS TRANSACTIONS LOG
echo -- Generated in real-time by College E-Library System
echo -- You can run or inspect these statements directly in DBeaver / Workbench!
echo -- ===================================================================
echo USE elibrary_db;
echo.
echo -- [LOGS CLEARED ^& READY]
echo -- Ready for real-time transactions from user clicks...
) > "%~dp0live_dbms_transactions.sql"
echo [OK] live_dbms_transactions.sql cleared and reset!
pause
