-- The schema meets the requirements for project and task management, user authentication, 
-- and team member assignment, and provides all the necessary relationships to manage different levels of user access effectively


-- Users Table: Stores information about users, including login credentials and roles
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    -- Defines the role column with allowed values, mandatory to be either 'Manager' or 'Team Member'
    role TEXT CHECK (role IN ('Manager', 'Team Member')) NOT NULL,
    email TEXT UNIQUE
);

-- Projects Table: Stores information about projects
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    -- Defines the status column with restricted values and sets default to 'In Progress'
    status TEXT CHECK (status IN ('In Progress', 'Completed')) DEFAULT 'In Progress'
);

-- Team Members Assignment Table: Stores relationships between projects and team members
CREATE TABLE project_team_members (
    project_team_member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects (project_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    -- Ensures each project-user pair is unique 
    -- Ensures each user is assigned to a project only once to prevent duplicate entries
    UNIQUE (project_id, user_id)
);

-- Tasks Table: Stores information about tasks associated with projects and assigned team members
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    task_name TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    -- Defines the status column with allowed values and sets default to 'Not Started'
    status TEXT CHECK (status IN ('Not Started', 'In Progress', 'Completed')) DEFAULT 'Not Started',
    assigned_user_id INTEGER,
    hours_logged REAL DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects (project_id),
    FOREIGN KEY (assigned_user_id) REFERENCES users (user_id)
);

-- Login Sessions Table: Stores session information for logged-in users
CREATE TABLE login_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- Task Logs Table: Table to log the time spent on tasks by users
CREATE TABLE task_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each log entry
    task_id INTEGER NOT NULL,                  -- References the task being logged
    user_id INTEGER NOT NULL,                  -- References the user logging the time
    hours_spent REAL NOT NULL,                 -- Amount of time spent (can be fractional)
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Timestamp for when the log entry is created
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),  -- Ensures task_id exists in tasks table
    FOREIGN KEY (user_id) REFERENCES users(user_id)   -- Ensures user_id exists in users table
);

