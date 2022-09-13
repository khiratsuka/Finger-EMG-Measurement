# realtime_graph.py
# グラフのリアルタイム描画

import matplotlib.pyplot as plt

class RealTimeDrawingLossAcc:
    def __init__(self, ax_xlim, loss_graph_setting='-ok', acc_graph_setting='-ok'):
        self.ax_xlim = ax_xlim  #x軸の最大値
        self.fig, self.axes = plt.subplots(nrows=1, ncols=2, sharex=False)   #プロットエリアの生成
        self.ax_x_list = [] #x軸の値を格納するリスト
        self.loss, self.acc = [], []    #プロットする値を格納するリスト

        self.axes[0].set_xlim(0, ax_xlim)    #loss, x軸の最大値を設定
        self.axes[1].set_xlim(0, ax_xlim)    #acc,  x軸の最大値を設定
        
        self.lines_loss, = self.axes[0].plot(0, 0, loss_graph_setting)
        self.lines_acc, = self.axes[1].plot(0, 0, acc_graph_setting)

    def plot(self, n_epoch, n_loss, n_acc):
        #描画する値を描画用リストへ追加
        self.ax_x_list.append(n_epoch)
        self.loss.append(n_loss)
        self.acc.append(n_acc)

        #軸の調整
        self.axes[0].set_ylim(min(self.loss)-1, max(self.loss)+1)
        self.axes[1].set_ylim(min(self.acc)-1, max(self.acc)+1)

        #データを追加
        self.lines_loss.set_data(self.ax_x_list, self.loss)
        self.lines_acc.set_data(self.ax_x_list, self.loss)
        
        #描画
        plt.pause(0.01)
    
    def save(self, file_name):
        self.fig.savefig(file_name, dpi=300)

