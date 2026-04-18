git init
git lfs install
git lfs track "erickson_vector_db/**"
git add .
git commit -m "Initial commit: Erickson Master AI with Vector DB"
git branch -M main
git remote remove origin
git remote add origin https://github.com//Erickson_Master_AI.git
git push -f origin main
Write-Host "업로드 최종 완료!" -ForegroundColor Green
