@echo off
title Erickson AI Setup
echo [Erickson AI] 다른 컴퓨터에서 실행하기 위한 환경 설정을 시작합니다...
echo.
echo 1. 파이썬 라이브러리 설치 중 (인터넷 연결 필요)...
pip install -r "%~dp0requirements.txt"
echo.
echo [완료] 모든 환경 설정이 끝났습니다! 
echo 이제 '에릭슨_훈련센터_실행하기.bat' 파일을 눌러서 실행하세요.
echo.
pause
