from model_allout import full_model_out
import numpy as np
import matplotlib.pyplot as plt

optim = [24.806892787238745,2.495102258810802,7.590108557252777,6.7059058664457005]
names = ["Cabin length [m]", "Cabin width [m]", "Empennage length [m]", "Boat-tail angle [deg]"]

for c in range(0,len(optim)):
    var = optim[c]
    optyRange,_,_ = full_model_out(optim)
    _,optyPAX,_ = full_model_out(optim)
    lower = var - 0.5*var
    upper = var + 0.5*var
    xs = np.linspace(lower, upper, 80)
    ysRange = np.zeros([80])
    ysPM = np.zeros([80])
    for i in range(0,len(xs)):
        new = xs[i]
        optim_this = [new if item==var else item for item in optim]
        res = full_model_out(optim_this)
        ysRange[i] = res[0]
        ysPM[i] = res[1] #0 for range, 2 for paxMiles

    plt.figure(c)
    fig, ax1 = plt.subplots()
    color='tab:blue'
    ax1.set_xlabel(names[c])
    ax1.set_ylabel('Range [nm]', color=color)
    ax1.plot(xs, ysRange, color=color)
    ax1.plot(var, optyRange, 'x', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    if c==2:
        ax1.set_xlim(3.8, 9.4)
    elif c==3:
        ax1.set_xlim(3.33, 8.3)
    else:
        pass

    ax2 = ax1.twinx()
    color='tab:red'
    ax2.set_ylabel('PAX', color=color)
    ax2.plot(xs, ysPM, color=color)
    ax2.plot(var, optyPAX, 'x', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout() 

plt.show()