import numpy as np
import matplotlib.pyplot as plt
# from parse import parse
import parse
import xlwt

node_cnt = 4
thread_cnt = 5
meta = "node,thread,remote_ratio,shared_ratio,read_ratio,space_locality,time_locality,op_type,memory_type,item_size,t_thr,a_thr,a_lat,cache_th"
stat_names = meta.split(',')
stats = {}
test_systems = {"gam", "gam-decentralized1", "gam-decentralized2"}
shared_ratios = [0, 20, 40, 60, 80, 100]
remote_ratios = [0, 30, 60, 75]
read_ratios = [0, 20, 40, 60, 80, 100]
op_types = [0, 1]

def parse_benchmark_log(log_dir):

    for log_name in test_systems:
        stats[log_name] = {}
        log_path = log_dir + '/' + log_name + '.log'
        with open(log_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                datas = line.strip().split(',')
                if len(datas) < len(stat_names):
                    continue
                remote_ratio = int(datas[2])
                shared_ratio = int(datas[3])
                read_ratio = int(datas[4])
                op_type = int(datas[7])
                throughput = int(datas[10])
                if op_type not in stats[log_name]:
                    stats[log_name][op_type] = {}
                if remote_ratio not in stats[log_name][op_type]:
                    stats[log_name][op_type][remote_ratio] = {}
                if shared_ratio not in stats[log_name][op_type][remote_ratio]:
                    stats[log_name][op_type][remote_ratio][shared_ratio] = {}
                if read_ratio not in stats[log_name][op_type][remote_ratio][shared_ratio]:
                    stats[log_name][op_type][remote_ratio][shared_ratio][read_ratio] = {}
                stats[log_name][op_type][remote_ratio][shared_ratio][read_ratio] = throughput
    pass

def plot_benchmark(save = False):
    # bar_width = 0.2
    # index0 = np.arange(len(dbs))
    # fig, axes = plt.subplots(6, 4, sharex=True, sharey=False)
    # fig.text(0.9, 0.03, 'DB Type', ha='right')
    # types = ["Q1", "Q1*"]

    # for i in range(0, 2):
    #     j = -1
    #     type = types[i]
    #     for group in groups[type]:
    #         j += 1
    #         axes[j, i].bar(index0, groups[type][group]["before"], width=bar_width, color='#33CCFF', edgecolor='grey', hatch='\\', label="Before Update")
    #         axes[j, i].bar(index0 + bar_width, groups[type][group]["after"], width=bar_width, color='royalblue', edgecolor='black', hatch='', label="After Update")
    #         # only show one legend
    #         if j == 0 and i == 1:
    #             axes[j, i].legend(fontsize=8, loc="upper right")
    #         # do not show ylabels of the 2-th column plots
    #         if j == 0:
    #             axes[j, i].set_ylim(0, 11000)
    #             axes[j, i].yaxis.set_major_locator(plt.MultipleLocator(2000))
    #             if i == 0:
    #                 axes[j, i].set_ylabel("Elapsed Time(ms)")
    #         elif j == 1:
    #             axes[j, i].set_ylim(0, 1.1)
    #             axes[j, i].yaxis.set_major_locator(plt.MultipleLocator(0.2))
    #             if i == 0:
    #                 axes[j, i].set_ylabel("Accessed Size(GB)", labelpad=19) # labelpad controls label loc
    #         elif j == 2:
    #             axes[j, i].set_ylim(0, 0.22)
    #             axes[j, i].yaxis.set_major_locator(plt.MultipleLocator(0.04))
    #             if i == 0:
    #                 axes[j, i].set_ylabel("Seek Ratio(%)", labelpad=12)
    #
    #         # do not show yticks of the 2-th column plots
    #         if i == 1:
    #             # axes[j, i].yaxis.set_visible(False)
    #             axes[j, i].yaxis.set_ticklabels([])
    #
    #         # show yaxis grid
    #         axes[j, i].grid(axis='y', linestyle=":", color="silver")
    #
    #     # set title and xticks only for the bottom plot
    #     axes[j, i].set_title(type, y=-0.5)
    #     axes[j, i].set_xticks(index0 + bar_width / 2, dbs, rotation=0,fontsize=9)

    fig, axes = plt.subplots(6, 4, sharex=True, sharey=False)
    # fig.text(0.9, 0.03, 'DB Type', ha='right')
    picked_op_type = 1
    i = 0
    for share_ratio in shared_ratios:
        j = 0
        for remote_ratio in remote_ratios:
            for test_system in test_systems:
                throughput = []
                for read_ratio in read_ratios:
                    if share_ratio in stats[test_system][picked_op_type][remote_ratio]:
                        if read_ratio in stats[test_system][picked_op_type][remote_ratio][share_ratio]:
                            throughput.append(stats[test_system][picked_op_type][remote_ratio][share_ratio][read_ratio])
                        else:
                            throughput.append(0)
                    else:
                        throughput.append(0)
                axes[i, j].plot(read_ratios, throughput, label=test_system)
            j += 1
        i += 1

    # adjust space among subplots
    # plt.subplots_adjust(wspace=0.1, hspace=0.4)
    # plt.grid(axis='y', linestyle=":", color="silver", alpha=0.5)
    # plt.xticks()
    if save:
        plt.savefig("figures/figure3-3" + ".pdf")
    plt.show()
    pass

def plot_benchmark_single(remote_ratio=0, save=False):
    fig, axes = plt.subplots(6, 1, sharex=True, sharey=False)
    # fig.text(0.9, 0.03, 'DB Type', ha='right')
    picked_op_type = 1
    i = 0
    picked_remote_ratios = [remote_ratio]
    picked_read_ratios = [20, 40, 60, 80]
    for share_ratio in shared_ratios:
        j = 0
        for remote_ratio in picked_remote_ratios:
            for test_system in test_systems:
                throughput = []
                for read_ratio in picked_read_ratios:
                    if share_ratio in stats[test_system][picked_op_type][remote_ratio]:
                        if read_ratio in stats[test_system][picked_op_type][remote_ratio][share_ratio]:
                            throughput.append(stats[test_system][picked_op_type][remote_ratio][share_ratio][read_ratio])
                        else:
                            throughput.append(0)
                    else:
                        throughput.append(0)
                axes[i].plot(picked_read_ratios, throughput, label=test_system)
                axes[i].legend(fontsize=8, loc="upper right")
            # j += 1
        i += 1

    # adjust space among subplots
    # plt.subplots_adjust(wspace=0.1, hspace=0.4)
    # plt.grid(axis='y', linestyle=":", color="silver", alpha=0.5)
    # plt.xticks()
    if save:
        plt.savefig("figures/figure3-3" + ".pdf")
    plt.show()
    pass

if __name__ == "__main__":
    log_dir = "logs/gam-logs-benchmark"
    parse_benchmark_log(log_dir)
    # plot_benchmark(False)
    plot_benchmark_single(75)
    pass
