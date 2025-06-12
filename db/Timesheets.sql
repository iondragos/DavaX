-- This database schema supports a timesheet management system.
-- It allows employees to log hours worked on tasks assigned to various projects.
-- The structure is normalized into separate entities: Employees, Projects, Tasks, Timecards, and TimecardEntries.
-- Constraints such as NOT NULL, UNIQUE, CHECK, and DEFAULT enforce data integrity.
-- A JSON-based metadata column is included in ProjectTasks for extensible task details.
-- Indexes are added to improve performance for common search and reporting operations.


-- ===============================
-- TABLE CREATION
-- ===============================

-- 1. EMPLOYEES
CREATE TABLE Employees (
    employee_id NUMBER PRIMARY KEY,
    full_name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE,
    hire_date DATE DEFAULT SYSDATE,
    salary NUMBER CHECK (salary > 0),
    CONSTRAINT chk_email_format CHECK (INSTR(email, '@') > 0)
);

CREATE INDEX idx_employee_name ON Employees(full_name);

-- 2. PROJECTS
CREATE TABLE Projects (
    project_id NUMBER PRIMARY KEY,
    project_name VARCHAR2(100) NOT NULL,
    description CLOB,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT chk_project_dates CHECK (end_date IS NULL OR end_date > start_date)
);

-- 3. PROJECT_TASKS
CREATE TABLE ProjectTasks (
    task_id NUMBER PRIMARY KEY,
    project_id NUMBER NOT NULL,
    task_name VARCHAR2(100) NOT NULL,
    estimated_hours NUMBER(5,2) DEFAULT 0 CHECK (estimated_hours >= 0),
    metadata CLOB CHECK (metadata IS JSON),  -- JSON semistructurat
    CONSTRAINT fk_task_project FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE
);

CREATE INDEX idx_task_name ON ProjectTasks(task_name);

-- 4. TIMECARDS
CREATE TABLE Timecards (
    timecard_id NUMBER PRIMARY KEY,
    employee_id NUMBER NOT NULL,
    submission_date DATE DEFAULT SYSDATE,
    status VARCHAR2(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    CONSTRAINT fk_timecard_employee FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    CONSTRAINT uq_timecard UNIQUE (employee_id, submission_date)
);

CREATE INDEX idx_timecard_status ON Timecards(status);

-- 5. TIMECARD_ENTRIES
CREATE TABLE TimecardEntries (
    entry_id NUMBER PRIMARY KEY,
    timecard_id NUMBER NOT NULL,
    task_id NUMBER NOT NULL,
    work_date DATE NOT NULL,
    hours_worked NUMBER(3,1) CHECK (hours_worked BETWEEN 0 AND 24),
    comments VARCHAR2(255),
    CONSTRAINT fk_entry_timecard FOREIGN KEY (timecard_id) REFERENCES Timecards(timecard_id) ON DELETE CASCADE,
    CONSTRAINT fk_entry_task FOREIGN KEY (task_id) REFERENCES ProjectTasks(task_id),
    CONSTRAINT uq_entry UNIQUE (timecard_id, task_id, work_date)
);

CREATE INDEX idx_work_date ON TimecardEntries(work_date);


-- ===============================
-- DATA INSERTION
-- ===============================
-- 1. EMPLOYEES
INSERT INTO Employees (employee_id, full_name, email, hire_date, salary)
VALUES (101, 'Alice Johnson', 'alice.johnson@endava.com', TO_DATE('2022-03-01', 'YYYY-MM-DD'), 4200);

INSERT INTO Employees (employee_id, full_name, email, hire_date, salary)
VALUES (102, 'Bob Smith', 'bob.smith@endava.com', TO_DATE('2023-07-15', 'YYYY-MM-DD'), 5000);

INSERT INTO Employees (employee_id, full_name, email, hire_date, salary)
VALUES (103, 'Clara White', 'clara.white@endava.com', TO_DATE('2021-10-20', 'YYYY-MM-DD'), 4600);

INSERT INTO Employees (employee_id, full_name, email, hire_date, salary)
VALUES (104, 'David Black', 'david.black@endava.com', TO_DATE('2022-12-05', 'YYYY-MM-DD'), 4700);

COMMIT;


-- 2. PROJECTS
INSERT INTO Projects (project_id, project_name, description, start_date, end_date)
VALUES (201, 'Apollo Migration', 'Migrate legacy systems to cloud', TO_DATE('2024-01-10', 'YYYY-MM-DD'), NULL);

INSERT INTO Projects (project_id, project_name, description, start_date, end_date)
VALUES (202, 'Nova Redesign', 'UI/UX revamp for Nova platform', TO_DATE('2023-11-01', 'YYYY-MM-DD'), TO_DATE('2024-06-30', 'YYYY-MM-DD'));

INSERT INTO Projects (project_id, project_name, description, start_date, end_date)
VALUES (203, 'Orion AI Tooling', 'Tooling and automation for ML Ops', TO_DATE('2024-05-01', 'YYYY-MM-DD'), NULL);

COMMIT;


-- 3. PROJECT_TASKS (cu JSON)
INSERT INTO ProjectTasks (task_id, project_id, task_name, estimated_hours, metadata)
VALUES (
  301, 201, 'Database refactoring', 50,
  '{
    "priority": "High",
    "skills": ["SQL", "Performance Tuning"],
    "notes": "Touch legacy schema"
  }'
);

INSERT INTO ProjectTasks (task_id, project_id, task_name, estimated_hours, metadata)
VALUES (
  302, 202, 'UI component audit', 30,
  '{
    "priority": "Medium",
    "tech_stack": ["React", "Figma"],
    "dependencies": ["UI Library"]
  }'
);

INSERT INTO ProjectTasks (task_id, project_id, task_name, estimated_hours, metadata)
VALUES (
  303, 202, 'Accessibility improvements', 25,
  '{
    "priority": "High",
    "compliance": "WCAG 2.1",
    "impact": "global"
  }'
);

INSERT INTO ProjectTasks (task_id, project_id, task_name, estimated_hours, metadata)
VALUES (
  304, 203, 'Build ML pipeline CLI', 40,
  '{
    "priority": "Medium",
    "language": "Python",
    "tools": ["Click", "MLflow"]
  }'
);

COMMIT;

-- 4. TIMECARDS
INSERT INTO Timecards (timecard_id, employee_id, submission_date, status)
VALUES (401, 101, TO_DATE('2025-06-10', 'YYYY-MM-DD'), 'Approved');

INSERT INTO Timecards (timecard_id, employee_id, submission_date, status)
VALUES (402, 102, TO_DATE('2025-06-10', 'YYYY-MM-DD'), 'Pending');

INSERT INTO Timecards (timecard_id, employee_id, submission_date, status)
VALUES (403, 101, TO_DATE('2025-06-03', 'YYYY-MM-DD'), 'Approved');

INSERT INTO Timecards (timecard_id, employee_id, submission_date, status)
VALUES (404, 103, TO_DATE('2025-06-10', 'YYYY-MM-DD'), 'Rejected');

COMMIT;

-- 5. TIMECARD_ENTRIES
INSERT INTO TimecardEntries (entry_id, timecard_id, task_id, work_date, hours_worked, comments)
VALUES (501, 401, 301, TO_DATE('2025-06-09', 'YYYY-MM-DD'), 6.0, 'Initial analysis and schema sketch');

INSERT INTO TimecardEntries (entry_id, timecard_id, task_id, work_date, hours_worked, comments)
VALUES (502, 401, 301, TO_DATE('2025-06-10', 'YYYY-MM-DD'), 7.5, 'Refactored 5 procedures');

INSERT INTO TimecardEntries (entry_id, timecard_id, task_id, work_date, hours_worked, comments)
VALUES (503, 402, 302, TO_DATE('2025-06-10', 'YYYY-MM-DD'), 4.0, 'Reviewed UI layouts');

INSERT INTO TimecardEntries (entry_id, timecard_id, task_id, work_date, hours_worked, comments)
VALUES (504, 403, 303, TO_DATE('2025-06-03', 'YYYY-MM-DD'), 5.5, 'Contrast and font-size fixes');

INSERT INTO TimecardEntries (entry_id, timecard_id, task_id, work_date, hours_worked, comments)
VALUES (505, 404, 304, TO_DATE('2025-06-10', 'YYYY-MM-DD'), 3.0, 'Prototype pipeline created');

INSERT INTO TimecardEntries (entry_id, timecard_id, task_id, work_date, hours_worked, comments)
VALUES (506, 403, 302, TO_DATE('2025-06-04', 'YYYY-MM-DD'), 6.5, 'Worked on design tokens');

INSERT INTO TimecardEntries (entry_id, timecard_id, task_id, work_date, hours_worked, comments)
VALUES (507, 401, 303, TO_DATE('2025-06-08', 'YYYY-MM-DD'), 4.5, 'ARIA role checks and validation');

COMMIT;


-- ===============================
-- VIEWS
-- ===============================

-- VIEW that shows detailed timesheet data per employee, per task, per project
CREATE OR REPLACE VIEW vw_employee_timesheet_summary AS
SELECT
    e.employee_id,             -- Employee ID
    e.full_name,               -- Full name of the employee
    t.submission_date,         -- Date when the timecard was submitted
    t.status,                  -- Timecard status (Approved / Pending / Rejected)
    te.work_date,              -- Date of the work entry
    pt.task_name,              -- Task name from the project
    pr.project_name,           -- Project name
    te.hours_worked            -- Hours worked on that task on that day
FROM
    Employees e
JOIN Timecards t ON e.employee_id = t.employee_id
JOIN TimecardEntries te ON t.timecard_id = te.timecard_id
JOIN ProjectTasks pt ON te.task_id = pt.task_id
JOIN Projects pr ON pt.project_id = pr.project_id;


-- Materialized view that stores total hours worked per employee
CREATE MATERIALIZED VIEW mv_total_hours_per_employee
BUILD IMMEDIATE                 -- Build the view now, not deferred
REFRESH COMPLETE                -- Full refresh of data each time

-- Refresh scheduling
START WITH SYSDATE
NEXT SYSDATE + 1

AS
SELECT
    e.employee_id,             -- Employee ID
    e.full_name,               -- Full name of the employee
    SUM(te.hours_worked) AS total_hours  -- Total worked hours
FROM
    Employees e
JOIN Timecards t ON e.employee_id = t.employee_id
JOIN TimecardEntries te ON t.timecard_id = te.timecard_id
GROUP BY
    e.employee_id,
    e.full_name;





-- ===============================
-- SELECTS
-- ===============================

-- This query groups timecard data by project and the priority level of tasks, 
-- which is extracted from the JSON metadata column.
-- It calculates how many tasks exist per priority level within each project 
-- and how many total hours have been logged for them.
SELECT
    pr.project_name,
    JSON_VALUE(pt.metadata, '$.priority') AS task_priority,
    COUNT(DISTINCT pt.task_id) AS num_tasks,
    SUM(te.hours_worked) AS total_hours
FROM
    Projects pr
JOIN ProjectTasks pt ON pr.project_id = pt.project_id
JOIN TimecardEntries te ON pt.task_id = te.task_id
GROUP BY
    pr.project_name,
    JSON_VALUE(pt.metadata, '$.priority');
    

-- This query lists all project tasks, including those that have never been worked on 
-- (no timecard entries), using a LEFT JOIN.
-- It retrieves each task’s name, project name, and the 'priority' field stored in metadata.
-- COALESCE ensures that if no hours are logged, the total is shown as zero instead of null.
SELECT
    pt.task_id,
    pt.task_name,
    pr.project_name,
    JSON_VALUE(pt.metadata, '$.priority') AS priority,
    COALESCE(SUM(te.hours_worked), 0) AS total_logged_hours
FROM
    ProjectTasks pt
LEFT JOIN TimecardEntries te ON pt.task_id = te.task_id
JOIN Projects pr ON pt.project_id = pr.project_id
GROUP BY
    pt.task_id,
    pt.task_name,
    pr.project_name,
    JSON_VALUE(pt.metadata, '$.priority');


-- This query ranks employees within each project based on the total number of hours 
-- they’ve worked on high-priority tasks (as defined in the JSON metadata).
-- It filters only tasks where priority = 'High' and aggregates total hours by employee and project.
-- The RANK() analytic function assigns a relative rank for each employee per project, 
-- allowing teams to identify top contributors on critical work.
SELECT
    e.full_name,
    pr.project_name,
    JSON_VALUE(pt.metadata, '$.priority') AS priority,
    SUM(te.hours_worked) AS total_hours,
    RANK() OVER (PARTITION BY pr.project_name ORDER BY SUM(te.hours_worked) DESC) AS rank_in_project
FROM
    Employees e
JOIN Timecards tc ON e.employee_id = tc.employee_id
JOIN TimecardEntries te ON tc.timecard_id = te.timecard_id
JOIN ProjectTasks pt ON te.task_id = pt.task_id
JOIN Projects pr ON pt.project_id = pr.project_id
WHERE
    JSON_VALUE(pt.metadata, '$.priority') = 'High'
GROUP BY
    e.full_name,
    pr.project_name,
    JSON_VALUE(pt.metadata, '$.priority');



