import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper,
  useTheme,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
} from 'recharts';
import {
  TrendingUp as TrendingIcon,
  Search as SearchIcon,
  Psychology as AIIcon,
  Description as DocumentIcon,
  Speed as PerformanceIcon,
  People as UsersIcon,
} from '@mui/icons-material';

// Mock analytics data
const mockAnalyticsData = {
  overview: {
    totalSearches: 12450,
    totalDocuments: 3200,
    aiQueries: 5600,
    activeUsers: 420,
    averageResponseTime: 0.8,
    successRate: 96.5,
  },
  searchTrends: [
    { date: '2024-01', searches: 800, ai_queries: 320 },
    { date: '2024-02', searches: 950, ai_queries: 380 },
    { date: '2024-03', searches: 1100, ai_queries: 450 },
    { date: '2024-04', searches: 1250, ai_queries: 520 },
    { date: '2024-05', searches: 1400, ai_queries: 600 },
    { date: '2024-06', searches: 1300, ai_queries: 580 },
  ],
  queryTypes: [
    { name: 'Semantic Search', value: 45, color: '#8884d8' },
    { name: 'Keyword Search', value: 30, color: '#82ca9d' },
    { name: 'AI Q&A', value: 15, color: '#ffc658' },
    { name: 'Summarization', value: 10, color: '#ff7300' },
  ],
  performanceMetrics: [
    { time: '00:00', response_time: 0.8, throughput: 100 },
    { time: '04:00', response_time: 0.7, throughput: 80 },
    { time: '08:00', response_time: 1.2, throughput: 200 },
    { time: '12:00', response_time: 1.5, throughput: 350 },
    { time: '16:00', response_time: 1.8, throughput: 400 },
    { time: '20:00', response_time: 1.1, throughput: 250 },
  ],
  documentCategories: [
    { category: 'Research Papers', count: 850 },
    { category: 'Technical Docs', count: 720 },
    { category: 'Business Reports', count: 650 },
    { category: 'Legal Documents', count: 480 },
    { category: 'Marketing Content', count: 320 },
    { category: 'Other', count: 180 },
  ],
};

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactElement;
  trend?: number;
  color?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  color = 'primary',
}) => {
  const theme = useTheme();

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ 
            color: typeof color === 'string' ? color : theme.palette.primary.main
          }}>
            {icon}
          </Box>
          {trend !== undefined && (
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              color: trend >= 0 ? 'success.main' : 'error.main' 
            }}>
              <TrendingIcon fontSize="small" />
              <Typography variant="caption" sx={{ ml: 0.5 }}>
                {trend >= 0 ? '+' : ''}{trend}%
              </Typography>
            </Box>
          )}
        </Box>
        
        <Typography variant="h4" component="div" sx={{ mb: 1, fontWeight: 'bold' }}>
          {value}
        </Typography>
        
        <Typography variant="h6" color="text.primary" sx={{ mb: 0.5 }}>
          {title}
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

const AnalyticsPage: React.FC = () => {
  const theme = useTheme();
  const { overview, searchTrends, queryTypes, performanceMetrics, documentCategories } = mockAnalyticsData;

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
          Analytics Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Comprehensive insights into your ConfluxAI system performance and usage patterns.
        </Typography>
      </Box>

      {/* Overview Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={2}>
          <MetricCard
            title="Total Searches"
            value={overview.totalSearches.toLocaleString()}
            icon={<SearchIcon />}
            trend={12.5}
            color="primary"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={2}>
          <MetricCard
            title="Documents"
            value={overview.totalDocuments.toLocaleString()}
            icon={<DocumentIcon />}
            trend={8.3}
            color="secondary"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={2}>
          <MetricCard
            title="AI Queries"
            value={overview.aiQueries.toLocaleString()}
            icon={<AIIcon />}
            trend={25.7}
            color="info"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={2}>
          <MetricCard
            title="Active Users"
            value={overview.activeUsers}
            icon={<UsersIcon />}
            trend={15.2}
            color="success"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={2}>
          <MetricCard
            title="Avg Response Time"
            value={`${overview.averageResponseTime}s`}
            icon={<PerformanceIcon />}
            trend={-5.8}
            color="warning"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={2}>
          <MetricCard
            title="Success Rate"
            value={`${overview.successRate}%`}
            icon={<TrendingIcon />}
            trend={2.1}
            color="success"
          />
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Search Trends */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Search Activity Trends
            </Typography>
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={searchTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area 
                  type="monotone" 
                  dataKey="searches" 
                  stackId="1"
                  stroke={theme.palette.primary.main} 
                  fill={theme.palette.primary.light}
                  name="Total Searches"
                />
                <Area 
                  type="monotone" 
                  dataKey="ai_queries" 
                  stackId="1"
                  stroke={theme.palette.secondary.main} 
                  fill={theme.palette.secondary.light}
                  name="AI Queries"
                />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Query Types Distribution */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Query Types Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={350}>
              <PieChart>
                <Pie
                  data={queryTypes}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {queryTypes.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Performance Metrics */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Performance (24h)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Line 
                  yAxisId="left"
                  type="monotone" 
                  dataKey="response_time" 
                  stroke={theme.palette.warning.main} 
                  strokeWidth={2}
                  name="Response Time (s)"
                />
                <Line 
                  yAxisId="right"
                  type="monotone" 
                  dataKey="throughput" 
                  stroke={theme.palette.success.main} 
                  strokeWidth={2}
                  name="Throughput (req/min)"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Document Categories */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Document Categories
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={documentCategories} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="category" type="category" width={100} />
                <Tooltip />
                <Bar 
                  dataKey="count" 
                  fill={theme.palette.primary.main}
                />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Additional Insights */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Key Insights
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Box sx={{ p: 2, borderLeft: `4px solid ${theme.palette.primary.main}` }}>
              <Typography variant="subtitle1" fontWeight="600">
                Peak Usage Hours
              </Typography>
              <Typography variant="body2" color="text.secondary">
                System usage peaks between 12:00-16:00, with average response time of 1.5s
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ p: 2, borderLeft: `4px solid ${theme.palette.secondary.main}` }}>
              <Typography variant="subtitle1" fontWeight="600">
                AI Adoption Growth
              </Typography>
              <Typography variant="body2" color="text.secondary">
                AI-powered features show 25.7% month-over-month growth in usage
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ p: 2, borderLeft: `4px solid ${theme.palette.success.main}` }}>
              <Typography variant="subtitle1" fontWeight="600">
                Document Processing
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Research papers constitute 26.6% of all indexed documents
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default AnalyticsPage;
