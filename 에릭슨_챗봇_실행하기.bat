@echo off
echo ===================================================
echo   밀턴 에릭슨 전략 AI 챗봇을 실행하고 있습니다...
echo ===================================================
echo.
echo 잠시만 기다려 주세요. 웹 브라우저가 자동으로 열립니다.
echo.

cd /d "C:\Users\magic\Downloads\erickson_data"
python -m streamlit run erickson_chatbot.py

pause
