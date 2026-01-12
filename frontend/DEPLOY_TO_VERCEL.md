# 🚀 Deploy PayCoreX Frontend to Vercel

## ✅ Fixed Issues

- ✅ PostCSS config renamed to `.cjs` for CommonJS compatibility
- ✅ Package.json configured correctly
- ✅ Build verified and working
- ✅ Vercel configuration optimized

## Quick Deployment Steps

### Step 1: Push Code to GitHub

```bash
cd /home/ubuntu/PayCoreX
git add frontend/
git commit -m "Frontend ready for Vercel deployment"
git push origin main
```

### Step 2: Deploy via Vercel Dashboard

1. **Go to Vercel**: https://vercel.com/new
2. **Import Git Repository**: Connect GitHub and select PayCoreX repo
3. **Configure Project**:
   - **Root Directory**: `frontend` ⚠️ **CRITICAL - Set this!**
   - Framework will auto-detect as Vite
   - Build settings will auto-detect

4. **Add Environment Variable**:
   - Click "Environment Variables"
   - Add:
     - **Name**: `VITE_API_URL`
     - **Value**: `https://api.buildforu.pw`
     - **Environments**: Select all (Production, Preview, Development)

5. **Deploy**: Click "Deploy" button

### Step 3: Verify

After deployment:
- ✅ Visit your Vercel URL
- ✅ Test login/signup
- ✅ Verify API calls work

## Vercel Settings Summary

| Setting | Value |
|---------|-------|
| Root Directory | `frontend` |
| Framework | Vite (auto) |
| Build Command | `npm run build` (auto) |
| Output Directory | `dist` (auto) |
| Install Command | `npm install` (auto) |
| Node Version | 18.x (default) |

## Environment Variables

**Required:**
```
VITE_API_URL=https://api.buildforu.pw
```

## Alternative: Vercel CLI

```bash
# Install CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Add environment variable
vercel env add VITE_API_URL
# Enter: https://api.buildforu.pw

# Deploy to production
vercel --prod
```

## Troubleshooting

### If Build Still Fails

1. **Check Root Directory**: Must be `frontend` in Vercel settings
2. **Verify Environment Variable**: `VITE_API_URL` must be set
3. **Check Build Logs**: Look for specific errors in Vercel dashboard
4. **Node Version**: Vercel uses Node 18.x by default (should work)

### Common Issues

- **Module not found**: Ensure root directory is `frontend`
- **Build fails**: Check that all dependencies are in `package.json`
- **API calls fail**: Verify `VITE_API_URL` environment variable

## Post-Deployment

### Update Backend CORS (If Needed)

If you get CORS errors, update `core/settings.py`:

```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://your-project.vercel.app",
    "https://buildforu.pw",
]
```

Then restart:
```bash
./manage-services.sh restart
```

## Your URLs

- **Frontend**: `https://your-project.vercel.app`
- **Backend API**: `https://api.buildforu.pw`
- **Documentation**: `https://your-project.vercel.app/docs`

## ✅ Ready to Deploy!

Your frontend is now properly configured for Vercel. Just:
1. Push to GitHub
2. Import in Vercel
3. Set root directory to `frontend`
4. Add environment variable
5. Deploy!
