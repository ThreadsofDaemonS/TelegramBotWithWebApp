/**
 * App component - Main application component
 */
import { useEffect, useState } from 'react';
import './styles/App.css';
import TaskList from './components/TaskList';
import AddTask from './components/AddTask';
import { tasksAPI } from './services/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddTask, setShowAddTask] = useState(false);

  // Initialize Telegram Web App
  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    
    console.log('[App] Telegram WebApp Debug Info:');
    console.log('  - WebApp available:', !!tg);
    console.log('  - initData:', tg?.initData || '(empty)');
    console.log('  - initDataUnsafe:', tg?.initDataUnsafe);
    console.log('  - version:', tg?.version);
    console.log('  - platform:', tg?.platform);
    console.log('  - colorScheme:', tg?.colorScheme);
    
    if (tg) {
      tg.ready();
      tg.expand();
      
      // Set theme colors
      document.body.style.backgroundColor = tg.themeParams.bg_color || '#ffffff';
      document.body.style.color = tg.themeParams.text_color || '#000000';
      
      console.log('[App] ✓ Telegram WebApp initialized successfully');
    } else {
      console.warn('[App] ⚠️ Not running inside Telegram WebApp!');
      console.warn('[App] The app should be opened from Telegram bot.');
    }
  }, []);

  // Fetch tasks and stats
  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('[App] Fetching tasks and stats...');
      
      const [tasksResponse, statsResponse] = await Promise.all([
        tasksAPI.getTasks(),
        tasksAPI.getStats(),
      ]);
      
      setTasks(tasksResponse.data);
      setStats(statsResponse.data);
      
      console.log('[App] ✓ Data loaded successfully:', {
        tasksCount: tasksResponse.data.length,
        stats: statsResponse.data
      });
    } catch (err) {
      console.error('[App] ✗ Error fetching data:', err);
      
      // Create detailed error message
      let errorMessage = 'Failed to load tasks. ';
      
      if (err.response?.status === 401) {
        errorMessage += 'Authentication failed. Make sure you opened the app from Telegram.';
      } else if (err.request && !err.response) {
        errorMessage += 'Cannot connect to server. Check your internet connection and API URL configuration.';
      } else {
        errorMessage += 'Please try again.';
      }
      
      setError(errorMessage);
      
      // Show error in Telegram
      const tg = window.Telegram?.WebApp;
      if (tg) {
        tg.showAlert(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Handle task creation
  const handleCreateTask = async (taskData) => {
    try {
      await tasksAPI.createTask(taskData);
      setShowAddTask(false);
      
      // Show success feedback
      const tg = window.Telegram?.WebApp;
      if (tg) {
        tg.HapticFeedback?.notificationOccurred('success');
      }
      
      // Refresh data
      await fetchData();
    } catch (err) {
      console.error('Error creating task:', err);
      
      const tg = window.Telegram?.WebApp;
      if (tg) {
        tg.showAlert('Failed to create task. Please try again.');
        tg.HapticFeedback?.notificationOccurred('error');
      }
    }
  };

  // Handle task update
  const handleUpdateTask = async (taskId, updateData) => {
    try {
      await tasksAPI.updateTask(taskId, updateData);
      
      // Show success feedback
      const tg = window.Telegram?.WebApp;
      if (tg) {
        tg.HapticFeedback?.notificationOccurred('success');
      }
      
      // Refresh data
      await fetchData();
    } catch (err) {
      console.error('Error updating task:', err);
      
      const tg = window.Telegram?.WebApp;
      if (tg) {
        tg.showAlert('Failed to update task. Please try again.');
        tg.HapticFeedback?.notificationOccurred('error');
      }
    }
  };

  // Handle task deletion
  const handleDeleteTask = async (taskId) => {
    try {
      await tasksAPI.deleteTask(taskId);
      
      // Show success feedback
      const tg = window.Telegram?.WebApp;
      if (tg) {
        tg.HapticFeedback?.notificationOccurred('success');
      }
      
      // Refresh data
      await fetchData();
    } catch (err) {
      console.error('Error deleting task:', err);
      
      const tg = window.Telegram?.WebApp;
      if (tg) {
        tg.showAlert('Failed to delete task. Please try again.');
        tg.HapticFeedback?.notificationOccurred('error');
      }
    }
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading tasks...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">{error}</div>
        <button onClick={fetchData} className="add-task-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="header">
        <h1>📝 Task Tracker</h1>
      </div>

      {stats && (
        <div className="stats">
          <div className="stat-card">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.todo}</div>
            <div className="stat-label">To Do</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.in_progress}</div>
            <div className="stat-label">In Progress</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.done}</div>
            <div className="stat-label">Done</div>
          </div>
        </div>
      )}

      <button
        className="add-task-button"
        onClick={() => setShowAddTask(true)}
      >
        <span>➕</span>
        <span>Add New Task</span>
      </button>

      <TaskList
        tasks={tasks}
        onUpdate={handleUpdateTask}
        onDelete={handleDeleteTask}
      />

      {showAddTask && (
        <AddTask
          onClose={() => setShowAddTask(false)}
          onSubmit={handleCreateTask}
        />
      )}
    </div>
  );
}

export default App;
