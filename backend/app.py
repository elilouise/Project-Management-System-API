# import `Flask` to create the web app
# import `request` to handle incoming data, and import `jsonify` to send JSON responses
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS


# import sqlite3 to connect and interact with the SQLite database
import sqlite3

# create an instance of the Flask class for the web app (i.e. initialize a new instance of the Flask app)
app = Flask(__name__)

# Enable CORS for all routes
# This will allow the frontend to make requests to the backend without being blocked by the browser's CORS policy
CORS(app)



# Helper function to get user role from the database based on authenticated session or token
def get_user_role(user_id):
    # Connect to the database to fetch user details
    conn = get_db_connection()
    
    # Execute a query to get the role of the user with the provided user_id
    user = conn.execute('SELECT role FROM users WHERE user_id = ?', (user_id,)).fetchone()
    
    # Close the database connection to free up resources
    conn.close()

    # Return the user's role if found; otherwise, default to 'Team Member'
    return user['role'] if user else 'Team Member'



# Helper function that checks if the user making a request has the necessary role to perform a specific action
def check_role(required_role):
    # Extract user ID from the request headers (assuming it's sent with headers)
    user_id = request.headers.get('user_id')
    
    # If user_id is missing, return unauthorized response
    if not user_id:
        return jsonify({"message": "Unauthorized: User ID is missing"}), 401

    # Get the user's role from the database
    role = get_user_role(user_id)
    
    # If the user's role does not match the required role, return a permission error response
    if role != required_role:
        return jsonify({"message": f"Permission denied: {required_role} access required"}), 403
    
    # Return None if the user is authorized
    return None



# function to get a connection to the SQLite database
def get_db_connection():

    # create a connection to the projects (SQLite) database
    connection = sqlite3.connect('../projects.db')
    # configure connection to return rows as dictionaries, allowing access by column name
    connection.row_factory = sqlite3.Row 
    
    return connection



@app.route('/')
def index():
    return "Welcome to the Project Management API", 200



# User Authentication
# Defines a route for user login, allowing only POST requests
@app.route('/login', methods=['POST'])
# Function to handles the user login logic
def login_user():

    # Get the request data (username and password)
    data = request.get_json()  

    # Extracts the username and password from the request data for authentication    
    username = data['username']
    password = data['password']

    # Connect to the database
    conn = get_db_connection()

    # Retrieves user information from the database for matching credentials and closes the connection
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    
    # Checks if user exists; 
    # if so, returns success message with role and user ID, otherwise returns an error message for invalid credentials
    if user:
        return jsonify({"message": "Login successful", "role": user['role'], "user_id": user['user_id']}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    


# Create a project (Manager Only)
# Defines a route to create a new project, allowing only POST requests 
@app.route('/projects', methods=['POST'])
# Function to handle the logic for creating a new project
def create_project():

    # Check if the user has 'Manager' access
    access_error = check_role('Manager')

    # If the user lacks the required role, return the access error response
    if access_error:
        return access_error

    # Get the request data 
    data = request.get_json()

    # Extracts project details from the request data, with default values for optional fields (description, start date, end date)
    project_name = data['project_name']
    description = data.get('description', '')
    start_date = data.get('start_date', None)
    end_date = data.get('end_date', None)

    # Connect to the database
    conn = get_db_connection()
    # Inserts a new project into the database with the provided project details (name, description, start date, end date)
    conn.execute('INSERT INTO projects (project_name, description, start_date, end_date) VALUES (?, ?, ?, ?)',
                 (project_name, description, start_date, end_date))
    
    # Commits the transaction to save changes and closes the database connection
    conn.commit()
    conn.close()

    # Returns a success message indicating the project was created, with a 201 status code 
    return jsonify({"message": "Project created successfully"}), 201



# View Project Details (Manager Access Only)
@app.route('/projects/<int:project_id>', methods=['GET'])
def view_project(project_id):
    # Check if the user has 'Manager' access
    access_error = check_role('Manager')
    if access_error:
        return access_error

    # Connect to the database
    conn = get_db_connection()

    # Retrieve the project from the database
    project = conn.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,)).fetchone()

    # Return error if the project does not exist
    if not project:
        conn.close()
        return jsonify({"message": "Project not found"}), 404

    # Return the project details
    project_details = dict(project)
    conn.close()
    return jsonify(project_details), 200



# Update Project Details (Manager Access Only)
@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    # Check if the user has 'Manager' access
    access_error = check_role('Manager')
    if access_error:
        return access_error

    # Get the updated project data from the request
    data = request.get_json()
    project_name = data.get('project_name', None)
    description = data.get('description', None)
    start_date = data.get('start_date', None)
    end_date = data.get('end_date', None)

    # Connect to the database and retrieve the project
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,)).fetchone()

    # Return error if the project does not exist
    if not project:
        conn.close()
        return jsonify({"message": "Project not found"}), 404

    # Update the project with the new values or retain the old ones if not provided
    conn.execute('''
        UPDATE projects
        SET project_name = COALESCE(?, project_name),
            description = COALESCE(?, description),
            start_date = COALESCE(?, start_date),
            end_date = COALESCE(?, end_date)
        WHERE project_id = ?
    ''', (project_name, description, start_date, end_date, project_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message indicating the project was updated
    return jsonify({"message": "Project updated successfully"}), 200



# Delete a Project (Manager Access Only)
@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    # Check if the user has 'Manager' access
    access_error = check_role('Manager')
    if access_error:
        return access_error

    # Connect to the database and check if the project exists
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,)).fetchone()

    # Return error if the project does not exist
    if not project:
        conn.close()
        return jsonify({"message": "Project not found"}), 404

    # Delete the project from the database
    conn.execute('DELETE FROM projects WHERE project_id = ?', (project_id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message indicating the project was deleted
    return jsonify({"message": "Project deleted successfully"}), 200



# Create a Task for a Project (Manager Access Only)
# Defines a route to create a task for a project:
@app.route('/tasks', methods=['POST'])
# Function to handle the logic for creating tasks a project
def create_task():

    # Check if the user has 'Manager' access
    access_error = check_role('Manager')
    if access_error:
        return access_error

    # Get the request data 
    data = request.get_json()

    # Extracts task details from the request data, with default values for optional fields (description, due date)
    project_id = data['project_id']
    task_name = data['task_name']
    description = data.get('description', '')
    due_date = data.get('due_date', None)
    status = data.get('status', 'Not Started')  # Default status is 'Not Started' if not provided
    assigned_user_id = data.get('assigned_user_id', None)
    
    # Validate that the status is one of the allowed values
    allowed_statuses = ['Not Started', 'In Progress', 'Completed']
    if status not in allowed_statuses:
        return jsonify({"message": f"Invalid status. Allowed values are: {allowed_statuses}"}), 400

    # Connect to the database
    conn = get_db_connection()

    # Inserts a new task into the database linked to a project, using the provided details (project ID, task name, description, due date, status, assigned user)
    conn.execute('INSERT INTO tasks (project_id, task_name, description, due_date, status, assigned_user_id) VALUES (?, ?, ?, ?, ?, ?)',
        (project_id, task_name, description, due_date, status, assigned_user_id))
    
    # Commits the transaction to save changes and closes the database connection
    conn.commit()
    conn.close()

    # Returns a success message indicating the task was created, with a 201 status code 
    return jsonify({"message": "Task created successfully"}), 201



# Assign or Reassign a Task (Manager Access Only)
@app.route('/tasks/<int:task_id>/assign', methods=['PUT'])
def assign_task(task_id):

    # Check if the user has 'Manager' access
    access_error = check_role('Manager')
    if access_error:
        return access_error

    # Get the assigned user ID from the request data
    data = request.get_json()
    assigned_user_id = data.get('assigned_user_id')

    # Validate that assigned_user_id is provided
    if not assigned_user_id:
        return jsonify({"message": "Invalid input: assigned_user_id must be provided"}), 400

    # Connect to the database
    conn = get_db_connection()

    # Check if the task exists
    task = conn.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,)).fetchone()
    if not task:
        conn.close()
        return jsonify({"message": "Task not found"}), 404

    # Update the assigned_user_id of the task
    conn.execute('UPDATE tasks SET assigned_user_id = ? WHERE task_id = ?', (assigned_user_id, task_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message indicating the task was assigned or reassigned
    return jsonify({"message": "Task assigned/reassigned successfully"}), 200



# Edit a Task (Manager Only)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):

    # Check if the user has 'Manager' access
    access_error = check_role('Manager')
    if access_error:
        return access_error

    # Get the updated task data from the request
    data = request.get_json()
    task_name = data.get('task_name', None)
    description = data.get('description', None)
    due_date = data.get('due_date', None)
    status = data.get('status', None)
    assigned_user_id = data.get('assigned_user_id', None)

    # Validate that the status is one of the allowed values, if provided
    allowed_statuses = ['Not Started', 'In Progress', 'Completed']
    if status and status not in allowed_statuses:
        return jsonify({"message": f"Invalid status. Allowed values are: {allowed_statuses}"}), 400
    
    # Connect to the database and retrieve the specified task
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,)).fetchone()

    # Return error if the task does not exist
    if not task:
        conn.close()
        return jsonify({"message": "Task not found"}), 404

    # Update the task with the new values or retain the old ones if not provided
    conn.execute('''
        UPDATE tasks 
        SET task_name = COALESCE(?, task_name),
            description = COALESCE(?, description),
            due_date = COALESCE(?, due_date),
            status = COALESCE(?, status),
            assigned_user_id = COALESCE(?, assigned_user_id)
        WHERE task_id = ?
    ''', (task_name, description, due_date, status, assigned_user_id, task_id))

    # Save changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({"message": "Task updated successfully"}), 200



# Delete a Task (Manager Only)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):

    # Check if the user has Manager access
    access_error = check_role('Manager')
    if access_error:
        return access_error

    # Connect to the database
    conn = get_db_connection()

    # Check if the task exists
    task = conn.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,)).fetchone()
    if not task:
        conn.close()
        return jsonify({"message": "Task not found"}), 404

    # Delete the task
    conn.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
    conn.commit()
    conn.close()

    # Return a success message indicating the task was deleted
    return jsonify({"message": "Task deleted successfully"}), 200



# View assigned tasks (Team Members)
@app.route('/tasks/assigned', methods=['GET'])
def view_assigned_tasks():
    # Extract user ID from the request headers
    user_id = request.headers.get('user_id')

    # If user_id is missing, return unauthorized response
    if not user_id:
        return jsonify({"message": "Unauthorized: User ID is missing"}), 401
    
    # Ensure that only Team Members can view assigned tasks
    if get_user_role(user_id) != 'Team Member':
        return jsonify({"message": "Permission denied: Only Team Members can view assigned tasks"}), 403

    # Connect to the database and retrieve tasks assigned to the user
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE assigned_user_id = ?', (user_id,)).fetchall()
    conn.close()
   
    # Return the list of assigned tasks
    return jsonify([dict(task) for task in tasks]), 200



#  Update the Status of an Assigned Task (Team Member)
@app.route('/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    # Extract user ID from the request headers
    user_id = request.headers.get('user_id')
    
    # If user_id is missing, return unauthorized response
    if not user_id:
        return jsonify({"message": "Unauthorized: User ID is missing"}), 401

    # Get the updated status from the request
    data = request.get_json()
    new_status = data.get('status')
    
    # Validate that the status is one of the allowed values
    allowed_statuses = ['Not Started', 'In Progress', 'Completed']
    if new_status not in allowed_statuses:
        return jsonify({"message": f"Invalid status. Allowed values are: {allowed_statuses}"}), 400

    # Connect to the database and retrieve the specified task
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE task_id = ? AND assigned_user_id = ?', (task_id, user_id)).fetchone()

    # Return error if the task does not exist or is not assigned to the user
    if not task:
        conn.close()
        return jsonify({"message": "Task not found or not assigned to the user"}), 404
    
    # Return error if the task is not assigned to the requesting user
    if task['assigned_user_id'] != int(user_id):
        conn.close()
        return jsonify({"message": "Permission denied: You are not assigned to this task"}), 403

    # Update the task status
    conn.execute('UPDATE tasks SET status = ? WHERE task_id = ?', (new_status, task_id))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({"message": "Task status updated successfully"}), 200



# Log Time Spent on a Task (Team Member)
# Endpoint for Team Members to log time spent on their assigned tasks
@app.route('/tasks/<int:task_id>/log-time', methods=['POST'])
def log_time_on_task(task_id):
    # Extract user ID from the request headers
    user_id = request.headers.get('user_id')
    
    # If user_id is missing, return unauthorized response
    if not user_id:
        return jsonify({"message": "Unauthorized: User ID is missing"}), 401

    # Check if the user is a 'Team Member'
    if get_user_role(user_id) != 'Team Member':
        return jsonify({"message": "Permission denied: Only Team Members can log time"}), 403

    # Get the time log data from the request
    data = request.get_json()
    hours_spent = data.get('hours_spent')

    # Validate that hours_spent is provided and is a positive number
    if not hours_spent or not isinstance(hours_spent, (int, float)) or hours_spent <= 0:
        return jsonify({"message": "Invalid input: hours_spent must be a positive number"}), 400

    # Connect to the database and check if the task is assigned to the user
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE task_id = ? AND assigned_user_id = ?', (task_id, user_id)).fetchone()

    # Return error if the task does not exist or is not assigned to the user
    if not task:
        conn.close()
        return jsonify({"message": "Task not found or not assigned to the user"}), 404
    
    # Return error if the task is not assigned to the requesting user
    if task['assigned_user_id'] != int(user_id):
        conn.close()
        return jsonify({"message": "Permission denied: You are not assigned to this task"}), 403

    # Log the time spent on the task by inserting a record in the task_logs table
    conn.execute('INSERT INTO task_logs (task_id, user_id, hours_spent) VALUES (?, ?, ?)', (task_id, user_id, hours_spent))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({"message": "Time logged successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)