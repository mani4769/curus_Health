import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Chip,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Add,
  MoreVert,
  Edit,
  Delete,
  Group,
} from '@mui/icons-material';
import { Project } from '../types';
import api, { projectAPI, userAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const Projects: React.FC = () => {
  const { user } = useAuth();
  const [projects, setProjects] = useState<Project[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    status: 'Active',
    deadline: '',
  });

  const canCreateProject = user?.role === 'Admin' || user?.role === 'Manager';

  useEffect(() => {
    fetchProjects();
    fetchUsers();
  }, []);

  const fetchProjects = async () => {
    try {
  const response = await api.get('/api/projects');
      console.log('Projects API response:', response.data);
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
  const response = await api.get('/api/users');
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleOpenDialog = (project?: Project) => {
    if (project) {
      setEditingProject(project);
      setFormData({
        name: project.name,
        description: project.description,
        status: project.status || 'Active',
        deadline: project.deadline ? project.deadline.split('T')[0] : '',
      });
    } else {
      setEditingProject(null);
      setFormData({
        name: '',
        description: '',
        status: 'Active',
        deadline: '',
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingProject(null);
  };

  const handleSubmit = async () => {
    try {
      const projectData = {
        name: formData.name,
        description: formData.description,
        status: formData.status,
        deadline: formData.deadline,
      };

      if (editingProject) {
        await api.put(`/api/projects/${editingProject._id}`, projectData);
      } else {
        await api.post('/api/projects', projectData);
      }
      fetchProjects();
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving project:', error);
    }
  };

  const handleDelete = async (projectId: string) => {
    try {
  await api.delete(`/api/projects/${projectId}`);
      fetchProjects();
    } catch (error) {
      console.error('Error deleting project:', error);
    }
    setAnchorEl(null);
  };

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, project: Project) => {
    setAnchorEl(event.currentTarget);
    setSelectedProject(project);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedProject(null);
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Projects</Typography>
        {canCreateProject && (
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => handleOpenDialog()}
          >
            Create Project
          </Button>
        )}
      </Box>

      <Grid container spacing={3}>
        {projects.map((project) => (
          <Grid item xs={12} md={6} lg={4} key={project._id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start">
                  <Typography variant="h6" component="h2">
                    {project.name}
                  </Typography>
                  {canCreateProject && (
                    <IconButton
                      size="small"
                      onClick={(e) => handleMenuClick(e, project)}
                    >
                      <MoreVert />
                    </IconButton>
                  )}
                </Box>
                <Typography color="textSecondary" gutterBottom>
                  {project.description}
                </Typography>
                <Box mt={2}>
                  <Typography variant="body2" color="textSecondary">
                    Team: {project.team_members ? project.team_members.length : 0} members
                  </Typography>
                  {project.deadline && (
                    <Typography variant="body2" color="textSecondary">
                      Deadline: {new Date(project.deadline).toLocaleDateString()}
                    </Typography>
                  )}
                </Box>
                <Box mt={1}>
                  <Chip
                    label={project.status}
                    color={project.status === 'Active' ? 'success' : 'default'}
                    size="small"
                  />
                </Box>
              </CardContent>
              <CardActions>
                <Button size="small" startIcon={<Group />}>
                  View Team
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Actions Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => {
          if (selectedProject) {
            handleOpenDialog(selectedProject);
          }
          handleMenuClose();
        }}>
          <Edit sx={{ mr: 1 }} />
          Edit
        </MenuItem>
        <MenuItem onClick={() => {
          if (selectedProject) {
            handleDelete(selectedProject._id);
          }
        }}>
          <Delete sx={{ mr: 1 }} />
          Delete
        </MenuItem>
      </Menu>

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingProject ? 'Edit Project' : 'Create New Project'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Project Name"
            fullWidth
            variant="outlined"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Deadline"
            type="date"
            fullWidth
            variant="outlined"
            InputLabelProps={{ shrink: true }}
            value={formData.deadline}
            onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            select
            margin="dense"
            label="Status"
            fullWidth
            variant="outlined"
            value={formData.status}
            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
            sx={{ mb: 2 }}
          >
            <MenuItem value="Active">Active</MenuItem>
            <MenuItem value="Completed">Completed</MenuItem>
            <MenuItem value="On Hold">On Hold</MenuItem>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingProject ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Projects;
