# To-Do-List-with-AI-suggestion
# To-Do List with AI Recommendations

A modern and user-friendly To-Do List application that provides AI-based task suggestions and color-coding based on task priority. The app allows users to manage their tasks by setting priorities, deadlines, and marking tasks as completed.

## Features
- **Add Tasks**: Users can add tasks with a title, priority (1-10), and a deadline.
- **AI Task Suggestions**: AI provides task recommendations based on priority and the proximity of the deadline.
- **Task Sorting**: Tasks are sorted by priority and deadline for better management.
- **Task Status**: Users can mark tasks as completed or delete them.
- **Color Coding**: Tasks are color-coded based on their priority level:
  - **Red** for high priority (1-3)
  - **Yellow** for medium priority (4-7)
  - **Green** for low priority (8-10)
- **Modern UI**: The app uses a modern and clean UI design for a better user experience.
  
## Requirements
- Python 3.x
- `tkinter` for the GUI (comes pre-installed with Python)
- `tkcalendar` for date picker functionality
- `sqlite3` for local database management

## Installation

To install the required dependencies, you can run the following:

```bash
pip install tkcalendar
```

## How to Use
1. **Add a Task**:
   - Enter the title of the task.
   - Set the priority (1-10), where 1 is the highest priority.
   - Set the deadline using the date picker.

2. **View Tasks**:
   - Tasks are displayed in two categories:
     - **Pending**: Tasks that are yet to be completed.
     - **Completed**: Tasks that have been marked as done.
   - Tasks are color-coded based on priority.

3. **Edit a Task**:
   - Select a task from the pending list, edit its details, and update it.

4. **Complete or Delete a Task**:
   - Select a task from the pending list and mark it as completed or delete it.

5. **AI Task Suggestions**:
   - AI will suggest tasks based on urgency (priority + deadline).

## Database
The application uses an SQLite database to store tasks. The database is automatically created if it does not exist and stores the following information for each task:
- Task ID (auto-incremented)
- Task Title
- Priority (1-10)
- Deadline (in MM/DD/YY format)
- Task Status (Pending/Completed)

## Screenshots
Add a screenshot here for a preview of the application.

## License
This project is open-source and available under the [MIT License](LICENSE).
© 2025 Lasindu Lakmina. All rights reserved.

## Author
Created by **Lasindu Lakmina**.
