import os
import time
from datetime import timedelta

import pandas as pd

from f1_中性策略回放 import compound_name as old_name
from function import curve_playback, root_path, log,rtn_data_path

# 回放名
compound_name = 'adaptV3'
data_path = os.path.join(rtn_data_path, compound_name)
if compound_name != old_name:
    log.warning(f'即将查看的策略: {compound_name}  与最近一次运行的策略:  {old_name}  不一致,请注意核实\n')
    time.sleep(3)
# 数据载入
save_path = os.path.join(data_path, '净值持仓数据.csv')
curve = pd.read_csv(save_path, encoding='gbk', skiprows=2)
curve['candle_begin_time'] = pd.to_datetime(curve['candle_begin_time'])
curve.set_index('candle_begin_time', inplace=True)
save_path = os.path.join(data_path, '虚拟账户数据.csv')
account_df = pd.read_csv(save_path, encoding='gbk')
save_path = os.path.join(data_path, '持仓面板数据.pkl')
display_df = pd.read_pickle(save_path)
save_path = os.path.join(data_path, '下单面板数据.pkl')
order_df = pd.read_pickle(save_path)

# ===1 净值回放
play_start_time = pd.to_datetime('2022-10-01 20:00:00')
# 回放步长小时
step = 24
# 步长间隔时间:s
sleeptime = 0.1
curve_playback(curve, play_start_time, step=step, sleeptime=sleeptime)

# ===2 面板数据查看
# 展示run_time 时刻持仓面板 run_time+1h 持仓面板  run_time+1m 下单面板
# 已过滤持仓不满总资产0.1%的币种
run_time = pd.to_datetime('2022-06-07 22:00:00')
if display_df.empty:
    log.warning('面板数据未生成,回放配置需hourly_details=True')
    exit()
log.info(f'交易前时点:{run_time}')
log.info(display_df.loc[run_time].to_markdown())

log.info(f'交易执行时点:{run_time + timedelta(minutes=1)}')
log.info(order_df.loc[run_time + timedelta(minutes=1)].to_markdown())

log.info(f'交易后时点:{run_time + timedelta(minutes=60)}')
log.info(display_df.loc[run_time + timedelta(minutes=60)].to_markdown())
