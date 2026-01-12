# Vercel Deployment Fix

## Issue
Vite module not found error on Vercel.

## Solution Applied

1. ✅ Pinned Vite version to exact `5.0.8` (no caret)
2. ✅ Added `.nvmrc` to specify Node 18
3. ✅ Simplified `vercel.json` configuration
4. ✅ Ensured `package-lock.json` is committed

## Important: Commit package-lock.json

Make sure `package-lock.json` is committed to Git:

```bash
cd frontend
git add package-lock.json
git commit -m "Add package-lock.json for Vercel"
git push
```

## Vercel Settings

When deploying on Vercel:

1. **Root Directory**: `frontend`
2. **Node Version**: 18.x (specified in `.nvmrc`)
3. **Environment Variable**: `VITE_API_URL=https://api.buildforu.pw`
4. **Build Command**: `npm run build` (auto-detected)
5. **Install Command**: `npm install` (auto-detected)

## If Still Failing

Try these in Vercel project settings:

1. **Override Build Command**: 
   ```
   npm install && npm run build
   ```

2. **Override Install Command**:
   ```
   npm install --legacy-peer-deps
   ```

3. **Node Version**: Set to 18.x explicitly in Vercel settings

## Verify Locally

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

If this works locally, it should work on Vercel.

