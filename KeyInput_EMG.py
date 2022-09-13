# KeyInput_EMG.py
# 読み取るデータはCH1のみでOK
# spsを測定したい

#import spidev
import os
import csv
import matplotlib.pyplot as plt
from utils.keyinput import GetInputKey
from utils.realtime_graph import RealTimeDrawingLossAcc

"""
#SPI通信準備
spi = spidev.SpiDev()
bus = 1
device = 2
spi.open(bus, device)
spi.max_speed_hz = 100 * 1000   #VDD=5:100ksps, VDD=2.7:50ksps
"""


emg_csv_data = []
emg_plot_data = []
key_data = [[], []]
unicode_dec_dict = {}
ax_x_list = []
data_n = 0

#unicodeのコードポイントと文字を紐づけて辞書化
with open('unicode_dec_list.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        unicode_dec_dict[row[0]] = row[1]

#筋電位波形描画の設定
fig, axes = plt.subplots(nrows=1, ncols=1, sharex=False)    #プロットエリアの設定
lines,  = axes.plot(0, 0, '-ok')  #一度描画してlinesを取得


with GetInputKey() as gik:
    while True:
        #波形データの取得と記録
        """
        raw_data = spi.xfer2([0x06, 0x00, 0x00])
        adc_data = ((raw_data[1] & 0x0F) << 8) | raw_data[2]
        emg_csv_data.append(str(2.048*adc_data/4096) + '\n')
        emg_plot_data.append(2.048*adc_data/4096)
        """
        emg_csv_data.append(str(data_n)+'\n')   #debug
        emg_plot_data.append(data_n)    #debug
        ax_x_list.append(data_n)

        #何かキーが押された時
        if gik.is_key_down():
            #押されたキーを取得
            push_key_codepoint = gik.get_key_unicode_codepoint()
            push_key_string = unicode_dec_dict[str(push_key_codepoint)]

            #キーのデータと配列番号を記録(0:キー名, 1:配列番号)
            key_data[0].append(push_key_string)
            key_data[1].append(data_n)

            #リアルタイム描画 - 軸の設定
            axes.set_xlim(0, max(ax_x_list)+1)  #x軸の設定
            axes.set_ylim(min(emg_plot_data)-1, max(emg_plot_data)-1)   #y軸の設定

            #リアルタイム描画 - データの追加
            lines.set_data(ax_x_list, emg_plot_data)

            #Escキー(unicode-codepoint=27)が押されたら終了
            if push_key_codepoint == 27:
                print(' \nEsc')
                break
        plt.pause(0.000001)
        
        data_n += 1

print(key_data)

"""
file_number = 0
file_name = '{:08}.csv'.format(file_number)
dataset_folder = 'dataset'
data_folder = 'data'

#通し番号の最後の番号をチェック
while True:
    file_name = '{:08}.csv'.format(file_number)
    file_path = os.path.join(dataset_folder, data_folder, file_name)
    if not os.path.exists(file_path):
        break
    file_number += 1

#キーごとに波形を分割して保存
start = 0
end = 0

for n in range(len(key_data[0])):
    #データを分割
    end = key_data[1][n] + 1  #キーが入力された瞬間の配列番号を取得
    emg_key_data = emg_csv_data[start:end]
    start = end

    #ファイルを保存
    file_name = '{:08}.csv'.format(file_number)
    file_path = os.path.join(dataset_folder, data_folder, file_name)
    with open(file_path, 'w') as f_file:
        f_file.writelines(emg_key_data)
    
    #ファイルとキーを紐づけるファイルを作成
    dataset_structure_path = os.path.join(dataset_folder, 'dataset_key.csv')
    with open(dataset_structure_path, 'a') as f_structure:
        writer = csv.writer(f_structure)
        writer.writerow([file_name, key_data[0][n]])
    
    file_number += 1
"""