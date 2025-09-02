import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  IconButton,
  Button,
  Tooltip,
  Divider,
  Chip,
  Grid,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  useTheme,
  Fab,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Description as DocumentIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  ExpandMore as ExpandMoreIcon,
  Psychology as AIIcon,
  Summarize as SummarizeIcon,
  QuestionAnswer as QAIcon,
  AccountTree as GraphIcon,
  Search as SearchIcon,
  MoreVert as MoreIcon,
  Refresh as RefreshIcon,
  CloudUpload as UploadIcon,
  Info as InfoIcon,
  Star as StarIcon,
  StarBorder as StarBorderIcon,
  Bookmark as BookmarkIcon,
  BookmarkBorder as BookmarkBorderIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { apiService, Document, SummaryRequest } from '../services/api';

interface DocumentViewerProps {
  documentId?: string;
}

interface DocumentActions {
  showMetadata: boolean;
  showAISummary: boolean;
  showQuestions: boolean;
  showKnowledgeGraph: boolean;
  isBookmarked: boolean;
  isStarred: boolean;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentId: propDocumentId }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { documentId: paramDocumentId } = useParams<{ documentId: string }>();
  
  const documentId = propDocumentId || paramDocumentId;

  // Component state
  const [actions, setActions] = useState<DocumentActions>({
    showMetadata: false,
    showAISummary: false,
    showQuestions: false,
    showKnowledgeGraph: false,
    isBookmarked: false,
    isStarred: false,
  });

  const [aiQuestion, setAiQuestion] = useState('');
  const [showQuestionDialog, setShowQuestionDialog] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  // Fetch document data
  const { data: document, isLoading: documentLoading, error: documentError } = useQuery({
    queryKey: ['document', documentId],
    queryFn: () => apiService.getDocument(documentId!),
    enabled: !!documentId,
  });

  // AI service mutations
  const summarizeMutation = useMutation({
    mutationFn: async (request: SummaryRequest) => {
      return apiService.summarizeText(request);
    },
  });

  const questionMutation = useMutation({
    mutationFn: async ({ question }: { question: string }) => {
      return apiService.askQuestion({ question, document_id: documentId });
    },
  });

  const knowledgeGraphMutation = useMutation({
    mutationFn: async () => {
      return apiService.analyzeKnowledgeGraph({ document_id: documentId });
    },
  });

  // Document management mutations
  const deleteMutation = useMutation({
    mutationFn: async () => {
      return apiService.deleteDocument(documentId!);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      navigate('/');
    },
  });

  const updateMutation = useMutation({
    mutationFn: async (updates: Partial<Document>) => {
      return apiService.updateDocument(documentId!, updates);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['document', documentId] });
    },
  });

  // Event handlers
  const handleActionToggle = (action: keyof DocumentActions) => {
    setActions(prev => ({
      ...prev,
      [action]: !prev[action],
    }));

    // Trigger AI services when toggled on
    if (!actions[action]) {
      switch (action) {
        case 'showAISummary':
          if (document) {
            summarizeMutation.mutate({
              text: document.content,
              max_length: 200,
              style: 'concise',
            });
          }
          break;
        case 'showKnowledgeGraph':
          knowledgeGraphMutation.mutate();
          break;
      }
    }
  };

  const handleQuestionSubmit = () => {
    if (aiQuestion.trim()) {
      questionMutation.mutate({ question: aiQuestion });
      setShowQuestionDialog(false);
      setAiQuestion('');
    }
  };

  const handleBookmark = () => {
    setActions(prev => ({ ...prev, isBookmarked: !prev.isBookmarked }));
    // In a real app, this would make an API call
  };

  const handleStar = () => {
    setActions(prev => ({ ...prev, isStarred: !prev.isStarred }));
    // In a real app, this would make an API call
  };

  const handleDownload = () => {
    if (document) {
      // Create download link
      const blob = new Blob([document.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = document.filename;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this document?')) {
      deleteMutation.mutate();
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (!documentId) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        No document ID provided
      </Alert>
    );
  }

  if (documentLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Loading document...</Typography>
      </Box>
    );
  }

  if (documentError || !document) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        Failed to load document. Please try again.
      </Alert>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
              {document.filename}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
              <Chip
                icon={<DocumentIcon />}
                label={document.metadata?.file_type || 'Unknown'}
                size="small"
                color="primary"
              />
              <Chip
                label={formatFileSize(document.metadata?.file_size || 0)}
                size="small"
                variant="outlined"
              />
              <Chip
                label={`Uploaded ${formatDate(document.created_at)}`}
                size="small"
                variant="outlined"
              />
              {document.metadata?.pages && (
                <Chip
                  label={`${document.metadata.pages} pages`}
                  size="small"
                  variant="outlined"
                />
              )}
            </Box>
          </Box>

          {/* Action buttons */}
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <Tooltip title={actions.isStarred ? 'Remove from favorites' : 'Add to favorites'}>
              <IconButton onClick={handleStar} color={actions.isStarred ? 'warning' : 'default'}>
                {actions.isStarred ? <StarIcon /> : <StarBorderIcon />}
              </IconButton>
            </Tooltip>
            
            <Tooltip title={actions.isBookmarked ? 'Remove bookmark' : 'Bookmark'}>
              <IconButton onClick={handleBookmark} color={actions.isBookmarked ? 'primary' : 'default'}>
                {actions.isBookmarked ? <BookmarkIcon /> : <BookmarkBorderIcon />}
              </IconButton>
            </Tooltip>

            <Tooltip title="Download">
              <IconButton onClick={handleDownload}>
                <DownloadIcon />
              </IconButton>
            </Tooltip>

            <Tooltip title="More actions">
              <IconButton onClick={(e) => setAnchorEl(e.currentTarget)}>
                <MoreIcon />
              </IconButton>
            </Tooltip>

            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={() => setAnchorEl(null)}
            >
              <MenuItem onClick={() => { handleActionToggle('showMetadata'); setAnchorEl(null); }}>
                <ListItemIcon><InfoIcon /></ListItemIcon>
                <ListItemText>View Metadata</ListItemText>
              </MenuItem>
              <MenuItem onClick={() => setShowQuestionDialog(true)}>
                <ListItemIcon><QAIcon /></ListItemIcon>
                <ListItemText>Ask Question</ListItemText>
              </MenuItem>
              <MenuItem onClick={() => { handleDelete(); setAnchorEl(null); }}>
                <ListItemIcon><DeleteIcon /></ListItemIcon>
                <ListItemText>Delete Document</ListItemText>
              </MenuItem>
            </Menu>
          </Box>
        </Box>

        {/* Quick actions */}
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <Button
            variant={actions.showAISummary ? 'contained' : 'outlined'}
            startIcon={<SummarizeIcon />}
            onClick={() => handleActionToggle('showAISummary')}
            disabled={summarizeMutation.isPending}
          >
            {summarizeMutation.isPending ? 'Generating...' : 'AI Summary'}
          </Button>
          
          <Button
            variant={actions.showKnowledgeGraph ? 'contained' : 'outlined'}
            startIcon={<GraphIcon />}
            onClick={() => handleActionToggle('showKnowledgeGraph')}
            disabled={knowledgeGraphMutation.isPending}
          >
            {knowledgeGraphMutation.isPending ? 'Analyzing...' : 'Knowledge Graph'}
          </Button>

          <Button
            variant="outlined"
            startIcon={<QAIcon />}
            onClick={() => setShowQuestionDialog(true)}
          >
            Ask Question
          </Button>
        </Box>
      </Paper>

      {/* AI Summary */}
      {actions.showAISummary && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            AI Summary
          </Typography>
          {summarizeMutation.isPending ? (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <CircularProgress size={20} />
              <Typography>Generating summary...</Typography>
            </Box>
          ) : summarizeMutation.data ? (
            <Typography variant="body1" sx={{ lineHeight: 1.8 }}>
              {summarizeMutation.data.summary}
            </Typography>
          ) : (
            <Alert severity="info">
              Click "AI Summary" to generate an AI-powered summary of this document.
            </Alert>
          )}
        </Paper>
      )}

      {/* Knowledge Graph */}
      {actions.showKnowledgeGraph && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Knowledge Graph
          </Typography>
          {knowledgeGraphMutation.isPending ? (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <CircularProgress size={20} />
              <Typography>Analyzing knowledge graph...</Typography>
            </Box>
          ) : knowledgeGraphMutation.data ? (
            <Box>
              <Typography variant="body1" sx={{ mb: 2 }}>
                Key entities and relationships discovered in this document:
              </Typography>
              {/* This would render the actual knowledge graph visualization */}
              <Alert severity="info">
                Knowledge graph visualization would be rendered here using D3.js or similar library.
              </Alert>
            </Box>
          ) : (
            <Alert severity="info">
              Click "Knowledge Graph" to analyze entities and relationships in this document.
            </Alert>
          )}
        </Paper>
      )}

      {/* Document Metadata */}
      {actions.showMetadata && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Document Metadata
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                File Name
              </Typography>
              <Typography variant="body1">{document.filename}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                File Type
              </Typography>
              <Typography variant="body1">{document.metadata?.file_type || 'Unknown'}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                File Size
              </Typography>
              <Typography variant="body1">{formatFileSize(document.metadata?.file_size || 0)}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Created At
              </Typography>
              <Typography variant="body1">{formatDate(document.created_at)}</Typography>
            </Grid>
            {document.metadata?.pages && (
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Pages
                </Typography>
                <Typography variant="body1">{document.metadata.pages}</Typography>
              </Grid>
            )}
            {document.metadata?.language && (
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Language
                </Typography>
                <Typography variant="body1">{document.metadata.language}</Typography>
              </Grid>
            )}
          </Grid>
        </Paper>
      )}

      {/* Document Content */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Document Content
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Typography
          variant="body1"
          component="pre"
          sx={{
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            lineHeight: 1.8,
            fontFamily: 'inherit',
          }}
        >
          {document.content}
        </Typography>
      </Paper>

      {/* Question Dialog */}
      <Dialog
        open={showQuestionDialog}
        onClose={() => setShowQuestionDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Ask a Question about this Document</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            multiline
            rows={4}
            placeholder="What would you like to know about this document?"
            value={aiQuestion}
            onChange={(e) => setAiQuestion(e.target.value)}
            sx={{ mt: 1 }}
          />
          {questionMutation.data && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                AI Answer:
              </Typography>
              <Typography variant="body1" sx={{ lineHeight: 1.8 }}>
                {questionMutation.data.answer}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowQuestionDialog(false)}>
            Cancel
          </Button>
          <Button
            onClick={handleQuestionSubmit}
            variant="contained"
            disabled={!aiQuestion.trim() || questionMutation.isPending}
          >
            {questionMutation.isPending ? 'Asking...' : 'Ask Question'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Floating Action Button for quick actions */}
      <Fab
        color="primary"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => setShowQuestionDialog(true)}
      >
        <QAIcon />
      </Fab>
    </Box>
  );
};

export default DocumentViewer;
