#https://kimamani89.com/2019/05/06/post-475/
import os
from PIL import Image
import img2pdf
import PyPDF2
import glob
from pathlib import Path

#ディレクトリを2つに分けている理由は画像を入れるフォルダとpdfを入れるフォルダを分けるため。
# このスクリプトの場所を基点にする
script_dir = Path(__file__).parent
path = script_dir/"jpg"
if not os.path.exists(script_dir/"output"):
    os.mkdir(script_dir/"output")
else:
    pass
    
pdf_path = script_dir/"output"
#pdf_path = script_dir/"jpg2"
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

    #開いているファイルを閉じる
    img.close()
    file.close()

#複数のpdfファイルを結合する
merge = PyPDF2.PdfMerger()
# ファイル名のリストを取得し、昇順にソート
pdf_files = sorted(os.listdir(pdf_path))

for j in pdf_files:
    merge.append(pdf_path / j)
#for j in os.listdir(pdf_path):
#    merge.append(pdf_path / j)

merge.write(pdf_path / "output.pdf")
merge.close()

#結合素材となったpdfを削除
os.chdir(pdf_path)
file_list = glob.glob('./PDF_*.pdf')
print(os.getcwd())
print((file_list))

for file in file_list:
    os.remove(file)

print("変換終了")
