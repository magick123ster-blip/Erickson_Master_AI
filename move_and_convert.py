import os
import shutil
import subprocess

# Paths
SRC_MD = r'C:\Users\magic\.gemini\antigravity\brain\c371ebd9-48cd-4a01-be5c-3b40b7433da7\erickson_situational_best_10.md'
DEST_DIR = r'C:\Users\magic\Downloads\erickson_data'
DEST_MD = os.path.join(DEST_DIR, 'erickson_situational_best_10.md')
DEST_TXT = os.path.join(DEST_DIR, 'erickson_situational_best_10.txt')
DEST_PDF = os.path.join(DEST_DIR, 'erickson_situational_best_10.pdf')
DEST_HTML = os.path.join(DEST_DIR, 'temp_for_pdf.html')

def execute_task():
    # 1. Copy original MD to public folder
    print(f"Copying MD file to {DEST_DIR}...")
    try:
        shutil.copy2(SRC_MD, DEST_MD)
        print("Copy successful.")
    except Exception as e:
        print(f"Error copying file: {e}")
        return

    # 2. Read content for conversion
    with open(DEST_MD, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Save as TXT
    print(f"Saving TXT version...")
    with open(DEST_TXT, 'w', encoding='utf-8') as f:
        f.write(content)
    print("TXT saved.")

    # 4. Generate PDF via HTML
    print("Generating PDF version...")
    # Add beautiful styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 40px auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #e67e22; border-bottom: 1px solid #eee; margin-top: 40px; }}
            h3 {{ color: #2980b9; margin-top: 25px; background: #f8f9fa; padding: 8px; border-radius: 4px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.9em; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #34495e; color: white; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            code {{ background-color: #eee; padding: 2px 4px; border-radius: 3px; font-family: monospace; }}
            .sequence {{ background: #f4f4f4; border-left: 5px solid #3498db; padding: 10px; margin: 15px 0; font-style: italic; }}
            @media print {{ body {{ padding: 0; }} }}
        </style>
    </head>
    <body>
        {content.replace('\n', '<br>').replace('###', '<h3>').replace('##', '<h2>').replace('#', '<h1>').replace('**Sequence**:', '<div class="sequence"><strong>Sequence</strong>:').replace('`', '<code>').replace('|', '</td><td>').replace('---', '<hr>')}
    </body>
    </html>
    """
    with open(DEST_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Convert to PDF using Edge headless
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "msedge"
    ]
    
    success = False
    for path in edge_paths:
        try:
            subprocess.run([
                path, "--headless", "--no-sandbox", "--disable-gpu", 
                f"--print-to-pdf={DEST_PDF}", DEST_HTML
            ], check=True, capture_output=True)
            success = True
            break
        except:
            continue
    
    if success:
        print("PDF generated successfully.")
    else:
        print("Failed to generate PDF. Please ensure Edge is installed.")
    
    if os.path.exists(DEST_HTML):
        os.remove(DEST_HTML)

if __name__ == "__main__":
    execute_task()
