# College E-Library DBMS Project: Complete Viva & Live Demonstration Script

**Course**: Database Management Systems (24CS520)  
**Database**: MySQL Server 8.0 (Port: `3307`, User: `sem5e2`, Database: `elibrary_db`)  
**Backend**: Java HTTP Server (`http://localhost:8080`)  
**Frontend**: Modern HTML5, CSS3, Vanilla JavaScript (ES6+)  
**Live Transaction Script**: `live_dbms_transactions.sql`  

---

## 🎯 Master Strategy: How to Ace Your Viva Without Getting Overwhelmed

During your viva, you want to show the examiner that **your website and your MySQL database are linked in real time**, and that **you understand every single SQL query executed under the hood**.

### The Two-Screen Setup
1. **Screen 1 (Browser)**: Have your website open at `http://localhost:8080`.
2. **Screen 2 (MySQL Workbench)**: Have MySQL Workbench connected to `localhost:3307` (`ubuntu DB`, schema `elibrary_db`), with `live_dbms_transactions.sql` open in a query tab.

### The "Batch & Declutter" Workflow (Prevents Confusion!)
Instead of performing 10 website actions at once and ending up with 200 lines of messy SQL in the log:
1. **Perform ONE small action** on the website (e.g., reserve a book).
2. **Switch to MySQL Workbench**: Right-click the file tab and click **"Revert to Saved"** (or open `live_dbms_transactions.sql`). You will see **ONLY the query for that specific action** plus a ready-to-run verification `SELECT` query!
3. **Execute the verification query** in Workbench to show the teacher the newly inserted/updated row in the grid.
4. **Explain the SQL line-by-line** to the teacher using the exact spoken scripts provided below.
5. **Click `[ 🗑️ Clear Logs ]`** at the top of the website! This wipes the log clean so you are ready for the next operation with zero clutter!

---

## 🔑 Login Accounts & Demonstration Personas

| Role / Persona | Name | USN (Username) | Password | Demonstration Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **👩‍💼 Chief Librarian** | Mrs. Shwetha Rao | `01JSTLIB001` | `admin123` | Approves counter checkouts, collects overdue fines, procures requested books. |
| **👨‍🎓 Student 1 (Clean)** | Rahul Sharma (CSE) | `01JST24UCS001` | `pass123` | Starts clean (0/5 books). Tests **12-Hour Reservation**, live countdown clock, and unvoting. |
| **👩‍🎓 Student 2 (Limit Demo)** | Priya Patel (ECE) | `01JST24UCS002` | `pass123` | Already has **4/5 active loans**. Demonstrates **Trigger 1: Maximum 5 Books Limit**. |
| **👨‍🎓 Student 3 (Fine Demo)** | Amit Kumar (MECH) | `01JST24UCS003` | `pass123` | Starts clean. Borrows a book live, then we **Fast-Forward +35 Days** to test overdue fine & borrowing lock! |

---

## 🧠 Core DBMS Theory: What Your Teacher Will Ask & What to Say

### 1. "Is this database normalized to Third Normal Form (3NF)?"
> **Your Confident Answer:**  
> *"Yes, Sir/Ma'am. Our database strictly adheres to Third Normal Form (3NF):*
> - ***1NF (Atomic Attributes):*** *Every attribute contains only single, atomic values. No multivalued attributes (e.g., authors are normalized into a separate `authors` table with foreign keys, and physical copies are tracked individually in `book_copies` rather than comma-separated lists).*
> - ***2NF (No Partial Dependencies):*** *Every non-prime attribute is fully functionally dependent on the entire primary key. For example, in our composite table `request_votes(request_id, user_id)`, the attribute `voted_at` depends on the combined key `(request_id, user_id)`, not just one part of it.*
> - ***3NF (No Transitive Dependencies):*** *No non-prime attribute depends on another non-prime attribute ($X \to Y \to Z$). For example, books do not directly store department names or HOD names; `books` references `branch_id`, and `branches` stores `branch_name` and `hod_name`. If a department changes its HOD, we update only ONE row in `branches`, eliminating update anomalies."*

### 2. "Why do you have separate `books` and `book_copies` tables?"
> **Your Confident Answer:**  
> *"This separates the **Abstract Catalog Metadata** (title, ISBN, author, publication year) from the **Physical Inventory Assets** (individual accession numbers/barcodes, rack location, physical copy status). If the library owns 5 physical copies of 'Fundamentals of Database Systems', we store the title and ISBN only once in `books`, and have 5 distinct rows in `book_copies` referencing `book_id`. This prevents severe data redundancy and avoids update anomalies."*

### 3. "How do you enforce ACID properties during circulation?"
> **Your Confident Answer:**  
> *"Through relational database constraints, atomic SQL state transitions, and InnoDB engine transaction isolation:*
> - ***Atomicity:*** *When a student reserves a book, marking the copy as 'RESERVED' and inserting the reservation record are executed as an atomic unit.*
> - ***Consistency:*** *Enforced via foreign key constraints (`ON DELETE CASCADE`) and stored triggers (`PreventBorrowOverLimit`, `PreventBorrowIfOverdue`).*
> - ***Isolation:*** *InnoDB ensures REPEATABLE READ isolation so two students clicking 'Reserve' at the exact same millisecond cannot both get the same physical copy.*
> - ***Durability:*** *All completed transactions are committed to disk in MySQL's redo log and tablespace."*

---

## 🎬 Chronological Viva Demonstration Workflow

---

### Phase 0: Pre-Viva Database Initialization in MySQL Workbench

Before your teacher sits down:
1. Open MySQL Workbench, connect to `ubuntu DB` (`localhost:3307`).
2. Open `/home/pink/e-libraryDB/schema.sql` and execute (⚡ yellow lightning bolt).
3. Confirm in Workbench:
   ```sql
   USE elibrary_db;
   SHOW TABLES;
   ```
4. Click **`[ 🗑️ Clear Logs ]`** on the website (`http://localhost:8080`) so the SQL log starts completely clean.

**🗣️ Your 30-Second Opening Elevator Pitch to the Teacher:**
> *"Good morning Sir/Ma'am. For our DBMS mini-project, we designed a College E-Library Management System. It is built on a 14-table 3NF normalized schema on MySQL 8.0, with a Java backend and responsive web frontend.*  
> *Rather than just presenting a static website, we implemented a real-time live transaction mirroring engine: every action performed on our portal generates exact SQL DML statements into a live transaction log, allowing us to inspect and verify state transitions directly in MySQL Workbench."*

---

### Batch 1: The 12-Hour Online Book Reservation

#### 🖥️ Action on Website:
1. Open `http://localhost:8080`.
2. Click **👨‍🎓 Student 1 (Rahul - CSE)** (`USN: 01JST24UCS001`).
3. Under **Library Books Catalog**, find **Fundamentals of Database Systems** (Copy: `CSE-DBMS-01`).
4. Click **`[ Reserve (12h) ]`**.
5. **Show the teacher on screen**: The book moves to **"My Active Book Reservations"** with a live ticking countdown timer (`⏳ 11h 59m 58s left`).

#### 🗄️ Action in MySQL Workbench:
Switch to Workbench and open `live_dbms_transactions.sql`. Show the teacher the exact SQL generated:
```sql
UPDATE book_copies SET status = 'RESERVED' WHERE copy_id = 201;
INSERT INTO reservations (reservation_id, user_id, copy_id, reserved_at, expires_at, status)
VALUES (101, 2, 201, NOW(), DATE_ADD(NOW(), INTERVAL 12 HOUR), 'PENDING');

-- [WORKBENCH VERIFICATION]: Run to inspect updated tables
SELECT r.reservation_id, u.usn, u.name, b.title, bc.copy_code, bc.status AS copy_status, r.expires_at
FROM reservations r
JOIN users u ON r.user_id = u.user_id
JOIN book_copies bc ON r.copy_id = bc.copy_id
JOIN books b ON bc.book_id = b.book_id
WHERE r.reservation_id = 101;
```
Now, **execute the verification query in Workbench** and show the teacher the row in the results grid!

#### 🔍 Line-by-Line SQL Explanation (To Make You Sound Like a DBMS Pro):
- `UPDATE book_copies SET status = 'RESERVED' WHERE copy_id = 201;`
  - **What it does**: This updates the physical asset table. We change the `status` column from `'AVAILABLE'` to `'RESERVED'` for this specific copy (`copy_id = 201`).
  - **Why it matters**: This prevents race conditions. Even if another student is on the catalog page, this copy cannot be selected by anyone else.
- `INSERT INTO reservations (...) VALUES (101, 2, 201, NOW(), DATE_ADD(NOW(), INTERVAL 12 HOUR), 'PENDING');`
  - **What it does**: Creates a transaction record tracking that Student 2 reserved Copy 201.
  - **`NOW()`**: A built-in MySQL date-time function that returns the current timestamp.
  - **`DATE_ADD(NOW(), INTERVAL 12 HOUR)`**: Uses MySQL date arithmetic to set the expiration timestamp exactly 12 hours from the reservation moment.
  - **`'PENDING'`**: An ENUM value indicating the student has placed the hold but has not yet picked up the physical book at the library counter.
- **The Verification Query with Multi-Table Joins**:
  - `FROM reservations r`
  - `JOIN users u ON r.user_id = u.user_id`: An **INNER JOIN** matching the foreign key `r.user_id` with the primary key `u.user_id` to retrieve the student's USN and full name.
  - `JOIN book_copies bc ON r.copy_id = bc.copy_id`: Joins the physical copy to verify its barcode `copy_code` and current status.
  - `JOIN books b ON bc.book_id = b.book_id`: Joins the catalog table to fetch the human-readable book title.
  - `WHERE r.reservation_id = 101`: Filters the join result to isolate the single reservation we just created.

#### 🗣️ Spoken Script for the Teacher:
> *"Sir/Ma'am, here we demonstrate a state-transition reservation. Notice that our database uses date arithmetic: `DATE_ADD(NOW(), INTERVAL 12 HOUR)` computes the exact deadline. In our verification query, we perform a 4-table relational INNER JOIN connecting `reservations`, `users`, `book_copies`, and `books` using their foreign keys. The Workbench grid shows `copy_status` is now 'RESERVED' and `expires_at` is exactly 12 hours ahead."*

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** at the top of the website so the log is ready for Batch 2.

---

### Batch 2: Physical Counter Issuance & Live 30-Day Due Date Countdown

#### 🖥️ Action on Website:
1. On the website, click **Logout** and log in as **👩‍💼 Chief Librarian** (`USN: 01JSTLIB001`, Password: `admin123`).
2. Under **"Pending 12-Hour Reservations"**, show the teacher that Rahul's reservation for *Fundamentals of Database Systems* is waiting at the counter.
3. Click **`[ ✅ Issue to Student ]`**.
4. Log back in as **Student 1 (Rahul)**:
   - The book has moved to **"My Borrowed Books"**.
   - Show the live ticking countdown badge: **`⏱️ 29d 23h 59m 55s`** counting down seconds in real time!

#### 🗄️ Action in MySQL Workbench:
Switch to Workbench and reload `live_dbms_transactions.sql`. Show the generated queries:
```sql
UPDATE book_copies SET status = 'BORROWED' WHERE copy_id = 201;
UPDATE reservations SET status = 'FULFILLED' WHERE reservation_id = 101;
INSERT INTO loans (loan_id, user_id, copy_id, borrow_date, due_date, status)
VALUES (101, 2, 201, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 'ACTIVE');

-- [WORKBENCH VERIFICATION]: Run to inspect newly active loan and updated copy status
SELECT l.loan_id, u.usn, u.name, b.title, bc.copy_code, bc.status AS copy_status, l.borrow_date, l.due_date
FROM loans l
JOIN users u ON l.user_id = u.user_id
JOIN book_copies bc ON l.copy_id = bc.copy_id
JOIN books b ON bc.book_id = b.book_id
WHERE l.loan_id = 101;
```
Execute the verification query in Workbench and show the updated grid!

#### 🔍 Line-by-Line SQL Explanation:
- `UPDATE book_copies SET status = 'BORROWED' WHERE copy_id = 201;`
  - Updates copy state from `'RESERVED'` to `'BORROWED'`.
- `UPDATE reservations SET status = 'FULFILLED' WHERE reservation_id = 101;`
  - Marks the reservation as fulfilled so it no longer counts as a pending hold.
- `INSERT INTO loans (...) VALUES (101, 2, 201, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 'ACTIVE');`
  - **What it does**: Inserts an official circulation loan record.
  - **`DATE_ADD(NOW(), INTERVAL 30 DAY)`**: Automatically computes the return due date by adding exactly 30 days to the checkout timestamp.
  - **`'ACTIVE'`**: The loan is currently active. When returned, this status changes to `'RETURNED'`.
- **The Verification Query**:
  - Joins `loans` $\to$ `users` on `user_id`, `loans` $\to$ `book_copies` on `copy_id`, and `book_copies` $\to$ `books` on `book_id`.
  - Verifies that `l.due_date` is exactly 30 days ahead and `bc.status` is `'BORROWED'`.

#### 🗣️ Spoken Script for the Teacher:
> *"When the student physically collects the book at the circulation desk, the librarian confirms issuance. The database updates `reservations.status = 'FULFILLED'`, marks `book_copies.status = 'BORROWED'`, and inserts a new row in `loans` setting `due_date = DATE_ADD(NOW(), INTERVAL 30 DAY)`. The live countdown on the website continuously calculates the millisecond difference between the browser clock and this `due_date` stored in MySQL."*

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** on the website.

---

### Batch 3: Fast-Forward +35 Days & Demonstrating Overdue Fine (₹1/Day) Live

#### 🖥️ Action on Website:
1. Log in as **👨‍🎓 Student 3 (Amit Kumar - MECH)** (`USN: 01JST24UCS003`, Password: `pass123`).
   - Point out to the teacher: Amit has **0 borrowed books** and **₹0.00 unpaid fines**.
2. Click **`[ Reserve (12h) ]`** on *Operating System Concepts*.
3. Switch to **Librarian** (`01JSTLIB001`) and click **`[ Issue to Student ]`** for Amit's reservation.
4. Now, open the **`[ 🎓 Teacher Demo Tools ]`** button in the top navigation.
5. Click **`[ ⏩ Fast-Forward +35 Days ]`**:
   - The countdown badge instantly transforms into a bold red warning: **`⚠️ OVERDUE by 5d | Fine: ₹5.00`**!
   - In the stats header, **Unpaid Fines** updates to **`₹5.00`**.
   - A red banner appears: *"🚨 Overdue Alert & Borrowing Lock: You have unpaid fines totaling ₹5.00! Return your overdue books to unblock borrowing."*
6. Click **`[ Reserve (12h) ]`** on another book to prove the lock:
   - Alert: *"Reservation Blocked: You have overdue books or unpaid fines! Pay fines to unblock."*

#### 🗄️ Action in MySQL Workbench:
Switch to Workbench and inspect `live_dbms_transactions.sql`:
```sql
-- [DEMO TIME-MACHINE SIMULATION: +35 DAYS]
UPDATE loans SET borrow_date = DATE_SUB(borrow_date, INTERVAL 35 DAY), due_date = DATE_SUB(due_date, INTERVAL 35 DAY) WHERE status = 'ACTIVE';
INSERT INTO fines (loan_id, user_id, days_overdue, amount, status)
SELECT loan_id, user_id, DATEDIFF(NOW(), due_date), DATEDIFF(NOW(), due_date) * 1.00, 'UNPAID'
FROM loans WHERE status = 'ACTIVE' AND NOW() > due_date
ON DUPLICATE KEY UPDATE days_overdue = VALUES(days_overdue), amount = VALUES(amount), status = 'UNPAID';

-- [WORKBENCH VERIFICATION]: Inspect OverdueLoansView and fines table
SELECT * FROM OverdueLoansView;
SELECT f.fine_id, u.usn, u.name AS student_name, b.title, f.days_overdue, f.amount, f.status
FROM fines f
JOIN users u ON f.user_id = u.user_id
JOIN loans l ON f.loan_id = l.loan_id
JOIN book_copies bc ON l.copy_id = bc.copy_id
JOIN books b ON bc.book_id = b.book_id
WHERE f.status = 'UNPAID';
```
Execute `SELECT * FROM OverdueLoansView;` in Workbench and show the teacher the row!

#### 🔍 Line-by-Line SQL Explanation:
- `UPDATE loans SET borrow_date = DATE_SUB(borrow_date, INTERVAL 35 DAY)... WHERE status = 'ACTIVE';`
  - Uses `DATE_SUB` to age the timestamps by 35 days, realistically simulating a 30-day loan that is 5 days overdue without waiting 35 real days!
- `INSERT INTO fines (...) SELECT loan_id, user_id, DATEDIFF(NOW(), due_date), DATEDIFF(NOW(), due_date) * 1.00, 'UNPAID' FROM loans WHERE status = 'ACTIVE' AND NOW() > due_date`
  - **`INSERT INTO ... SELECT` (Subquery Insertion)**: Evaluates all active loans in the database where `NOW() > due_date`.
  - **`DATEDIFF(NOW(), due_date)`**: Calculates the exact integer count of elapsed days past the due date. Because 35 days elapsed on a 30-day loan, $35 - 30 = 5$ days.
  - **`DATEDIFF(...) * 1.00`**: Calculates the monetary fine at the institutional rate of ₹1.00 per day ($5 \times ₹1.00 = ₹5.00$).
- `ON DUPLICATE KEY UPDATE days_overdue = VALUES(days_overdue), amount = VALUES(amount), status = 'UNPAID';`
  - **UPSERT Pattern**: If a fine record already exists for this loan, it updates the overdue days and fine amount rather than crashing with a primary key duplicate error.
- `SELECT * FROM OverdueLoansView;`
  - Queries our database view which automatically encapsulates the `DATEDIFF` logic and multi-table joins.

#### 🗣️ Spoken Script for the Teacher:
> *"Sir/Ma'am, to test overdue penalties during our viva, we created a demo simulation tool that shifts timestamps by 35 days using `DATE_SUB`. Because the loan period is 30 days, MySQL calculates `DATEDIFF(NOW(), due_date) = 5 days`. At ₹1 per day, the fine is exactly ₹5.00. Notice our database view `OverdueLoansView` instantly isolates Amit's overdue loan, and the application locks Amit from reserving any more books until the fine is resolved."*

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** on the website.

---

### Batch 4: Overdue Return & Fine Settlement (Counter-Only: 2 Librarian Options)

> **Important College Rule**: A student **cannot** pay fines online and keep the physical book. There is **no student online payment interface**. All money collection and physical book check-ins are handled exclusively by the **Librarian at the desk**. When a student brings an overdue book to the counter, the librarian manages one of two options:
> - **Option 1**: Student pays the fine in cash/fee and returns the book (Single-step atomic settlement).
> - **Option 2**: Student returns the physical book now (so it becomes available for others) and pays the fine later. The fine is recorded as `UNPAID`, and student borrowing remains locked until settled.

---

#### 🌟 Option 1: Pay Fine & Return Book Together (Atomic Counter Settlement)

#### 🖥️ Action on Website:
1. Log in as **👩‍💼 Chief Librarian** (`01JSTLIB001`, Password: `admin123`).
2. Under **"All overdue loans and unpaid fines across campus"**, locate Amit Kumar's overdue loan:
   - Copy Code: `CSE-OS-01`, Overdue: `5 days overdue`, Amount: `₹5.00`.
   - Point out the green button: **`[ 💳 Pay & Return Book (₹5.00) ]`**.
3. Click **`[ 💳 Pay & Return Book (₹5.00) ]`** and confirm:
   - Alert: *"✅ Book returned & fine of ₹5.00 collected! Student borrowing lock removed."*
   - Total Fine Revenue increments to **`₹5.00`**.
   - Book copy `CSE-OS-01` returns to **`AVAILABLE`** status in the catalog.
4. Log in as **👨‍🎓 Student 3 (Amit Kumar)**:
   - Unpaid Fines shows **`₹0.00`**, active loans is **0 / 5**, and the overdue banner is gone. Amit can borrow freely again!

#### 🗄️ Action in MySQL Workbench:
Copy and paste from `live_dbms_transactions.sql`:
```sql
UPDATE loans SET return_date = NOW(), status = 'RETURNED' WHERE loan_id = 101;
UPDATE book_copies SET status = 'AVAILABLE' WHERE copy_id = 301;
INSERT INTO fines (fine_id, loan_id, user_id, days_overdue, amount, status, assessed_at, paid_at)
VALUES (101, 101, 4, 5, 5.00, 'PAID', NOW(), NOW())
ON DUPLICATE KEY UPDATE status = 'PAID', paid_at = NOW();
INSERT INTO fine_collections (fine_id, user_id, amount_paid, collected_by, collection_date)
VALUES (101, 4, 5.00, 1, NOW());

-- [WORKBENCH VERIFICATION]: Verify return state and fine settlement
SELECT l.loan_id, u.usn, u.name, bc.copy_code, bc.status AS copy_status, l.return_date, l.status AS loan_status
FROM loans l JOIN users u ON l.user_id = u.user_id JOIN book_copies bc ON l.copy_id = bc.copy_id WHERE l.loan_id = 101;
SELECT * FROM fines WHERE user_id = 4;
SELECT * FROM fine_collections WHERE user_id = 4 ORDER BY collection_id DESC LIMIT 1;
SELECT * FROM BranchFineSummaryView;
```

#### 🔍 Line-by-Line SQL Explanation:
- `UPDATE loans SET return_date = NOW(), status = 'RETURNED' WHERE loan_id = 101;`
  - Records the exact physical return timestamp and terminates the loan.
- `UPDATE book_copies SET status = 'AVAILABLE' WHERE copy_id = 301;`
  - Restores shelf availability so other students can immediately reserve or borrow the copy.
- `ON DUPLICATE KEY UPDATE status = 'PAID', paid_at = NOW();`
  - Records the fine and flags it as `'PAID'` with payment timestamp.
- `INSERT INTO fine_collections (...) VALUES (...);`
  - Audits institutional cash flow with the student ID and the collecting librarian's ID (`collected_by = 1`).
- `SELECT * FROM BranchFineSummaryView;`
  - Aggregates collected departmental revenue, incrementing Mechanical Engineering's revenue by ₹5.00.

#### 🗣️ Spoken Script for the Teacher:
> *"Sir/Ma'am, in Option 1, the student settles the overdue fine in cash while handing over the book. The librarian triggers an atomic transaction: updating `loans.status = 'RETURNED'`, restoring `book_copies.status = 'AVAILABLE'`, writing a `'PAID'` fine record, and creating an audit record in `fine_collections` with the librarian's ID. In `BranchFineSummaryView`, department revenue increases by ₹5.00, and Amit's borrowing lock is immediately lifted."*

---

#### 🌟 Option 2: Return Book Now & Pay Fine Later (2-Stage Settlement)

#### 🖥️ Action on Website:
1. When Amit brings the book to the counter without cash, the librarian clicks:
   - **`[ ↩️ Return Book (Pay Later) ]`**.
2. Alert announces:
   - *"⚠️ Book returned to shelf! Overdue fine of ₹5.00 marked as UNPAID (Pay Later). Student borrowing remains locked until settled."*
3. Show the teacher the immediate state changes:
   - The book copy `CSE-OS-01` is already back on the shelf (**`AVAILABLE`** for other students).
   - In the librarian's overdue table, the row transitions to: **`[ BOOK RETURNED (FINE UNPAID) ]`** with action: **`[ 💳 Collect Fine & Clear Lock (₹5.00) ]`**.
   - If Amit logs in, his dashboard shows: **Unpaid Fines: `₹5.00`** and banner: *"⚠️ Unpaid Fine Lock: You have an outstanding fine of ₹5.00 from a previously returned book. Please pay the librarian at the counter to unblock borrowing privileges."* (He is locked from borrowing any new book!).
4. Later, when Amit returns with money, the librarian clicks:
   - **`[ 💳 Collect Fine & Clear Lock (₹5.00) ]`** $\rightarrow$ Fine is collected, and Amit's borrowing privileges are restored!

#### 🗄️ Action in MySQL Workbench:
Copy and paste from `live_dbms_transactions.sql`:
```sql
-- Stage 1: Book Returned, Fine Assessed as UNPAID:
UPDATE loans SET return_date = NOW(), status = 'RETURNED' WHERE loan_id = 101;
UPDATE book_copies SET status = 'AVAILABLE' WHERE copy_id = 301;
INSERT INTO fines (fine_id, loan_id, user_id, days_overdue, amount, status, assessed_at)
VALUES (101, 101, 4, 5, 5.00, 'UNPAID', NOW())
ON DUPLICATE KEY UPDATE status = 'UNPAID';

-- Stage 2: Later Fine Payment at Desk:
UPDATE fines SET status = 'PAID', paid_at = NOW() WHERE fine_id = 101;
INSERT INTO fine_collections (fine_id, user_id, amount_paid, collected_by, collection_date)
VALUES (101, 4, 5.00, 1, NOW());
```

#### 🗣️ Spoken Script for the Teacher:
> *"Option 2 demonstrates practical campus library flexibility while preserving database integrity. If a student forgets their wallet, the library can still recover the physical book so other students aren't starved of copies. The book copy immediately becomes `'AVAILABLE'`, but the fine is registered as `'UNPAID'`. The database trigger checks `fines WHERE status='UNPAID'`, keeping Amit blocked from borrowing new books. Once Amit pays the librarian later, `fines` updates to `'PAID'`, an entry is appended to `fine_collections`, and borrowing is unlocked."*

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** on the website.

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** on the website.

---

### Batch 5: Database Triggers in Action (Max 5 Loans & Defaulter Block)

#### 🖥️ Action on Website:
1. Log in as **👩‍🎓 Student 2 (Priya Patel - ECE)** (`USN: 01JST24UCS002`).
   - Point out to the teacher: Priya already has **4 / 5 books borrowed**.
2. Switch to **Librarian** (`01JSTLIB001`).
3. Under **"Issue Book at Counter"**:
   - Select **Priya Patel (01JST24UCS002) [4/5 books]**.
   - Select available copy **Theory of Machines (MECH-TOM-01)**.
   - Click **`[ Issue Book ]`** $\rightarrow$ Success! Priya now has **5 / 5 books**.
4. Now, attempt to issue a **6th book** to Priya:
   - Select Priya (now showing **5/5 books**).
   - Select another available copy.
   - Click **`[ Issue Book ]`**.
5. **Immediate Rejection Popup**:
   > *"TRIGGER ERROR [SQLSTATE 45000]: Borrowing limit exceeded: Maximum 5 books allowed per student (USN: 01JST24UCS002)."*

#### 🗄️ Action in MySQL Workbench:
Show the teacher the trigger code from `schema.sql`:
```sql
DELIMITER //
CREATE TRIGGER PreventBorrowOverLimit
BEFORE INSERT ON loans
FOR EACH ROW
BEGIN
    DECLARE active_count INT;
    SELECT COUNT(*) INTO active_count 
    FROM loans 
    WHERE user_id = NEW.user_id AND status = 'ACTIVE';
    
    IF active_count >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Borrowing limit exceeded: Maximum 5 books allowed per student';
    END IF;
END;
//
DELIMITER ;
```

#### 🔍 Line-by-Line Trigger Explanation:
- `DELIMITER //`: Changes MySQL's statement delimiter from semicolon to `//` so the semicolons inside the trigger block don't terminate the trigger definition prematurely.
- `BEFORE INSERT ON loans`: Specifies that the trigger executes **before** the row is actually inserted into `loans`. If an error is raised, the insertion is completely aborted.
- `FOR EACH ROW`: Row-level trigger that runs for every incoming record.
- `DECLARE active_count INT;`: Declares a local integer variable to hold the count.
- `SELECT COUNT(*) INTO active_count FROM loans WHERE user_id = NEW.user_id AND status = 'ACTIVE';`
  - **`NEW.user_id`**: The `NEW` pseudo-record refers to the student ID in the row being inserted.
  - Queries `loans` to count how many books this student currently has checked out.
- `IF active_count >= 5 THEN`: Checks if the student has reached the institutional limit of 5.
- `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...';`:
  - **`SQLSTATE '45000'`**: The standard ANSI SQL state code for a generic user-defined exception. It forces MySQL to abort the transaction and pass the error message up to the Java backend.

#### 🗣️ Spoken Script for the Teacher:
> *"Sir/Ma'am, this is our `BEFORE INSERT` trigger `PreventBorrowOverLimit`. Notice that the borrowing quota of 5 books is NOT just enforced on the frontend or in Java—it is enforced directly inside the MySQL database engine. If a student tries to borrow a 6th book, the trigger queries active loans using `NEW.user_id` and raises `SQLSTATE 45000`, stopping the transaction dead in its tracks. This is identical in concept to the `PreventParticipation` trigger in our Insurance Lab."*

---

### Batch 6: Missing 12-Hour Pickup & 1-Day Suspension Rule

#### 🖥️ Action on Website:
1. Log in as **Student 1 (Rahul)** (`01JST24UCS001`).
2. Click **`[ Reserve (12h) ]`** on any available textbook (e.g., *Introduction to Algorithms*).
3. Now open the **`[ 🎓 Teacher Demo Tools ]`** button in the top navigation.
4. Click **`[ ⏩ Fast-Forward +13 Hours ]`**:
   - The reservation automatically expires.
   - The book copy returns to `'AVAILABLE'`.
   - Rahul's dashboard displays a warning banner:
     *"⚠️ Reservation Suspended (1-Day Penalty): You failed to physically pick up a reserved book within 12 hours. You cannot reserve books until: [Tomorrow's Date]."*
   - The "Reserve" buttons across the catalog are disabled!

#### 🗄️ Action in MySQL Workbench:
Switch to Workbench and inspect `live_dbms_transactions.sql`:
```sql
UPDATE reservations SET status = 'EXPIRED' WHERE reservation_id = 102;
UPDATE book_copies SET status = 'AVAILABLE' WHERE copy_id = 401;
UPDATE users SET reservation_blocked_until = DATE_ADD(NOW(), INTERVAL 1 DAY) WHERE user_id = 2;

-- [RUN TO SHOW TEACHER VISUAL RESULT IN WORKBENCH]:
SELECT r.reservation_id, r.status AS reservation_status, bc.copy_code, bc.status AS copy_status, u.usn, u.name, u.reservation_blocked_until
FROM reservations r
JOIN book_copies bc ON r.copy_id = bc.copy_id
JOIN users u ON r.user_id = u.user_id
WHERE r.reservation_id = 102;
```
Execute the verification query in Workbench and show `reservation_blocked_until` populated!

#### 🔍 Line-by-Line SQL Explanation:
- `UPDATE reservations SET status = 'EXPIRED'`: Marks the reservation as forfeited.
- `UPDATE book_copies SET status = 'AVAILABLE'`: Releases the physical copy back to the public catalog so other students are not blocked.
- `UPDATE users SET reservation_blocked_until = DATE_ADD(NOW(), INTERVAL 1 DAY)`:
  - Adds a 24-hour penalty timestamp to the student's profile.
  - The application checks `WHERE NOW() < reservation_blocked_until` to reject future reservation requests until the penalty expires.

#### 🗣️ Spoken Script for the Teacher:
> *"To prevent students from placing frivolous reservations that block physical books from peers, we implemented an automated 12-hour expiration rule. If the student does not collect the book within 12 hours, the database resets the copy to 'AVAILABLE' and sets `reservation_blocked_until = DATE_ADD(NOW(), INTERVAL 1 DAY)`. This demonstrates fair resource management through temporal database constraints."*

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** on the website.

---

### Batch 7: Student Book Suggestion, Upvoting & Democratic Unvoting

#### 🖥️ Action on Website:
1. Log in as **Student 1 (Rahul)** (`01JST24UCS001`).
2. Scroll down to **"Request a Missing Book"**.
3. Enter:
   - Title: `Computer Architecture: A Quantitative Approach`
   - Author: `John L. Hennessy & David A. Patterson`
   - Branch: `CSE`
   - Genre: `Core Syllabus Textbook`
   - Click **`[ Submit Acquisition Request ]`**.
4. Notice the request appears with **`👍 1 Vote`**.
5. Switch to **Student 2 (Priya)** (`01JST24UCS002`):
   - Find Hennessy & Patterson's book in the community request list.
   - Click **`[ 👍 +1 Vote ]`** $\rightarrow$ Votes count becomes **`👍 2`**!
   - Click **`[ 👎 Remove Vote ]`** $\rightarrow$ Votes count decreases back to **`👍 1`**!

#### 🗄️ Action in MySQL Workbench:
Switch to Workbench and inspect `live_dbms_transactions.sql`:
```sql
-- Initial Request Submission:
INSERT INTO book_requests (request_id, title, author, branch_id, genre_id, suggested_by, votes_count, status)
VALUES (101, 'Computer Architecture: A Quantitative Approach', 'John L. Hennessy & David A. Patterson', 
        (SELECT branch_id FROM branches WHERE branch_code='CSE'), 
        (SELECT genre_id FROM genres WHERE genre_name='Core Syllabus Textbook'), 2, 1, 'PENDING');
INSERT INTO request_votes (request_id, user_id) VALUES (101, 2);

-- Upvote by Student 3 (Priya):
UPDATE book_requests SET votes_count = votes_count + 1 WHERE request_id = 101;
INSERT INTO request_votes (request_id, user_id) VALUES (101, 3);

-- Unvote by Student 3 (Priya):
UPDATE book_requests SET votes_count = votes_count - 1 WHERE request_id = 101;
DELETE FROM request_votes WHERE request_id = 101 AND user_id = 3;

-- [RUN TO SHOW TEACHER VISUAL RESULT IN WORKBENCH]:
SELECT r.request_id, r.title, r.votes_count, COUNT(rv.user_id) AS total_vote_records
FROM book_requests r
LEFT JOIN request_votes rv ON r.request_id = rv.request_id
WHERE r.request_id = 101
GROUP BY r.request_id, r.title, r.votes_count;
```
Execute the verification query in Workbench and show `votes_count` matches the count of rows in `request_votes`!

#### 🔍 Line-by-Line SQL Explanation:
- `(SELECT branch_id FROM branches WHERE branch_code='CSE')`:
  - **Scalar Subquery**: Instead of hardcoding foreign key numbers, the query looks up the primary key `branch_id` dynamically based on the department code.
- `INSERT INTO request_votes (request_id, user_id) VALUES (101, 3);`:
  - `request_votes` is an **M:N Associative Junction Table**.
  - Its primary key is composite: `PRIMARY KEY (request_id, user_id)`.
  - **Why this is critical**: If Priya clicks "+1 Vote" a second time, MySQL throws a `Duplicate entry for key 'PRIMARY'` error, mathematically guaranteeing that a student can vote at most once per request!
- `DELETE FROM request_votes WHERE request_id = 101 AND user_id = 3;`:
  - Removes the specific voting record when the student withdraws their vote.

#### 🗣️ Spoken Script for the Teacher:
> *"This module implements democratic acquisition using an M:N relationship table `request_votes`. By defining a composite primary key on `(request_id, user_id)`, the relational schema guarantees at the database level that no student can cast duplicate votes. When Priya unvotes, the row is deleted and `votes_count` is decremented."*

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** on the website.

---

### Batch 8: Chief Librarian One-Click Procurement into Live Catalog

#### 🖥️ Action on Website:
1. Log in as **👩‍💼 Chief Librarian** (`01JSTLIB001`, Password: `admin123`).
2. Scroll to **"Student Book Purchase Requests"**.
3. Find the pending request for **Designing Data-Intensive Applications** (by Martin Kleppmann, with student votes).
4. Click **`[ ✅ Approve & Procure ]`**:
   - Alert: *"🎉 Book procured and added to catalog with 2 copies!"*
5. Switch to **Student 1 (Rahul)** and look at the catalog:
   - *Designing Data-Intensive Applications* is now **live in the catalog** with **`2 of 2 Available Copies`**, complete with stack location!

#### 🗄️ Action in MySQL Workbench:
Switch to Workbench and inspect `live_dbms_transactions.sql`:
```sql
UPDATE book_requests SET status = 'PROCURED' WHERE request_id = 1;
INSERT INTO books (book_id, title, isbn, branch_id, genre_id, publisher_id, author_id, edition, pub_year, rating, description)
VALUES (101, 'Designing Data-Intensive Applications', '978-5210217324', 
        (SELECT branch_id FROM branches WHERE branch_code='CSE'), 1, 1, 1, '1st Edition', 2024, 4.8, 'Procured via student votes');
INSERT INTO book_copies (copy_id, book_id, copy_code, status, rack_location) VALUES
(2001, 101, 'CSE-NEW-1', 'AVAILABLE', 'Stack CSE-01'),
(2002, 101, 'CSE-NEW-2', 'AVAILABLE', 'Stack CSE-01');

-- [WORKBENCH VERIFICATION]: Verify newly procured title and available physical copies
SELECT b.book_id, b.title, br.branch_code, b.rating, COUNT(bc.copy_id) AS available_copies
FROM books b 
JOIN branches br ON b.branch_id = br.branch_id
JOIN book_copies bc ON b.book_id = bc.book_id
WHERE b.book_id = 101 
GROUP BY b.book_id, b.title, br.branch_code, b.rating;
```
Execute the verification query in Workbench and show `available_copies = 2`!

#### 🔍 Line-by-Line SQL Explanation:
- `UPDATE book_requests SET status = 'PROCURED' WHERE request_id = 1;`:
  - Closes the student suggestion request.
- `INSERT INTO books (...) VALUES (...);`:
  - Creates the master catalog entry with ISBN, branch, and author foreign keys.
- `INSERT INTO book_copies (...) VALUES (2001, 101, ...), (2002, 101, ...);`:
  - **Multi-Row Insert**: Inserts multiple physical copies in a single SQL statement, establishing their initial `'AVAILABLE'` status and shelf stack.
- The verification query uses `COUNT(bc.copy_id)` with `GROUP BY` to confirm that exactly 2 physical assets are linked to this new catalog title.

#### 🗣️ Spoken Script for the Teacher:
> *"Here we demonstrate procurement fulfillment. When the librarian approves the suggestion, the database executes a multi-table insertion: updating `book_requests.status = 'PROCURED'`, inserting a new row in `books`, and performing a multi-row insert into `book_copies` creating 2 physical copies with barcodes and rack shelf codes. The book is immediately visible in the student catalog."*

#### 🧹 Declutter Step:
Click **`[ 🗑️ Clear Logs ]`** on the website.

---

### Batch 9: Institutional Analytical Views & Advanced Syllabus Queries

Run these queries directly in MySQL Workbench to show your mastery of advanced SQL concepts (Joins, Aggregates, HAVING, CASE WHEN, and Relational Division).

#### 1. High Demand Books View (`HighDemandBooksView`)
```sql
SELECT * FROM HighDemandBooksView;
```
Show the definition from `schema.sql`:
```sql
CREATE OR REPLACE VIEW HighDemandBooksView AS
SELECT 
    b.book_id,
    b.title,
    b.isbn,
    br.branch_code,
    b.rating,
    COUNT(l.loan_id) AS total_borrows
FROM books b
JOIN book_copies bc ON b.book_id = bc.book_id
JOIN loans l ON bc.copy_id = l.copy_id
LEFT JOIN branches br ON b.branch_id = br.branch_id
GROUP BY b.book_id, b.title, b.isbn, br.branch_code, b.rating
HAVING COUNT(l.loan_id) >= 2;
```
- **Line-by-Line Explanation**:
  - `JOIN book_copies bc ON b.book_id = bc.book_id`: Connects books to their physical copies.
  - `JOIN loans l ON bc.copy_id = l.copy_id`: Connects copies to loan history.
  - `GROUP BY b.book_id, ...`: Groups borrow transactions by book.
  - `HAVING COUNT(l.loan_id) >= 2`: **HAVING vs WHERE**. Explain to the teacher: *"WHERE filters individual rows before aggregation; HAVING filters aggregate groups after `COUNT()` is calculated. Here, it filters for books that have been borrowed 2 or more times."*

---

#### 2. Department Revenue & Fine Audit View (`BranchFineSummaryView`)
```sql
SELECT * FROM BranchFineSummaryView;
```
Show the definition from `schema.sql`:
```sql
CREATE OR REPLACE VIEW BranchFineSummaryView AS
SELECT 
    br.branch_code,
    br.branch_name,
    COUNT(DISTINCT u.user_id) AS registered_students,
    COUNT(f.fine_id) AS total_fines_levied,
    COALESCE(SUM(CASE WHEN f.status = 'PAID' THEN f.amount ELSE 0 END), 0.00) AS revenue_collected,
    COALESCE(SUM(CASE WHEN f.status = 'UNPAID' THEN f.amount ELSE 0 END), 0.00) AS pending_fines
FROM branches br
LEFT JOIN users u ON br.branch_id = u.branch_id
LEFT JOIN fines f ON u.user_id = f.user_id
GROUP BY br.branch_id, br.branch_code, br.branch_name;
```
- **Line-by-Line Explanation**:
  - `LEFT JOIN users u ON br.branch_id = u.branch_id`: Ensures that even branches with zero registered students are included in the report.
  - `COUNT(DISTINCT u.user_id)`: Counts unique students without inflating numbers due to multiple fines.
  - `SUM(CASE WHEN f.status = 'PAID' THEN f.amount ELSE 0 END)`: **Conditional Aggregation**. Evaluates fine status per row; if `'PAID'`, includes the amount; otherwise adds 0.
  - `COALESCE(..., 0.00)`: If a branch has no fines, `SUM()` returns `NULL`. `COALESCE` replaces `NULL` with `0.00` for clean display.

---

#### 3. Relational Division using Double `NOT EXISTS` (Sailors / Company Lab Concept)
In your Teacher Demo Tools on the website, click **Query 2 (Relational Division)** or run in Workbench:
```sql
SELECT u.usn, u.name, br.branch_name AS student_dept
FROM users u
JOIN branches br ON u.branch_id = br.branch_id
WHERE u.role = 'STUDENT'
  AND NOT EXISTS (
      SELECT b.branch_id FROM branches b WHERE b.branch_code IN ('CSE', 'ECE', 'MECH')
      AND NOT EXISTS (
          SELECT l.loan_id FROM loans l
          JOIN book_copies bc ON l.copy_id = bc.copy_id
          JOIN books bk ON bc.book_id = bk.book_id
          WHERE l.user_id = u.user_id AND bk.branch_id = b.branch_id
      )
  );
```
- **Line-by-Line Explanation**:
  - **Relational Division Concept ($A \div B$)**: Finds tuples in relation $A$ that match ALL tuples in relation $B$.
  - In SQL, relational division has no native operator, so it is expressed using **Correlated Double `NOT EXISTS`**.
  - **Outer `NOT EXISTS`**: *"There does not exist an engineering branch..."*
  - **Inner `NOT EXISTS`**: *"...for which there does not exist a loan taken by this student."*
  - **English meaning**: *"Find all students who have borrowed books from EVERY engineering branch (CSE, ECE, and MECH)."*
  - **Result**: Priya Patel (Student 2), who holds active books across CSE, ECE, and MECH!

---

## 🎯 Master Viva Defense: 10 Hardest Questions & Bulletproof Answers

| # | Question Teacher May Ask | Your Bulletproof Answer |
| :---: | :--- | :--- |
| **1** | **"Why use triggers instead of Java code to check max 5 books?"** | *"If someone opens MySQL Workbench, Python, or another tool and runs an `INSERT` directly, Java application code is bypassed completely! A database-level `BEFORE INSERT` trigger guarantees data integrity regardless of which client connects to the database."* |
| **2** | **"What does `SQLSTATE '45000'` mean?"** | *"It is the ANSI SQL standard code for unhandled user-defined exceptions. In MySQL, `SIGNAL SQLSTATE '45000'` immediately rolls back the current statement and returns our custom error message."* |
| **3** | **"Why is `request_votes` a composite primary key?"** | *"It has `PRIMARY KEY (request_id, user_id)`. Neither attribute alone is unique, but their combination is. This enforces at the schema level that a user can vote for a request at most once."* |
| **4** | **"What is the difference between `NOW()` and `CURRENT_TIMESTAMP`?"** | *"In MySQL, `NOW()` and `CURRENT_TIMESTAMP` are synonyms that return the current date and time in `'YYYY-MM-DD HH:MM:SS'` format. `CURRENT_TIMESTAMP` is standard ANSI SQL, while `NOW()` is commonly used in procedural statements."* |
| **5** | **"Why use `LEFT JOIN` in `BranchFineSummaryView` instead of `INNER JOIN`?"** | *"An `INNER JOIN` would exclude departments like Civil or Electrical that have zero fines levied. A `LEFT JOIN` preserves all rows from `branches`, ensuring every department appears in the report with `0.00` revenue."* |
| **6** | **"Where is referential integrity cascading used?"** | *"In `schema.sql`: `FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE`. If an obsolete book title is removed from the catalog, all of its physical copy records are automatically purged, preventing orphaned records."* |
| **7** | **"How do you prevent SQL injection?"** | *"In our backend, all user inputs are bound via parameterized JDBC `PreparedStatement` placeholders (`?`). Values are treated as literal data, preventing attackers from injecting SQL control tokens."* |
| **8** | **"How is the fine calculated dynamically?"** | *"Using MySQL date arithmetic: `DATEDIFF(NOW(), due_date) * 1.00`. It calculates the exact elapsed days and multiplies by ₹1.00 per day."* |
| **9** | **"What is the advantage of using Views?"** | *"Views provide data abstraction, simplify complex multi-table joins into a single virtual table, and provide security by restricting direct table access to sensitive financial columns."* |
| **10**| **"How does the live transaction log work?"** | *"Every action in the Java backend executes within a synchronized logger that intercepts the query and synchronously appends formatted SQL statements into `live_dbms_transactions.sql`. This allows external tools like MySQL Workbench to observe changes instantaneously."* |
