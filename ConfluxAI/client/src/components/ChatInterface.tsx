import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Settings, FileText, Image, Video, Music, Calendar, HardDrive, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { toast } from '@/hooks/use-toast';
import { useDocumentTracker } from '@/hooks/useDocumentTracker';
import { format } from 'date-fns';
import SharedHeader from '@/components/SharedHeader';

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

const ChatInterface = () => {
  const { documents } = useDocumentTracker();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      content: "Hi! I'm your AI assistant for your ConfluxAI knowledge base. I can help you find information in your uploaded documents, images, videos, and audio files. Upload some content first, then ask me questions about it!",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isProduction, setIsProduction] = useState(() => {
    // Load from localStorage, default to test mode (false)
    const saved = localStorage.getItem('n8n-webhook-mode');
    return saved ? JSON.parse(saved) : false;
  });
  const [showDocuments, setShowDocuments] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Save webhook mode to localStorage
    localStorage.setItem('n8n-webhook-mode', JSON.stringify(isProduction));
  }, [isProduction]);

  const getWebhookUrl = () => {
    if (isProduction) {
      return 'https://kasimlohar.app.n8n.cloud/webhook/bdd9a358-e97e-4da2-8aed-6fd474dec5a7';
    } else {
      return 'https://kasimlohar.app.n8n.cloud/webhook-test/bdd9a358-e97e-4da2-8aed-6fd474dec5a7';
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputValue.trim() || isLoading) return;

    // Get current webhook URL based on toggle
    const webhookUrl = getWebhookUrl();

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    // Debug: Log browser environment details
    console.log('🔍 [DEBUG] Browser debugging info:', {
      userAgent: navigator.userAgent,
      currentOrigin: window.location.origin,
      targetWebhook: webhookUrl,
      timestamp: new Date().toISOString()
    });

    try {
      console.log('📤 [DEBUG] Sending message via backend proxy:', { 
        message: currentInput, 
        originalWebhookUrl: webhookUrl,
        requestPayload: {
          message: currentInput,
          timestamp: new Date().toISOString(),
        }
      });

      // Use backend proxy only (direct connection fails due to CORS)
      const response = await fetch('/api/webhook/n8n', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          message: currentInput,
          timestamp: new Date().toISOString(),
          source: 'conflux-ai-frontend',
          webhookUrl: webhookUrl // Pass the selected webhook URL
        }),
      });

      console.log('📥 [DEBUG] Backend proxy response received:', {
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries()),
        url: response.url,
        type: response.type
      });

      if (!response.ok) {
        console.error('❌ [DEBUG] Backend proxy HTTP error:', {
          status: response.status,
          statusText: response.statusText,
          url: response.url
        });
        throw new Error(`Backend proxy error ${response.status}: ${response.statusText}`);
      }

      // Get the JSON response from backend proxy
      const result = await response.json();
      console.log('✅ [DEBUG] Backend proxy JSON response:', result);
      
      // Check if backend proxy had an error
      if (!result.success) {
        console.error('❌ [DEBUG] Backend proxy returned error:', result);
        throw new Error(result.error || 'Backend proxy request failed');
      }
      
      // Extract the actual n8n response data
      const actualN8nResult = result.data;
      console.log('🔄 [DEBUG] n8n webhook response data:', actualN8nResult);
      
      // Check for empty responses
      if (actualN8nResult && actualN8nResult.raw === "") {
        console.log('⚠️ [DEBUG] n8n returned EMPTY response - workflow may have errors');
      }
      
      // Handle different response formats from n8n
      let botResponse = 'Task completed successfully!';
      
      console.log('🔄 [DEBUG] Processing n8n response format:', typeof actualN8nResult, actualN8nResult);
      
      if (typeof actualN8nResult === 'string') {
        botResponse = actualN8nResult;
        console.log('📝 [DEBUG] Using string response directly');
      } else if (actualN8nResult && actualN8nResult.response) {
        botResponse = actualN8nResult.response;
        console.log('📝 [DEBUG] Using result.response field');
      } else if (actualN8nResult && actualN8nResult.output) {
        botResponse = actualN8nResult.output;
        console.log('📝 [DEBUG] Using result.output field');
      } else if (actualN8nResult && actualN8nResult.text) {
        botResponse = actualN8nResult.text;
        console.log('📝 [DEBUG] Using result.text field');
      } else if (actualN8nResult && actualN8nResult.message) {
        botResponse = actualN8nResult.message;
        console.log('📝 [DEBUG] Using result.message field');
      } else if (actualN8nResult && actualN8nResult.raw) {
        if (actualN8nResult.raw.trim() === "") {
          botResponse = "⚠️ n8n workflow returned empty response. Check your workflow for errors, especially the LangChain memory buffer configuration.";
          console.log('⚠️ [DEBUG] Empty raw response from n8n workflow');
        } else {
          botResponse = actualN8nResult.raw;
          console.log('📝 [DEBUG] Using result.raw field (plain text from n8n)');
        }
      } else if (actualN8nResult && actualN8nResult.data) {
        botResponse = JSON.stringify(actualN8nResult.data);
        console.log('📝 [DEBUG] Using result.data field (stringified)');
      } else {
        botResponse = JSON.stringify(actualN8nResult);
        console.log('📝 [DEBUG] Using stringified full result');
      }

      console.log('✅ [DEBUG] Final bot response:', botResponse);

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: botResponse,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);

      toast({
        title: "Success",
        description: "Message processed successfully",
      });

    } catch (error) {
      console.error('❌ [DEBUG] Detailed error information:', {
        error: error,
        errorMessage: error instanceof Error ? error.message : 'Unknown error',
        errorStack: error instanceof Error ? error.stack : 'No stack trace',
        errorName: error instanceof Error ? error.name : 'Unknown error type',
        webhookUrl: webhookUrl,
        inputMessage: currentInput
      });

      // Check for specific error types
      if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
        console.error('🚫 [DEBUG] Network/CORS Error detected');
        console.log('💡 [DEBUG] This could be:');
        console.log('  1. Backend proxy route not working');
        console.log('  2. n8n workflow not active');
        console.log('  3. Network connectivity issue');
        console.log('  4. Webhook URL incorrect');
      }
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: `I'm sorry, I encountered an error processing your request. 

Error: ${error instanceof Error ? error.message : 'Unknown error'}

Troubleshooting steps:
1. Check that your n8n workflow is active
2. Verify the webhook URL: ${webhookUrl}
3. Check the browser console for detailed debug logs
4. Ensure your internet connection is stable

The system uses a backend proxy to avoid CORS issues. Check the server logs as well.`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
      
      toast({
        title: "Connection Error",
        description: "Check console for detailed error information",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleDateString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return <FileText className="w-4 h-4 text-red-500" />;
      case 'image':
        return <Image className="w-4 h-4 text-purple-500" />;
      case 'video':
        return <Video className="w-4 h-4 text-blue-500" />;
      case 'audio':
        return <Music className="w-4 h-4 text-emerald-500" />;
      default:
        return <FileText className="w-4 h-4 text-gray-500" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };



  return (
    <div className="flex flex-col h-full max-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-slate-900 dark:via-slate-800 dark:to-purple-900/20 transition-colors">
      <SharedHeader
        title="AI Assistant"
        subtitle="Powered by n8n automation"
        icon={
          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
            <Bot className="w-6 h-6 text-white" />
          </div>
        }
        isProduction={isProduction}
        onProductionToggle={(checked: boolean) => setIsProduction(checked)}
        testId="webhook-mode-toggle"
      />

      {/* Main Content with Sidebar */}
      <div className="flex-1 flex overflow-hidden">
        {/* Chat Messages */}
        <div className={`flex-1 flex flex-col transition-all duration-300 ${showDocuments && documents.length > 0 ? 'mr-80' : ''}`}>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
              >
                <div className={`flex gap-3 max-w-[85%] lg:max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg transition-transform hover:scale-105 ${
                    message.type === 'user' 
                      ? 'bg-gradient-to-r from-green-500 to-emerald-600' 
                      : 'bg-gradient-to-r from-blue-500 to-purple-600'
                  }`}>
                    {message.type === 'user' ? (
                      <User className="w-4 h-4 text-white" />
                    ) : (
                      <Bot className="w-4 h-4 text-white" />
                    )}
                  </div>
                  <Card className={`p-4 transition-all hover:shadow-lg ${
                    message.type === 'user'
                      ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white border-0 shadow-lg'
                      : 'bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-gray-200/50 dark:border-slate-700/50 shadow-md'
                  }`}>
                    <p className={`text-sm leading-relaxed whitespace-pre-wrap ${
                      message.type === 'user' ? 'text-white' : 'text-gray-800 dark:text-gray-200'
                    }`}>{message.content}</p>
                    <p className={`text-xs mt-2 transition-opacity ${
                      message.type === 'user' ? 'text-green-100' : 'text-gray-500 dark:text-gray-400'
                    }`}>
                      {formatTime(message.timestamp)}
                    </p>
                  </Card>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start animate-fade-in">
                <div className="flex gap-3 max-w-[80%]">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <Card className="p-4 bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm border-gray-200/50 dark:border-slate-700/50 shadow-md">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                      <p className="text-sm text-gray-600 dark:text-gray-300">AI is processing your request...</p>
                    </div>
                  </Card>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border-t border-gray-200/50 dark:border-slate-700/50">
            <form onSubmit={handleSendMessage} className="flex gap-3 animate-fade-in">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask questions about your uploaded files, images, videos, or audio content..."
                className="flex-1 bg-white/90 dark:bg-slate-700/90 border-gray-300/50 dark:border-slate-600/50 focus:border-blue-500 focus:ring-blue-500/20 transition-all"
                disabled={isLoading}
              />
              <Button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 border-0 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </Button>
            </form>
            <div className="mt-3 text-center space-y-1 animate-slide-in">
              <p className="text-xs text-gray-600 dark:text-gray-300">
                Try: "What is the main topic of my PDF?" or "What's in this image?" or "Summarize the video content"
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                Connected to: kasimlohar.app.n8n.cloud
              </p>
            </div>
          </div>
        </div>

        {/* Documents Sidebar */}
        {documents.length > 0 && (
          <div className={`fixed right-0 top-0 h-full w-80 bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm border-l border-gray-200/50 dark:border-slate-700/50 shadow-xl transition-transform duration-300 z-10 ${
            showDocuments ? 'translate-x-0' : 'translate-x-full'
          }`}>
            <div className="flex flex-col h-full">
              {/* Sidebar Header */}
              <div className="p-4 border-b border-gray-200/50 dark:border-slate-700/50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-slate-500 to-gray-600 rounded-full flex items-center justify-center">
                      <FileText className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800 dark:text-white text-sm">Knowledge Base</h3>
                      <p className="text-xs text-gray-600 dark:text-gray-300">{documents.length} document{documents.length !== 1 ? 's' : ''}</p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowDocuments(false)}
                    className="p-1 h-8 w-8"
                    data-testid="hide-documents-sidebar"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                </div>
              </div>

              {/* Documents List */}
              <ScrollArea className="flex-1 p-2">
                <div className="space-y-2">
                  {documents.map((doc) => (
                    <Card key={doc.id} className="p-3 hover:shadow-md transition-all cursor-pointer border-l-2 border-l-transparent hover:border-l-blue-500 dark:hover:border-l-blue-400">
                      <div className="flex items-start gap-2">
                        <div className="flex-shrink-0 mt-0.5">
                          {getFileIcon(doc.fileType)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-1 mb-1">
                            <h4 className="font-medium text-xs text-gray-800 dark:text-white truncate" title={doc.fileName}>
                              {doc.fileName}
                            </h4>
                            <Badge className={`text-xs px-1 py-0.5 ${
                              doc.webhookMode === 'production' 
                                ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300' 
                                : 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300'
                            }`}>
                              {doc.webhookMode === 'production' ? 'Prod' : 'Test'}
                            </Badge>
                          </div>
                          
                          <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-1">
                            <span className="flex items-center gap-1">
                              <HardDrive className="w-3 h-3" />
                              {formatFileSize(doc.fileSize)}
                            </span>
                            <span className="flex items-center gap-1">
                              <Calendar className="w-3 h-3" />
                              {format(new Date(doc.uploadedAt), 'MMM dd')}
                            </span>
                          </div>
                          
                          {doc.description && (
                            <p className="text-xs text-gray-600 dark:text-gray-300 truncate" title={doc.description}>
                              {doc.description}
                            </p>
                          )}
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </ScrollArea>
            </div>
          </div>
        )}

        {/* Toggle Button for Sidebar */}
        {documents.length > 0 && !showDocuments && (
          <Button
            onClick={() => setShowDocuments(true)}
            className="fixed right-4 top-1/2 -translate-y-1/2 z-20 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 rounded-full p-2 shadow-lg"
            data-testid="show-documents-sidebar"
          >
            <FileText className="w-4 h-4" />
          </Button>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;
