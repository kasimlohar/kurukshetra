import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Tooltip,
  IconButton,
  Fab,
  Drawer,
  FormControlLabel,
  Switch,
  Slider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Snackbar,
  Badge,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  ExpandMore as ExpandMoreIcon,
  Psychology as AIIcon,
  Description as DocumentIcon,
  TrendingUp as TrendingIcon,
  Share as ShareIcon,
  BookmarkBorder as BookmarkIcon,
  Refresh as RefreshIcon,
  Settings as SettingsIcon,
  QuestionAnswer as QAIcon,
  Summarize as SummarizeIcon,
  AccountTree as GraphIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useWebSocket } from '../hooks/useWebSocket';
import { apiService, SearchRequest, SearchResult } from '../services/api';

interface SearchFilters {
  fileTypes: string[];
  dateRange: [number, number];
  confidenceThreshold: number;
  enableSemanticSearch: boolean;
  enableHybridSearch: boolean;
  maxResults: number;
}

interface SearchPageState {
  query: string;
  filters: SearchFilters;
  searchHistory: string[];
  selectedAIService: string;
  isRealTimeSearch: boolean;
  showFilters: boolean;
  bookmarkedResults: string[];
}

const defaultFilters: SearchFilters = {
  fileTypes: [],
  dateRange: [0, 100],
  confidenceThreshold: 0.5,
  enableSemanticSearch: true,
  enableHybridSearch: true,
  maxResults: 20,
};

const SearchPage: React.FC = () => {
  const theme = useTheme();
  const queryClient = useQueryClient();
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Component state
  const [state, setState] = useState<SearchPageState>({
    query: '',
    filters: defaultFilters,
    searchHistory: [],
    selectedAIService: 'search',
    isRealTimeSearch: false,
    showFilters: false,
    bookmarkedResults: [],
  });

  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' as 'info' | 'success' | 'warning' | 'error' });

  // WebSocket for real-time search
  const { isConnected, progress, subscribe, unsubscribe } = useWebSocket();

  // Search mutation
  const searchMutation = useMutation({
    mutationFn: async (searchRequest: SearchRequest) => {
      return apiService.search(searchRequest);
    },
    onSuccess: (data) => {
      // Add to search history
      setState(prev => ({
        ...prev,
        searchHistory: [state.query, ...prev.searchHistory.filter(q => q !== state.query)].slice(0, 10),
      }));
      
      setSnackbar({ open: true, message: `Found ${data.results?.length || 0} results`, severity: 'success' });
    },
    onError: (error) => {
      setSnackbar({ open: true, message: 'Search failed. Please try again.', severity: 'error' });
      console.error('Search error:', error);
    },
  });

  // AI service mutations
  const summarizeMutation = useMutation({
    mutationFn: async (content: string) => {
      return apiService.summarizeText({ content, max_length: 150 });
    },
  });

  const qaMutation = useMutation({
    mutationFn: async ({ question, context }: { question: string; context: string }) => {
      return apiService.askQuestion({ question, context });
    },
  });

  // Mock recent searches for now
  const { data: recentSearches } = useQuery({
    queryKey: ['recentSearches'],
    queryFn: () => Promise.resolve(['artificial intelligence', 'machine learning', 'neural networks']),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // WebSocket subscriptions
  useEffect(() => {
    if (state.isRealTimeSearch) {
      const unsubscribeSearch = subscribe('search_progress' as any, (data) => {
        console.log('Real-time search progress:', data);
      });

      const unsubscribeResults = subscribe('search_results' as any, (data) => {
        queryClient.invalidateQueries({ queryKey: ['searchResults'] });
      });

      return () => {
        unsubscribeSearch();
        unsubscribeResults();
      };
    }
  }, [state.isRealTimeSearch, subscribe, queryClient]);

  // Event handlers
  const handleSearch = async () => {
    if (!state.query.trim()) return;

    const searchRequest: SearchRequest = {
      query: state.query,
      options: {
        enable_semantic_search: state.filters.enableSemanticSearch,
        enable_hybrid_search: state.filters.enableHybridSearch,
        max_results: state.filters.maxResults,
        real_time: state.isRealTimeSearch,
      },
    };

    searchMutation.mutate(searchRequest);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSearch();
    }
  };

  const handleFilterChange = (filterType: keyof SearchFilters, value: any) => {
    setState(prev => ({
      ...prev,
      filters: {
        ...prev.filters,
        [filterType]: value,
      },
    }));
  };

  const handleHistorySearch = (query: string) => {
    setState(prev => ({ ...prev, query }));
    searchInputRef.current?.focus();
  };

  const handleBookmark = (resultId: string) => {
    setState(prev => ({
      ...prev,
      bookmarkedResults: prev.bookmarkedResults.includes(resultId)
        ? prev.bookmarkedResults.filter(id => id !== resultId)
        : [...prev.bookmarkedResults, resultId],
    }));
  };

  const handleAIAction = async (action: string, content: string, resultId?: string) => {
    try {
      switch (action) {
        case 'summarize':
          const summary = await summarizeMutation.mutateAsync(content);
          setSnackbar({ open: true, message: 'Summary generated successfully', severity: 'success' });
          break;
        case 'qa':
          if (state.query) {
            const answer = await qaMutation.mutateAsync({ question: state.query, context: content });
            setSnackbar({ open: true, message: 'Answer generated successfully', severity: 'success' });
          }
          break;
        default:
          break;
      }
    } catch (error) {
      setSnackbar({ open: true, message: `AI action failed: ${action}`, severity: 'error' });
    }
  };

  const SearchFiltersDrawer = () => (
    <Drawer
      anchor="right"
      open={state.showFilters}
      onClose={() => setState(prev => ({ ...prev, showFilters: false }))}
      sx={{ '& .MuiDrawer-paper': { width: 320, p: 2 } }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">Search Filters</Typography>
        <IconButton onClick={() => setState(prev => ({ ...prev, showFilters: false }))}>
          <CloseIcon />
        </IconButton>
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControlLabel
          control={
            <Switch
              checked={state.filters.enableSemanticSearch}
              onChange={(e) => handleFilterChange('enableSemanticSearch', e.target.checked)}
            />
          }
          label="Semantic Search"
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControlLabel
          control={
            <Switch
              checked={state.filters.enableHybridSearch}
              onChange={(e) => handleFilterChange('enableHybridSearch', e.target.checked)}
            />
          }
          label="Hybrid Search"
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <Typography gutterBottom>Confidence Threshold</Typography>
        <Slider
          value={state.filters.confidenceThreshold}
          onChange={(_, value) => handleFilterChange('confidenceThreshold', value)}
          min={0}
          max={1}
          step={0.1}
          marks
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${Math.round(value * 100)}%`}
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControl fullWidth>
          <InputLabel>Max Results</InputLabel>
          <Select
            value={state.filters.maxResults}
            onChange={(e) => handleFilterChange('maxResults', e.target.value)}
            label="Max Results"
          >
            <MenuItem value={10}>10</MenuItem>
            <MenuItem value={20}>20</MenuItem>
            <MenuItem value={50}>50</MenuItem>
            <MenuItem value={100}>100</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControlLabel
          control={
            <Switch
              checked={state.isRealTimeSearch}
              onChange={(e) => setState(prev => ({ ...prev, isRealTimeSearch: e.target.checked }))}
            />
          }
          label="Real-time Search"
        />
      </Box>
    </Drawer>
  );

  const SearchResults = () => {
    const results = searchMutation.data?.results || [];

    if (searchMutation.isPending) {
      return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 4 }}>
          <CircularProgress />
          <Typography sx={{ mt: 2 }}>Searching...</Typography>
          {state.isRealTimeSearch && progress && (
            <Typography variant="body2" sx={{ mt: 1 }}>
              {progress.message} ({progress.percentage}%)
            </Typography>
          )}
        </Box>
      );
    }

    if (results.length === 0 && searchMutation.data) {
      return (
        <Alert severity="info" sx={{ mt: 2 }}>
          No results found for "{state.query}". Try adjusting your search terms or filters.
        </Alert>
      );
    }

    return (
      <Box sx={{ mt: 3 }}>
        {results.map((result: SearchResult, index: number) => (
          <Card key={result.id || index} sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="div" sx={{ mb: 1 }}>
                    {result.filename}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {result.content?.slice(0, 200)}...
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip label={`Score: ${result.score?.toFixed(2)}`} size="small" color="primary" />
                    <Chip label={result.metadata?.source || 'Unknown'} size="small" variant="outlined" />
                    <Chip label={result.metadata?.file_type || 'Unknown'} size="small" variant="outlined" />
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Tooltip title="Bookmark">
                    <IconButton
                      size="small"
                      onClick={() => handleBookmark(result.id)}
                      color={state.bookmarkedResults.includes(result.id) ? 'primary' : 'default'}
                    >
                      <BookmarkIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Summarize">
                    <IconButton
                      size="small"
                      onClick={() => handleAIAction('summarize', result.content)}
                      disabled={summarizeMutation.isPending}
                    >
                      <SummarizeIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Ask Question">
                    <IconButton
                      size="small"
                      onClick={() => handleAIAction('qa', result.content, result.id)}
                      disabled={qaMutation.isPending}
                    >
                      <QAIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>

              {/* Expandable content */}
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="body2">View Full Content</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                    {result.content}
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </CardContent>
          </Card>
        ))}
      </Box>
    );
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
          Search
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Search through your documents using AI-powered semantic and hybrid search.
        </Typography>
      </Box>

      {/* Search Interface */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
          <TextField
            ref={searchInputRef}
            fullWidth
            variant="outlined"
            placeholder="Search your documents..."
            value={state.query}
            onChange={(e) => setState(prev => ({ ...prev, query: e.target.value }))}
            onKeyPress={handleKeyPress}
            disabled={searchMutation.isPending}
            InputProps={{
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
            }}
          />
          <Button
            variant="contained"
            onClick={handleSearch}
            disabled={!state.query.trim() || searchMutation.isPending}
            sx={{ minWidth: 120 }}
          >
            {searchMutation.isPending ? <CircularProgress size={24} /> : 'Search'}
          </Button>
          <Badge badgeContent={Object.keys(state.filters).length} color="primary">
            <IconButton onClick={() => setState(prev => ({ ...prev, showFilters: true }))}>
              <FilterIcon />
            </IconButton>
          </Badge>
        </Box>

        {/* Search Mode Selector */}
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <FormControlLabel
            control={
              <Switch
                checked={state.isRealTimeSearch}
                onChange={(e) => setState(prev => ({ ...prev, isRealTimeSearch: e.target.checked }))}
              />
            }
            label={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                Real-time Search
                {isConnected && <Chip label="Connected" size="small" color="success" />}
              </Box>
            }
          />
        </Box>
      </Paper>

      {/* Search History */}
      {state.searchHistory.length > 0 && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            Recent Searches
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {state.searchHistory.map((query, index) => (
              <Chip
                key={index}
                label={query}
                variant="outlined"
                clickable
                onClick={() => handleHistorySearch(query)}
                size="small"
              />
            ))}
          </Box>
        </Paper>
      )}

      {/* Search Results */}
      <SearchResults />

      {/* Filters Drawer */}
      <SearchFiltersDrawer />

      {/* Floating Action Button for Advanced Features */}
      <Fab
        color="primary"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => setState(prev => ({ ...prev, showFilters: true }))}
      >
        <SettingsIcon />
      </Fab>

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

export default SearchPage;
