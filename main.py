#https://kimamani89.com/2019/05/06/post-475/
import os
from PIL import Image
import img2pdf
import PyPDF2
import glob
from pathlib import Path
import datetime

# このスクリプトの場所を基点にする
script_dir = Path(__file__).parent

jpg_root = script_dir / "jpg"
pdf_root = script_dir / "pdf"
output_root = script_dir / "output"

# 必要なフォルダがなければ作成
os.makedirs(pdf_root, exist_ok=True)
os.makedirs(output_root, exist_ok=True)

#画像を読み込み、pdfファイルに変換
for subdir in jpg_root.iterdir():
    if not subdir.is_dir():
        continue
    # サブフォルダごとにpdf保存先を作成
    pdf_path = pdf_root / subdir.name
    os.makedirs(pdf_path, exist_ok=True)

    for i in os.listdir(subdir):
        #pdfファイルの保存名を指定
        # 画像ファイルのみ処理（jpg, jpeg, png など必要に応じて追加）
        if not i.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        img_path = subdir / i
        pdf_name = pdf_path / ("PDF_" + i[0:9] + ".pdf")
        img = Image.open(img_path)
        cov_pdf = img2pdf.convert(str(img_path))
        with open(pdf_name, "wb") as file:
                file.write(cov_pdf)
        img.close()

    #複数のpdfファイルを結合する
    merge = PyPDF2.PdfMerger()
    # ファイル名のリストを取得し、昇順にソート
    pdf_files = sorted(os.listdir(pdf_path))

    for j in pdf_files:
        pdf_file_path = pdf_path / j
        # ファイルサイズが0の場合はスキップ
        if os.path.getsize(pdf_file_path) == 0:
            continue
        merge.append(pdf_file_path)

    now = datetime.datetime.now()
    output_pdf = output_root / f"{subdir.name}_output_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    merge.write(output_pdf)
    merge.close()

    #結合素材となったpdfを削除
    for file in pdf_path.glob('PDF_*.pdf'):
        os.remove(file)

print("変換終了")
