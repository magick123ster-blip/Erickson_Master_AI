import os
import subprocess
import markdown

# Paths
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
MD_PATH = os.path.join(DATA_DIR, 'erickson_data_overview_report.md')
HTML_PATH = os.path.join(DATA_DIR, 'temp_overview_report.html')
PDF_PATH = os.path.join(DATA_DIR, 'erickson_data_overview_report.pdf')

def convert():
    if not os.path.exists(MD_PATH):
        print(f"Error: Markdown file not found at {MD_PATH}")
        return

    print("Reading Markdown...")
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML properly
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # 2. Prepare HTML for PDF
    print("Creating temporary HTML for PDF conversion...")
    # Add modern styling for a premium feel (Aesthetics)
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #2c3e50; max-width: 1000px; margin: 40px auto; padding: 40px; background: #fff; }}
            h1 {{ color: #1a2a3a; border-bottom: 3px solid #3498db; padding-bottom: 15px; font-size: 2.5em; }}
            h2 {{ color: #e67e22; border-bottom: 1px solid #ddd; margin-top: 50px; font-size: 1.8em; }}
            h3 {{ color: #2980b9; margin-top: 30px; background: #f8f9fa; padding: 10px; border-radius: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.85em; table-layout: fixed; }}
            th, td {{ border: 1px solid #eee; padding: 12px; text-align: left; overflow: hidden; word-wrap: break-word; }}
            th {{ background-color: #34495e; color: white; text-transform: uppercase; letter-spacing: 1px; width: 25%; }}
            td {{ vertical-align: top; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            code {{ background-color: #f1f2f6; color: #e74c3c; padding: 2px 6px; border-radius: 3px; font-family: 'Consolas', 'Courier New', monospace; font-size: 0.9em; }}
            .sequence {{ background: #fdfdfd; border-left: 5px solid #3498db; padding: 15px; margin: 20px 0; font-style: italic; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }}
            blockquote {{ background: #f9f9f9; border-left: 10px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px; }}
            hr {{ border: 0; border-top: 2px solid #3498db; margin: 40px 0; opacity: 0.2; }}
            @media print {{
                body {{ padding: 20px; }}
                h2, h3 {{ page-break-after: avoid; }}
                table {{ page-break-inside: auto; }}
                tr {{ page-break-inside: avoid; page-break-after: auto; }}
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_template)

    # 3. Convert HTML to PDF using Headless Edge
    print(f"Generating PDF using Microsoft Edge: {PDF_PATH}")
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "msedge"
    ]
    
    success = False
    for path in edge_paths:
        try:
            subprocess.run([
                path,
                "--headless",
                "--disable-gpu",
                "--no-sandbox", # Often needed in containerized/agent environments
                "--print-to-pdf=" + PDF_PATH,
                HTML_PATH
            ], check=True, capture_output=True)
            success = True
            print(f"Successfully generated PDF using {path}")
            break
        except Exception as e:
            continue
            
    if not success:
        print("Error: Could not find Microsoft Edge or failed to print to PDF.")
    
    if os.path.exists(HTML_PATH):
        os.remove(HTML_PATH)

if __name__ == "__main__":
    convert()
