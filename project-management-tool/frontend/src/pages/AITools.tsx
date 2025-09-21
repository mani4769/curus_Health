import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Chip,
  FormControlLabel,
  Checkbox,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
  Grid,
} from '@mui/material';
import {
  SmartToy,
  AutoStories,
  AddTask,
  Psychology,
} from '@mui/icons-material';
import { Project } from '../types';
import api from '../services/api';

const AITools: React.FC = () => {
  const [projectDescription, setProjectDescription] = useState('');
  const [selectedProject, setSelectedProject] = useState('');
  const [createTasks, setCreateTasks] = useState(false);
  const [userStories, setUserStories] = useState<string[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await api.get('/api/projects');
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const handleGenerateStories = async () => {
    if (!projectDescription.trim()) {
      setError('Please enter a project description');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');
    setUserStories([]);

    try {
      const response = await api.post('/api/ai/generate-user-stories', {
        projectDescription: projectDescription.trim(),
        projectId: selectedProject || undefined,
        createTasks,
      });

      setUserStories(response.data.user_stories);
      setSuccess(`Generated ${response.data.count} user stories successfully!`);

      if (createTasks && response.data.count > 0) {
        setSuccess(prev => prev + ' Tasks have been created automatically.');
      }
    } catch (error: any) {
      console.error('Error generating user stories:', error);
      setError(error.response?.data?.error || 'Failed to generate user stories. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setProjectDescription('');
    setSelectedProject('');
    setCreateTasks(false);
    setUserStories([]);
    setError('');
    setSuccess('');
  };

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
        🤖 AI-Powered User Story Generator
      </Typography>

      <Grid container spacing={3}>
        {/* Input Section */}
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
              <Box display="flex" alignItems="center" mb={2}>
                <Psychology sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                  Generate User Stories
                </Typography>
              </Box>

              <TextField
                label="Project Description"
                multiline
                rows={6}
                fullWidth
                value={projectDescription}
                onChange={(e) => setProjectDescription(e.target.value)}
                placeholder="Describe your project in plain English. For example: 'An ecommerce website where customers can browse products, add to cart, and make payments online. Admin should manage products and view orders.'"
                sx={{
                  mb: 2,
                  '& .MuiOutlinedInput-root': {
                    background: 'rgba(255,255,255,0.8)',
                    borderRadius: 2
                  }
                }}
              />

              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Link to Project (Optional)</InputLabel>
                <Select
                  value={selectedProject}
                  label="Link to Project (Optional)"
                  onChange={(e) => setSelectedProject(e.target.value)}
                  sx={{
                    background: 'rgba(255,255,255,0.8)',
                    borderRadius: 2
                  }}
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  {projects.map((project) => (
                    <MenuItem key={project._id} value={project._id}>
                      {project.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControlLabel
                control={
                  <Checkbox
                    checked={createTasks}
                    onChange={(e) => setCreateTasks(e.target.checked)}
                    color="primary"
                  />
                }
                label="Automatically create tasks from user stories"
                sx={{ mb: 2 }}
              />

              <Box display="flex" gap={2}>
                <Button
                  variant="contained"
                  onClick={handleGenerateStories}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <SmartToy />}
                  sx={{
                    background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                    boxShadow: '0 3px 5px 2px rgba(33, 150, 243, .3)',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #2196F3 60%, #21CBF3 100%)',
                    }
                  }}
                >
                  {loading ? 'Generating...' : 'Generate Stories'}
                </Button>

                <Button
                  variant="outlined"
                  onClick={handleClear}
                  disabled={loading}
                  sx={{
                    borderColor: 'rgba(255,255,255,0.3)',
                    color: 'white',
                    '&:hover': {
                      borderColor: 'white',
                      background: 'rgba(255,255,255,0.1)'
                    }
                  }}
                >
                  Clear
                </Button>
              </Box>

              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}

              {success && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  {success}
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Output Section */}
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
              <Box display="flex" alignItems="center" mb={2}>
                <AutoStories sx={{ mr: 1, color: 'secondary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                  Generated User Stories
                </Typography>
                {userStories.length > 0 && (
                  <Chip
                    label={`${userStories.length} stories`}
                    color="primary"
                    size="small"
                    sx={{ ml: 'auto' }}
                  />
                )}
              </Box>

              {userStories.length === 0 ? (
                <Box
                  display="flex"
                  flexDirection="column"
                  alignItems="center"
                  justifyContent="center"
                  sx={{ py: 4, color: 'text.secondary' }}
                >
                  <SmartToy sx={{ fontSize: 48, mb: 2, opacity: 0.5 }} />
                  <Typography variant="body1" textAlign="center">
                    Enter a project description and click "Generate Stories" to see AI-generated user stories here.
                  </Typography>
                </Box>
              ) : (
                <List sx={{ maxHeight: 400, overflow: 'auto' }}>
                  {userStories.map((story, index) => (
                    <ListItem key={index} divider sx={{
                      borderRadius: 2,
                      mb: 1,
                      background: 'rgba(33, 150, 243, 0.05)',
                      '&:hover': {
                        background: 'rgba(33, 150, 243, 0.1)'
                      }
                    }}>
                      <ListItemText
                        primary={
                          <Typography variant="body1" sx={{ fontWeight: 500 }}>
                            {story}
                          </Typography>
                        }
                        secondary={
                          <Box display="flex" alignItems="center" mt={1}>
                            <AddTask sx={{ mr: 0.5, fontSize: 16 }} />
                            <Typography variant="caption" color="text.secondary">
                              Story {index + 1}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Info Section */}
      <Card sx={{
        mt: 3,
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: 3,
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)'
      }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#333' }}>
            💡 How It Works
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            This AI-powered tool uses GROQ's fast inference API with the Mixtral language model to generate detailed user stories from your project descriptions. Each story follows the standard format: "As a [role], I want to [action], so that [benefit]."
          </Typography>
          <Typography variant="body2" color="text.secondary">
            <strong>Features:</strong> Link stories to projects, automatically create tasks, cinematic UI with smooth animations.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default AITools;
