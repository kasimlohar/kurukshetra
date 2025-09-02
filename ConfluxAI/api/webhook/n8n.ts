import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

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

    // Forward request to n8n webhook
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Vercel-ChatBot-Proxy/1.0',
        'Accept': 'application/json, text/plain, */*'
      },
      body: JSON.stringify({
        message,
        timestamp: timestamp || new Date().toISOString(),
        source: source || 'vercel-chat-backend'
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

    // Get response text first to handle any format
    const responseText = await response.text();
    console.log(`📄 [WEBHOOK] Raw n8n response (full): "${responseText}"`);
    console.log(`📏 [WEBHOOK] Response length: ${responseText.length} characters`);

    let result;
    try {
      result = JSON.parse(responseText);
      console.log('✅ [WEBHOOK] Parsed n8n JSON response successfully');
    } catch (parseError) {
      console.log('📝 [WEBHOOK] n8n response was not JSON, treating as text');
      result = { message: responseText, raw: responseText };
    }

    // Return the result to frontend
    const successResponse = {
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
      source: 'vercel-backend-proxy',
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
}
