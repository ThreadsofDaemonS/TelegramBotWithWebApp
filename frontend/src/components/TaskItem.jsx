/**
 * TaskItem component - Single task card
 */
import { useState } from 'react';

function TaskItem({ task, onUpdate, onDelete }) {
  const [isUpdating, setIsUpdating] = useState(false);

  const handleStatusChange = async (newStatus) => {
    if (isUpdating) return;
    
    setIsUpdating(true);
    try {
      await onUpdate(task.id, { status: newStatus });
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (isUpdating) return;
    
    if (window.confirm('Are you sure you want to delete this task?')) {
      setIsUpdating(true);
      try {
        await onDelete(task.id);
      } finally {
        setIsUpdating(false);
      }
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusEmoji = (status) => {
    switch (status) {
      case 'todo':
        return '⏳';
      case 'in_progress':
        return '🔄';
      case 'done':
        return '✅';
      default:
        return '⚪';
    }
  };

  const getNextStatus = (currentStatus) => {
    switch (currentStatus) {
      case 'todo':
        return 'in_progress';
      case 'in_progress':
        return 'done';
      case 'done':
        return 'todo';
      default:
        return 'todo';
    }
  };

  const getStatusButtonText = (currentStatus) => {
    switch (currentStatus) {
      case 'todo':
        return 'Start';
      case 'in_progress':
        return 'Complete';
      case 'done':
        return 'Reopen';
      default:
        return 'Update';
    }
  };

  return (
    <div className="task-item">
      <div className="task-header">
        <div className="task-title">
          {getStatusEmoji(task.status)} {task.title}
        </div>
        <div className={`task-priority ${task.priority}`}>
          {task.priority}
        </div>
      </div>

      {task.description && (
        <div className="task-description">{task.description}</div>
      )}

      <div className="task-footer">
        <div className="task-date">
          {task.deadline && `Due: ${formatDate(task.deadline)}`}
          {!task.deadline && `Created: ${formatDate(task.created_at)}`}
        </div>
        <div className="task-actions">
          <button
            className="task-action-btn"
            onClick={() => handleStatusChange(getNextStatus(task.status))}
            disabled={isUpdating}
          >
            {getStatusButtonText(task.status)}
          </button>
          <button
            className="task-action-btn delete"
            onClick={handleDelete}
            disabled={isUpdating}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

export default TaskItem;
