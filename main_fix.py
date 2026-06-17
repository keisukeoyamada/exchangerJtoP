import os
from pathlib import Path
import datetime
import shutil
import img2pdf

script_dir = Path(__file__).parent

jpg_root = script_dir / "jpg"
output_root = script_dir / "output"
processed_root = jpg_root / "processed"

os.makedirs(output_root, exist_ok=True)
os.makedirs(processed_root, exist_ok=True)

for subdir in jpg_root.iterdir():
    if not subdir.is_dir() or subdir.name == "processed":
        continue

    # 画像ファイルをソートして取得
    images = sorted([
        str(p) for p in subdir.iterdir()
        if p.suffix.lower() in ('.jpg', '.jpeg', '.png')
    ])

    if not images:
        continue

    now = datetime.datetime.now()
    output_pdf = output_root / f"{subdir.name}_output_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

    # 複数画像を一発でPDF化（中間ファイル不要）
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(images))

    shutil.move(str(subdir), str(processed_root / subdir.name))

print("変換終了")