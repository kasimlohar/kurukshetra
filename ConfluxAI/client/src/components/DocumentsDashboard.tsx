import React, { useState } from 'react';
import { useDocumentTracker } from '@/hooks/useDocumentTracker';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  FileText, 
  Image, 
  Video, 
  Music, 
  Trash2, 
  Calendar,
  HardDrive,
  Filter,
  Download,
  Eye,
  BarChart3,
  Folder
} from 'lucide-react';
import { format } from 'date-fns';

const DocumentsDashboard = () => {
  const { documents, removeDocument, clearAllDocuments, getDocumentsByType, getTotalSize } = useDocumentTracker();
  const [selectedType, setSelectedType] = useState<string>('all');

  const getFileIcon = (type: string, extension: string) => {
    switch (type) {
      case 'pdf':
        return <FileText className="w-8 h-8 text-red-500" />;
      case 'image':
        return <Image className="w-8 h-8 text-purple-500" />;
      case 'video':
        return <Video className="w-8 h-8 text-blue-500" />;
      case 'audio':
        return <Music className="w-8 h-8 text-emerald-500" />;
      default:
        return <FileText className="w-8 h-8 text-gray-500" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'pdf':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'image':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'video':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'audio':
        return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const filteredDocuments = selectedType === 'all' 
    ? documents 
    : documents.filter(doc => doc.fileType === selectedType);

  const stats = {
    total: documents.length,
    pdf: getDocumentsByType('pdf').length,
    image: getDocumentsByType('image').length,
    video: getDocumentsByType('video').length,
    audio: getDocumentsByType('audio').length,
    totalSize: getTotalSize(),
  };

  return (
    <div className="flex flex-col h-full max-h-screen bg-gradient-to-br from-slate-50 via-white to-gray-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200/50 p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-slate-500 to-gray-600 rounded-full flex items-center justify-center">
              <Folder className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-800">📁 Documents Library</h1>
              <p className="text-sm text-gray-600">Track all your uploaded knowledge base content</p>
            </div>
          </div>
          
          {documents.length > 0 && (
            <Button
              onClick={clearAllDocuments}
              variant="outline"
              className="text-red-600 border-red-200 hover:bg-red-50"
              data-testid="clear-all-documents-button"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              Clear All
            </Button>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="p-4 border-b border-gray-200/50">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
          <Card className="p-3 bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-blue-600" />
              <div>
                <p className="text-xs text-blue-600 font-medium">Total Files</p>
                <p className="text-lg font-bold text-blue-800">{stats.total}</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-3 bg-gradient-to-r from-red-50 to-red-100 border-red-200">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-red-600" />
              <div>
                <p className="text-xs text-red-600 font-medium">PDFs</p>
                <p className="text-lg font-bold text-red-800">{stats.pdf}</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-3 bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
            <div className="flex items-center gap-2">
              <Image className="w-4 h-4 text-purple-600" />
              <div>
                <p className="text-xs text-purple-600 font-medium">Images</p>
                <p className="text-lg font-bold text-purple-800">{stats.image}</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-3 bg-gradient-to-r from-blue-50 to-cyan-100 border-blue-200">
            <div className="flex items-center gap-2">
              <Video className="w-4 h-4 text-blue-600" />
              <div>
                <p className="text-xs text-blue-600 font-medium">Videos</p>
                <p className="text-lg font-bold text-blue-800">{stats.video}</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-3 bg-gradient-to-r from-emerald-50 to-emerald-100 border-emerald-200">
            <div className="flex items-center gap-2">
              <Music className="w-4 h-4 text-emerald-600" />
              <div>
                <p className="text-xs text-emerald-600 font-medium">Audio</p>
                <p className="text-lg font-bold text-emerald-800">{stats.audio}</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-3 bg-gradient-to-r from-gray-50 to-gray-100 border-gray-200">
            <div className="flex items-center gap-2">
              <HardDrive className="w-4 h-4 text-gray-600" />
              <div>
                <p className="text-xs text-gray-600 font-medium">Total Size</p>
                <p className="text-sm font-bold text-gray-800">{formatFileSize(stats.totalSize)}</p>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="p-4 border-b border-gray-200/50">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600 mr-2">Filter:</span>
          <div className="flex gap-2">
            {[
              { key: 'all', label: 'All Files', count: stats.total },
              { key: 'pdf', label: 'PDFs', count: stats.pdf },
              { key: 'image', label: 'Images', count: stats.image },
              { key: 'video', label: 'Videos', count: stats.video },
              { key: 'audio', label: 'Audio', count: stats.audio },
            ].map(filter => (
              <Button
                key={filter.key}
                onClick={() => setSelectedType(filter.key)}
                variant={selectedType === filter.key ? "default" : "outline"}
                size="sm"
                className="text-xs"
                data-testid={`filter-${filter.key}-button`}
              >
                {filter.label} ({filter.count})
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Documents List */}
      <div className="flex-1 overflow-y-auto p-4">
        {filteredDocuments.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <Folder className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-600 mb-2">
              {selectedType === 'all' ? 'No documents uploaded yet' : `No ${selectedType} files found`}
            </h3>
            <p className="text-sm text-gray-500">
              Start uploading files using the upload tabs to see them here.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredDocuments.map((doc) => (
              <Card key={doc.id} className="p-4 hover:shadow-md transition-shadow border-l-4 border-l-gray-300">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {/* File Icon */}
                    <div className="flex-shrink-0">
                      {getFileIcon(doc.fileType, doc.extension)}
                    </div>
                    
                    {/* File Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-medium text-gray-800 truncate" title={doc.fileName}>
                          {doc.fileName}
                        </h4>
                        <Badge className={`text-xs ${getTypeColor(doc.fileType)}`}>
                          {doc.extension.toUpperCase()}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                          {doc.webhookMode === 'production' ? '🟢 Prod' : '🟡 Test'}
                        </Badge>
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span className="flex items-center gap-1">
                          <HardDrive className="w-3 h-3" />
                          {formatFileSize(doc.fileSize)}
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {format(new Date(doc.uploadedAt), 'MMM dd, yyyy HH:mm')}
                        </span>
                      </div>
                      
                      {doc.description && (
                        <p className="text-xs text-gray-600 mt-1 truncate">
                          {doc.description}
                        </p>
                      )}
                    </div>
                  </div>
                  
                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <Button
                      onClick={() => removeDocument(doc.id)}
                      variant="ghost"
                      size="sm"
                      className="text-red-500 hover:text-red-700 hover:bg-red-50"
                      data-testid={`remove-document-${doc.id}-button`}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentsDashboard;