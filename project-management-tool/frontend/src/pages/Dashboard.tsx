import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  Paper,
} from '@mui/material';
import {
  TrendingUp,
  Assignment,
  FolderOpen,
  People,
  Warning,
} from '@mui/icons-material';
import { DashboardData } from '../types';
import { reportAPI } from '../services/api';

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await reportAPI.getDashboard();
        console.log('Dashboard API response:', data);
        console.log('Tasks by status:', data.tasks_by_status);
        setDashboardData(data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return <LinearProgress />;
  }

  if (!dashboardData) {
    return <Typography>Error loading dashboard data</Typography>;
  }

  const statCards = [
    {
      title: 'Total Projects',
      value: dashboardData.total_projects || 0,
      icon: <FolderOpen fontSize="large" />,
      color: '#1976d2',
    },
    {
      title: 'Total Tasks',
      value: dashboardData.total_tasks || 0,
      icon: <Assignment fontSize="large" />,
      color: '#388e3c',
    },
    {
      title: 'Team Members',
      value: dashboardData.total_users || 0,
      icon: <People fontSize="large" />,
      color: '#f57c00',
    },
    {
      title: 'Overdue Tasks',
      value: dashboardData.overdue_tasks || 0,
      icon: <Warning fontSize="large" />,
      color: '#d32f2f',
    },
  ];

  return (
    <Box sx={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      p: 3
    }}>
      <Typography variant="h4" gutterBottom sx={{
        color: 'white',
        fontWeight: 'bold',
        textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
        textAlign: 'center',
        mb: 4
      }}>
        📊 Project Management Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {statCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
              borderRadius: 3,
              boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s ease-in-out',
              '&:hover': {
                transform: 'translateY(-5px)',
                boxShadow: '0 12px 40px rgba(0,0,0,0.2)'
              }
            }}>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="textSecondary" gutterBottom sx={{ fontWeight: 500 }}>
                      {card.title}
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: card.color }}>
                      {card.value}
                    </Typography>
                  </Box>
                  <Box sx={{ color: card.color, fontSize: '3rem' }}>
                    {card.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Completion Rate */}
        <Grid item xs={12} md={6}>
          <Card sx={{
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
            transition: 'transform 0.3s ease-in-out',
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 12px 40px rgba(0,0,0,0.2)'
            }
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#333' }}>
                📈 Project Completion Rate
              </Typography>
              <Box display="flex" alignItems="center" sx={{ mb: 2 }}>
                <TrendingUp sx={{ mr: 1, color: 'success.main' }} />
                <Typography variant="h4" color="success.main" sx={{ fontWeight: 'bold' }}>
                  {dashboardData.completion_rate || 0}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={dashboardData.completion_rate || 0}
                sx={{
                  height: 12,
                  borderRadius: 6,
                  background: 'rgba(0,0,0,0.1)',
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 6,
                    background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)'
                  }
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Task Status Distribution */}
        <Grid item xs={12} md={6}>
          <Card sx={{
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
            transition: 'transform 0.3s ease-in-out',
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 12px 40px rgba(0,0,0,0.2)'
            }
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#333' }}>
                📋 Task Status Distribution
              </Typography>
              <Box>
                {dashboardData.tasks_by_status && Object.entries(dashboardData.tasks_by_status).map(([status, count]) => (
                  <Box key={status} display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                    <Typography sx={{ fontWeight: 500 }}>{status}</Typography>
                    <Chip
                      label={count}
                      color={
                        status === 'Done' ? 'success' :
                        status === 'In Progress' ? 'warning' : 'default'
                      }
                      size="small"
                      sx={{
                        fontWeight: 'bold',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                      }}
                    />
                  </Box>
                ))}
                {!dashboardData.tasks_by_status && (
                  <Typography color="textSecondary">
                    No task status data available
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Overdue Tasks */}
        <Grid item xs={12}>
          <Paper sx={{
            p: 3,
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
            transition: 'transform 0.3s ease-in-out',
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 12px 40px rgba(0,0,0,0.2)'
            }
          }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#333' }}>
              ⚠️ Recent Overdue Tasks
            </Typography>
            {dashboardData.recent_overdue_tasks && dashboardData.recent_overdue_tasks.length > 0 ? (
              <List>
                {dashboardData.recent_overdue_tasks.map((task) => (
                  <ListItem key={task._id} divider sx={{
                    borderRadius: 2,
                    mb: 1,
                    background: 'rgba(255, 255, 255, 0.8)',
                    '&:hover': {
                      background: 'rgba(255, 255, 255, 0.9)'
                    }
                  }}>
                    <ListItemText
                      primary={<Typography sx={{ fontWeight: 'bold' }}>{task.title}</Typography>}
                      secondary={`Deadline: ${new Date(task.deadline || '').toLocaleDateString()} | Status: ${task.status}`}
                    />
                    <Chip
                      label="Overdue"
                      color="error"
                      size="small"
                      sx={{
                        fontWeight: 'bold',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                      }}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography color="textSecondary" sx={{ textAlign: 'center', py: 2 }}>
                🎉 No overdue tasks! Great job!
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
