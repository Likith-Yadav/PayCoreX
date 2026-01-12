# 🚀 Deploy PayCoreX Frontend to Vercel

## Quick Deployment Guide

### Step 1: Prepare Your Code

```bash
cd /home/ubuntu/PayCoreX/frontend

# Make sure everything is committed
git add .
git commit -m "Ready for Vercel deployment"
git push
```

### Step 2: Deploy via Vercel Dashboard

1. **Go to Vercel**: https://vercel.com/new
2. **Import Git Repository**: Connect your GitHub/GitLab account
3. **Select Repository**: Choose the PayCoreX repository
4. **Configure Project**:
   - **Root Directory**: `frontend` ⚠️ IMPORTANT
   - **Framework Preset**: Vite (auto-detected)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

5. **Add Environment Variable**:
   - Click "Environment Variables"
   - Add:
     - **Name**: `VITE_API_URL`
     - **Value**: `https://api.buildforu.pw`
     - **Environment**: Select all (Production, Preview, Development)

6. **Deploy**: Click "Deploy" button

### Step 3: Verify Deployment

After deployment completes:
- ✅ Visit your Vercel URL: `https://your-project.vercel.app`
- ✅ Test login/signup
- ✅ Verify API calls work
- ✅ Check all routes work

## Alternative: Deploy via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Navigate to frontend
cd frontend

# Deploy
vercel

# Add environment variable
vercel env add VITE_API_URL production
# Enter: https://api.buildforu.pw

# Deploy to production
vercel --prod
```

## Environment Variables

**Required:**
- `VITE_API_URL` = `https://api.buildforu.pw`

## Custom Domain Setup

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain: `buildforu.pw` or `www.buildforu.pw`
3. Follow DNS instructions:
   - Add A record pointing to Vercel's IP
   - Or add CNAME record pointing to Vercel's domain

## Post-Deployment

### Update Backend CORS (If Needed)

If you get CORS errors, update `core/settings.py`:

```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://your-project.vercel.app",
    "https://buildforu.pw",
    "https://www.buildforu.pw",
]
```

Then restart backend:
```bash
./manage-services.sh restart
```

## Troubleshooting

### Build Fails
- ✅ Check Node.js version (Vercel uses 18.x)
- ✅ Verify all dependencies in `package.json`
- ✅ Check build logs in Vercel dashboard

### API Calls Fail
- ✅ Verify `VITE_API_URL` environment variable is set
- ✅ Check backend CORS settings
- ✅ Verify API is accessible: `curl https://api.buildforu.pw`

### Routes Not Working
- ✅ `vercel.json` is configured with SPA rewrites
- ✅ All routes should redirect to `/index.html`

## Your URLs

- **Frontend (Vercel)**: `https://your-project.vercel.app`
- **Backend API**: `https://api.buildforu.pw`
- **Documentation**: `https://your-project.vercel.app/docs`

## Continuous Deployment

Vercel automatically deploys:
- ✅ Push to `main` branch → Production
- ✅ Push to other branches → Preview deployment

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support

