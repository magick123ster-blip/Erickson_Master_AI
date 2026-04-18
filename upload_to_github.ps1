# GitHub 업로드 자동화 스크립트

$repo_url = Read-Host "GitHub 저장소 URL을 입력하세요 (예: https://github.com/사용자명/Erickson_AI.git)"

Write-Host "1. Git 초기화 중..." -ForegroundColor Cyan
git init

Write-Host "2. 대용량 파일 처리(Git LFS) 설정 중..." -ForegroundColor Cyan
git lfs install
# 벡터 DB 내의 대용량 파일들을 LFS로 추적하도록 설정
git lfs track "erickson_vector_db/**"
git add .gitattributes

Write-Host "3. 파일 추가 및 첫 커밋 생성 중..." -ForegroundColor Cyan
git add .
git commit -m "Initial commit: Erickson Master AI with Vector DB"

Write-Host "4. GitHub 연결 및 업로드 시작 (시간이 다소 걸릴 수 있습니다)..." -ForegroundColor Cyan
git branch -M main
git remote add origin $repo_url
git push -u origin main

Write-Host "==========================================" -ForegroundColor Green
Write-Host "  업로드가 완료되었습니다! GitHub를 확인하세요."
Write-Host "=========================================="
