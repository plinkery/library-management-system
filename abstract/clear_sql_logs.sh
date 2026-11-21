#!/usr/bin/env bash
# Reset live_dbms_transactions.sql to clean state
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cat << 'EOF' > "$DIR/live_dbms_transactions.sql"
-- ===================================================================
-- LIVE DBMS TRANSACTIONS LOG
-- Generated in real-time by College E-Library System
-- You can run or inspect these statements directly in DBeaver / Workbench!
-- ===================================================================
USE elibrary_db;

-- [LOGS CLEARED & READY]
-- Ready for real-time transactions from user clicks...
EOF
echo "[OK] live_dbms_transactions.sql cleared and reset!"
