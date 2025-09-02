import type { VercelRequest, VercelResponse } from '@vercel/node';
import { FormData } from 'formdata-node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    console.log('🖼️ [IMAGE] Received image upload request');
    
    // Check if we have form data
    if (!req.body || !req.body.file) {
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

    console.log(`📋 [IMAGE] Processing file: ${fileName} (${req.body.file.length} bytes)`);
    console.log(`📤 [IMAGE] Forwarding to n8n: ${webhookUrl}`);

    // Prepare form data for n8n
    const formData = new FormData();
    formData.append('file', new Blob([req.body.file], { type: req.body.mimeType || 'image/jpeg' }), fileName);
    formData.append('fileName', fileName);
    formData.append('timestamp', timestamp || new Date().toISOString());
    formData.append('source', 'vercel-image-uploader');

    // Forward to n8n webhook
    const response = await fetch(webhookUrl, {
      method: 'POST',
      body: formData as any,
      headers: {
        'User-Agent': 'Vercel-Image-Proxy/1.0',
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

    // Get response text first to handle any format
    const responseText = await response.text();
    console.log(`📄 [IMAGE] Raw n8n response (full): "${responseText}"`);
    console.log(`📏 [IMAGE] Response length: ${responseText.length} characters`);

    let result;
    try {
      result = JSON.parse(responseText);
      console.log('✅ [IMAGE] Parsed n8n JSON response successfully');
    } catch (parseError) {
      console.log('📝 [IMAGE] n8n response was not JSON, treating as text');
      result = { message: responseText, raw: responseText };
    }

    // Return the result to frontend
    const successResponse = {
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
      source: 'vercel-image-backend-proxy',
      webhookUrl: webhookUrl,
      fileName: fileName,
      fileSize: req.body.file.length
    };

    console.log('✅ [IMAGE] Sending success response to frontend');
    res.json(successResponse);

  } catch (error) {
    console.log(`❌ [IMAGE] Upload error: ${error instanceof Error ? error.message : 'Unknown error'}`);

    res.status(200).json({
      success: false,
      error: 'Internal server error while processing image upload',
      details: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    });
  }
}
