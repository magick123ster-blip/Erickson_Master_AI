Write-Host "1. Git 초기화 중..." -ForegroundColor Cyan
git init
git lfs install
git lfs track "erickson_vector_db/**"
git add .gitattributes
git add .
git commit -m "Initial commit: Erickson Master AI with Vector DB"
git branch -M main
git remote add origin https://github.com//Erickson_Master_AI.git
git push -f origin main
Write-Host "업로드 완료!" -ForegroundColor Green
