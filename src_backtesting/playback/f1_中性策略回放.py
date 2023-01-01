import pprint

from function import filter_generate, log, parallel_filter_handle
from job import playback_start, playCfg
tag = 'loc'

compound_name = 'Cbr_v1'  # name
# ===常规配置
cal_factor_type = 'cross'  # cross/ vertical
start_date = '2022-01-01'
end_date = '2022-11-20'
factor_long_list = [('Cbr_v1', True, 96, 0, 0.5)]
factor_short_list = [('Cbr_v1', True, 96, 0, 0.5)]
trade_type = 'swap'
playCfg['c_rate'] = 6 / 10000  # 手续费
playCfg['hold_hour_num'] = 1  # hold_hour
# 只跑指定的N个offset,空列表则全offset
long_select_offset = []
short_select_offset = []

# ===回放增强配置
playCfg['long_coin_num'] = 1  # 多头选币数
playCfg['short_coin_num'] = 1  # 空头选币数
# 多币权重参数(不小于0),多币时有效,详见https://bbs.quantclass.cn/thread/8835
playCfg['long_p'] = 0  # 0 :等权, 0 -> ∞ :多币头部集中度逐渐降低
playCfg['short_p'] = 0  # long_coin_num = 3, long_p = 1 ;rank 1,2,3 的资金分配 [0.43620858, 0.34568712, 0.21810429]
playCfg['leverage'] = 1  # 杠杆率
playCfg['long_risk_position'] = 0  # 多头风险暴露 0.1 对冲后 10% 净多头, -0.2 对冲后 20% 净空头
playCfg['initial_trade_usdt'] = 10000  # 初始投入,金额过小会导致某些币无法开仓
# offset 止盈止损,都为0时,该功能关闭
playCfg['offset_stop_win'] = 0  # offset 止盈
playCfg['offset_stop_loss'] = 0   # offset 止损

# 固定白名单 'BTCUSDT'
long_white_list = []
short_white_list = []
# 固定黑名单
long_black_list = []
short_black_list = []

# ===过滤配置(元素皆为字符串,仿照e.g.写即可 支持 & |)
# 前置过滤 筛选出选币的币池

# 写法1

filter_before_params = [
    (['df1', 'Volume_fl_24', 'pct', 'gte', 0.5],
    ['df1', 'Volume_fl_24', 'rank', 'lte', 30],
     '1|2'),
    ['df2', 'Volume_fl_24', 'pct', 'gte', 0.5],
    ['df1', '涨跌幅max_fl_24', 'value', 'lte', 0.2],
    ['df2', '涨跌幅max_fl_24', 'value', 'lte', 0.2],
    (
        ['df2', '费率min_fl_24', 'rank', 'gte', 10, True],
        ['df2', 'fundingRate', 'value', 'gte', 0.01],
        '1|2'
    )
]
filter_before_exec = [filter_generate(param=param) for param in filter_before_params]

filter_before_exec = [filter_generate(param=param) for param in filter_before_params]
# 将默认的串联过滤转化为并联,只针对前置过滤且有使用了rank/pct类型的过滤集,value类型串并联无影响
filter_before_exec, tag = parallel_filter_handle(filter_before_exec)

# filter_info = """filter_factor = ['涨跌幅max_fl_24'][0]
# df1 = df1[df1[f'涨跌幅max_fl_24']<0.2]
# filter_factor = ['涨跌幅max_fl_24'][0]
# df2 = df2[df2[f'涨跌幅max_fl_24']<0.2]
# """
# filter_before_exec = [filter_info]


# 后置过滤 在选币后下单前控制选定币种的资金分配系数
filter_after_exec = [
    # filter_generate(direction='df2', filter_factor='fundingRate', filter_type='value', filter_value=-0.0001,
    #                 compare_operator='lte', rank_ascending=False, filter_after=True,weight_ratio=0),
]
# ===花式配置
# 资金曲线择时:(param[-1] 默认为计算signal需要的最少小时数)
p_signal_fun = None
# param = [48, 48]
# p_signal_fun = partial(ma_signal, param)

# ===回放参数配置
hourly_details = False  # True 会生成详细截面数据 持仓面板和下单面板,耗时增加20S左右
select_by_hour = False  # True 为逐小时,会对退市币精确处理,速度慢；False 速度快,模糊处理
othCfg = {
    'log_level': 'INFO',
    'cal_factor_type': cal_factor_type,
    'hourly_details': hourly_details,
    'select_by_hour': select_by_hour,
    'filter_before_exec': filter_before_exec,
    'filter_after_exec': filter_after_exec,
    'start_date': start_date,
    'end_date': end_date,
    'factor_long_list': factor_long_list,
    'factor_short_list': factor_short_list,
    'trade_type': trade_type,
    'compound_name': compound_name,
    'quit_symbol_filter_hour': playCfg['hold_hour_num'][0],
    'p_signal_fun': p_signal_fun,
    'select_offsets': [long_select_offset, short_select_offset],
    'white_list': [long_white_list, short_white_list],
    'black_list': [long_black_list, short_black_list],
}
if playCfg['offset_stop_win'][0] != 0 or playCfg['offset_stop_loss'][0] != 0:
    assert playCfg['offset_stop_win'][0] > 0 and playCfg['offset_stop_loss'][0] < 0


def main():
    if filter_before_exec:
        print('前置过滤源码：')
        [print(x, '\n') if tag in x else print(x) for x in filter_before_exec]
    if filter_before_exec:
        print('后置过滤源码：')
        [print(x, '\n') if tag in x else print(x) for x in filter_after_exec]
    res = playback_start(playCfg, othCfg)


if __name__ == '__main__':
    main()
