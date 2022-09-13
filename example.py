import datetime
import utils.realtime_graph as realtime_graph

def main():
    now = datetime.datetime.now()
    epoch = 20
    RTDLA = realtime_graph.RealTimeDrawingLossAcc(epoch)
    
    for i in range(epoch):
        RTDLA.plot(i, 1/(i+1), 1/(i+1))
    fname = now.strftime("%Y_%m_%d_%H%M%S") + '_learning-rate.png'
    RTDLA.save(fname)
    #plt.show() #これをつけると最後に表示できる

if __name__ == '__main__':
    main()