import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Switch,
  FormControlLabel,
  Slider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Card,
  CardContent,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Security as SecurityIcon,
  Palette as ThemeIcon,
  Notifications as NotificationsIcon,
  Speed as PerformanceIcon,
  Psychology as AIIcon,
} from '@mui/icons-material';

interface SettingsState {
  theme: 'light' | 'dark' | 'auto';
  notifications: {
    email: boolean;
    push: boolean;
    searchAlerts: boolean;
    systemUpdates: boolean;
  };
  search: {
    enableSemanticSearch: boolean;
    enableHybridSearch: boolean;
    maxResults: number;
    confidenceThreshold: number;
    autoSave: boolean;
  };
  ai: {
    enableRealTimeProcessing: boolean;
    summaryLength: 'short' | 'medium' | 'long';
    languageModel: 'gpt-3.5' | 'gpt-4' | 'claude';
    responseStyle: 'formal' | 'casual' | 'technical';
  };
  performance: {
    cacheEnabled: boolean;
    maxConcurrentRequests: number;
    requestTimeout: number;
  };
  privacy: {
    dataRetention: number; // days
    shareAnalytics: boolean;
    trackUsage: boolean;
  };
}

const defaultSettings: SettingsState = {
  theme: 'auto',
  notifications: {
    email: true,
    push: false,
    searchAlerts: true,
    systemUpdates: true,
  },
  search: {
    enableSemanticSearch: true,
    enableHybridSearch: true,
    maxResults: 20,
    confidenceThreshold: 0.5,
    autoSave: true,
  },
  ai: {
    enableRealTimeProcessing: false,
    summaryLength: 'medium',
    languageModel: 'gpt-3.5',
    responseStyle: 'formal',
  },
  performance: {
    cacheEnabled: true,
    maxConcurrentRequests: 10,
    requestTimeout: 30,
  },
  privacy: {
    dataRetention: 90,
    shareAnalytics: false,
    trackUsage: true,
  },
};

const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<SettingsState>(defaultSettings);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  const [hasChanges, setHasChanges] = useState(false);

  const handleSettingChange = (
    section: keyof SettingsState,
    key: string,
    value: any
  ) => {
    setSettings(prev => {
      const currentSection = prev[section] as Record<string, any>;
      return {
        ...prev,
        [section]: {
          ...currentSection,
          [key]: value,
        },
      };
    });
    setHasChanges(true);
  };

  const handleSave = async () => {
    try {
      // In a real app, this would save to API
      console.log('Saving settings:', settings);
      setSnackbar({ open: true, message: 'Settings saved successfully!', severity: 'success' });
      setHasChanges(false);
    } catch (error) {
      setSnackbar({ open: true, message: 'Failed to save settings', severity: 'error' });
    }
  };

  const handleReset = () => {
    setSettings(defaultSettings);
    setHasChanges(false);
    setSnackbar({ open: true, message: 'Settings reset to defaults', severity: 'success' });
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
          Settings
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Configure ConfluxAI to match your preferences and workflow.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Theme & Appearance */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <ThemeIcon sx={{ mr: 2, color: 'primary.main' }} />
                <Typography variant="h6">Theme & Appearance</Typography>
              </Box>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Theme</InputLabel>
                <Select
                  value={settings.theme}
                  onChange={(e) => handleSettingChange('theme', 'theme', e.target.value)}
                  label="Theme"
                >
                  <MenuItem value="light">Light</MenuItem>
                  <MenuItem value="dark">Dark</MenuItem>
                  <MenuItem value="auto">Auto (System)</MenuItem>
                </Select>
              </FormControl>
            </CardContent>
          </Card>
        </Grid>

        {/* Notifications */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <NotificationsIcon sx={{ mr: 2, color: 'secondary.main' }} />
                <Typography variant="h6">Notifications</Typography>
              </Box>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.email}
                    onChange={(e) => handleSettingChange('notifications', 'email', e.target.checked)}
                  />
                }
                label="Email Notifications"
                sx={{ display: 'block', mb: 1 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.push}
                    onChange={(e) => handleSettingChange('notifications', 'push', e.target.checked)}
                  />
                }
                label="Push Notifications"
                sx={{ display: 'block', mb: 1 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.searchAlerts}
                    onChange={(e) => handleSettingChange('notifications', 'searchAlerts', e.target.checked)}
                  />
                }
                label="Search Alerts"
                sx={{ display: 'block', mb: 1 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.systemUpdates}
                    onChange={(e) => handleSettingChange('notifications', 'systemUpdates', e.target.checked)}
                  />
                }
                label="System Updates"
                sx={{ display: 'block' }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Search Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SettingsIcon sx={{ mr: 2, color: 'info.main' }} />
                <Typography variant="h6">Search Settings</Typography>
              </Box>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.search.enableSemanticSearch}
                    onChange={(e) => handleSettingChange('search', 'enableSemanticSearch', e.target.checked)}
                  />
                }
                label="Enable Semantic Search"
                sx={{ display: 'block', mb: 2 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.search.enableHybridSearch}
                    onChange={(e) => handleSettingChange('search', 'enableHybridSearch', e.target.checked)}
                  />
                }
                label="Enable Hybrid Search"
                sx={{ display: 'block', mb: 2 }}
              />
              
              <Typography gutterBottom>Max Results: {settings.search.maxResults}</Typography>
              <Slider
                value={settings.search.maxResults}
                onChange={(_, value) => handleSettingChange('search', 'maxResults', value)}
                min={10}
                max={100}
                step={10}
                marks
                sx={{ mb: 2 }}
              />
              
              <Typography gutterBottom>
                Confidence Threshold: {Math.round(settings.search.confidenceThreshold * 100)}%
              </Typography>
              <Slider
                value={settings.search.confidenceThreshold}
                onChange={(_, value) => handleSettingChange('search', 'confidenceThreshold', value)}
                min={0}
                max={1}
                step={0.1}
                marks
                valueLabelDisplay="auto"
                valueLabelFormat={(value) => `${Math.round(value * 100)}%`}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* AI Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AIIcon sx={{ mr: 2, color: 'success.main' }} />
                <Typography variant="h6">AI Settings</Typography>
              </Box>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.ai.enableRealTimeProcessing}
                    onChange={(e) => handleSettingChange('ai', 'enableRealTimeProcessing', e.target.checked)}
                  />
                }
                label="Real-time AI Processing"
                sx={{ display: 'block', mb: 2 }}
              />
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Summary Length</InputLabel>
                <Select
                  value={settings.ai.summaryLength}
                  onChange={(e) => handleSettingChange('ai', 'summaryLength', e.target.value)}
                  label="Summary Length"
                >
                  <MenuItem value="short">Short (50-100 words)</MenuItem>
                  <MenuItem value="medium">Medium (100-200 words)</MenuItem>
                  <MenuItem value="long">Long (200-300 words)</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Language Model</InputLabel>
                <Select
                  value={settings.ai.languageModel}
                  onChange={(e) => handleSettingChange('ai', 'languageModel', e.target.value)}
                  label="Language Model"
                >
                  <MenuItem value="gpt-3.5">GPT-3.5 Turbo</MenuItem>
                  <MenuItem value="gpt-4">GPT-4</MenuItem>
                  <MenuItem value="claude">Claude</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth>
                <InputLabel>Response Style</InputLabel>
                <Select
                  value={settings.ai.responseStyle}
                  onChange={(e) => handleSettingChange('ai', 'responseStyle', e.target.value)}
                  label="Response Style"
                >
                  <MenuItem value="formal">Formal</MenuItem>
                  <MenuItem value="casual">Casual</MenuItem>
                  <MenuItem value="technical">Technical</MenuItem>
                </Select>
              </FormControl>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <PerformanceIcon sx={{ mr: 2, color: 'warning.main' }} />
                <Typography variant="h6">Performance</Typography>
              </Box>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.performance.cacheEnabled}
                    onChange={(e) => handleSettingChange('performance', 'cacheEnabled', e.target.checked)}
                  />
                }
                label="Enable Caching"
                sx={{ display: 'block', mb: 2 }}
              />
              
              <Typography gutterBottom>
                Max Concurrent Requests: {settings.performance.maxConcurrentRequests}
              </Typography>
              <Slider
                value={settings.performance.maxConcurrentRequests}
                onChange={(_, value) => handleSettingChange('performance', 'maxConcurrentRequests', value)}
                min={1}
                max={20}
                step={1}
                marks
                sx={{ mb: 2 }}
              />
              
              <Typography gutterBottom>
                Request Timeout: {settings.performance.requestTimeout}s
              </Typography>
              <Slider
                value={settings.performance.requestTimeout}
                onChange={(_, value) => handleSettingChange('performance', 'requestTimeout', value)}
                min={10}
                max={120}
                step={10}
                marks
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Privacy Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SecurityIcon sx={{ mr: 2, color: 'error.main' }} />
                <Typography variant="h6">Privacy & Security</Typography>
              </Box>
              
              <Typography gutterBottom>
                Data Retention: {settings.privacy.dataRetention} days
              </Typography>
              <Slider
                value={settings.privacy.dataRetention}
                onChange={(_, value) => handleSettingChange('privacy', 'dataRetention', value)}
                min={7}
                max={365}
                step={7}
                marks={[
                  { value: 7, label: '1w' },
                  { value: 30, label: '1m' },
                  { value: 90, label: '3m' },
                  { value: 365, label: '1y' },
                ]}
                sx={{ mb: 2 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.privacy.shareAnalytics}
                    onChange={(e) => handleSettingChange('privacy', 'shareAnalytics', e.target.checked)}
                  />
                }
                label="Share Anonymous Analytics"
                sx={{ display: 'block', mb: 1 }}
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.privacy.trackUsage}
                    onChange={(e) => handleSettingChange('privacy', 'trackUsage', e.target.checked)}
                  />
                }
                label="Track Usage Statistics"
                sx={{ display: 'block' }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Action Buttons */}
      <Paper sx={{ p: 3, mt: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Button
          variant="outlined"
          onClick={handleReset}
          disabled={!hasChanges}
        >
          Reset to Defaults
        </Button>
        
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={!hasChanges}
          sx={{ minWidth: 120 }}
        >
          Save Changes
        </Button>
      </Paper>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
      >
        <Alert
          onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default SettingsPage;
