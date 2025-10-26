# Railway Deployment Guide

## Quick Start

This project is configured for deployment on Railway.app.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. A Google Gemini API key (get one at [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key))

## Deployment Steps

### 1. Create a New Project on Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose this repository

### 2. Configure Environment Variables

In your Railway project dashboard, go to the **Variables** tab and add:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important**: The app can also save the API key through the web interface, but setting it as an environment variable is recommended for production deployments.

### 3. Deploy

Railway will automatically:
- Detect the Python project
- Install dependencies from `requirements.txt`
- Run the app using the `Procfile` or `railway.json` configuration

### 4. Access Your App

Once deployed, Railway will provide you with a public URL (e.g., `your-app.railway.app`).

## Configuration Files

The following files are used for Railway deployment:

- **`Procfile`**: Tells Railway how to start the app
- **`requirements.txt`**: Python dependencies
- **`railway.json`**: Railway-specific configuration
- **`app.py`**: Main application (configured to use Railway's PORT variable)

## Local Development

To run locally:

```bash
uv run python app.py
```

Or with standard Python:

```bash
pip install -r requirements.txt
python app.py
```

The app will be available at `http://localhost:7860`

## Troubleshooting

### Build Fails

- Check that all dependencies in `requirements.txt` are compatible
- Review the build logs in Railway dashboard

### App Doesn't Start

- Verify the `GEMINI_API_KEY` environment variable is set
- Check the deployment logs for errors

### 404 or Connection Issues

- Ensure the app is binding to `0.0.0.0` (already configured)
- Verify Railway assigned the PORT correctly (already configured)

## Support

For Railway-specific issues, see [Railway Documentation](https://docs.railway.app/)
For app-specific issues, check the main README.md
