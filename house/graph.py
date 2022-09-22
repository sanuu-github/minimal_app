#参考サイトhttps://di-acc2.com/programming/python/5322/

import matplotlib.pyplot as plt
import base64
from io import BytesIO


#プロットしたグラフを画像データとして出力するための関数
def Output_Graph():
	buffer=BytesIO()                     #バイナリI/O(画像や音声データを取り扱う際に利用)
	plt.savefig(buffer,format="png")     #png形式の画像データを取り扱う
	buffer.seek(0)                       #ストリーム先頭のoffset byteに変更
	img=buffer.getvalue()                #バッファの全内容を含むbytes
	graph=base64.b64encode(img)          #画像ファイルをbase64でエンコード
	graph=graph.decode("utf-8")          #デコードして文字列から画像に変換
	buffer.close()
	return graph


#グラフをプロットするための関数>>棒グラフ用
def Plot_Graph(x,y):
	plt.switch_backend("AGG")             #スクリプトを出力させない
	plt.figure(figsize=(5.5,4.5))         #グラフサイズ
	plt.bar(x,y)                          #グラフ作成
	plt.xticks(rotation=0)                #X軸値を45度傾けて表示
	plt.title("Revenue per Date")         #グラフタイトル
	plt.xlabel("Date")                    #xラベル
	plt.ylabel("Reveueモノサイズ")         #yラベル
	plt.tight_layout()                    #レイアウト
	graph = Output_Graph()                #グラフプロット
	return graph


#グラフをプロットするための関数>>円グラフ用
def Plot_PieChart(p,l):
    plt.rcParams['font.family']='Yu Gothic'                 #日本語表示する設定
    c=["skyblue",'powderblue','lightcyan','cadetblue',"cornflowerblue"]  #円グラフの色の設定。順番に適用されて最後まできたら最初に戻り繰り返す。
    plt.switch_backend("AGG")
    plt.figure(figsize=(5,4))                              #グラフの画像サイズ　円グラフを描画。デフォルトは3時の方向から開始
    wedgeprops={"edgecolor":"white", "width":0.7}          #扇状の周りの白い線（隙間）
    textprops={"size":"large"}
    plt.pie(p,autopct="%d%%",labels=l,colors=c,            #autopoct:比率を表示するようにしている。小数点第一位まで表示するときはautopct='%.1f%%'。
    counterclock=False,startangle=90,                      #counterclock=Falseで時計回り。startangle=90で12時の方向から開始
    radius=1.5,center=(0,0),wedgeprops=wedgeprops,         #radius:エングラフのサイズ
    labeldistance=0.75,textprops=textprops)                #ラベルの位置 小さいと円の上、大きいと円の外
    #plt.title('内訳', fontsize=10)                        #グラフのタイトルを設定

    graph = Output_Graph()
    return graph