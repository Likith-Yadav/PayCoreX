# Script to resolve Git merge conflict and push changes

Write-Host "Step 1: Aborting unfinished merge..." -ForegroundColor Yellow
git merge --abort

Write-Host "`nStep 2: Staging all changes..." -ForegroundColor Yellow
git add .

Write-Host "`nStep 3: Committing changes..." -ForegroundColor Yellow
git commit -m "Update PayCoreX: Custom admin branding, Documentation page fixes, Node.js 24.x"

Write-Host "`nStep 4: Pulling remote changes with rebase..." -ForegroundColor Yellow
git pull --rebase origin main

Write-Host "`nStep 5: Pushing to remote..." -ForegroundColor Yellow
git push origin main

Write-Host "`n✅ Done! Changes pushed successfully." -ForegroundColor Green

