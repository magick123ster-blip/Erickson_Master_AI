@echo off
setlocal
echo ===================================================
echo   밀턴 에릭슨 전략 AI - 자동 환경 설정 도구
echo ===================================================
echo.

:: 1. 파이썬 설치 여부 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] 파이썬이 설치되어 있지 않습니다.
    echo python.org에서 Python 3.10 이상을 설치한 후 다시 시도해 주세요.
    pause
    exit /b
)

echo [1/3] 필수 라이브러리 설치를 시작합니다...
python -m pip install --upgrade pip
python -m pip install streamlit chromadb sentence-transformers pandas openai tqdm

echo.
echo [2/3] 데이터베이스 무결성을 확인합니다...
if not exist "erickson_vector_db" (
    echo [경고] erickson_vector_db 폴더가 없습니다. 
    echo 데이터베이스가 포함된 압축 파일을 제대로 풀었는지 확인해 주세요.
) else (
    echo 데이터베이스 확인 완료.
)

echo.
echo [3/3] 실행 바로가기를 점검합니다...
echo python -m streamlit run erickson_chatbot.py > "에릭슨_챗봇_실행하기.bat"

echo.
echo ===================================================
echo   설치가 완료되었습니다! 
echo   이제 '에릭슨_챗봇_실행하기.bat'를 더블 클릭하세요.
echo ===================================================
echo.
pause
