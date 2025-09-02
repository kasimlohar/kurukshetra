import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Tooltip,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  Description as DocumentIcon,
  TrendingUp as TrendingIcon,
  Memory as AIIcon,
  Speed as PerformanceIcon,
  Refresh as RefreshIcon,
  CloudUpload as UploadIcon,
  Psychology as BrainIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../services/api';

// Mock data for development
const mockSystemStatus = {
  services: {
    search: { status: 'healthy', response_time: 45 },
    ai: { status: 'healthy', response_time: 120 },
    indexing: { status: 'healthy', response_time: 30 },
    knowledge_graph: { status: 'healthy', response_time: 80 },
  },
  documents: {
    total: 1247,
    indexed: 1230,
    pending: 17,
  },
  ai_metrics: {
    total_queries: 3456,
    successful_responses: 3298,
    average_confidence: 0.82,
  },
  recent_activity: [
    { type: 'search', query: 'machine learning algorithms', time: '2 minutes ago' },
    { type: 'upload', filename: 'research_paper.pdf', time: '5 minutes ago' },
    { type: 'ai', query: 'summarize quarterly report', time: '8 minutes ago' },
  ],
};

const mockPerformanceData = [
  { time: '00:00', searches: 12, ai_requests: 8 },
  { time: '04:00', searches: 8, ai_requests: 5 },
  { time: '08:00', searches: 45, ai_requests: 32 },
  { time: '12:00', searches: 78, ai_requests: 56 },
  { time: '16:00', searches: 92, ai_requests: 71 },
  { time: '20:00', searches: 34, ai_requests: 28 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

interface DashboardCardProps {
  title: string;
  value: string | number;
  icon: React.ReactElement;
  subtitle?: string;
  color?: string;
  action?: () => void;
  actionLabel?: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  value,
  icon,
  subtitle,
  color = 'primary',
  action,
  actionLabel,
}) => {
  const theme = useTheme();
  
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 2,
            color: theme.palette[color as keyof typeof theme.palette]?.main || color 
          }}>
            {icon}
            <Typography variant="h6" component="div">
              {title}
            </Typography>
          </Box>
          {action && (
            <Tooltip title={actionLabel || 'Action'}>
              <IconButton size="small" onClick={action}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          )}
        </Box>
        
        <Typography variant="h3" component="div" sx={{ mb: 1, fontWeight: 'bold' }}>
          {value}
        </Typography>
        
        {subtitle && (
          <Typography variant="body2" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

const Dashboard: React.FC = () => {
  const theme = useTheme();
  
  // In a real app, these would be actual API calls
  const { data: systemStatus, isLoading: statusLoading, refetch: refetchStatus } = useQuery({
    queryKey: ['systemStatus'],
    queryFn: () => apiService.getSystemStatus(),
    refetchInterval: 30000, // Refetch every 30 seconds
    initialData: mockSystemStatus,
  });

  const { data: analytics, isLoading: analyticsLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => apiService.getAnalytics(),
    refetchInterval: 60000, // Refetch every minute
  });

  const getServiceStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return '#4caf50';
      case 'warning': return '#ff9800';
      case 'error': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  const handleQuickSearch = () => {
    // Navigate to search page or open search dialog
    window.location.href = '/search';
  };

  const handleUploadDocs = () => {
    // Navigate to upload page or open upload dialog
    console.log('Opening upload dialog...');
  };

  if (statusLoading) {
    return (
      <Box sx={{ width: '100%' }}>
        <LinearProgress />
        <Typography sx={{ mt: 2, textAlign: 'center' }}>Loading dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome to ConfluxAI. Monitor your AI-powered document search system.
        </Typography>
      </Box>

      {/* Quick Actions */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Button
              variant="contained"
              fullWidth
              startIcon={<SearchIcon />}
              onClick={handleQuickSearch}
              sx={{ py: 2 }}
            >
              Quick Search
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<UploadIcon />}
              onClick={handleUploadDocs}
              sx={{ py: 2 }}
            >
              Upload Documents
            </Button>
          </Grid>
        </Grid>
      </Box>

      {/* System Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Total Documents"
            value={systemStatus?.documents?.total || 0}
            icon={<DocumentIcon />}
            subtitle={`${systemStatus?.documents?.indexed || 0} indexed, ${systemStatus?.documents?.pending || 0} pending`}
            color="primary"
            action={refetchStatus}
            actionLabel="Refresh"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="AI Queries Today"
            value={systemStatus?.ai_metrics?.total_queries || 0}
            icon={<BrainIcon />}
            subtitle={`${Math.round((systemStatus?.ai_metrics?.successful_responses / systemStatus?.ai_metrics?.total_queries) * 100) || 0}% success rate`}
            color="secondary"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Avg. Confidence"
            value={`${Math.round((systemStatus?.ai_metrics?.average_confidence || 0) * 100)}%`}
            icon={<TrendingIcon />}
            subtitle="AI response confidence"
            color="success"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="System Health"
            value="Excellent"
            icon={<PerformanceIcon />}
            subtitle="All services operational"
            color="info"
          />
        </Grid>
      </Grid>

      {/* Service Status and Recent Activity */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Service Status */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Service Status
              </Typography>
              <List>
                {Object.entries(systemStatus?.services || {}).map(([service, data]: [string, any]) => (
                  <ListItem key={service} divider>
                    <ListItemIcon>
                      <Box
                        sx={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          backgroundColor: getServiceStatusColor(data.status),
                        }}
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="body1" sx={{ textTransform: 'capitalize' }}>
                            {service.replace('_', ' ')}
                          </Typography>
                          <Chip
                            label={`${data.response_time}ms`}
                            size="small"
                            variant="outlined"
                          />
                        </Box>
                      }
                      secondary={`Status: ${data.status}`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <List>
                {(systemStatus?.recent_activity || []).map((activity: any, index: number) => (
                  <ListItem key={index} divider>
                    <ListItemIcon>
                      {activity.type === 'search' && <SearchIcon color="primary" />}
                      {activity.type === 'upload' && <UploadIcon color="secondary" />}
                      {activity.type === 'ai' && <AIIcon color="info" />}
                    </ListItemIcon>
                    <ListItemText
                      primary={activity.query || activity.filename}
                      secondary={activity.time}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Performance Charts */}
      <Grid container spacing={3}>
        {/* Activity Timeline */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Activity Timeline (24h)
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={mockPerformanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <RechartsTooltip />
                  <Line 
                    type="monotone" 
                    dataKey="searches" 
                    stroke={theme.palette.primary.main} 
                    strokeWidth={2}
                    name="Searches"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="ai_requests" 
                    stroke={theme.palette.secondary.main} 
                    strokeWidth={2}
                    name="AI Requests"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Service Usage Distribution */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Service Usage
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Search', value: 45 },
                      { name: 'AI/Q&A', value: 30 },
                      { name: 'Summarization', value: 15 },
                      { name: 'Upload', value: 10 },
                    ]}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {mockPerformanceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
