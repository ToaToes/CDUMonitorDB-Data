import pandas as pd # Import pandas for Excel support
import os

class Item:
    def __init__(self, name, unit, up_limit, low_limit, type):
        self.name = name
        self.unit = unit
        self.up_limit = up_limit
        self.low_limit = low_limit
        self.type = type

container = [
"10.1.7.159",
"10.2.7.252",
"10.3.7.252",
"10.4.7.252",
"10.5.7.252",
"10.6.7.252",
"10.7.7.252",
"10.8.7.252",
"10.9.7.252",
"10.10.7.253",
"10.11.7.252",
"10.12.7.252",
"10.13.7.253",
"10.14.7.252",
"10.15.7.253",
"10.16.7.253",
"10.17.7.253",
"10.18.7.253",
"10.19.7.253",
"10.20.7.253",
"10.21.7.253"
]

name = [
Item("压力P1", "bar", " ", " ", "38"),
Item("压力P2", "bar", " ", " ", "38"),
Item("压力P3", "bar", " ", " ", "38"),
Item("压力P4", "bar", "1.5", "0.6", "38"),
Item("压力P5", "bar", "3.5", "2", "38"),
Item("出水温度T1", "C", "50", " ", "42"),
Item("进水温度T2", "C", "35", "22", "42"),
Item("泵流速", "Hz", "40", "0", "23"),
Item("P1-P2压力差", "bar", "0.3", " ", "38"),
Item("T1-T2温度差", "C", "15", " ", "42")
]


for c in container:

    result_Excel_Path = rf'C:\Users\42591\Desktop\{c}.xlsx'

    results = []
    

    for item in name:
        row = [
            f"{c}_P5P1",  # 点位编码
            c,            # 前置机编号
            "40100",      # 连接端口
            item.name,    # 点位名称
            "AP",         # 点位类型
            "-",          # 控制上限
            "0",          # 控制下限
            item.unit,    # 工量单位
            item.up_limit, # 报警上限
            item.low_limit, # 报警下限
            "",           # 视频链接地址
            item.name,    # 应用编码
            "",           # 区域编号
            item.type,    # 部件类型
            "F",          # 系统类型
            "null",       # 控制输出参数
            "30",         # xpos
            "50"          # ypos
        ]

        results.append(row)
    
    df = pd.DataFrame(results, columns=[
                                        "点位编码", 
                                        "前置机编号", 
                                        "连接端口", 
                                        "点位名称", 
                                        "点位类型", 
                                        "控制上限", 
                                        "控制下限", 
                                        "工量单位", 
                                        "报警上限",
                                        "报警下限",
                                        "视频链接地址",
                                        "应用编码",
                                        "区域编号",
                                        "部件类型",
                                        "系统类型",
                                        "控制输出参数",
                                        "xpos",
                                        "ypos" ])

    try:
        df.to_excel(result_Excel_Path, index = False, engine = 'openpyxl')
        print(f"Query results saved to {result_Excel_Path}")
    except Exception as e:
        print(f"Error saving the new Excel file: {e}")
