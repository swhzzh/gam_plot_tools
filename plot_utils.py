# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
# from parse import parse
import parse

kv_sizes = ["8", "16", "32", "64", "128", "256", "512", "1K", "2K", "4K", "8K", "16K"]
block_sizes = ["2K", "4K", "8K", "16K"]
# fanouts = ["5", "10", "20", "40"]
fanouts = ["10", "40", "70", "100"]

latencies = {"fillseq":{}, "readseq":{}, "readrandom":{}, "updaterandom":{}, "deleterandom":{}}
iops = {"fillseq":{}, "readseq":{}, "readrandom":{}, "updaterandom":{}, "deleterandom":{}}
bws = {"fillseq":{}, "readseq":{}, "readrandom":{}, "updaterandom":{}, "deleterandom":{}}
iter_next_cpu_nanos = {}
block_read_times = {}
decompression_times = {}
checksum_times = {}
block_read_counts = {}

cpu_times = {"fillseq":{}, "readseq":{}, "readrandom":{}, "updaterandom":{}, "deleterandom":{}}
elapsed_times = {"fillseq":{}, "readseq":{}, "readrandom":{}, "updaterandom":{}, "deleterandom":{}}
cpu_utilities = {"fillseq":{}, "readseq":{}, "readrandom":{}, "updaterandom":{}, "deleterandom":{}}

# patterns for parsing log
db_name_pattern = parse.compile("DB path: [./test_db/{value_size}-{block_size}-{fanout}]\n")
fillseq_pattern = parse.compile("fillseq      :      {latency} micros/op {iops} ops/sec;  {bw} MB/s\n")
readseq_pattern = parse.compile("readseq      :      {latency} micros/op {iops} ops/sec;  {bw} MB/s PERF_CONTEXT:\n")
readrandom_pattern = parse.compile("readrandom   :     {latency} micros/op {iops} ops/sec;   {bw} MB/s{useless}")
updaterandom_pattern = parse.compile("updaterandom :     {latency} micros/op {iops} ops/sec;  {bw} MB/s{useless}")
deleterandom_pattern = parse.compile("deleterandom :       {latency} micros/op {iops} ops/sec;\n")
patterns = {"fillseq":fillseq_pattern, "readseq":readseq_pattern, "readrandom":readrandom_pattern, "updaterandom":updaterandom_pattern,
            "deleterandom":deleterandom_pattern}


perf_context_pattern = parse.compile(
    "{useless0}block_read_count = {block_read_count}, block_read_byte = {block_read_byte}, block_read_time = {block_read_time}, {useless1}block_checksum_time = {block_checksum_time}, block_decompress_time = {block_decompress_time}, {useless2}iter_read_bytes = {iter_read_bytes}, internal_key_skipped_count = {internal_key_skipped_count}, {useless3}seek_internal_seek_time = {seek_internal_seek_time}, find_next_user_entry_time = {find_next_user_entry_time}, {useless4}new_table_block_iter_nanos = {new_table_block_iter_nanos}, new_table_iterator_nanos = {new_table_iterator_nanos}, {useless5}iter_next_cpu_nanos = {iter_next_cpu_nanos}, iter_prev_cpu_nanos = {iter_prev_cpu_nanos}, iter_seek_cpu_nanos = {iter_seek_cpu_nanos}, {useless6}\n")


def parse_type(db_line, line, type, perf_line=""):
    db_name_result = db_name_pattern.parse(db_line)
    if db_name_result is None:
        print(type, "parse db name error")
        return
    block_size = db_name_result["block_size"]
    fanout = db_name_result["fanout"]
    value_size = db_name_result["value_size"]
    result = patterns[type].parse(line)
    if result is None:
        print(type, "parse readseq error")
        return

    # latency
    if "latency" in result:
        if block_size not in latencies[type]:
            latencies[type][block_size] = {}
        if fanout not in latencies[type][block_size]:
            latencies[type][block_size][fanout] = {}
        latencies[type][block_size][fanout][value_size] = float(result["latency"])

    # iops
    if "iops" in result:
        if block_size not in iops[type]:
            iops[type][block_size] = {}
        if fanout not in iops[type][block_size]:
            iops[type][block_size][fanout] = {}
        iops[type][block_size][fanout][value_size] = float(result["iops"])

    # bw
    if "bw" in result:
        if block_size not in bws[type]:
            bws[type][block_size] = {}
        if fanout not in bws[type][block_size]:
            bws[type][block_size][fanout] = {}
        bws[type][block_size][fanout][value_size] = float(result["bw"])

    # rocksdb native perf result only for readseq
    if type == "readseq":
        perf_contex_result = perf_context_pattern.parse(perf_line)

        # iter next cpu nanos
        if block_size not in iter_next_cpu_nanos:
            iter_next_cpu_nanos[block_size] = {}
        if fanout not in iter_next_cpu_nanos[block_size]:
            iter_next_cpu_nanos[block_size][fanout] = {}
        iter_next_cpu_nanos[block_size][fanout][value_size] = float(perf_contex_result["iter_next_cpu_nanos"])

        # block read time
        if block_size not in block_read_times:
            block_read_times[block_size] = {}
        if fanout not in block_read_times[block_size]:
            block_read_times[block_size][fanout] = {}
        block_read_times[block_size][fanout][value_size] = float(perf_contex_result["block_read_time"])

        # decompression time
        if block_size not in decompression_times:
            decompression_times[block_size] = {}
        if fanout not in decompression_times[block_size]:
            decompression_times[block_size][fanout] = {}
        decompression_times[block_size][fanout][value_size] = float(perf_contex_result["block_decompress_time"])

        # checksum time
        if block_size not in checksum_times:
            checksum_times[block_size] = {}
        if fanout not in checksum_times[block_size]:
            checksum_times[block_size][fanout] = {}
        checksum_times[block_size][fanout][value_size] = float(perf_contex_result["block_checksum_time"])

        # block read count
        if block_size not in block_read_counts:
            block_read_counts[block_size] = {}
        if fanout not in block_read_counts[block_size]:
            block_read_counts[block_size][fanout] = {}
        block_read_counts[block_size][fanout][value_size] = float(perf_contex_result["block_read_count"])

    pass

def parse_log(log_path):

    with open(log_path, 'r') as f:
        lines = f.readlines()
        for lineno in range(len(lines)):
            line = lines[lineno]

            if line.startswith("readseq"):
                parse_type(lines[lineno-1], line, "readseq", lines[lineno+1])
            elif line.startswith("fillseq"):
                parse_type(lines[lineno-1], line, "fillseq")
            elif line.startswith("readrandom"):
                parse_type(lines[lineno - 1], line, "readrandom")
            elif line.startswith("updaterandom"):
                parse_type(lines[lineno-1], line, "updaterandom")
            elif line.startswith("deleterandom"):
                parse_type(lines[lineno-1], line, "deleterandom")
    pass

def parse_perf_data(perf_data_path):

    db_param_pattern = parse.compile("Performance counter stats for '/root/code/rocksdb/db_bench --benchmarks={type},stats --key_size=16 --value_size={value_size} --num={num} --cache_size={cache_size} --perf_level=4 --db=./test_db/{db_name} --block_size={block_size} --max_bytes_for_level_multiplier={fanout} --statistics{useless}")
    cpu_time_pattern = parse.compile("{cpu_time}      task-clock (msec)         #    {cpu_utility} CPUs utilized")
    elapsed_time_pattern = parse.compile("{elapsed_time} seconds time elapsed")
    # cpu_time_pattern = parse.compile('       {cpu_time}      task-clock (msec)         #    {cpu_utility} CPUs utilized{useless}')
    with open(perf_data_path, 'r') as f:
        lines = f.readlines()
        cur_value_size = ""
        cur_block_size = ""
        cur_fanout = ""
        cur_type = ""
        for lineno in range(len(lines)):
            line = lines[lineno]
            if line.find("Performance") != -1:
                db_param_result = db_param_pattern.parse(line.strip())
                if db_param_result is None:
                    print("failed to parse db param")
                    return
                cur_value_size = db_param_result["value_size"]
                cur_block_size = db_param_result["block_size"]
                cur_fanout = db_param_result["fanout"]
                cur_type = db_param_result["type"]

            elif line.find("task-clock") != -1:

                cpu_time_result = cpu_time_pattern.parse(line.strip())
                if cpu_time_result is None:
                    print("failed to parse cpu time")
                    return
                # cpu time
                if cur_block_size not in cpu_times[cur_type]:
                    cpu_times[cur_type][cur_block_size] = {}
                if cur_fanout not in cpu_times[cur_type][cur_block_size]:
                    cpu_times[cur_type][cur_block_size][cur_fanout] = {}
                cpu_times[cur_type][cur_block_size][cur_fanout][cur_value_size] = float(cpu_time_result["cpu_time"])

                # cpu utility
                if cur_block_size not in cpu_utilities[cur_type]:
                    cpu_utilities[cur_type][cur_block_size] = {}
                if cur_fanout not in cpu_utilities[cur_type][cur_block_size]:
                    cpu_utilities[cur_type][cur_block_size][cur_fanout] = {}
                cpu_utilities[cur_type][cur_block_size][cur_fanout][cur_value_size] = float(cpu_time_result["cpu_utility"])

            elif line.find("elapsed") != -1:
                elapsed_time_result = elapsed_time_pattern.parse(line.strip())
                if elapsed_time_result is None:
                    print("failed to parse elapsed time")
                    return

                # elapsed time
                if cur_block_size not in elapsed_times[cur_type]:
                    elapsed_times[cur_type][cur_block_size] = {}
                if cur_fanout not in elapsed_times[cur_type][cur_block_size]:
                    elapsed_times[cur_type][cur_block_size][cur_fanout] = {}
                elapsed_times[cur_type][cur_block_size][cur_fanout][cur_value_size] = float(elapsed_time_result["elapsed_time"])
    pass

import matplotlib as mpl

font_size = 12  # 字体大小
# 更新字体大小
plt.rcParams['font.sans-serif'] = ['Times New Roman']
mpl.rcParams['font.size'] = font_size

def plot_3_2_1_0(type="readseq", save=False):
    if "readseq" not in bws:
        return
    marker_size = 8
    colors = ['#33CCFF', 'blue', 'red', '#33CCFF']
    markers = ['o', 'o', '^', '^']
    cur_bws = list(bws[type]["4096"]["10"].values())
    cur_bws.reverse()
    plt.figure(figsize=(8, 4.5))
    plt.plot(kv_sizes, cur_bws, '',color='#33CCFF',linestyle='-',linewidth='2',markersize=marker_size, marker='o', label='Bandwidth')

    plt.legend()
    plt.grid(axis='y', linestyle=":", color="silver")
    # plt.xticks(fontsize=8)
    plt.xlabel("KV Granularity (Byte)")
    plt.ylabel("Scan Bandwidth (MB/s)")

    if save:
        plt.savefig("figures/figure3-2-1-0" + ".pdf")
    plt.show()

# block_size = 4K, fanout = 10
def plot_3_2_1_1(types=["readseq"],save=False):

    marker_size = 8
    fig = plt.figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111)
    colors = ['#33CCFF', 'blue', 'red', 'orange', 'forestgreen', 'wheat']
    # markers = []
    for i in range(len(types)):
        type = types[i]
        if len(bws[type]) != 0:
            cur_bws = list(bws[type]["4096"]["10"].values())
            cur_bws.reverse()
            ax.plot(kv_sizes, cur_bws, '',color=colors[i],linestyle='-',linewidth='2',markersize=marker_size, marker='o', label='BW-' + type)


    ax2 = ax.twinx()
    colors2 = ['red', '#33CCFF', 'blue', 'plum', 'orange', 'forestgreen']
    # cur_latencies = list(latencies["4096"]["10"].values())
    # cur_latencies.reverse()
    # ax2.plot(kv_sizes, cur_latencies, '',color='red',linestyle='-',linewidth='2',markersize=marker_size, marker='^', label="Latency")
    for i in range(len(types)):
        type = types[i]
        if len(iops[type]) != 0:
            cur_iops = list(iops[type]["4096"]["10"].values())
            cur_iops.reverse()
            ax2.plot(kv_sizes, cur_iops, '',color=colors2[i],linestyle='-',linewidth='2',markersize=marker_size, marker='^', label="IOPS-"+type)

    ax.legend(loc="center left")
    ax.grid(axis='y', linestyle=":", color="silver")
    ax.set_xlabel("KV Granularity (Byte)")
    ax.set_ylabel("Bandwidth (MB/s)")
    # ax2.set_ylabel("Latency (micros)")
    ax2.set_ylabel("IOPS")
    ax2.legend(loc="center right")
    if save:
        plt.savefig("figures/figure3-2-1-1" + ".pdf")
    plt.show()
    pass

#
def plot_3_2_1_1_0(types=["readseq"],save=False):
    marker_size = 8
    # fig = plt.figure(figsize=(8, 4.5))
    fig, axes = plt.subplots(2, 1, sharex=True, sharey=False)
    # ax = fig.add_subplot(111)
    colors = ['#33CCFF', 'blue', 'red', 'orange', 'forestgreen', 'wheat']
    # markers = []
    for i in range(len(types)):
        type = types[i]
        if len(bws[type]) != 0:
            cur_bws = list(bws[type]["4096"]["10"].values())
            cur_bws.reverse()
            axes[0].plot(kv_sizes, cur_bws, '',color=colors[i],linestyle='-',linewidth='2',markersize=marker_size, marker='o', label='BW-' + type)
    axes[0].legend(loc="upper left", fontsize=11)
    axes[0].grid(axis='y', linestyle=":", color="silver")
    axes[0].set_ylabel("Bandwidth (MB/s)")

    # ax2 = ax.twinx()
    colors2 = ['red', '#33CCFF', 'blue', 'plum', 'orange', 'forestgreen']
    # cur_latencies = list(latencies["4096"]["10"].values())
    # cur_latencies.reverse()
    # ax2.plot(kv_sizes, cur_latencies, '',color='red',linestyle='-',linewidth='2',markersize=marker_size, marker='^', label="Latency")
    for i in range(len(types)):
        type = types[i]
        if len(iops[type]) != 0:
            cur_iops = list(iops[type]["4096"]["10"].values())
            cur_iops.reverse()
            axes[1].plot(kv_sizes, cur_iops, '',color=colors[i],linestyle='-',linewidth='2',markersize=marker_size, marker='^', label="IOPS-"+type)


    axes[1].set_ylabel("IOPS")
    axes[1].set_xlabel("KV Granularity (Byte)")
    axes[1].grid(axis='y', linestyle=":", color="silver")
    axes[1].legend(loc="upper right", fontsize=11)

    plt.subplots_adjust(wspace=0, hspace=0.12)
    if save:
        plt.savefig("figures/figure3-2-1-1-0" + ".pdf")
    plt.show()
    pass

# bw and block size
def plot_3_2_1_2(type="readseq", save=False):
    if type == "deleterandom":
        return
    marker_size = 8
    colors = ['#33CCFF', 'blue', 'red', 'plum', 'royalblue']
    markers = ['o', '^', 's', 'p', '*']
    block_size_strs = ["2048", "4096", "8192", str(8192 * 2)]

    plt.figure(figsize=(8, 4.5))
    for i in range(4):
        cur_bws = list(bws[type][block_size_strs[i]]["10"].values())
        cur_bws.reverse()
        plt.plot(kv_sizes, cur_bws, '', color=colors[i],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[i], label="Block Size " + block_sizes[i])


    plt.legend()
    plt.grid(axis='y', linestyle=":", color="silver")
    plt.xlabel("KV Granularity (Byte)", loc="right")
    plt.ylabel("Bandwidth (MB/s)")
    plt.title(type + " Bandwidth")
    if save:
        plt.savefig("figures/figure3-2-1-2-" + type + ".pdf")
    plt.show()

    pass

# iops and block sizes
def plot_3_2_1_2_0(type="readseq", save=False):

    marker_size = 8
    colors = ['#33CCFF', 'blue', 'red', 'plum', 'royalblue']
    markers = ['o', '^', 's', 'p', '*']
    block_size_strs = ["2048", "4096", "8192", str(8192 * 2)]

    plt.figure(figsize=(8, 4.5))
    for i in range(4):
        cur_iops = list(iops[type][block_size_strs[i]]["10"].values())
        cur_iops.reverse()
        plt.plot(kv_sizes, cur_iops, '', color=colors[i],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[i], label="Block Size " + block_sizes[i])


    plt.legend()
    plt.grid(axis='y', linestyle=":", color="silver")
    plt.xlabel("KV Granularity (Byte)", loc="right")
    plt.ylabel("IOPS")
    plt.title(type + " IOPS")

    if save:
        plt.savefig("figures/figure3-2-1-2-" + type + ".pdf")
    plt.show()

    pass

# since data scale is not enough, fanout does not work
def plot_3_2_1_3(type="readseq", save=False):
    if type == "deleterandom":
        return
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)

    # fig.text(0.9, 0.01, 'KV Granularity (Byte)', fontsize=11, ha='right')
    # fig.text(0.02, 0.5, "Scan Bandwidth (MB/s)", fontsize=11, va='center', rotation='vertical')
    fig.text(0.9, 0.01, 'KV Granularity (Byte)', ha='right')
    fig.text(0.45, 0.01, type, ha='center')
    fig.text(0.02, 0.5, "Bandwidth (MB/s)", va='center', rotation='vertical')
    marker_size = 8
    colors = ['#33CCFF', 'blue', 'red', 'plum', 'royalblue']
    markers = ['o', '^', 's', 'p', '*']
    block_size_strs = ["2048", "4096", "8192", str(8192 * 2)]

    for i in range(2):
        for j in range(2):
            block_size_str = block_size_strs[i * 2 + j]
            block_size = block_sizes[i * 2 + j]
            for k in range(4):
                cur_bws = list(bws[type][block_size_str][fanouts[k]].values())
                cur_bws.reverse()
                axes[j, i].plot(kv_sizes, cur_bws, '', color=colors[k],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[k], label="Fanout " + fanouts[k])
            if i == 1 and j == 0:
                axes[j, i].legend(fontsize=10, loc="lower right")
            # if i != 0:
                # axes[j, i].yaxis.set_ticklabels([])
            # show yaxis grid
            axes[j, i].grid(axis='y', linestyle=":", color="silver")
            axes[j, i].set_title("Block Size " + block_size, y = 1.0, pad=-14)
            axes[j, i].tick_params(axis="x", labelsize=9, rotation=45)
            axes[j, i].tick_params(axis="y", labelsize=9, rotation=0)
            axes[j, i].yaxis.set_visible(True)
    # plt.ylabel("Scan Bandwidth (MB/s)")
    # adjust space among subplots
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.ylim(ymin=0)
    # plt.ylim(ymax=480)
    ax = plt.gca()
    # ax.yaxis.set_major_locator(plt.MultipleLocator(50))
    if save:
        plt.savefig("figures/figure3-2-1-3-" + type + ".pdf")
    plt.show()
    pass

# since data scale is not enough, fanout does not work
def plot_3_2_1_3_0(type="readseq", save=False):

    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)

    # fig.text(0.9, 0.01, 'KV Granularity (Byte)', fontsize=11, ha='right')
    # fig.text(0.02, 0.5, "Scan Bandwidth (MB/s)", fontsize=11, va='center', rotation='vertical')
    fig.text(0.9, 0.01, 'KV Granularity (Byte)', ha='right')
    fig.text(0.45, 0.01, type, ha='center')
    fig.text(0.02, 0.5, "Bandwidth (MB/s)", va='center', rotation='vertical')
    marker_size = 8
    colors = ['#33CCFF', 'blue', 'red', 'plum', 'royalblue']
    markers = ['o', '^', 's', 'p', '*']
    block_size_strs = ["2048", "4096", "8192", str(8192 * 2)]

    for i in range(2):
        for j in range(2):
            block_size_str = block_size_strs[i * 2 + j]
            block_size = block_sizes[i * 2 + j]
            for k in range(4):
                cur_iops = list(iops[type][block_size_str][fanouts[k]].values())
                cur_iops.reverse()
                axes[j, i].plot(kv_sizes, cur_iops, '', color=colors[k],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[k], label="Fanout " + fanouts[k])
            if i == 1 and j == 0:
                axes[j, i].legend(fontsize=10, loc="lower right")
            # if i != 0:
                # axes[j, i].yaxis.set_ticklabels([])
            # show yaxis grid
            axes[j, i].grid(axis='y', linestyle=":", color="silver")
            axes[j, i].set_title("Block Size " + block_size, y = 1.0, pad=-14)
            axes[j, i].tick_params(axis="x", labelsize=9, rotation=45)
            axes[j, i].tick_params(axis="y", labelsize=9, rotation=0)
            axes[j, i].yaxis.set_visible(True)
    # plt.ylabel("Scan Bandwidth (MB/s)")
    # adjust space among subplots
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.ylim(ymin=0)
    # plt.ylim(ymax=480)
    ax = plt.gca()
    # ax.yaxis.set_major_locator(plt.MultipleLocator(50))
    if save:
        plt.savefig("figures/figure3-2-1-3-" + type + ".pdf")
    plt.show()
    pass

def plot_3_2_2_0(save=False):

    marker_size = 8
    colors = ['#33CCFF', 'blue', 'red', 'plum', 'royalblue']
    markers = ['o', '^', 's', 'p', '*']

    fig = plt.figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111)

    cur_iter_next_cpu_nanos = list(iter_next_cpu_nanos["4096"]["10"].values())
    for i in range(len(cur_iter_next_cpu_nanos)):
        cur_iter_next_cpu_nanos[i] /= (1000.0 * 1000 * 1000)
    cur_iter_next_cpu_nanos.reverse()
    ax.plot(kv_sizes, cur_iter_next_cpu_nanos, '', color=colors[0],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[0], label="Iter Next CPU Time")

    cur_decompression_times = list(decompression_times["4096"]["10"].values())
    for i in range(len(cur_decompression_times)):
        cur_decompression_times[i] /= (1000.0 * 1000 * 1000)
    cur_decompression_times.reverse()
    ax.plot(kv_sizes, cur_decompression_times, '', color=colors[2], linestyle='-', linewidth='2',
            markersize=marker_size, marker=markers[2], label="Data Decompression Time")

    cur_block_read_times = list(block_read_times["4096"]["10"].values())
    for i in range(len(cur_block_read_times)):
        cur_block_read_times[i] /= (1000.0 * 1000 * 1000)
    cur_block_read_times.reverse()
    ax.plot(kv_sizes, cur_block_read_times, '', color=colors[1],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[1], label="Data Read Time")


    # cur_checksum_times = list(checksum_times["4096"]["10"].values())
    # for i in range(len(cur_checksum_times)):
    #     cur_checksum_times[i] /= (1000.0 * 1000 * 1000)
    # cur_checksum_times.reverse()
    # ax.plot(kv_sizes, cur_checksum_times, '', color=colors[3],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[3], label="Block Checksum Time")

    ax.set_ylabel("Time (s)")
    ax.legend()

    # ax2 = ax.twinx()
    # cur_block_read_counts = list(block_read_counts["4096"]["10"].values())
    # cur_block_read_counts.reverse()
    # ax2.plot(kv_sizes, cur_block_read_counts, '', color=colors[4],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[4], label="Block Read Count")
    # ax2.set_ylabel("Block Read Count")
    # ax2.legend(loc="center right")

    # plt.legend()
    plt.grid(axis='y', linestyle=":", color="silver")
    plt.xlabel("KV Granularity (Byte)")


    if save:
        plt.savefig("figures/figure3-2-2-0" + ".pdf")
    plt.show()

    pass

def plot_3_2_2_1(type="readseq", save=False):

    marker_size = 8

    bar_width = 0.2
    index0 = np.arange(len(kv_sizes))

    fig = plt.figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111)
    cur_cpu_times = list(cpu_times[type]["4096"]["10"].values())
    for i in range(len(cur_cpu_times)):
        cur_cpu_times[i] /= 1000.0
    cur_cpu_times.reverse()

    cur_elapsed_times = list(elapsed_times[type]["4096"]["10"].values())
    cur_elapsed_times.reverse()

    ax.bar(index0, cur_cpu_times, width=bar_width, color='#33CCFF', edgecolor='grey',
                   hatch='\\', label="CPU Usage")
    ax.bar(index0 + bar_width, cur_elapsed_times, width=bar_width, color='royalblue',
                   edgecolor='black', hatch='', label="Elapsed Time")

    ax.set_xticks(index0 + bar_width / 2, kv_sizes, rotation=0)

    ax2 = ax.twinx()

    cur_cpu_utilities = list(cpu_utilities[type]["4096"]["10"].values())
    for i in range(len(cur_cpu_utilities)):
        cur_cpu_utilities[i] *= 100.0
    cur_cpu_utilities.reverse()
    ax2.plot(kv_sizes, cur_cpu_utilities, '',color='red',linestyle='-',linewidth='2',markersize=marker_size, marker='^', label="CPU Utility")
    ax.set_ylim(0, 100)
    ax2.set_ylim(0, 100)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax2.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.legend(loc="upper center")
    ax.grid(axis='y', linestyle=":", color="silver")
    ax.set_xlabel("KV Granularity (Byte)")
    ax.set_ylabel("Time (s)")
    ax2.set_ylabel("CPU Utility (%)")
    ax2.legend(loc="upper right")
    if save:
        plt.savefig("figures/figure3-2-2-1" + ".pdf")
    plt.show()
    pass



if __name__ == "__main__":

    # logs = ["logs/2022-04-19-16-58-33.log", "logs/2022-04-19-21-14-07.log", "logs/2022-04-20-15-25-21.log"]
    # logs = ["logs/2022-04-22-21-18-30.log"]
    logs = ["logs/2022-04-30-21-51-19.log"]
    for log in logs:
        parse_log(log)

    # perf_datas = ["logs/read-2022-04-19-16-58-33.data", "logs/read-2022-04-19-21-14-07.data", "logs/read-2022-04-20-15-25-21.data"]
    # perf_datas = ["logs/read-2022-04-22-21-18-30.data"]
    perf_datas = ["logs/read-2022-04-30-21-51-19.data", "logs/write-2022-04-30-21-51-19.data"]
    for perf_data in perf_datas:
        parse_perf_data(perf_data)

    #
    # plot_3_2_1_0(True)
    types = ["fillseq", "readseq", "readrandom", "updaterandom", "deleterandom"]
    for type in types:
        print(type)
        if len(bws[type]) > 0:
            print("bw: ", bws[type]["4096"]["10"])
        print("iops: ", iops[type]["4096"]["10"])

    # plot_3_2_1_1(["readseq"], True)
    # plot_3_2_1_1_0(types, True)
    # for type in types:
    #     plot_3_2_1_2(type, False)
    #     plot_3_2_1_2_0(type, False)
    # for type in types:
    #     plot_3_2_1_3(type, False)
    #     plot_3_2_1_3_0(type, False)
    # #
    # plot_3_2_2_0(True)
    # plot_3_2_2_1("readseq", True)

    print("hello world")

    # line = "readrandom   :     189.133 micros/op 5287 ops/sec;   82.7 MB/s (65536 of 65536 found)\n"
    #
    # readrandom_pattern = parse.compile("readrandom   :     {latency} micros/op {iops} ops/sec;   {bw} MB/s{useless}")
    # ret = readrandom_pattern.parse(line)
    # if "latency" in ret:
    #     print(ret["latency"])
    # if "iops" in ret:
    #     print(ret["iops"])
    # if "bw" in ret:
    #     print(ret["bw"])
    # line = "updaterandom :     168.050 micros/op 5950 ops/sec;  186.1 MB/s ( updates:65536 found:65536)\n"
    # updaterandom_pattern = parse.compile("updaterandom :     {latency} micros/op {iops} ops/sec;  {bw} MB/s{useless}")
    # ret = updaterandom_pattern.parse(line)
    # if "latency" in ret:
    #     print(ret["latency"])
    # if "iops" in ret:
    #     print(ret["iops"])
    # if "bw" in ret:
    #     print(ret["bw"])
    # line = "deleterandom :       4.995 micros/op 200204 ops/sec;\n"
    # deleterandom_pattern = parse.compile("deleterandom :       {latency} micros/op {iops} ops/sec;\n")
    # ret = deleterandom_pattern.parse(line)
    # if "latency" in ret:
    #     print(ret["latency"])
    # if "iops" in ret:
    #     print(ret["iops"])
    # if "bw" in ret:
    #     print(ret["bw"])
    # line = "fillseq      :      35.615 micros/op 28077 ops/sec;  439.1 MB/s\n"
    # fillseq_pattern = parse.compile("fillseq      :      {latency} micros/op {iops} ops/sec;  {bw} MB/s\n")
    # ret = fillseq_pattern.parse(line)
    # if "latency" in ret:
    #     print(ret["latency"])
    # if "iops" in ret:
    #     print(ret["iops"])
    # if "bw" in ret:
    #     print(ret["bw"])
    pass