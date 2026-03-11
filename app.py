#!/usr/bin/env python3
"""
万Case成本计算器 - 网页版
使用Streamlit构建的交互式网页应用
"""

import streamlit as st

st.set_page_config(
    page_title="万Case成本计算器",
    page_icon="🦐",
    layout="wide"
)

#### 基准数据（1月）
base_data = {
    "抖音开放平台生态运营": {
        "人力": 306,
        "成本": 166099,
        "量级": 105375,
        "人均成本": 542.81
    },
    "短剧生态运营": {
        "人力": 57,
        "成本": 25012,
        "量级": 24395,
        "人均成本": 438.81
    },
    "游戏与社交生态运营": {
        "人力": 474,
        "成本": 220879,
        "量级": 180361,
        "人均成本": 465.99
    }
}

st.title("🦐 万Case成本计算器 🦐")
st.markdown("---")

#### 侧边栏 - 用工模式（待补充）
st.sidebar.header("用工模式设置")
st.sidebar.info("⚠️ 用工模式人均成本待补充")

labor_modes = st.sidebar.selectbox(
    "选择用工模式",
    ["默认（综合人均成本）", "自营", "X", "BPO"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 说明")
st.sidebar.markdown("""
- 调整各子部门的人力和量级
- 点击「开始测算」查看结果
- 支持实时更新测算
""")

#### 主界面 - 输入区域
st.header("📊 调整参数")

col1, col2, col3 = st.columns(3)
adjustments = {}

with col1:
    st.subheader("抖音开放平台生态运营")
    dept = "抖音开放平台生态运营"
    adjustments[dept] = {
        "人力": st.number_input(
            "人力", 
            min_value=0, 
            value=base_data[dept]["人力"],
            key=f"{dept}_人力"
        ),
        "量级": st.number_input(
            "量级", 
            min_value=0, 
            value=base_data[dept]["量级"],
            key=f"{dept}_量级"
        )
    }

with col2:
    st.subheader("短剧生态运营")
    dept = "短剧生态运营"
    adjustments[dept] = {
        "人力": st.number_input(
            "人力", 
            min_value=0, 
            value=base_data[dept]["人力"],
            key=f"{dept}_人力"
        ),
        "量级": st.number_input(
            "量级", 
            min_value=0, 
            value=base_data[dept]["量级"],
            key=f"{dept}_量级"
        )
    }

with col3:
    st.subheader("游戏与社交生态运营")
    dept = "游戏与社交生态运营"
    adjustments[dept] = {
        "人力": st.number_input(
            "人力", 
            min_value=0, 
            value=base_data[dept]["人力"],
            key=f"{dept}_人力"
        ),
        "量级": st.number_input(
            "量级", 
            min_value=0, 
            value=base_data[dept]["量级"],
            key=f"{dept}_量级"
        )
    }

#### 测算按钮
st.markdown("---")
if st.button("🧮 开始测算", type="primary"):
    st.header("📈 测算结果")
    
    total_cost = 0
    total_volume = 0
    results = {}

    # 计算子部门
    for dept, data in base_data.items():
        adj = adjustments[dept]
        new_cost = adj["人力"] * data["人均成本"]
        # 计算旧万Case成本
        if data["量级"] > 0:
            old_wancase = (data["成本"] / data["量级"]) * 10000
        else:
            old_wancase = 0
        # 计算新万Case成本
        if adj["量级"] > 0:
            new_wancase = (new_cost / adj["量级"]) * 10000
        else:
            new_wancase = 0
        results[dept] = {
            "旧人力": data["人力"],
            "新人力": adj["人力"],
            "旧成本": data["成本"],
            "新成本": new_cost,
            "旧量级": data["量级"],
            "新量级": adj["量级"],
            "旧万Case成本": old_wancase,
            "新万Case成本": new_wancase
        }
        total_cost += new_cost
        total_volume += adj["量级"]

    # 显示子部门结果
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dept = "抖音开放平台生态运营"
        res = results[dept]
        st.subheader(dept)
        labor_diff = res["新人力"] - res["旧人力"]
        if res["旧万Case成本"] > 0:
            cost_change = ((res["新万Case成本"] - res["旧万Case成本"]) / res["旧万Case成本"]) * 100
        else:
            cost_change = 0
        
        st.metric("人力", f"{res['新人力']} 人", f"{labor_diff:+d}")
        st.metric("万Case成本", f"{res['新万Case成本']:,.0f} 元", f"{cost_change:+.1f}%")
        st.write(f"成本: {res['旧成本']:,.0f} → {res['新成本']:,.0f} 元")
        st.write(f"量级: {res['旧量级']:,} → {res['新量级']:,}")

    with col2:
        dept = "短剧生态运营"
        res = results[dept]
