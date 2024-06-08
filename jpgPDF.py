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
path = script_dir/"jpg"
if not os.path.exists(script_dir/"pdf"):
    os.mkdir(script_dir/"pdf")
else:
    pass
pdf_path = script_dir/"pdf"
os.chdir(path)

#画像を読み込み、pdfファイルに変換
for i in os.listdir(path):
    #pdfファイルの保存名を指定
    pdf_name = pdf_path / ("PDF_" + str(i[0:9]) + ".pdf")

    #Pillowモジュールを使用し画像の読み込み
    img = Image.open(i)
    #img = img.rotate(-90, expand = True)#この部分は画像を回転させる必要がある場合のみ使用

    #画像→pdfファイルに変換
    cov_pdf = img2pdf.convert(i)
    #pdfファイルを読み込み（pdf_nameで指定したpdfがない場合、pdf_nameをファイル名として新規にpdfファイルを作成）
    file = open(pdf_name, "wb")
    #file = open(path, "wb")
    file.write(cov_pdf)
    img.close()
    file.close()

#複数のpdfファイルを結合する
merge = PyPDF2.PdfMerger()
# ファイル名のリストを取得し、昇順にソート
pdf_files = sorted(os.listdir(pdf_path))

for j in pdf_files:
    merge.append(pdf_path / j)

now = datetime.datetime.now()
merge.write(script_dir/"output"/ f"output_{now.strftime('%Y%m%d_%H%M%S')}.pdf")
merge.close()

#結合素材となったpdfを削除
os.chdir(pdf_path)
file_list = glob.glob('./PDF_*.pdf')
print(os.getcwd())
print((file_list))

for file in file_list:
    os.remove(file)

print("変換終了")
