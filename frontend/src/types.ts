// types.ts
export interface User {
  _id: string;
  username: string;
  email: string;
  role: string;
  created_at: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface SignupData {
  username: string;
  email: string;
  password: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

export interface Project {
  _id: string;
  name: string;
  description: string;
  status: string;
  start_date?: string;
  end_date?: string;
  deadline?: string;
  team_members: string[];
  created_by: string;
  created_at: string;
}

export interface Task {
  _id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  assigned_to: string;
  project_id: string;
  deadline: string;
  created_at: string;
  comments: Comment[];
}

export interface Comment {
  _id: string;
  text: string;
  author: string;
  created_at: string;
}

export interface DashboardData {
  total_projects: number;
  total_tasks: number;
  total_users: number;
  overdue_tasks: number;
  completion_rate: number;
  tasks_by_status: { [key: string]: number };
  recent_overdue_tasks: Task[];
}

export interface ReportData {
  tasks_by_status: { [key: string]: number };
  overdue_tasks: Task[];
  user_workload: { [key: string]: number };
}
