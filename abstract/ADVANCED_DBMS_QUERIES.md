# College E-Library DBMS Project: Advanced SQL Query Bank & Concept Guide
**Course Code**: 24CS520 — Database Management Systems (JSSSTU CSE)  
**Database**: MySQL Server 8.0 (Port: `3307`, User: `sem5e2`, Database: `elibrary_db`)  
**Target Audience**: Students preparing for DBMS Lab Viva & Theory Defense  

---

## 📑 Table of Contents

1. [Executive Summary & Syllabus Alignment (24CS520)](#1-executive-summary--syllabus-alignment)
2. [Master Concept Inventory: What Query Concepts Exist in This Project?](#2-master-concept-inventory)
3. [PART I: Active Database Concepts — Stored Triggers Demonstration](#part-i-stored-triggers-demonstration)
   - [Trigger 1: `PreventBorrowOverLimit` (Max 5 Books Quota)](#trigger-1-preventborrowoverlimit)
   - [Trigger 2: `PreventBorrowIfOverdue` (Defaulter / Fine Lock)](#trigger-2-preventborrowifoverdue)
   - [Trigger 3: `UpdateCopyOnLoan` (Auto Copy State Synchronization)](#trigger-3-updatecopyonloan)
   - [Trigger 4: `UpdateCopyOnReturn` (Auto Copy Release Synchronization)](#trigger-4-updatecopyonreturn)
4. [PART II: Advanced Query Bank (Copy-Paste Ready for MySQL Workbench)](#part-ii-advanced-query-bank)
   - [Set 1: Multi-Table Joins & Outer Joins (INNER, LEFT, RIGHT, FULL OUTER)](#set-1-multi-table-joins--outer-joins)
   - [Set 2: Self-Joins & Cartesian Cross Joins](#set-2-self-joins--cartesian-cross-joins)
   - [Set 3: Aggregates, GROUP BY & The HAVING Clause](#set-3-aggregates-group-by--the-having-clause)
   - [Set 4: Nested & Quantified Subqueries (IN, NOT IN, ALL, ANY)](#set-4-nested--quantified-subqueries)
   - [Set 5: Correlated Subqueries & Relational Division ($A \div B$)](#set-5-correlated-subqueries--relational-division)
   - [Set 6: Set Operations in SQL (UNION, INTERSECT, EXCEPT)](#set-6-set-operations-in-sql)
   - [Set 7: Inline Derived Tables & Window Aggregates](#set-7-inline-derived-tables)
   - [Set 8: Database Views & Virtual Relations](#set-8-database-views)
5. [PART III: Normalization Theory & Functional Dependencies (1NF, 2NF, 3NF, BCNF)](#part-iii-normalization-theory--proof)
6. [PART IV: Spoken Viva Cheat Sheet & Anticipated Questions](#part-iv-spoken-viva-cheat-sheet)

---

## 1. Executive Summary & Syllabus Alignment

This guide maps the **College E-Library Database System** directly to the official VTU / JSSSTU **24CS520 Database Management Systems** syllabus:

| Syllabus Unit | Course Outcome | Core Topics Covered in This Project |
| :--- | :--- | :--- |
| **Unit 2: ER Model & Constraints** | **CO2** (L3) | Entity sets, weak entities, foreign key referential actions (`ON DELETE CASCADE`, `ON DELETE SET NULL`), check constraints. |
| **Unit 3: Relational Algebra** | **CO3** (L3) | Selection ($\sigma$), Projection ($\pi$), Cartesian Product ($\times$), Theta Join ($\bowtie$), Equijoin, Aggregate ($\gamma$), Outer Joins ($\unicode{x27D5}, \unicode{x27D6}, \unicode{x27D7}$). |
| **Unit 4: Advanced SQL & Retrieval** | **CO4** (L3) | Complex multi-table joins, nested subqueries (`IN`, `NOT IN`), quantified subqueries (`ALL`, `ANY`), correlated subqueries (`EXISTS`, `NOT EXISTS`), relational division ($A \div B$), conditional aggregates (`CASE WHEN`), views, and **stored triggers**. |
| **Unit 5: Normalization Theory** | **CO5** (L3) | Functional dependencies (FDs), 1NF, 2NF, 3NF, BCNF proofs, and elimination of insertion, deletion, and update anomalies. |

---

## 2. Master Concept Inventory

### "What SQL Concepts Are in This Project Besides Simple Joins?"

Many students assume relational databases only do basic `SELECT ... JOIN`. In reality, this College E-Library project implements **16 distinct, advanced DBMS concepts**:

1. **Unary Relational Algebra Operations**: Selection ($\sigma$) and Projection ($\pi$).
2. **Multi-Table Relational Equi-Joins**: 3-way, 4-way, and 5-way inner joins linking students, branches, subjects, copies, and loans.
3. **Outer Joins (`LEFT JOIN` and `RIGHT JOIN`)**: Preserving non-matching tuples (e.g., branches with zero active loans or subjects without textbook copies).
4. **Self-Joins**: Joining a table with itself to compare records (e.g., finding higher-rated books within the same department).
5. **Cartesian Product / Cross Joins (`CROSS JOIN`)**: Generating the complete combinatorial matrix of engineering departments $\times$ book genres.
6. **Aggregate Functions with `GROUP BY`**: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`, and `COUNT(DISTINCT)`.
7. **The `HAVING` Clause vs `WHERE`**: Post-aggregation filtering on grouped data (e.g., `HAVING COUNT(l.loan_id) >= 2`).
8. **Conditional Aggregation (`CASE WHEN ... THEN ... ELSE ... END`)**: Calculating multiple conditional totals (e.g., paid fines vs unpaid fines) inside a single query.
9. **Nested Set-Membership Subqueries (`IN`, `NOT IN`)**: Filtering records using uncorrelated subquery results.
10. **Quantified Set-Comparison Subqueries (`> ALL`, `> ANY`)**: Comparing a value against an entire subquery set.
11. **Correlated Subqueries (`EXISTS`, `NOT EXISTS`)**: Inner queries that reference attributes from the outer query row-by-row.
12. **Relational Division ($A \div B$) via Double `NOT EXISTS`**: Answering universal quantification questions (*"Find students who borrowed books from EVERY branch"*).
13. **Set Operations**: `UNION` and `UNION ALL`, plus SQL emulation of `INTERSECT` and `EXCEPT`.
14. **Date-Time Arithmetic**: `NOW()`, `DATE_ADD()`, `DATE_SUB()`, `DATEDIFF()` for 12-hour reservations, 30-day loans, and daily overdue fines.
15. **Virtual Relations (Views)**: `CREATE OR REPLACE VIEW` for security, data independence, and query reusability.
16. **Active Database Concepts (Triggers)**: `BEFORE INSERT`, `AFTER INSERT`, `AFTER UPDATE`, row-level execution (`FOR EACH ROW`), pseudo-records (`NEW`, `OLD`), and exception signaling (`SIGNAL SQLSTATE '45000'`).

---

## PART I: Stored Database Triggers Demonstration

### "Is there a concept of Triggers here? How do I demonstrate them?"

**YES!** The database `elibrary_db` includes **4 production-grade stored triggers** compiled directly into MySQL. In DBMS theory, triggers represent **Active Database Rules** (E-C-A: Event-Condition-Action model). They enforce business integrity rules that cannot be bypassed even if someone accesses the database directly via MySQL Workbench or command line!

---

### Trigger 1: `PreventBorrowOverLimit`
- **Trigger Event**: `BEFORE INSERT ON loans`
- **Rule Enforced**: A student can have a maximum of **5 active loans** across the entire university.
- **Trigger Code (from `schema.sql`)**:
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

#### 🧪 Live Workbench Demonstration Query:
Student **Priya Patel** (`user_id = 3`, USN `01JST24UCS002`) already has **4 active loans** seeded in the database.
1. Run this query in MySQL Workbench to verify Priya currently has 4 loans:
```sql
SELECT u.user_id, u.usn, u.name, COUNT(l.loan_id) AS active_loans
FROM users u
JOIN loans l ON u.user_id = l.user_id
WHERE u.user_id = 3 AND l.status = 'ACTIVE'
GROUP BY u.user_id, u.usn, u.name;
```

2. Now, insert a 5th valid loan for Priya (Copy 701, Thermodynamics):
```sql
INSERT INTO loans (user_id, copy_id, borrow_date, due_date, status)
VALUES (3, 701, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 'ACTIVE');
-- Result: Query OK, 1 row affected (5/5 loans reached)
```

3. Now, **attempt to force a 6th loan** for Priya (Copy 801, Theory of Machines):
```sql
INSERT INTO loans (user_id, copy_id, borrow_date, due_date, status)
VALUES (3, 801, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 'ACTIVE');
```

4. **💥 Watch MySQL Workbench Throw the Trigger Exception**:
```text
Error Code: 1644. Borrowing limit exceeded: Maximum 5 books allowed per student
```

#### 🔍 Line-by-Line Explanation for the Teacher:
- `BEFORE INSERT ON loans`: The trigger executes *prior* to inserting the row. If the condition fails, the row is never written to disk.
- `FOR EACH ROW`: This is a row-level trigger that fires for every incoming record.
- `NEW.user_id`: The `NEW` keyword refers to the row being inserted. We capture the student ID.
- `SELECT COUNT(*) INTO active_count ...`: Executes a query counting how many loans currently have `status = 'ACTIVE'` for this student.
- `IF active_count >= 5 THEN`: Checks if the limit has been reached.
- `SIGNAL SQLSTATE '45000'`: Standard ANSI SQL error code for unhandled user exceptions. It immediately rolls back the insert and sends our custom error text.

---

### Trigger 2: `PreventBorrowIfOverdue`
- **Trigger Event**: `BEFORE INSERT ON loans`
- **Rule Enforced**: If a student holds any book past its `due_date`, OR has an unsettled fine (`status = 'UNPAID'`), all borrowing is locked!
- **Trigger Code (from `schema.sql`)**:
```sql
DELIMITER //
CREATE TRIGGER PreventBorrowIfOverdue
BEFORE INSERT ON loans
FOR EACH ROW
BEGIN
    DECLARE overdue_count INT;
    DECLARE unpaid_fine_count INT;

    SELECT COUNT(*) INTO overdue_count 
    FROM loans 
    WHERE user_id = NEW.user_id 
      AND status = 'ACTIVE' 
      AND NOW() > due_date;

    SELECT COUNT(*) INTO unpaid_fine_count
    FROM fines
    WHERE user_id = NEW.user_id AND status = 'UNPAID';
      
    IF overdue_count > 0 OR unpaid_fine_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Borrowing blocked: Student has overdue books or unpaid fines';
    END IF;
END;
//
DELIMITER ;
```

#### 🧪 Live Workbench Demonstration Query:
1. Create an unpaid fine of ₹10.00 for Student **Rahul Sharma** (`user_id = 2`):
```sql
INSERT INTO fines (loan_id, user_id, days_overdue, amount, status)
VALUES (2, 2, 10, 10.00, 'UNPAID');
```

2. Now try to issue a new book to Rahul:
```sql
INSERT INTO loans (user_id, copy_id, borrow_date, due_date, status)
VALUES (2, 501, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 'ACTIVE');
```

3. **💥 Watch MySQL Workbench Throw the Trigger Exception**:
```text
Error Code: 1644. Borrowing blocked: Student has overdue books or unpaid fines
```

4. Clean up the test fine:
```sql
DELETE FROM fines WHERE user_id = 2 AND amount = 10.00;
```

---

### Trigger 3: `UpdateCopyOnLoan`
- **Trigger Event**: `AFTER INSERT ON loans`
- **Rule Enforced**: When a loan row is created, automatically update `book_copies.status = 'BORROWED'`.
- **Trigger Code**:
```sql
DELIMITER //
CREATE TRIGGER UpdateCopyOnLoan
AFTER INSERT ON loans
FOR EACH ROW
BEGIN
    UPDATE book_copies 
    SET status = 'BORROWED' 
    WHERE copy_id = NEW.copy_id;
END;
//
DELIMITER ;
```

#### 🧪 Live Workbench Demonstration Query:
```sql
-- Step 1: Check copy 501 is currently AVAILABLE
SELECT copy_id, copy_code, status FROM book_copies WHERE copy_id = 501;

-- Step 2: Insert a loan for Student 4 (Amit)
INSERT INTO loans (user_id, copy_id, borrow_date, due_date, status)
VALUES (4, 501, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 'ACTIVE');

-- Step 3: Check copy 501 again - notice it automatically became BORROWED!
SELECT copy_id, copy_code, status FROM book_copies WHERE copy_id = 501;
```

---

### Trigger 4: `UpdateCopyOnReturn`
- **Trigger Event**: `AFTER UPDATE ON loans`
- **Rule Enforced**: When a loan record is stamped with a `return_date`, automatically reset `book_copies.status = 'AVAILABLE'`.
- **Trigger Code**:
```sql
DELIMITER //
CREATE TRIGGER UpdateCopyOnReturn
AFTER UPDATE ON loans
FOR EACH ROW
BEGIN
    IF NEW.return_date IS NOT NULL AND OLD.return_date IS NULL THEN
        UPDATE book_copies 
        SET status = 'AVAILABLE' 
        WHERE copy_id = NEW.copy_id;
    END IF;
END;
//
DELIMITER ;
```

#### 🧪 Live Workbench Demonstration Query:
```sql
-- Step 1: Return the loan created in Trigger 3
UPDATE loans 
SET return_date = NOW(), status = 'RETURNED' 
WHERE user_id = 4 AND copy_id = 501 AND status = 'ACTIVE';

-- Step 2: Check copy 501 - notice it automatically reverted to AVAILABLE!
SELECT copy_id, copy_code, status FROM book_copies WHERE copy_id = 501;
```

---

## PART II: Advanced Query Bank

All queries below can be copied and pasted directly into MySQL Workbench. Each query includes its **Relational Algebra notation**, **SQL code**, **line-by-line explanation**, and **what to say to your teacher**.

---

### Set 1: Multi-Table Joins & Outer Joins

#### Query 1.1: 5-Table Master Circulation Inner Join
- **Syllabus Topic**: Unit 3 (Binary Relational Operation: JOIN) & Unit 4 (Multi-table Retrieval)
- **Relational Algebra**:  
  $$\pi_{\text{loan\_id, usn, student\_name, title, copy\_code, branch\_code, due\_date}}(\text{loans} \bowtie \text{users} \bowtie \text{book\_copies} \bowtie \text{books} \bowtie \text{branches})$$
- **SQL Query**:
```sql
SELECT 
    l.loan_id,
    u.usn,
    u.name AS student_name,
    bk.title AS book_title,
    bc.copy_code,
    br.branch_code AS book_dept,
    l.borrow_date,
    l.due_date,
    l.status AS loan_status
FROM loans l
JOIN users u ON l.user_id = u.user_id
JOIN book_copies bc ON l.copy_id = bc.copy_id
JOIN books bk ON bc.book_id = bk.book_id
JOIN branches br ON bk.branch_id = br.branch_id
WHERE l.status = 'ACTIVE'
ORDER BY l.due_date ASC;
```
- **Line-by-Line Explanation**:
  - `FROM loans l`: The transaction fact table representing current circulation.
  - `JOIN users u ON l.user_id = u.user_id`: An **equijoin** on `user_id` to pull patron identity.
  - `JOIN book_copies bc ON l.copy_id = bc.copy_id`: Equijoin to retrieve the physical barcode `copy_code`.
  - `JOIN books bk ON bc.book_id = bk.book_id`: Equijoin to fetch the catalog title and author metadata.
  - `JOIN branches br ON bk.branch_id = br.branch_id`: Equijoin to resolve the engineering department owning the book.
  - `WHERE l.status = 'ACTIVE'`: Selection ($\sigma$) filtering out historical returned loans.
  - `ORDER BY l.due_date ASC`: Sorts loans by earliest return deadline first.
- **🗣️ Spoken Script for Teacher**:
  > *"Sir/Ma'am, this is a 5-table relational equi-join. It traverses our normalized schema from the transaction relation `loans` up through `users`, `book_copies`, `books`, and `branches`. This demonstrates how Third Normal Form decouples data into separate tables while SQL joins reconstruct the complete business view on demand."*

---

#### Query 1.2: Left Outer Join for Comprehensive Department Audit
- **Syllabus Topic**: Unit 3 (OUTER JOIN Operations: Left Outer Join $R \ \unicode{x27D5} \ S$)
- **Relational Algebra**:  
  $$\text{branches} \ \unicode{x27D5}_{\text{branches.branch\_id} = \text{books.branch\_id}} \text{books}$$
- **SQL Query**:
```sql
SELECT 
    br.branch_code,
    br.branch_name,
    br.hod_name,
    COUNT(bk.book_id) AS total_catalog_titles,
    COALESCE(AVG(bk.rating), 0.0) AS avg_rating
FROM branches br
LEFT JOIN books bk ON br.branch_id = bk.branch_id
GROUP BY br.branch_id, br.branch_code, br.branch_name, br.hod_name
ORDER BY total_catalog_titles DESC;
```
- **Line-by-Line Explanation**:
  - `LEFT JOIN books bk ON br.branch_id = bk.branch_id`:
    - **Crucial Concept**: An `INNER JOIN` would drop branches like Civil or EEE if they had zero books.
    - A `LEFT JOIN` guarantees that **every single row from `branches` is preserved** in the result. If a branch has no books, the columns from `books` are padded with `NULL`.
  - `COUNT(bk.book_id)`: Counts non-null book IDs. If a branch has no books, it returns `0` (unlike `COUNT(*)` which would return `1` for the NULL row!).
  - `COALESCE(AVG(bk.rating), 0.0)`: Replaces `NULL` with `0.0` when no ratings exist.
- **🗣️ Spoken Script for Teacher**:
  > *"Here we demonstrate a LEFT OUTER JOIN ($R \ \unicode{x27D5} \ S$). Unlike an inner join which eliminates non-matching tuples, the left outer join preserves all branches—even if a newly established department has zero registered books—returning 0 titles instead of discarding the department."*

---

#### Query 1.3: Right Outer Join Showing Courses Lacking Library Books
- **Syllabus Topic**: Unit 3 (Right Outer Join $R \ \unicode{x27D6} \ S$)
- **SQL Query**:
```sql
SELECT 
    s.subject_code,
    s.subject_name,
    s.semester,
    bk.title AS mapped_book_title
FROM books bk
RIGHT JOIN subjects s ON bk.subject_id = s.subject_id
WHERE bk.book_id IS NULL;
```
- **Line-by-Line Explanation**:
  - `RIGHT JOIN subjects s`: Preserves all curriculum subjects from the right table `subjects`.
  - `WHERE bk.book_id IS NULL`: Finds subjects that have **no matching textbook** in the catalog.
  - This is an **Anti-Join pattern** used by librarians for curriculum gap auditing.

---

### Set 2: Self-Joins & Cartesian Cross Joins

#### Query 2.1: Self-Join Comparing Book Ratings Within the Same Department
- **Syllabus Topic**: Unit 3 & Unit 4 (Self-Join — joining a table with itself)
- **SQL Query**:
```sql
SELECT 
    b1.title AS higher_rated_book,
    b1.rating AS higher_rating,
    b2.title AS lower_rated_book,
    b2.rating AS lower_rating,
    br.branch_code
FROM books b1
JOIN books b2 ON b1.branch_id = b2.branch_id AND b1.rating > b2.rating
JOIN branches br ON b1.branch_id = br.branch_id
ORDER BY br.branch_code, (b1.rating - b2.rating) DESC;
```
- **Line-by-Line Explanation**:
  - `FROM books b1 JOIN books b2`: We alias `books` twice (`b1` and `b2`) as if they were two distinct tables.
  - `b1.branch_id = b2.branch_id`: Ensures both books belong to the **same academic branch**.
  - `b1.rating > b2.rating`: Compares ratings within that branch.
- **🗣️ Spoken Script for Teacher**:
  > *"This is a Self-Join. We join the `books` relation to itself using two distinct tuple variables `b1` and `b2` to compare tuples within the same department partition without requiring subqueries."*

---

#### Query 2.2: Cartesian Cross Join ($\times$) for Curriculum Coverage Matrix
- **Syllabus Topic**: Unit 3 (Cartesian Product $R \times S$)
- **Relational Algebra**:  
  $$\pi_{\text{branch\_code}}(\text{branches}) \times \pi_{\text{genre\_name}}(\text{genres})$$
- **SQL Query**:
```sql
SELECT 
    br.branch_code,
    g.genre_name,
    COUNT(bk.book_id) AS books_available
FROM branches br
CROSS JOIN genres g
LEFT JOIN books bk ON bk.branch_id = br.branch_id AND bk.genre_id = g.genre_id
GROUP BY br.branch_code, g.genre_name
ORDER BY br.branch_code, books_available ASC;
```
- **Line-by-Line Explanation**:
  - `CROSS JOIN genres g`: Computes the Cartesian Product ($5 \text{ branches} \times 5 \text{ genres} = 25 \text{ combinations}$).
  - `LEFT JOIN books bk`: Connects books to check if the library owns titles for that specific combination.
  - Identifies which departments are missing specific genres (e.g. Mechanical having 0 AI books).

---

### Set 3: Aggregates, GROUP BY & The HAVING Clause

#### Query 3.1: Catalog Statistics with Multiple Aggregates
- **Syllabus Topic**: Unit 3 (Aggregate Functions $\gamma$) & Unit 4 (Grouping in SQL)
- **SQL Query**:
```sql
SELECT 
    br.branch_code,
    COUNT(bk.book_id) AS total_titles,
    ROUND(AVG(bk.rating), 2) AS average_rating,
    MIN(bk.pub_year) AS oldest_edition,
    MAX(bk.pub_year) AS newest_edition
FROM branches br
JOIN books bk ON br.branch_id = bk.branch_id
GROUP BY br.branch_code;
```
- **Line-by-Line Explanation**:
  - `COUNT()`: Computes cardinality of tuples in each group.
  - `AVG()`, `MIN()`, `MAX()`: Computes mean, lowest, and highest values of attributes per group.
  - `GROUP BY br.branch_code`: Partitions the relation into equivalence classes based on department.

---

#### Query 3.2: High-Demand Books with `HAVING` vs `WHERE`
- **Syllabus Topic**: Unit 4 (The HAVING Clause — Filtering Groups)
- **SQL Query**:
```sql
SELECT 
    b.book_id,
    b.title,
    b.isbn,
    COUNT(l.loan_id) AS times_borrowed
FROM books b
JOIN book_copies bc ON b.book_id = bc.book_id
JOIN loans l ON bc.copy_id = l.copy_id
WHERE l.borrow_date >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
GROUP BY b.book_id, b.title, b.isbn
HAVING COUNT(l.loan_id) >= 2;
```
- **Line-by-Line Explanation**:
  - `WHERE l.borrow_date >= ...`: Filters individual rows **before** aggregation.
  - `HAVING COUNT(l.loan_id) >= 2`: Filters the **aggregated groups** after `COUNT()` is evaluated.
- **🗣️ Spoken Script for Teacher**:
  > *"Examiners frequently test the difference between `WHERE` and `HAVING`. In this query, `WHERE` eliminates loans older than one year before grouping occurs. `HAVING` operates on the aggregate result, selecting only books whose grouped borrow count is 2 or more."*

---

#### Query 3.3: Department Revenue Ledger via Conditional Aggregation
- **Syllabus Topic**: Unit 4 (Conditional SQL Expressions with `CASE WHEN`)
- **SQL Query**:
```sql
SELECT 
    br.branch_code,
    COUNT(DISTINCT u.user_id) AS registered_students,
    COUNT(f.fine_id) AS total_fines_levied,
    COALESCE(SUM(CASE WHEN f.status = 'PAID' THEN f.amount ELSE 0 END), 0.00) AS collected_revenue,
    COALESCE(SUM(CASE WHEN f.status = 'UNPAID' THEN f.amount ELSE 0 END), 0.00) AS pending_revenue
FROM branches br
LEFT JOIN users u ON br.branch_id = u.branch_id
LEFT JOIN fines f ON u.user_id = f.user_id
GROUP BY br.branch_code;
```
- **Line-by-Line Explanation**:
  - `SUM(CASE WHEN f.status = 'PAID' THEN f.amount ELSE 0 END)`: Instead of writing two separate queries for paid vs unpaid fines, `CASE WHEN` acts as an inline `IF-ELSE` expression evaluated for every row during aggregation.

---

### Set 4: Nested & Quantified Subqueries

#### Query 4.1: Uncorrelated Nested Subquery with `IN`
- **Syllabus Topic**: Unit 4 (Set Membership Operator `IN`)
- **SQL Query**:
```sql
SELECT usn, name, email, semester
FROM users
WHERE role = 'STUDENT'
  AND branch_id IN (
      SELECT branch_id 
      FROM subjects 
      WHERE subject_name LIKE '%Database%' OR subject_name LIKE '%Java%'
  );
```
- **Line-by-Line Explanation**:
  - The inner subquery executes once, returning the set of branch IDs offering Database or Java subjects.
  - The outer query selects students whose `branch_id` belongs to that set.

---

#### Query 4.2: Subquery with `NOT IN` (Set Difference $R - S$)
- **Syllabus Topic**: Unit 3 & Unit 4 (Finding Unreferenced Tuples via `NOT IN`)
- **SQL Query**:
```sql
SELECT book_id, title, isbn, edition
FROM books
WHERE book_id NOT IN (
    SELECT DISTINCT bc.book_id
    FROM book_copies bc
    JOIN loans l ON bc.copy_id = l.copy_id
);
```
- **Line-by-Line Explanation**:
  - Inner query: Finds all `book_id`s that have appeared in the `loans` table.
  - Outer query: Retrieves books that have **never been borrowed** by any student (dormant catalog items).

---

#### Query 4.3: Quantified Subquery using `> ALL`
- **Syllabus Topic**: Unit 4 (Set Comparison Operator `ALL`)
- **SQL Query**:
```sql
SELECT title, rating, pub_year
FROM books
WHERE rating > ALL (
    SELECT rating 
    FROM books 
    WHERE branch_id = (SELECT branch_id FROM branches WHERE branch_code = 'MECH')
);
```
- **Line-by-Line Explanation**:
  - `> ALL (...)`: Evaluates to `TRUE` only if the book's rating is **strictly greater than every single rating** in the Mechanical Engineering department.
  - If MECH books have ratings of 4.5 and 4.6, only books with rating $> 4.6$ (e.g., 4.7, 4.8, 4.9) are selected.

---

#### Query 4.4: Quantified Subquery using `> ANY` (or `> SOME`)
- **Syllabus Topic**: Unit 4 (Set Comparison Operator `ANY` / `SOME`)
- **SQL Query**:
```sql
SELECT title, rating, pub_year
FROM books
WHERE rating > ANY (
    SELECT rating 
    FROM books 
    WHERE branch_id = (SELECT branch_id FROM branches WHERE branch_code = 'CSE')
);
```
- **Line-by-Line Explanation**:
  - `> ANY (...)`: Evaluates to `TRUE` if the book's rating is greater than **at least one** book in the CSE department.

---

### Set 5: Correlated Subqueries & Relational Division

#### Query 5.1: Correlated Subquery with `EXISTS`
- **Syllabus Topic**: Unit 4 (Correlated Subquery & `EXISTS` Operator)
- **SQL Query**:
```sql
SELECT a.author_id, a.author_name, a.country
FROM authors a
WHERE EXISTS (
    SELECT 1 
    FROM books b
    JOIN book_copies bc ON b.book_id = bc.book_id
    JOIN loans l ON bc.copy_id = l.copy_id
    WHERE b.author_id = a.author_id AND l.status = 'ACTIVE'
);
```
- **Line-by-Line Explanation**:
  - **Correlated Subquery**: The inner query references `a.author_id` from the outer query row.
  - `EXISTS`: Returns `TRUE` the moment the inner query finds at least one matching active loan for that author, short-circuiting execution for maximum performance.

---

#### Query 5.2: Relational Division ($A \div B$) Using Double `NOT EXISTS`
- **Syllabus Topic**: Unit 3 (Relational Division $A \div B$) & Unit 4 (Universal Quantification)
- **Concept Question**: *"Find all students who have borrowed books from EVERY engineering branch (CSE, ECE, and MECH)!"*
- **Relational Algebra Equation**:
  $$\text{Result} = \pi_{\text{user\_id, usn, name}}(\text{users}) \div \pi_{\text{branch\_id}}(\sigma_{\text{branch\_code} \in \{\text{'CSE', 'ECE', 'MECH'}\}}(\text{branches}))$$
- **SQL Query**:
```sql
SELECT u.usn, u.name, br.branch_name AS enrolled_department
FROM users u
JOIN branches br ON u.branch_id = br.branch_id
WHERE u.role = 'STUDENT'
  AND NOT EXISTS (
      -- Set B: All required branches
      SELECT b.branch_id 
      FROM branches b 
      WHERE b.branch_code IN ('CSE', 'ECE', 'MECH')
      AND NOT EXISTS (
          -- Set A: Branches from which this student has borrowed
          SELECT l.loan_id 
          FROM loans l
          JOIN book_copies bc ON l.copy_id = bc.copy_id
          JOIN books bk ON bc.book_id = bk.book_id
          WHERE l.user_id = u.user_id 
            AND bk.branch_id = b.branch_id
      )
  );
```
- **Expected Result**:
  | usn | name | enrolled_department |
  | :--- | :--- | :--- |
  | `01JST24UCS002` | Priya Patel | Electronics and Communication Engineering |

- **Step-by-Step Logic Breakdown**:
  - Relational Division has no native SQL keyword like `DIVIDE BY`.
  - It is mathematically formulated as:  
    $$\forall b \in B, \exists a \in A \equiv \neg (\exists b \in B \text{ such that } \neg (\exists a \in A))$$
  - **Outer `NOT EXISTS`**: *"There does not exist a required branch..."*
  - **Inner `NOT EXISTS`**: *"...for which this student has NOT borrowed a book."*
  - If a student has borrowed from CSE, ECE, and MECH, the inner `NOT EXISTS` is false for all 3 branches, meaning no unborrowed branch exists, so the outer `NOT EXISTS` evaluates to `TRUE`!

---

### Set 6: Set Operations in SQL

#### Query 6.1: `UNION` vs `UNION ALL` — Unified Patron Hold List
- **Syllabus Topic**: Unit 3 & Unit 4 (Set Union Operation)
- **SQL Query**:
```sql
-- Unified List of All Active Patron Commitments (Reservations + Loans)
SELECT 
    '12-Hour Reservation' AS commitment_type,
    r.user_id,
    u.usn,
    u.name AS student_name,
    bc.copy_code,
    r.expires_at AS deadline
FROM reservations r
JOIN users u ON r.user_id = u.user_id
JOIN book_copies bc ON r.copy_id = bc.copy_id
WHERE r.status = 'PENDING'

UNION ALL

SELECT 
    '30-Day Active Loan' AS commitment_type,
    l.user_id,
    u.usn,
    u.name AS student_name,
    bc.copy_code,
    l.due_date AS deadline
FROM loans l
JOIN users u ON l.user_id = u.user_id
JOIN book_copies bc ON l.copy_id = bc.copy_id
WHERE l.status = 'ACTIVE'

ORDER BY deadline ASC;
```
- **Line-by-Line Explanation**:
  - `UNION ALL`: Combines rows from two queries with identical schemas without sorting or deduplicating, preserving high execution speed.

---

### Set 7: Inline Derived Tables & Window Aggregates

#### Query 7.1: Deviation from Department Average Rating
- **Syllabus Topic**: Unit 4 (Subqueries in the `FROM` Clause / Derived Tables)
- **SQL Query**:
```sql
SELECT 
    b.title,
    br.branch_code,
    b.rating AS book_rating,
    dept_avg.avg_rating AS branch_average,
    ROUND(b.rating - dept_avg.avg_rating, 2) AS rating_deviation
FROM books b
JOIN branches br ON b.branch_id = br.branch_id
JOIN (
    SELECT branch_id, ROUND(AVG(rating), 2) AS avg_rating
    FROM books
    GROUP BY branch_id
) dept_avg ON b.branch_id = dept_avg.branch_id
ORDER BY rating_deviation DESC;
```
- **Line-by-Line Explanation**:
  - `dept_avg` is a **Derived Table** created on-the-fly in the `FROM` clause.
  - It computes department averages first, then joins back to individual books to compute deviation.

---

### Set 8: Database Views & Virtual Relations

#### Query 8.1: Querying the Three Pre-Compiled System Views
```sql
-- 1. Real-Time Overdue Loans View with Dynamically Computed Fines:
SELECT * FROM OverdueLoansView;

-- 2. High-Demand Books View (HAVING COUNT >= 2):
SELECT * FROM HighDemandBooksView;

-- 3. Institutional Financial & Department Revenue Audit View:
SELECT * FROM BranchFineSummaryView;
```
- **Line-by-Line Explanation**:
  - A View is a stored query that behaves as a virtual table. It stores no physical data; instead, it executes its underlying `SELECT` dynamically when referenced.
  - **Benefits for Viva**:
    1. **Data Security**: Hides sensitive user credentials from report viewers.
    2. **Logical Data Independence**: If underlying tables change slightly, views can keep the API contracts stable.
    3. **Query Simplification**: Eliminates the need to write complex 4-table joins repeatedly.

---

## PART III: Normalization Theory & Proof

During your viva, examiners frequently ask you to prove why your tables are in **Third Normal Form (3NF)**. Here is your complete theoretical proof:

### 1. First Normal Form (1NF)
- **Rule**: A relation is in 1NF if and only if all domain values are **atomic** (single-valued) and there are no repeating groups.
- **Proof in `elibrary_db`**:
  - No comma-separated lists (e.g., authors are normalized into an `authors` table rather than `books(authors)` containing `"Elmasri, Navathe"`).
  - Physical copies are tracked as individual rows in `book_copies` rather than an array of barcodes inside `books`.

### 2. Second Normal Form (2NF)
- **Rule**: A relation is in 2NF if it is in 1NF and **no non-prime attribute is partially dependent on any candidate key**. (Applies to tables with composite primary keys).
- **Proof in `elibrary_db`**:
  - In `request_votes(request_id, user_id)`:
    - Primary Key: `(request_id, user_id)` (composite).
    - Attribute: `voted_at`.
    - `voted_at` is dependent on the **entire composite key** (the timestamp of that specific user's vote on that specific request). There are no partial functional dependencies.
  - In `books` and `book_copies`: We separated abstract catalog metadata (`books`) from physical asset tracking (`book_copies`). If we had combined them into one table `books_and_copies(book_id, copy_id, title, isbn, copy_status)`, then `title` and `isbn` would depend only on `book_id` (a partial key), violating 2NF! Splitting them into two relations achieves strict 2NF.

### 3. Third Normal Form (3NF)
- **Rule**: A relation is in 3NF if it is in 2NF and **no non-prime attribute is transitively dependent on the primary key** ($X \to Y \to Z$ is disallowed if $Y$ is not a superkey).
- **Proof in `elibrary_db`**:
  - In `users`: Attributes are `(user_id, usn, name, email, role, branch_id, semester)`. We store `branch_id`, NOT `branch_name` or `hod_name`. If `users` contained `hod_name`, we would have a transitive dependency:  
    $$\text{user\_id} \to \text{branch\_id} \to \text{hod\_name}$$
    If an HOD changed, we would need to update hundreds of student rows (Update Anomaly)! By normalizing `branches` into its own table, we eliminate transitive dependencies.
  - In `books`: Attributes reference `author_id` and `publisher_id` rather than storing author country or publisher address inline.

### 4. Boyce-Codd Normal Form (BCNF)
- **Rule**: For every functional dependency $X \to Y$, $X$ must be a **superkey**.
- **Proof**: In all 14 tables, every determinant attribute is a candidate key or primary key. Therefore, the schema is in 3NF and BCNF.

---

## PART IV: Spoken Viva Cheat Sheet

Keep these punchy explanations in mind when answering the examiner:

| Concept | What to Say in 15 Seconds |
| :--- | :--- |
| **Why Triggers?** | *"Triggers enforce business rules inside the database engine itself. Even if someone writes raw SQL in MySQL Workbench, the database will abort illegal checkouts with `SQLSTATE 45000`."* |
| **Relational Division** | *"Relational division finds entities that relate to ALL items in a subset. In SQL, it is implemented using double `NOT EXISTS`: 'There does not exist a branch for which this student has not borrowed'."* |
| **INNER vs LEFT JOIN** | *"INNER JOIN discards non-matching tuples. LEFT JOIN preserves all rows from the primary table, filling missing values with NULL—crucial for auditing departments with zero active loans."* |
| **HAVING vs WHERE** | *"WHERE filters individual tuples before grouping; HAVING filters aggregated partition statistics after `GROUP BY` completes."* |
| **3NF Justification** | *"We separated abstract catalog titles from physical copies, and normalized branches and authors, eliminating all partial and transitive functional dependencies."* |
