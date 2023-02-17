# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
# from parse import parse
import parse
import xlwt

workbook = xlwt.Workbook(encoding='utf-8')

def parse_gam_log(log_dir, test_name, test_type=0):

    patterns = []

    avg_execution_time_pattern = parse.compile("avg execution_time = {value} ms")
    avg_index_read_time_pattern = parse.compile("phase = INDEX_READ, avg elapsed_time = {value} ms")
    avg_cc_select_time_pattern = parse.compile("phase = CC_SELECT, avg elapsed_time = {value} ms")
    avg_cc_insert_time_pattern = parse.compile("phase = CC_INSERT, avg elapsed_time = {value} ms")
    avg_cc_commit_time_pattern = parse.compile("phase = CC_COMMIT, avg elapsed_time = {value} ms")
    avg_abort_time_pattern = parse.compile("avg abort time = {value} ms")
    # ts_alloc_time_pattern = parse.compile("thread_id = 0, elapsed_time = {value} ms")
    avg_gam_read_time_pattern = parse.compile("gam operation = GAM_READ, avg elapsed_time = {value} ms")
    avg_gam_write_time_pattern = parse.compile("gam operation = GAM_WRITE, avg elapsed_time = {value} ms")
    avg_gam_rlock_time_pattern = parse.compile("gam operation = GAM_RLOCK, avg elapsed_time = {value} ms")
    avg_gam_wlock_time_pattern = parse.compile("gam operation = GAM_WLOCK, avg elapsed_time = {value} ms")
    avg_gam_try_rlock_time_pattern = parse.compile("gam operation = GAM_TRY_RLOCK, avg elapsed_time = {value} ms")
    avg_gam_try_wlock_time_pattern = parse.compile("gam operation = GAM_TRY_WLOCK, avg elapsed_time = {value} ms")
    avg_gam_malloc_time_pattern = parse.compile("gam operation = GAM_MALLOC, avg elapsed_time = {value} ms")
    avg_gam_unlock_time_pattern = parse.compile("gam operation = GAM_UNLOCK, avg elapsed_time = {value} ms")
    agg_total_count_pattern = parse.compile("agg_total_count	{value}")
    agg_total_abort_count_pattern = parse.compile("agg_total_abort_count	{value}")
    abort_rate_pattern = parse.compile("abort_rate	{value}")
    per_node_elapsed_time_pattern = parse.compile("per_node_elapsed_time	{value}")
    total_throughput_pattern = parse.compile("total_throughput	{value}")
    per_node_throughput_pattern = parse.compile("per_node_throughput	{value}")
    per_core_throughput_pattern = parse.compile("per_core_throughput	{value}")

    patterns.append(total_throughput_pattern)
    patterns.append(per_node_throughput_pattern)
    patterns.append(per_core_throughput_pattern)
    patterns.append(agg_total_count_pattern)
    patterns.append(agg_total_abort_count_pattern)
    patterns.append(abort_rate_pattern)
    patterns.append(per_node_elapsed_time_pattern)
    patterns.append(avg_execution_time_pattern)
    patterns.append(avg_index_read_time_pattern)
    patterns.append(avg_cc_select_time_pattern)
    patterns.append(avg_cc_insert_time_pattern)
    patterns.append(avg_cc_commit_time_pattern)
    patterns.append(avg_abort_time_pattern)
    # patterns.append(ts_alloc_time_pattern)
    patterns.append(avg_gam_read_time_pattern)
    patterns.append(avg_gam_write_time_pattern)
    patterns.append(avg_gam_rlock_time_pattern)
    patterns.append(avg_gam_wlock_time_pattern)
    patterns.append(avg_gam_try_rlock_time_pattern)
    patterns.append(avg_gam_try_wlock_time_pattern)
    patterns.append(avg_gam_malloc_time_pattern)
    patterns.append(avg_gam_unlock_time_pattern)

    stat_names_temp = ["avg execution_time", "phase = INDEX_READ, avg elapsed_time", "phase = CC_SELECT, avg elapsed_time", "phase = CC_INSERT, avg elapsed_time", "phase = CC_COMMIT, avg elapsed_time", "avg abort time"]

    stat_names = []
    stat_names.append("total_throughput")
    stat_names.append("per_node_throughput")
    stat_names.append("per_core_throughput")
    stat_names.append("agg_total_count")
    stat_names.append("agg_total_abort_count")
    stat_names.append("abort_rate")
    stat_names.append("per_node_elapsed_time")
    stat_names.extend(stat_names_temp)
    # stat_names.append(stat_names_temp)
    stat_names.append("gam operation = GAM_READ, avg elapsed_time")
    stat_names.append("gam operation = GAM_WRITE, avg elapsed_time")
    stat_names.append("gam operation = GAM_RLOCK, avg elapsed_time")
    stat_names.append("gam operation = GAM_WLOCK, avg elapsed_time")
    stat_names.append("gam operation = GAM_TRY_RLOCK, avg elapsed_time")
    stat_names.append("gam operation = GAM_TRY_WLOCK, avg elapsed_time")
    stat_names.append("gam operation = GAM_MALLOC, avg elapsed_time")
    stat_names.append("gam operation = GAM_UNLOCK, avg elapsed_time")

    stats = []
    avg_execution_times = []
    avg_index_read_times = []
    avg_cc_select_times = []
    avg_cc_insert_times = []
    avg_cc_commit_times = []
    avg_abort_times = []
    # ts_alloc_times = []
    avg_gam_read_times = []
    avg_gam_write_times = []
    avg_gam_rlock_times = []
    avg_gam_wlock_times = []
    avg_gam_try_rlock_times = []
    avg_gam_try_wlock_times = []
    avg_gam_malloc_times = []
    avg_gam_unlock_times = []
    agg_total_counts = []
    agg_total_abort_counts = []
    abort_rates = []
    per_node_elapsed_times = []
    total_throughputs = []
    per_node_throughputs = []
    per_core_throughputs = []

    stats.append(total_throughputs)
    stats.append(per_node_throughputs)
    stats.append(per_core_throughputs)
    stats.append(agg_total_counts)
    stats.append(agg_total_abort_counts)
    stats.append(abort_rates)
    stats.append(per_node_elapsed_times)
    stats.append(avg_execution_times)
    stats.append(avg_index_read_times)
    stats.append(avg_cc_select_times)
    stats.append(avg_cc_insert_times)
    stats.append(avg_cc_commit_times)
    stats.append(avg_abort_times)
    # stats.append(ts_alloc_times)
    stats.append(avg_gam_read_times)
    stats.append(avg_gam_write_times)
    stats.append(avg_gam_rlock_times)
    stats.append(avg_gam_wlock_times)
    stats.append(avg_gam_try_rlock_times)
    stats.append(avg_gam_try_wlock_times)
    stats.append(avg_gam_malloc_times)
    stats.append(avg_gam_unlock_times)

    dist_ratios = [0, 20, 40, 60, 80, 100]

    for dist_ratio in dist_ratios:
        log_path = log_dir + "/" + str(dist_ratio) + "_tpcc.log"

        with open(log_path, 'r') as f:
            lines = f.readlines()
            execute_time = 0
            begin_parsing = False
            for lineno in range(len(lines)):
                line = lines[lineno]
                if line.find("BEGIN EXECUTION PROFILING REPORT") != -1:
                    execute_time += 1
                    if execute_time == 3:
                        begin_parsing = True
                elif begin_parsing:
                    for i in range(len(patterns)):
                        if line.find(stat_names[i]) != -1:
                            result = patterns[i].parse(line.strip())
                            if result is None:
                                print("failed to parse " + stat_names[i])
                                print(line.strip())
                                return
                            stats[i].append(float(result["value"]))

    worksheet = workbook.add_sheet(test_name)
    for i in range(len(dist_ratios)):
        worksheet.write(i, 0, dist_ratios[i])
        for j in range(len(patterns)):
            if len(stats[j]) == 0:
                worksheet.write(i, j + 1, 0)
            else:
                worksheet.write(i, j + 1, stats[j][i])

    pass

stats = {}

def parse_gam_log_scale_up(log_dir, test_name, test_type=0):

    patterns = []

    avg_execution_time_pattern = parse.compile("avg execution_time = {value} ms")
    avg_index_read_time_pattern = parse.compile("phase = INDEX_READ, avg elapsed_time = {value} ms")
    avg_cc_select_time_pattern = parse.compile("phase = CC_SELECT, avg elapsed_time = {value} ms")
    avg_cc_insert_time_pattern = parse.compile("phase = CC_INSERT, avg elapsed_time = {value} ms")
    avg_cc_commit_time_pattern = parse.compile("phase = CC_COMMIT, avg elapsed_time = {value} ms")
    avg_abort_time_pattern = parse.compile("avg abort time = {value} ms")
    ts_alloc_time_pattern = parse.compile("avg cc_ts_alloc_time = {value} ms")
    avg_gam_read_time_pattern = parse.compile("gam operation = GAM_READ, avg elapsed_time = {value} ms")
    avg_gam_write_time_pattern = parse.compile("gam operation = GAM_WRITE, avg elapsed_time = {value} ms")
    avg_gam_rlock_time_pattern = parse.compile("gam operation = GAM_RLOCK, avg elapsed_time = {value} ms")
    avg_gam_wlock_time_pattern = parse.compile("gam operation = GAM_WLOCK, avg elapsed_time = {value} ms")
    avg_gam_try_rlock_time_pattern = parse.compile("gam operation = GAM_TRY_RLOCK, avg elapsed_time = {value} ms")
    avg_gam_try_wlock_time_pattern = parse.compile("gam operation = GAM_TRY_WLOCK, avg elapsed_time = {value} ms")
    avg_gam_malloc_time_pattern = parse.compile("gam operation = GAM_MALLOC, avg elapsed_time = {value} ms")
    avg_gam_unlock_time_pattern = parse.compile("gam operation = GAM_UNLOCK, avg elapsed_time = {value} ms")
    agg_total_count_pattern = parse.compile("agg_total_count	{value}")
    agg_total_abort_count_pattern = parse.compile("agg_total_abort_count	{value}")
    abort_rate_pattern = parse.compile("abort_rate	{value}")
    per_node_elapsed_time_pattern = parse.compile("per_node_elapsed_time	{value}")
    total_throughput_pattern = parse.compile("total_throughput	{value}")
    per_node_throughput_pattern = parse.compile("per_node_throughput	{value}")
    per_core_throughput_pattern = parse.compile("per_core_throughput	{value}")

    patterns.append(total_throughput_pattern)
    patterns.append(per_node_throughput_pattern)
    patterns.append(per_core_throughput_pattern)
    patterns.append(agg_total_count_pattern)
    patterns.append(agg_total_abort_count_pattern)
    patterns.append(abort_rate_pattern)
    patterns.append(per_node_elapsed_time_pattern)
    # enable profiling
    if test_type == 0:
        patterns.append(avg_execution_time_pattern)
        patterns.append(avg_index_read_time_pattern)
        patterns.append(avg_cc_select_time_pattern)
        patterns.append(avg_cc_insert_time_pattern)
        patterns.append(avg_cc_commit_time_pattern)
        patterns.append(avg_abort_time_pattern)
        patterns.append(ts_alloc_time_pattern)
        patterns.append(avg_gam_read_time_pattern)
        patterns.append(avg_gam_write_time_pattern)
        patterns.append(avg_gam_rlock_time_pattern)
        patterns.append(avg_gam_wlock_time_pattern)
        patterns.append(avg_gam_try_rlock_time_pattern)
        patterns.append(avg_gam_try_wlock_time_pattern)
        patterns.append(avg_gam_malloc_time_pattern)
        patterns.append(avg_gam_unlock_time_pattern)

    stat_names_temp = ["avg execution_time", "phase = INDEX_READ, avg elapsed_time", "phase = CC_SELECT, avg elapsed_time", "phase = CC_INSERT, avg elapsed_time", "phase = CC_COMMIT, avg elapsed_time", "avg abort time"]

    stat_names = []
    stat_names.append("total_throughput")
    stat_names.append("per_node_throughput")
    stat_names.append("per_core_throughput")
    stat_names.append("agg_total_count")
    stat_names.append("agg_total_abort_count")
    stat_names.append("abort_rate")
    stat_names.append("per_node_elapsed_time")
    # enable profiling
    if test_type == 0:
        stat_names.extend(stat_names_temp)
        stat_names.append("avg cc_ts_alloc_time")
        stat_names.append("gam operation = GAM_READ, avg elapsed_time")
        stat_names.append("gam operation = GAM_WRITE, avg elapsed_time")
        stat_names.append("gam operation = GAM_RLOCK, avg elapsed_time")
        stat_names.append("gam operation = GAM_WLOCK, avg elapsed_time")
        stat_names.append("gam operation = GAM_TRY_RLOCK, avg elapsed_time")
        stat_names.append("gam operation = GAM_TRY_WLOCK, avg elapsed_time")
        stat_names.append("gam operation = GAM_MALLOC, avg elapsed_time")
        stat_names.append("gam operation = GAM_UNLOCK, avg elapsed_time")

    # stats = []
    # avg_execution_times = []
    # avg_index_read_times = []
    # avg_cc_select_times = []
    # avg_cc_insert_times = []
    # avg_cc_commit_times = []
    # avg_abort_times = []
    # ts_alloc_times = []
    # avg_gam_read_times = []
    # avg_gam_write_times = []
    # avg_gam_rlock_times = []
    # avg_gam_wlock_times = []
    # avg_gam_try_rlock_times = []
    # avg_gam_try_wlock_times = []
    # avg_gam_malloc_times = []
    # avg_gam_unlock_times = []
    # agg_total_counts = []
    # agg_total_abort_counts = []
    # abort_rates = []
    # per_node_elapsed_times = []
    # total_throughputs = []
    # per_node_throughputs = []
    # per_core_throughputs = []
    #
    # stats.append(total_throughputs)
    # stats.append(per_node_throughputs)
    # stats.append(per_core_throughputs)
    # stats.append(agg_total_counts)
    # stats.append(agg_total_abort_counts)
    # stats.append(abort_rates)
    # stats.append(per_node_elapsed_times)
    # # enable profiling
    # if test_type == 0:
    #     stats.append(avg_execution_times)
    #     stats.append(avg_index_read_times)
    #     stats.append(avg_cc_select_times)
    #     stats.append(avg_cc_insert_times)
    #     stats.append(avg_cc_commit_times)
    #     stats.append(avg_abort_times)
    #     stats.append(ts_alloc_times)
    #     stats.append(avg_gam_read_times)
    #     stats.append(avg_gam_write_times)
    #     stats.append(avg_gam_rlock_times)
    #     stats.append(avg_gam_wlock_times)
    #     stats.append(avg_gam_try_rlock_times)
    #     stats.append(avg_gam_try_wlock_times)
    #     stats.append(avg_gam_malloc_times)
    #     stats.append(avg_gam_unlock_times)

    cc_types = ["lock_nowait", "lock_wait", "occ", "silo_localversioncheck"]
    thetas = [0.5, 0.7, 0.9, 0.99]
    core_cnts = [1, 5, 10, 15, 20]
    read_ratios = [0.2, 0.5, 0.8]

    log_path_format = log_dir + "/{}_overall_logs_0213/theta{}_core{}_get{}_update{}_ycsb.log"
    # stats = {}
    for cc_type in cc_types:
        stats[cc_type] = {}
        for read_ratio in read_ratios:
            stats[cc_type][read_ratio] = {}
            for core_cnt in core_cnts:
                stats[cc_type][read_ratio][core_cnt] = {}
                for theta in thetas:
                    stats[cc_type][read_ratio][core_cnt][theta] = {}
                    log_path = log_path_format.format(cc_type, theta, core_cnt, int(read_ratio * 10), int(10 - read_ratio * 10))

                    with open(log_path, 'r') as f:
                        lines = f.readlines()
                        execute_time = 0
                        begin_parsing = False
                        for lineno in range(len(lines)):
                            line = lines[lineno]
                            if not begin_parsing and line.find("perf statistics summary") != -1:
                                begin_parsing = True
                            # if not begin_parsing and test_type == 1 and line.find("perf statistics summary") != -1:
                            #     begin_parsing = True
                            # elif not begin_parsing and test_type == 0 and line.find("BEGIN EXECUTION PROFILING REPORT") != -1:
                            #     execute_time += 1
                            #     if execute_time == 3:
                            #         begin_parsing = True
                            elif begin_parsing:
                                for i in range(len(patterns)):
                                    if line.find(stat_names[i]) != -1:
                                        result = patterns[i].parse(line.strip())
                                        if result is None:
                                            print("failed to parse " + stat_names[i])
                                            print(line.strip())
                                            return
                                        # stats[i].append(float(result["value"]))
                                        stats[cc_type][read_ratio][core_cnt][theta][stat_names[i]] = float(result["value"])

    # worksheet = workbook.add_sheet(test_name)
    #
    # for read_ratio in read_ratios:
    #     for core_cnt in core_cnts:
    #         for theta in thetas:
    #
    # for i in range(len(core_cnts)):
    #     worksheet.write(i, 0, core_cnts[i])
    #     for j in range(len(patterns)):
    #         if len(stats[j]) == 0:
    #             worksheet.write(i, j + 1, 0)
    #         else:
    #             worksheet.write(i, j + 1, stats[j][i])

    pass

def plot_cc(save=False):
    marker_size = 8
    colors = ['#33CCFF', 'blue', 'red', 'plum', 'royalblue']
    markers = ['o', '^', 's', 'p', '*']

    cc_types = ["lock_nowait", "lock_wait", "occ", "silo_localversioncheck"]
    thetas = [0.5, 0.7, 0.9, 0.99]
    core_cnts = [1, 5, 10, 15, 20]
    read_ratios = [0.2, 0.5, 0.8]
    picked_core_cnt = 20
    picked_read_ratio = 0.5

    plt.figure(figsize=(8, 4.5))
    for i in range(len(cc_types)):
        throughputs = []
        for theta in thetas:
            throughputs.append(stats[cc_types[i]][picked_read_ratio][picked_core_cnt][theta]["total_throughput"])

        plt.plot(thetas, throughputs, '', color=colors[i],linestyle='-',linewidth='2',markersize=marker_size, marker=markers[i], label=cc_types[i])

    plt.legend()
    plt.grid(axis='y', linestyle=":", color="silver")
    plt.xlabel("ycsb zipf theta", loc="right")
    plt.ylabel("throughput (txn/s)")
    plt.title("cc performance, core=" + str(picked_core_cnt) + ", read_ratio=" + str(picked_read_ratio))
    if save:
        plt.savefig("figures/figure_cc_overall-" + "core" + str(picked_core_cnt) + "-read_ratio" + str(picked_read_ratio) + ".pdf")
    plt.show()

    pass

if __name__ == "__main__":

    # log_dirs = ["logs/gam-logs/lock_no_wait_dist_ratio_profiling_results_20230104-warehouse12-sf1-core4", "logs/gam-logs/occ_dist_ratio_profiling_results_20230108-warehouse12-sf1-core4", "logs/gam-logs/silo_dist_ratio_profiling_results_20230105-warehouse12-sf1-core4"]
    # test_names = ["lock_no_wait", "occ", "silo"]

    # for i in range(len(log_dirs)):
    #     parse_gam_log(log_dirs[i], test_names[i])

    # log_dirs = ["logs/gam-logs/lock_no_wait_core_single_node_profiling_results_20230110-sf10-remove-insert-and-atomics", "logs/gam-logs/silo_core_single_node_profiling_results_20230110-sf10-remove-insert-and-atomics"]
    # test_names = ["lock_no_wait", "silo"]
    #
    # for i in range(len(log_dirs)):
    #     parse_gam_log_scale_up(log_dirs[i], test_names[i], 0)
    #
    # workbook.save("results/result-0108.xls")


    parse_gam_log_scale_up("logs/gam-logs-ycsb", "", 0)
    plot_cc(False)

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