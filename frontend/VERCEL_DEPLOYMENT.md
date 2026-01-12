# Deploy PayCoreX Frontend to Vercel

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub/GitLab/Bitbucket**: Your code should be in a Git repository

## Quick Deployment Steps

### Option 1: Deploy via Vercel Dashboard

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Go to Vercel Dashboard**:
   - Visit [vercel.com/new](https://vercel.com/new)
   - Import your Git repository
   - Select the repository containing PayCoreX

3. **Configure Project**:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Environment Variables**:
   Add the following environment variable:
   ```
   VITE_API_URL=https://api.buildforu.pw
   ```

5. **Deploy**: Click "Deploy"

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

4. **Deploy**:
   ```bash
   vercel
   ```

5. **Set Environment Variable**:
   ```bash
   vercel env add VITE_API_URL
   # Enter: https://api.buildforu.pw
   ```

6. **Redeploy with environment variable**:
   ```bash
   vercel --prod
   ```

## Environment Variables

### Required
- `VITE_API_URL`: Your backend API URL
  - Production: `https://api.buildforu.pw`
  - Development: `http://localhost:8000`

### Setting in Vercel Dashboard

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://api.buildforu.pw`
   - **Environment**: Production, Preview, Development (select all)

## Project Configuration

The `vercel.json` file is already configured with:
- ✅ Build command: `npm run build`
- ✅ Output directory: `dist`
- ✅ SPA routing (all routes redirect to index.html)
- ✅ Asset caching headers

## Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your domain: `buildforu.pw` or `www.buildforu.pw`
4. Follow DNS configuration instructions

## Post-Deployment Checklist

- [ ] Verify environment variable `VITE_API_URL` is set
- [ ] Test login/signup functionality
- [ ] Test API calls from frontend
- [ ] Verify all routes work (SPA routing)
- [ ] Check console for any errors
- [ ] Test on mobile devices

## Troubleshooting

### Build Fails
- Check Node.js version (Vercel uses Node 18+ by default)
- Verify all dependencies are in `package.json`
- Check build logs in Vercel dashboard

### API Calls Fail
- Verify `VITE_API_URL` is set correctly
- Check CORS settings on backend
- Verify API endpoint is accessible

### Routes Not Working
- Ensure `vercel.json` has rewrite rules
- Check that all routes redirect to `/index.html`

## Production URL

After deployment, your frontend will be available at:
- `https://your-project-name.vercel.app`
- Or your custom domain if configured

## Update Backend CORS (If Needed)

If you get CORS errors, update your Django settings:

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-project.vercel.app",
    "https://buildforu.pw",
    "https://www.buildforu.pw",
]
```

## Continuous Deployment

Vercel automatically deploys on every push to your main branch:
- Push to `main` → Production deployment
- Push to other branches → Preview deployment

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support

