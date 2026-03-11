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

st.title("🦐 万Case成本计算器 🦐")
st.markdown("---")

# 侧边栏 - 用工模式说明
st.sidebar.header("用工模式设置")
st.sidebar.info("💡 支持同时调整自营/X/BPO三种用工模式")
st.sidebar.markdown("---")
st.sidebar.markdown("### 说明")
st.sidebar.markdown("""
- 先设置基线数据（1月数据）
- 再调整各子部门不同用工模式的人力和量级
- 点击「开始测算」查看结果
- 支持实时更新测算
- 显示三级部门（开发者生态）汇总数据
""")

# ==========================================
# 第一步：设置基线数据
# ==========================================

st.header("📋 第一步：设置基线数据")

# 初始化session state中的基线数据
if 'base_data' not in st.session_state:
    # 默认基线数据
    st.session_state.base_data = {
        "抖音开放平台生态运营": {
            "自营": {"人力": 100, "成本": 54281, "量级": 35125},
            "X": {"人力": 100, "成本": 54281, "量级": 35125},
            "BPO": {"人力": 106, "成本": 57537, "量级": 35125}
        },
        "短剧生态运营": {
            "自营": {"人力": 19, "成本": 8337, "量级": 8132},
            "X": {"人力": 19, "成本": 8337, "量级": 8132},
            "BPO": {"人力": 19, "成本": 8338, "量级": 8131}
        },
        "游戏与社交生态运营": {
            "自营": {"人力": 158, "成本": 73626, "量级": 60120},
            "X": {"人力": 158, "成本": 73626, "量级": 60120},
            "BPO": {"人力": 158, "成本": 73627, "量级": 60121}
        }
    }

# 显示基线数据设置界面
for dept in st.session_state.base_data.keys():
    with st.expander(f"📊 {dept} - 基线数据", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        for idx, mode in enumerate(["自营", "X", "BPO"]):
            with [col1, col2, col3][idx]:
                st.markdown(f"**{mode}**")
                st.session_state.base_data[dept][mode]["人力"] = st.number_input(
                    f"{mode}人力", 
                    min_value=0, 
                    value=st.session_state.base_data[dept][mode]["人力"],
                    key=f"base_{dept}_{mode}_人力"
                )
                st.session_state.base_data[dept][mode]["成本"] = st.number_input(
                    f"{mode}成本（万元）", 
                    min_value=0, 
                    value=st.session_state.base_data[dept][mode]["成本"],
                    key=f"base_{dept}_{mode}_成本"
                )
                st.session_state.base_data[dept][mode]["量级"] = st.number_input(
                    f"{mode}量级", 
                    min_value=0, 
                    value=st.session_state.base_data[dept][mode]["量级"],
                    key=f"base_{dept}_{mode}_量级"
                )

st.markdown("---")

# ==========================================
# 第二步：调整参数
# ==========================================

st.header("📊 第二步：调整参数")

# 存储调整后的数据
adjustments = {}

# 遍历每个子部门
for dept in st.session_state.base_data.keys():
    st.subheader(f"🎯 {dept}")
    adjustments[dept] = {}

    # 三种用工模式并列显示
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**自营**")
        adjustments[dept]["自营"] = {
            "人力": st.number_input(
                "自营人力", 
                min_value=0, 
                value=st.session_state.base_data[dept]["自营"]["人力"],
                key=f"{dept}_自营_人力"
            ),
            "量级": st.number_input(
                "自营量级", 
                min_value=0, 
                value=st.session_state.base_data[dept]["自营"]["量级"],
                key=f"{dept}_自营_量级"
            )
        }

    with col2:
        st.markdown("**X**")
        adjustments[dept]["X"] = {
            "人力": st.number_input(
                "X人力", 
                min_value=0, 
                value=st.session_state.base_data[dept]["X"]["人力"],
                key=f"{dept}_X_人力"
            ),
            "量级": st.number_input(
                "X量级", 
                min_value=0, 
                value=st.session_state.base_data[dept]["X"]["量级"],
                key=f"{dept}_X_量级"
            )
        }

    with col3:
        st.markdown("**BPO**")
        adjustments[dept]["BPO"] = {
            "人力": st.number_input(
                "BPO人力", 
                min_value=0, 
                value=st.session_state.base_data[dept]["BPO"]["人力"],
                key=f"{dept}_BPO_人力"
            ),
            "量级": st.number_input(
                "BPO量级", 
                min_value=0, 
                value=st.session_state.base_data[dept]["BPO"]["量级"],
                key=f"{dept}_BPO_量级"
            )
        }

    st.markdown("---")

# 测算按钮
st.markdown("---")
if st.button("🧮 开始测算", type="primary"):
    st.header("📈 测算结果")

    # 存储结果
    results = {}
    total_dept_cost = 0
    total_dept_volume = 0

    # 遍历每个子部门
    for dept in st.session_state.base_data.keys():
        st.subheader(f"📊 {dept}")

        dept_results = {}
        dept_total_cost = 0
        dept_total_volume = 0

        # 显示三种用工模式的结果
        col1, col2, col3 = st.columns(3)

        for idx, mode in enumerate(["自营", "X", "BPO"]):
            # 计算该模式的成本
            old_data = st.session_state.base_data[dept][mode]
            new_data = adjustments[dept][mode]

            # 计算人均成本
            if old_data["人力"] > 0:
                per_capita_cost = old_data["成本"] / old_data["人力"]
            else:
                per_capita_cost = 0

            old_cost = old_data["成本"]
            new_cost = new_data["人力"] * per_capita_cost

            old_volume = old_data["量级"]
            new_volume = new_data["量级"]

            # 计算万Case成本
            if old_volume > 0:
                old_wancase = (old_cost / old_volume) * 10000
            else:
                old_wancase = 0

            if new_volume > 0:
                new_wancase = (new_cost / new_volume) * 10000
            else:
                new_wancase = 0

            # 计算变动
            labor_diff = new_data["人力"] - old_data["人力"]
            if old_wancase > 0:
                cost_change = ((new_wancase - old_wancase) / old_wancase) * 100
            else:
                cost_change = 0

            # 存储结果
            dept_results[mode] = {
                "旧人力": old_data["人力"],
                "新人力": new_data["人力"],
                "旧成本": old_cost,
                "新成本": new_cost,
                "旧量级": old_volume,
                "新量级": new_volume,
                "旧万Case成本": old_wancase,
                "新万Case成本": new_wancase
            }

            # 累加部门总量
            dept_total_cost += new_cost
            dept_total_volume += new_volume

            # 显示该模式结果
            with [col1, col2, col3][idx]:
                st.markdown(f"**{mode}**")
                st.metric("人力", f"{new_data['人力']} 人", f"{labor_diff:+d}")
                st.metric("万Case成本", f"{new_wancase:,.0f} 元", f"{cost_change:+.1f}%")
                st.write(f"成本: {old_cost:,.0f} → {new_cost:,.0f} 万元")
                st.write(f"量级: {old_volume:,} → {new_volume:,}")

        # 显示子部门汇总
        st.markdown("---")
        st.markdown(f"**📌 {dept} 汇总**")

        # 计算旧的汇总数据
        old_dept_cost = sum(st.session_state.base_data[dept][mode]["成本"] for mode in ["自营", "X", "BPO"])
        old_dept_volume = sum(st.session_state.base_data[dept][mode]["量级"] for mode in ["自营", "X", "BPO"])

        if old_dept_volume > 0:
            old_dept_wancase = (old_dept_cost / old_dept_volume) * 10000
        else:
            old_dept_wancase = 0

        if dept_total_volume > 0:
            new_dept_wancase = (dept_total_cost / dept_total_volume) * 10000
        else:
            new_dept_wancase = 0

        if old_dept_wancase > 0:
            dept_cost_change = ((new_dept_wancase - old_dept_wancase) / old_dept_wancase) * 100
        else:
            dept_cost_change = 0

        # 显示子部门汇总结果
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总成本", f"{dept_total_cost:,.0f} 万元", f"{dept_total_cost - old_dept_cost:+,.0f}")
        with col2:
            st.metric("总量级", f"{dept_total_volume:,}", f"{dept_total_volume - old_dept_volume:+,}")
        with col3:
            st.metric("万Case成本", f"{new_dept_wancase:,.0f} 元", f"{dept_cost_change:+.1f}%")

        # 累加到三级部门总量
        total_dept_cost += dept_total_cost
        total_dept_volume += dept_total_volume

        st.markdown("---")
        st.markdown("---")

    # 显示三级部门（开发者生态）汇总
    st.header("🎯 三级部门：开发者生态 汇总")

    # 计算旧的汇总数据
    old_total_cost = 0
    old_total_volume = 0
    for dept in st.session_state.base_data.keys():
        old_total_cost += sum(st.session_state.base_data[dept][mode]["成本"] for mode in ["自营", "X", "BPO"])
        old_total_volume += sum(st.session_state.base_data[dept][mode]["量级"] for mode in ["自营", "X", "BPO"])

    if old_total_volume > 0:
        old_total_wancase = (old_total_cost / old_total_volume) * 10000
    else:
        old_total_wancase = 0

    if total_dept_volume > 0:
        new_total_wancase = (total_dept_cost / total_dept_volume) * 10000
    else:
        new_total_wancase = 0

    if old_total_wancase > 0:
        total_cost_change = ((new_total_wancase - old_total_wancase) / old_total_wancase) * 100
    else:
        total_cost_change = 0

    # 显示三级部门汇总结果
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总成本", f"{total_dept_cost:,.0f} 万元", f"{total_dept_cost - old_total_cost:+,.0f}")
    with col2:
        st.metric("总量级", f"{total_dept_volume:,}", f"{total_dept_volume - old_total_volume:+,}")
    with col3:
        st.metric("万Case成本", f"{new_total_wancase:,.0f} 元", f"{total_cost_change:+.1f}%")

st.markdown("---")
st.caption("🦐 虾滑团团出品 | 万Case成本计算器 v3.0 | 基线可设置 + 用工模式拆分 + 三级部门汇总")
