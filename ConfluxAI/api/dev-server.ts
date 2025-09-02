import express from 'express';
import { createServer } from 'http';
import { storage } from '../server/storage';
import multer from 'multer';
import { FormData as NodeFormData } from 'formdata-node';

const app = express();
app.use(express.json({ limit: '100mb' }));
app.use(express.urlencoded({ extended: false, limit: '100mb' }));

// Configure multer for different file types
const uploadPDF = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF files are allowed!'));
    }
  },
});

const uploadImage = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed!'));
    }
  },
});

const uploadVideo = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 100 * 1024 * 1024 }, // 100MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('video/')) {
      cb(null, true);
    } else {
      cb(new Error('Only video files are allowed!'));
    }
  },
});

const uploadAudio = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('audio/')) {
      cb(null, true);
    } else {
      cb(new Error('Only audio files are allowed!'));
    }
  },
});

// n8n webhook proxy route
app.post("/api/webhook/n8n", async (req, res) => {
  try {
    console.log('🔄 [WEBHOOK] Received proxy request');
    console.log(`📋 [WEBHOOK] Request body: ${JSON.stringify(req.body)}`);

    const { message, timestamp, source, webhookUrl } = req.body;
    
    if (!message) {
      console.log('❌ [WEBHOOK] Missing message in request body');
      return res.status(400).json({ 
        success: false,
        error: 'Missing message in request body',
        received: req.body 
      });
    }

    if (!webhookUrl) {
      console.log('❌ [WEBHOOK] Missing webhookUrl in request body');
      return res.status(400).json({ 
        success: false,
        error: 'Missing webhookUrl in request body',
        received: req.body 
      });
    }
    
    console.log(`📤 [WEBHOOK] Forwarding to n8n: ${webhookUrl}`);

    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Dev-Server-ChatBot-Proxy/1.0',
        'Accept': 'application/json, text/plain, */*'
      },
      body: JSON.stringify({
        message,
        timestamp: timestamp || new Date().toISOString(),
        source: source || 'dev-server-chat-backend'
      })
    });

    console.log(`📥 [WEBHOOK] n8n response: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      console.log(`❌ [WEBHOOK] n8n error: ${response.status} ${response.statusText}`);
      return res.status(200).json({
        success: false,
        error: `n8n webhook returned ${response.status}: ${response.statusText}`,
        details: {
          status: response.status,
          statusText: response.statusText,
          webhookUrl: webhookUrl
        }
      });
    }

    const responseText = await response.text();
    console.log(`📄 [WEBHOOK] Raw n8n response: "${responseText}"`);

    let result;
    try {
      result = JSON.parse(responseText);
      console.log('✅ [WEBHOOK] Parsed n8n JSON response successfully');
    } catch (parseError) {
      console.log('📝 [WEBHOOK] n8n response was not JSON, treating as text');
      result = { message: responseText, raw: responseText };
    }

    const successResponse = {
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
      source: 'dev-server-backend-proxy',
      webhookUrl: webhookUrl
    };

    console.log('✅ [WEBHOOK] Sending success response to frontend');
    res.json(successResponse);

  } catch (error) {
    console.log(`❌ [WEBHOOK] Proxy error: ${error instanceof Error ? error.message : 'Unknown error'}`);

    res.status(200).json({
      success: false,
      error: 'Internal server error while proxying to n8n webhook',
      details: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    });
  }
});

// PDF Upload endpoint
app.post("/api/upload-pdf", uploadPDF.single('file'), async (req, res) => {
  try {
    console.log('📄 [PDF] Received PDF upload request');
    
    if (!req.file) {
      console.log('❌ [PDF] No file in request');
      return res.status(400).json({ 
        success: false,
        error: 'No file uploaded',
        received: req.body 
      });
    }

    const { webhookUrl, fileName, timestamp } = req.body;
    
    if (!webhookUrl) {
      console.log('❌ [PDF] Missing webhookUrl in request body');
      return res.status(400).json({ 
        success: false,
        error: 'Missing webhookUrl in request body',
        received: req.body 
      });
    }

    console.log(`📋 [PDF] Processing file: ${req.file.originalname} (${req.file.size} bytes)`);
    console.log(`📤 [PDF] Forwarding to n8n: ${webhookUrl}`);

    const formData = new NodeFormData();
    formData.append('file', new Blob([req.file.buffer], { type: 'application/pdf' }), req.file.originalname);
    formData.append('fileName', fileName || req.file.originalname);
    formData.append('timestamp', timestamp || new Date().toISOString());
    formData.append('source', 'dev-server-pdf-uploader');

    const response = await fetch(webhookUrl, {
      method: 'POST',
      body: formData as any,
      headers: {
        'User-Agent': 'Dev-Server-PDF-Proxy/1.0',
      }
    });

    console.log(`📥 [PDF] n8n response: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      console.log(`❌ [PDF] n8n error: ${response.status} ${response.statusText}`);
      return res.status(200).json({
        success: false,
        error: `n8n webhook returned ${response.status}: ${response.statusText}`,
        details: {
          status: response.status,
          statusText: response.statusText,
          webhookUrl: webhookUrl
        }
      });
    }

    const responseText = await response.text();
    console.log(`📄 [PDF] Raw n8n response: "${responseText}"`);

    let result;
    try {
      result = JSON.parse(responseText);
      console.log('✅ [PDF] Parsed n8n JSON response successfully');
    } catch (parseError) {
      console.log('📝 [PDF] n8n response was not JSON, treating as text');
      result = { message: responseText, raw: responseText };
    }

    const successResponse = {
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
      source: 'dev-server-pdf-backend-proxy',
      webhookUrl: webhookUrl,
      fileName: req.file.originalname,
      fileSize: req.file.size
    };

    console.log('✅ [PDF] Sending success response to frontend');
    res.json(successResponse);

  } catch (error) {
    console.log(`❌ [PDF] Upload error: ${error instanceof Error ? error.message : 'Unknown error'}`);

    if (error instanceof multer.MulterError) {
      if (error.code === 'LIMIT_FILE_SIZE') {
        return res.status(200).json({
          success: false,
          error: 'File too large. Maximum size is 10MB.',
          details: error.message
        });
      }
    }

    res.status(200).json({
      success: false,
      error: 'Internal server error while processing PDF upload',
      details: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    });
  }
});

// Image Upload endpoint
app.post("/api/upload-image", uploadImage.single('file'), async (req, res) => {
  try {
    console.log('🖼️ [IMAGE] Received image upload request');
    
    if (!req.file) {
      console.log('❌ [IMAGE] No file in request');
      return res.status(400).json({ 
        success: false,
        error: 'No file uploaded',
        received: req.body 
      });
    }

    const { webhookUrl, fileName, timestamp } = req.body;
    
    if (!webhookUrl) {
      console.log('❌ [IMAGE] Missing webhookUrl in request body');
      return res.status(400).json({ 
        success: false,
        error: 'Missing webhookUrl in request body',
        received: req.body 
      });
    }

    console.log(`📋 [IMAGE] Processing file: ${req.file.originalname} (${req.file.size} bytes)`);
    console.log(`📤 [IMAGE] Forwarding to n8n: ${webhookUrl}`);

    const formData = new NodeFormData();
    formData.append('file', new Blob([req.file.buffer], { type: req.file.mimetype }), req.file.originalname);
    formData.append('fileName', fileName || req.file.originalname);
    formData.append('timestamp', timestamp || new Date().toISOString());
    formData.append('source', 'dev-server-image-uploader');

    const response = await fetch(webhookUrl, {
      method: 'POST',
      body: formData as any,
      headers: {
        'User-Agent': 'Dev-Server-Image-Proxy/1.0',
      }
    });

    console.log(`📥 [IMAGE] n8n response: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      console.log(`❌ [IMAGE] n8n error: ${response.status} ${response.statusText}`);
      return res.status(200).json({
        success: false,
        error: `n8n webhook returned ${response.status}: ${response.statusText}`,
        details: {
          status: response.status,
          statusText: response.statusText,
          webhookUrl: webhookUrl
        }
      });
    }

    const responseText = await response.text();
    console.log(`📄 [IMAGE] Raw n8n response: "${responseText}"`);

    let result;
    try {
      result = JSON.parse(responseText);
      console.log('✅ [IMAGE] Parsed n8n JSON response successfully');
    } catch (parseError) {
      console.log('📝 [IMAGE] n8n response was not JSON, treating as text');
      result = { message: responseText, raw: responseText };
    }

    const successResponse = {
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
      source: 'dev-server-image-backend-proxy',
      webhookUrl: webhookUrl,
      fileName: req.file.originalname,
      fileSize: req.file.size
    };

    console.log('✅ [IMAGE] Sending success response to frontend');
    res.json(successResponse);

  } catch (error) {
    console.log(`❌ [IMAGE] Upload error: ${error instanceof Error ? error.message : 'Unknown error'}`);

    if (error instanceof multer.MulterError) {
      if (error.code === 'LIMIT_FILE_SIZE') {
        return res.status(200).json({
          success: false,
          error: 'File too large. Maximum size is 10MB.',
          details: error.message
        });
      }
    }

    res.status(200).json({
      success: false,
      error: 'Internal server error while processing image upload',
      details: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    });
  }
});

// Video Upload endpoint
app.post("/api/upload-video", uploadVideo.single('file'), async (req, res) => {
  try {
    console.log('🎬 [VIDEO] Received video upload request');
    
    if (!req.file) {
      console.log('❌ [VIDEO] No file in request');
      return res.status(400).json({ 
        success: false,
        error: 'No file uploaded',
        received: req.body 
      });
    }

    const { webhookUrl, fileName, timestamp } = req.body;
    
    if (!webhookUrl) {
      console.log('❌ [VIDEO] Missing webhookUrl in request body');
      return res.status(400).json({ 
        success: false,
        error: 'Missing webhookUrl in request body',
        received: req.body 
      });
    }

    console.log(`📋 [VIDEO] Processing file: ${req.file.originalname} (${req.file.size} bytes)`);
    console.log(`📤 [VIDEO] Forwarding to n8n: ${webhookUrl}`);

    const formData = new NodeFormData();
    formData.append('file', new Blob([req.file.buffer], { type: req.file.mimetype }), req.file.originalname);
    formData.append('fileName', fileName || req.file.originalname);
    formData.append('timestamp', timestamp || new Date().toISOString());
    formData.append('source', 'dev-server-video-uploader');

    const response = await fetch(webhookUrl, {
      method: 'POST',
      body: formData as any,
      headers: {
        'User-Agent': 'Dev-Server-Video-Proxy/1.0',
      }
    });

    console.log(`📥 [VIDEO] n8n response: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      console.log(`❌ [VIDEO] n8n error: ${response.status} ${response.statusText}`);
      return res.status(200).json({
        success: false,
        error: `n8n webhook returned ${response.status}: ${response.statusText}`,
        details: {
          status: response.status,
          statusText: response.statusText,
          webhookUrl: webhookUrl
        }
      });
    }

    const responseText = await response.text();
    console.log(`📄 [VIDEO] Raw n8n response: "${responseText}"`);

    let result;
    try {
      result = JSON.parse(responseText);
      console.log('✅ [VIDEO] Parsed n8n JSON response successfully');
    } catch (parseError) {
      console.log('📝 [VIDEO] n8n response was not JSON, treating as text');
      result = { message: responseText, raw: responseText };
    }

    const successResponse = {
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
      source: 'dev-server-video-backend-proxy',
      webhookUrl: webhookUrl,
      fileName: req.file.originalname,
      fileSize: req.file.size
    };

    console.log('✅ [VIDEO] Sending success response to frontend');
    res.json(successResponse);

  } catch (error) {
    console.log(`❌ [VIDEO] Upload error: ${error instanceof Error ? error.message : 'Unknown error'}`);

    if (error instanceof multer.MulterError) {
      if (error.code === 'LIMIT_FILE_SIZE') {
        return res.status(200).json({
          success: false,
          error: 'File too large. Maximum size is 100MB.',
          details: error.message
        });
      }
    }

    res.status(200).json({
      success: false,
      error: 'Internal server error while processing video upload',
      details: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    });
  }
});

// Audio Upload endpoint
app.post("/api/upload-audio", uploadAudio.single('file'), async (req, res) => {
  try {
    console.log('🎵 [AUDIO] Received audio upload request');
    
    if (!req.file) {
      console.log('❌ [AUDIO] No file in request');
      return res.status(400).json({ 
        success: false,
        error: 'No file uploaded',
        received: req.body 
      });
    }

    const { webhookUrl, fileName, timestamp } = req.body;
    
    if (!webhookUrl) {
      console.log('❌ [AUDIO] Missing webhookUrl in request body');
      return res.status(400).json({ 
        success: false,
        error: 'Missing webhookUrl in request body',
        received: req.body 
      });
    }

    console.log(`📋 [AUDIO] Processing file: ${req.file.originalname} (${req.file.size} bytes)`);
    console.log(`📤 [AUDIO] Forwarding to n8n: ${webhookUrl}`);

    const formData = new NodeFormData();
    formData.append('file', new Blob([req.file.buffer], { type: req.file.mimetype }), req.file.originalname);
    formData.append('fileName', fileName || req.file.originalname);
    formData.append('timestamp', timestamp || new Date().toISOString());
    formData.append('source', 'dev-server-audio-uploader');

    const response = await fetch(webhookUrl, {
      method: 'POST',
      body: formData as any,
      headers: {
        'User-Agent': 'Dev-Server-Audio-Proxy/1.0',
      }
    });

    console.log(`📥 [AUDIO] n8n response: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      console.log(`❌ [AUDIO] n8n error: ${response.status} ${response.statusText}`);
      return res.status(200).json({
        success: false,
        error: `n8n webhook returned ${response.status}: ${response.statusText}`,
        details: {
          status: response.status,
          statusText: response.statusText,
          webhookUrl: webhookUrl
        }
      });
    }

    const responseText = await response.text();
    console.log(`📄 [AUDIO] Raw n8n response: "${responseText}"`);

    let result;
    try {
      result = JSON.parse(responseText);
      console.log('✅ [AUDIO] Parsed n8n JSON response successfully');
    } catch (parseError) {
      console.log('📝 [AUDIO] n8n response was not JSON, treating as text');
      result = { message: responseText, raw: responseText };
    }

    const successResponse = {
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
      source: 'dev-server-audio-backend-proxy',
      webhookUrl: webhookUrl,
      fileName: req.file.originalname,
      fileSize: req.file.size
    };

    console.log('✅ [AUDIO] Sending success response to frontend');
    res.json(successResponse);

  } catch (error) {
    console.log(`❌ [AUDIO] Upload error: ${error instanceof Error ? error.message : 'Unknown error'}`);

    if (error instanceof multer.MulterError) {
      if (error.code === 'LIMIT_FILE_SIZE') {
        return res.status(200).json({
          success: false,
          error: 'File too large. Maximum size is 50MB.',
          details: error.message
        });
      }
    }

    res.status(200).json({
      success: false,
      error: 'Internal server error while processing audio upload',
      details: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    });
  }
});

// Serve static files from the client build
app.use(express.static('client/dist'));

// Catch-all route to serve the React app
app.get('*', (req, res) => {
  res.sendFile('client/dist/index.html', { root: '.' });
});

const httpServer = createServer(app);
const port = process.env.PORT || 5000;

httpServer.listen(port, () => {
  console.log(`🚀 Dev server running on port ${port}`);
  console.log(`📱 Frontend: http://localhost:${port}`);
  console.log(`🔌 API: http://localhost:${port}/api`);
  console.log(`🔄 n8n Webhook: http://localhost:${port}/api/webhook/n8n`);
  console.log(`📄 PDF Upload: http://localhost:${port}/api/upload-pdf`);
  console.log(`🖼️ Image Upload: http://localhost:${port}/api/upload-image`);
  console.log(`🎬 Video Upload: http://localhost:${port}/api/upload-video`);
  console.log(`🎵 Audio Upload: http://localhost:${port}/api/upload-audio`);
});
