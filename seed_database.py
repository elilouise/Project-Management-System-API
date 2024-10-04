import sqlite3

def seed_database():
    conn = sqlite3.connect('projects.db')
    conn.row_factory = sqlite3.Row

    # Insert Users
    conn.execute("INSERT INTO users (username, password, name, role, email) VALUES ('manager1', 'password123', 'Alice Johnson', 'Manager', 'alice.johnson@example.com')")
    conn.execute("INSERT INTO users (username, password, name, role, email) VALUES ('manager2', 'password123', 'Robert Brown', 'Manager', 'robert.brown@example.com')")
    conn.execute("INSERT INTO users (username, password, name, role, email) VALUES ('team_member1', 'password123', 'John Doe', 'Team Member', 'john.doe@example.com')")
    conn.execute("INSERT INTO users (username, password, name, role, email) VALUES ('team_member2', 'password123', 'Emma Smith', 'Team Member', 'emma.smith@example.com')")
    conn.execute("INSERT INTO users (username, password, name, role, email) VALUES ('team_member3', 'password123', 'James White', 'Team Member', 'james.white@example.com')")

    # Insert Projects
    conn.execute("INSERT INTO projects (project_name, description, start_date, end_date, status) VALUES ('Website Redesign', 'Redesign the company website for a modern look', '2024-10-01', '2025-01-31', 'In Progress')")
    conn.execute("INSERT INTO projects (project_name, description, start_date, end_date, status) VALUES ('Marketing Campaign', 'Plan and execute a digital marketing campaign', '2024-11-01', '2025-02-28', 'In Progress')")
    conn.execute("INSERT INTO projects (project_name, description, start_date, end_date, status) VALUES ('Mobile App Development', 'Develop a new mobile application for customer engagement', '2024-10-15', '2025-04-15', 'In Progress')")

    # Insert Tasks
    conn.execute("INSERT INTO tasks (project_id, task_name, description, due_date, status, assigned_user_id) VALUES (1, 'Create Wireframes', 'Design wireframes for the new website layout', '2024-11-10', 'Not Started', 3)")
    conn.execute("INSERT INTO tasks (project_id, task_name, description, due_date, status, assigned_user_id) VALUES (1, 'Develop Frontend', 'Implement frontend for the redesigned website', '2024-12-20', 'Not Started', 4)")
    conn.execute("INSERT INTO tasks (project_id, task_name, description, due_date, status, assigned_user_id) VALUES (2, 'Create Marketing Content', 'Develop blog posts and social media content', '2024-11-15', 'In Progress', 5)")
    conn.execute("INSERT INTO tasks (project_id, task_name, description, due_date, status, assigned_user_id) VALUES (2, 'Social Media Ads', 'Run Facebook and Instagram ads', '2024-12-05', 'Not Started', NULL)")
    conn.execute("INSERT INTO tasks (project_id, task_name, description, due_date, status, assigned_user_id) VALUES (3, 'Design App UI', 'Create user interface for the mobile app', '2024-11-30', 'In Progress', 4)")
    conn.execute("INSERT INTO tasks (project_id, task_name, description, due_date, status, assigned_user_id) VALUES (3, 'API Development', 'Develop backend APIs for mobile app', '2025-01-15', 'Not Started', NULL)")

    conn.commit()
    conn.close()

seed_database()
