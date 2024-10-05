# Project Management System 

## Overview
This is a Python-based Project Management System designed for a company to manage projects, tasks, and team members. The system includes user authentication with different access levels for managers and team members, providing an organized way to monitor project progress and efficiently assign tasks.

## Key Features

### User Authentication
- Users log in using a username and password.
- Two types of users: Managers and Team Members.
- Managers have full access, including creating projects and assigning tasks.
- Team Members can view assigned tasks, update task status, and log hours.

### Project Management (Manager Access Only)
- Managers can create, view, update, or delete projects.
- Projects include a name, description, start date, and end date.

### Team Management (Manager Access Only)
- Managers can add team members with a name, role, email, and login credentials.
- Team members can be assigned to one or more projects.
- Managers can assign tasks to team members.

### Task Management
- Managers can create tasks under projects with details such as task name, description, due date, and assigned team member.
- Tasks have statuses: “Not Started,” “In Progress,” or “Completed.”
- Team members can update task status and log time spent on tasks.

### Project Progress Tracking (Manager Access Only)
- Managers can view the overall progress of each project based on the completion percentage of tasks.
- Projects are marked as “In Progress” or “Completed” accordingly.

### Saving and Loading Data
- Project, task, user, and team member information is saved in a database.
- Data is loaded when the program starts, ensuring continuity.
