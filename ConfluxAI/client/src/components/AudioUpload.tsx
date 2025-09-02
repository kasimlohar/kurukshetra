import React, { useState } from 'react';
import { Upload, Music, Loader2, CheckCircle, XCircle, Settings, Volume2, Mic } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Progress } from '@/components/ui/progress';
import { toast } from '@/hooks/use-toast';
import { useDocumentTracker } from '@/hooks/useDocumentTracker';

interface UploadResult {
  success: boolean;
  message: string;
  details?: any;
}

const AudioUpload = () => {
  const { addDocument } = useDocumentTracker();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
  const [isProduction, setIsProduction] = useState(() => {
    // Load from localStorage, default to test mode (false)
    const saved = localStorage.getItem('n8n-audio-webhook-mode');
    return saved ? JSON.parse(saved) : false;
  });

  const getAudioWebhookUrl = () => {
    if (isProduction) {
      return 'https://kasimlohar.app.n8n.cloud/webhook/2bb25d11-1ed8-4299-9ef4-f5bf091c3695';
    } else {
      return 'https://kasimlohar.app.n8n.cloud/webhook-test/2bb25d11-1ed8-4299-9ef4-f5bf091c3695';
    }
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.type.startsWith('audio/')) {
        toast({
          title: "Invalid file type",
          description: "Please select an audio file (MP3, WAV, AAC, etc.).",
          variant: "destructive",
        });
        return;
      }
      
      if (file.size > 50 * 1024 * 1024) { // 50MB limit for audio
        toast({
          title: "File too large",
          description: "Please select an audio file smaller than 50MB.",
          variant: "destructive",
        });
        return;
      }
      
      setSelectedFile(file);
      setUploadResult(null);
      console.log('🎵 [AUDIO] File selected:', file.name, `${(file.size / 1024 / 1024).toFixed(2)}MB`);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast({
        title: "No file selected",
        description: "Please select an audio file first.",
        variant: "destructive",
      });
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setUploadResult(null);

    console.log('📤 [AUDIO] Starting upload:', {
      fileName: selectedFile.name,
      fileSize: selectedFile.size,
      webhookMode: isProduction ? 'production' : 'test',
      webhookUrl: getAudioWebhookUrl()
    });

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('webhookUrl', getAudioWebhookUrl());
      formData.append('fileName', selectedFile.name);
      formData.append('timestamp', new Date().toISOString());

      // Simulate progress for audio processing
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 88) {
            clearInterval(progressInterval);
            return 88;
          }
          return prev + Math.random() * 18;
        });
      }, 300);

      const response = await fetch('/api/upload-audio', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      console.log('📥 [AUDIO] Upload response received:', {
        status: response.status,
        statusText: response.statusText,
        url: response.url
      });

      const result = await response.json();
      console.log('📊 [AUDIO] Upload result:', result);

      if (result.success) {
        setUploadResult({
          success: true,
          message: 'Audio successfully uploaded and processed! Speech has been transcribed and stored in the knowledge base.',
          details: result.data
        });
        
        toast({
          title: "Upload successful!",
          description: `${selectedFile.name} has been added to the knowledge base.`,
        });

        // Track the document in the dashboard
        const extension = selectedFile.name.split('.').pop() || 'mp3';
        addDocument({
          fileName: selectedFile.name,
          fileSize: selectedFile.size,
          fileType: 'audio',
          extension: extension,
          webhookMode: isProduction ? 'production' : 'test',
          status: 'success',
          description: result.data?.content?.parts?.[0]?.text || result.data?.text || 'Audio transcribed and stored in knowledge base'
        });

        // Clear file selection after successful upload
        setSelectedFile(null);
        const fileInput = document.getElementById('audio-upload') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
        
      } else {
        setUploadResult({
          success: false,
          message: result.error || 'Upload failed. Please try again.',
          details: result.details
        });
        
        toast({
          title: "Upload failed",
          description: result.error || 'An error occurred during upload.',
          variant: "destructive",
        });
      }

    } catch (error) {
      console.error('❌ [AUDIO] Upload error:', error);
      
      setUploadResult({
        success: false,
        message: 'Network error occurred. Please check your connection and try again.',
        details: error instanceof Error ? error.message : 'Unknown error'
      });
      
      toast({
        title: "Upload error",
        description: "Network error occurred. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-h-screen bg-gradient-to-br from-emerald-50 via-white to-teal-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200/50 p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-full flex items-center justify-center">
              <Music className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-800">🎵 Save Audio</h1>
              <p className="text-sm text-gray-600">Upload audio to knowledge base</p>
            </div>
          </div>
          
          {/* Webhook Mode Toggle */}
          <div className="flex items-center gap-3" data-testid="audio-webhook-mode-toggle">
            <div className="flex items-center gap-2">
              <Settings className="w-4 h-4 text-gray-600" />
              <span className={`text-sm font-medium ${!isProduction ? 'text-orange-600' : 'text-gray-500'}`}>
                Test
              </span>
              <Switch
                checked={isProduction}
                onCheckedChange={(checked) => {
                  setIsProduction(checked);
                  localStorage.setItem('n8n-audio-webhook-mode', JSON.stringify(checked));
                  toast({
                    title: checked ? "Production Mode" : "Test Mode",
                    description: checked ? "Using production webhook" : "Using test webhook",
                  });
                }}
                data-testid="audio-production-mode-switch"
              />
              <span className={`text-sm font-medium ${isProduction ? 'text-green-600' : 'text-gray-500'}`}>
                Production
              </span>
            </div>
          </div>
        </div>
        
        {/* Mode Indicator */}
        <div className="mt-2">
          <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
            isProduction 
              ? 'bg-green-100 text-green-800' 
              : 'bg-orange-100 text-orange-800'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              isProduction ? 'bg-green-500' : 'bg-orange-500'
            }`} />
            {isProduction ? 'Production Mode' : 'Test Mode'}
          </div>
        </div>
      </div>

      {/* Upload Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-2xl mx-auto space-y-6">
          
          {/* Upload Card */}
          <Card className="p-6 border-2 border-dashed border-gray-300 hover:border-emerald-400 transition-colors">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 mx-auto bg-emerald-100 rounded-full flex items-center justify-center">
                <Mic className="w-8 h-8 text-emerald-600" />
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Upload Audio to Knowledge Base</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Your audio will be transcribed, analyzed for content, and stored in the knowledge base for retrieval.
                </p>
              </div>

              {/* File Input */}
              <div className="space-y-4">
                <input
                  id="audio-upload"
                  type="file"
                  accept="audio/*"
                  onChange={handleFileSelect}
                  className="hidden"
                  data-testid="audio-file-input"
                />
                <label
                  htmlFor="audio-upload"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 cursor-pointer transition-colors"
                  data-testid="audio-file-select-button"
                >
                  <Music className="w-4 h-4" />
                  Select Audio File
                </label>

                {selectedFile && (
                  <div className="flex items-center gap-2 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                    <Volume2 className="w-4 h-4" />
                    <span className="font-medium">{selectedFile.name}</span>
                    <span className="text-gray-400">
                      ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                    </span>
                  </div>
                )}
              </div>

              {/* Upload Button */}
              <Button
                onClick={handleUpload}
                disabled={!selectedFile || isUploading}
                className="w-full sm:w-auto bg-emerald-600 hover:bg-emerald-700"
                data-testid="save-audio-to-knowledge-base-button"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="w-4 h-4 mr-2" />
                    Save to Knowledge Base
                  </>
                )}
              </Button>
            </div>
          </Card>

          {/* Progress Bar */}
          {isUploading && (
            <Card className="p-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Transcribing and processing audio...</span>
                  <span>{Math.round(uploadProgress)}%</span>
                </div>
                <Progress value={uploadProgress} className="w-full" />
              </div>
            </Card>
          )}

          {/* Upload Result */}
          {uploadResult && (
            <Card className={`p-4 ${uploadResult.success ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'}`}>
              <div className="flex items-start gap-3">
                {uploadResult.success ? (
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-600 mt-0.5" />
                )}
                <div className="flex-1">
                  <h4 className={`font-medium ${uploadResult.success ? 'text-green-800' : 'text-red-800'}`}>
                    {uploadResult.success ? 'Success!' : 'Upload Failed'}
                  </h4>
                  <p className={`text-sm mt-1 ${uploadResult.success ? 'text-green-700' : 'text-red-700'}`}>
                    {uploadResult.message}
                  </p>
                  {uploadResult.details && (
                    <details className="mt-2">
                      <summary className={`text-xs cursor-pointer ${uploadResult.success ? 'text-green-600' : 'text-red-600'}`}>
                        View details
                      </summary>
                      <pre className={`text-xs mt-1 p-2 rounded ${uploadResult.success ? 'bg-green-100' : 'bg-red-100'} overflow-auto`}>
                        {JSON.stringify(uploadResult.details, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>
              </div>
            </Card>
          )}

          {/* Info */}
          <Card className="p-4 bg-emerald-50 border-emerald-200">
            <div className="flex items-start gap-3">
              <Music className="w-5 h-5 text-emerald-600 mt-0.5" />
              <div className="text-sm text-emerald-800">
                <h4 className="font-medium mb-1">How it works:</h4>
                <ul className="space-y-1 text-emerald-700">
                  <li>• Audio is transcribed using advanced speech-to-text</li>
                  <li>• Content is analyzed for key topics and themes</li>
                  <li>• Speaker identification and emotional tone detection</li>
                  <li>• Transcription is converted to embeddings for search</li>
                </ul>
              </div>
            </div>
          </Card>

        </div>
      </div>
    </div>
  );
};

export default AudioUpload;