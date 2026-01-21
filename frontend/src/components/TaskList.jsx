/**
 * TaskList component - Displays tasks grouped by status
 */
import TaskItem from './TaskItem';

function TaskList({ tasks, onUpdate, onDelete }) {
  // Group tasks by status
  const groupedTasks = {
    todo: tasks.filter((task) => task.status === 'todo'),
    in_progress: tasks.filter((task) => task.status === 'in_progress'),
    done: tasks.filter((task) => task.status === 'done'),
  };

  const statusLabels = {
    todo: '⏳ To Do',
    in_progress: '🔄 In Progress',
    done: '✅ Done',
  };

  const renderTaskSection = (status, label) => {
    const statusTasks = groupedTasks[status];
    
    if (statusTasks.length === 0) return null;

    return (
      <div key={status} className="task-section">
        <h2>{label} ({statusTasks.length})</h2>
        <div className="task-list">
          {statusTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onUpdate={onUpdate}
              onDelete={onDelete}
            />
          ))}
        </div>
      </div>
    );
  };

  if (tasks.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📝</div>
        <div className="empty-state-text">
          No tasks yet. Create your first task to get started!
        </div>
      </div>
    );
  }

  return (
    <>
      {renderTaskSection('todo', statusLabels.todo)}
      {renderTaskSection('in_progress', statusLabels.in_progress)}
      {renderTaskSection('done', statusLabels.done)}
    </>
  );
}

export default TaskList;
