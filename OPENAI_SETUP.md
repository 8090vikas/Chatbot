# OpenAI API Key Setup Instructions

## Quick Setup

### Method 1: Environment Variable (Recommended)
1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. Restart the Streamlit app

### Method 2: .env File
1. Create a `.env` file in the project root
2. Add your API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
3. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```
4. Add this to your app.py:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Getting Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-`)
5. Keep it secure - don't share it publicly

## Testing the Setup

Once configured, you should see:
- ✅ "OpenAI API key configured!" in the sidebar
- Real AI responses instead of demo messages
- Full functionality of all AI models and personalities

## Troubleshooting

- **"API key not configured"**: Make sure the environment variable is set correctly
- **"Invalid API key"**: Check that your key is correct and has credits
- **"Rate limit exceeded"**: You may need to upgrade your OpenAI plan

## Cost Information

- GPT-3.5 Turbo: ~$0.002 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens  
- GPT-4 Turbo: ~$0.01 per 1K tokens

Monitor your usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)
