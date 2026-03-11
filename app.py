#!/usr/bin/env python3
"""
万Case成本计算器 - 网页版 v7.0
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

# 侧边栏 - 目录导航
st.sidebar.header("📋 目录导航")

# 部门列表
departments = [
    "抖音开放平台生态运营",
    "短剧生态运营",
    "游戏与社交生态运营",
    "总的测算"
]

# 侧边栏的单选按钮
selected_page = st.sidebar.radio("选择查看内容", departments)

# 侧边栏 - 用工模式说明
st.sidebar.markdown("---")
st.sidebar.info("💡 支持同时调整自营/X/BPO三种用工模式")
st.sidebar.markdown("---")
st.sidebar.markdown("### 说明")
st.sidebar.markdown("""
- 先设置各部门基线数据
- 再调整各子部门不同用工模式的人力和量级
- 点击「开始测算」查看结果
- 支持实时更新测算
- 显示三级部门（开发者生态）汇总数据
""")

# 初始化session state中的基线数据
for dept in departments[:3]:
    if dept not in st.session_state:
        st.session_state[dept] = {
            "自营": {"人力": 0, "成本": 0, "量级": 0},
            "X": {"人力": 0, "成本": 0, "量级": 0},
            "BPO": {"人力": 0, "成本": 0, "量级": 0}
        }

# ==========================================
# 根据选择的页面显示内容
# ==========================================

if selected_page in departments[:3]:
    # 显示单个部门
    dept = selected_page

    # 第一步：设置该部门基线数据
    st.header(f"📋 第一步：设置 {dept} 基线数据")

    with st.expander(f"📊 {dept} - 基线数据", expanded=True):
        col1, col2, col3 = st.columns(3)

        for idx, mode in enumerate(["自营", "X", "BPO"]):
            with [col1, col2, col3][idx]:
                st.markdown(f"**{mode}**")
                st.session_state[dept][mode]["人力"] = st.number_input(
                    f"{mode}人力",
                    min_value=0,
                    value=st.session_state[dept][mode]["人力"],
                    key=f"base_{dept}_{mode}_人力"
                )
                st.session_state[dept][mode]["成本"] = st.number_input(
                    f"{mode}成本（万元）",
                    min_value=0,
                    value=st.session_state[dept][mode]["成本"],
                    key=f"base_{dept}_{mode}_成本"
                )
                st.session_state[dept][mode]["量级"] = st.number_input(
                    f"{mode}量级",
                    min_value=0,
                    value=st.session_state[dept][mode]["量级"],
                    key=f"base_{dept}_{mode}_量级"
                )

    st.markdown("---")

    # 第二步：调整该部门参数
    st.header(f"📊 第二步：调整 {dept} 参数")

    st.subheader(f"🎯 {dept}")
    adjustments = {}
    adjustments[dept] = {}

    # 三种用工模式并列显示
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**自营**")
        adjustments[dept]["自营"] = {
            "人力": st.number_input(
                "自营人力",
                min_value=0,
                value=st.session_state[dept]["自营"]["人力"],
                key=f"{dept}_自营_人力"
            ),
            "量级": st.number_input(
                "自营量级",
                min_value=0,
                value=st.session_state[dept]["自营"]["量级"],
                key=f"{dept}_自营_量级"
            )
        }

    with col2:
        st.markdown("**X**")
        adjustments[dept]["X"] = {
            "人力": st.number_input(
                "X人力",
                min_value=0,
                value=st.session_state[dept]["X"]["人力"],
                key=f"{dept}_X_人力"
            ),
            "量级": st.number_input(
                "X量级",
                min_value=0,
                value=st.session_state[dept]["X"]["量级"],
                key=f"{dept}_X_量级"
            )
        }

    with col3:
        st.markdown("**BPO**")
        adjustments[dept]["BPO"] = {
            "人力": st.number_input(
                "BPO人力",
                min_value=0,
                value=st.session_state[dept]["BPO"]["人力"],
                key=f"{dept}_BPO_人力"
            ),
            "量级": st.number_input(
                "BPO量级",
                min_value=0,
                value=st.session_state[dept]["BPO"]["量级"],
                key=f"{dept}_BPO_量级"
            )
        }

    st.markdown("---")

    # 测算按钮
    if st.button("🧮 开始测算", type="primary"):
        # 计算该部门结果，同时用基线数据计算其他部门
        all_dept_results = {}

        for current_dept in departments[:3]:
            dept_results = {}
            dept_total_cost = 0
            dept_total_volume = 0

            for idx, mode in enumerate(["自营", "X", "BPO"]):
                old_data = st.session_state[current_dept][mode]

                if current_dept == dept:
                    # 当前选中的部门用调整后的数据
                    new_data = adjustments[current_dept][mode]
                else:
                    # 其他部门用基线数据
                    new_data = old_data

                if old_data["人力"] > 0:
                    per_capita_cost = old_data["成本"] / old_data["人力"]
                else:
                    per_capita_cost = 0

                old_cost = old_data["成本"]
                new_cost = new_data["人力"] * per_capita_cost

                old_volume = old_data["量级"]
                new_volume = new_data["量级"]

                if old_volume > 0:
                    old_wancase = (old_cost / old_volume) * 10000
                else:
                    old_wancase = 0

                if new_volume > 0:
                    new_wancase = (new_cost / new_volume) * 10000
                else:
                    new_wancase = 0

                labor_diff = new_data["人力"] - old_data["人力"]
                if old_wancase > 0:
                    cost_change = ((new_wancase - old_wancase) / old_wancase) * 100
                else:
                    cost_change = 0

                dept_results[mode] = {
                    "旧人力": old_data["人力"],
                    "新人力": new_data["人力"],
                    "旧成本": old_cost,
                    "新成本": new_cost,
                    "旧量级": old_volume,
                    "新量级": new_volume,
                    "旧万Case成本": old_wancase,
                    "新万Case成本": new_wancase,
                    "人力变动": labor_diff,
                    "成本变动": cost_change
                }

                dept_total_cost += new_cost
                dept_total_volume += new_volume

            # 计算该部门汇总
            old_dept_cost = sum(st.session_state[current_dept][mode]["成本"] for mode in ["自营", "X", "BPO"])
            old_dept_volume = sum(st.session_state[current_dept][mode]["量级"] for mode in ["自营", "X", "BPO"])

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

            all_dept_results[current_dept] = {
                "mode_results": dept_results,
                "dept_total_cost": dept_total_cost,
                "dept_total_volume": dept_total_volume,
                "old_dept_cost": old_dept_cost,
                "old_dept_volume": old_dept_volume,
                "old_dept_wancase": old_dept_wancase,
                "new_dept_wancase": new_dept_wancase,
                "dept_cost_change": dept_cost_change
            }

        # 计算总的汇总
        total_dept_cost = sum(all_dept_results[d]["dept_total_cost"] for d in departments[:3])
        total_dept_volume = sum(all_dept_results[d]["dept_total_volume"] for d in departments[:3])

        old_total_cost = 0
        old_total_volume = 0
        for current_dept in departments[:3]:
            old_total_cost += sum(st.session_state[current_dept][mode]["成本"] for mode in ["自营", "X", "BPO"])
            old_total_volume += sum(st.session_state[current_dept][mode]["量级"] for mode in ["自营", "X", "BPO"])

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

        # 保存到session state
        st.session_state.all_dept_results = all_dept_results
        st.session_state.total_result = {
            "total_dept_cost": total_dept_cost,
            "total_dept_volume": total_dept_volume,
            "old_total_cost": old_total_cost,
            "old_total_volume": old_total_volume,
            "old_total_wancase": old_total_wancase,
            "new_total_wancase": new_total_wancase,
            "total_cost_change": total_cost_change
        }

    # 显示该部门结果
    if 'all_dept_results' in st.session_state and 'total_result' in st.session_state:
        st.header("📈 测算结果")

        dept_data = st.session_state.all_dept_results[dept]

        st.subheader(f"📊 {dept}")

        # 显示三种用工模式的结果
        col1, col2, col3 = st.columns(3)

        for idx, mode in enumerate(["自营", "X", "BPO"]):
            mode_data = dept_data["mode_results"][mode]
            with [col1, col2, col3][idx]:
                st.markdown(f"**{mode}**")
                st.metric("人力", f"{mode_data['新人力']} 人", f"{mode_data['人力变动']:+d}")
                st.metric("万Case成本", f"{mode_data['新万Case成本']:,.0f} 元", f"{mode_data['成本变动']:+.1f}%")
                st.write(f"成本: {mode_data['旧成本']:,.0f} → {mode_data['新成本']:,.0f} 万元")
                st.write(f"量级: {mode_data['旧量级']:,} → {mode_data['新量级']:,}")

        # 显示该部门汇总
        st.markdown("---")
        st.markdown(f"**📌 {dept} 汇总**")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总成本", f"{dept_data['dept_total_cost']:,.0f} 万元", f"{dept_data['dept_total_cost'] - dept_data['old_dept_cost']:+,.0f}")
        with col2:
            st.metric("总量级", f"{dept_data['dept_total_volume']:,}", f"{dept_data['dept_total_volume'] - dept_data['old_dept_volume']:+,}")
        with col3:
            st.metric("万Case成本", f"{dept_data['new_dept_wancase']:,.0f} 元", f"{dept_data['dept_cost_change']:+.1f}%")

else:
    # 显示总的测算
    st.header("📋 第一步：设置各部门基线数据")

    # 显示每个部门的基线数据设置界面
    for dept in departments[:3]:
        with st.expander(f"📊 {dept} - 基线数据", expanded=True):
            col1, col2, col3 = st.columns(3)

            for idx, mode in enumerate(["自营", "X", "BPO"]):
                with [col1, col2, col3][idx]:
                    st.markdown(f"**{mode}**")
                    st.session_state[dept][mode]["人力"] = st.number_input(
                        f"{mode}人力",
                        min_value=0,
                        value=st.session_state[dept][mode]["人力"],
                        key=f"base_{dept}_{mode}_人力"
                    )
                    st.session_state[dept][mode]["成本"] = st.number_input(
                        f"{mode}成本（万元）",
                        min_value=0,
                        value=st.session_state[dept][mode]["成本"],
                        key=f"base_{dept}_{mode}_成本"
                    )
                    st.session_state[dept][mode]["量级"] = st.number_input(
                        f"{mode}量级",
                        min_value=0,
                        value=st.session_state[dept][mode]["量级"],
                        key=f"base_{dept}_{mode}_量级"
                    )

    st.markdown("---")

    # 第二步：调整参数
    st.header("📊 第二步：调整参数")

    # 存储调整后的数据
    adjustments = {}

    # 遍历每个子部门
    for dept in departments[:3]:
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
                    value=st.session_state[dept]["自营"]["人力"],
                    key=f"{dept}_自营_人力"
                ),
                "量级": st.number_input(
                    "自营量级",
                    min_value=0,
                    value=st.session_state[dept]["自营"]["量级"],
                    key=f"{dept}_自营_量级"
                )
            }

        with col2:
            st.markdown("**X**")
            adjustments[dept]["X"] = {
                "人力": st.number_input(
                    "X人力",
                    min_value=0,
                    value=st.session_state[dept]["X"]["人力"],
                    key=f"{dept}_X_人力"
                ),
                "量级": st.number_input(
                    "X量级",
                    min_value=0,
                    value=st.session_state[dept]["X"]["量级"],
                    key=f"{dept}_X_量级"
                )
            }

        with col3:
            st.markdown("**BPO**")
            adjustments[dept]["BPO"] = {
                "人力": st.number_input(
                    "BPO人力",
                    min_value=0,
                    value=st.session_state[dept]["BPO"]["人力"],
                    key=f"{dept}_BPO_人力"
                ),
                "量级": st.number_input(
                    "BPO量级",
                    min_value=0,
                    value=st.session_state[dept]["BPO"]["量级"],
                    key=f"{dept}_BPO_量级"
                )
            }

        st.markdown("---")

    # 测算按钮
    st.markdown("---")
    if st.button("🧮 开始测算", type="primary"):
        # 先计算总的结果，保存到session state
        total_dept_cost = 0
        total_dept_volume = 0
        all_dept_results = {}

        for dept in departments[:3]:
            dept_results = {}
            dept_total_cost = 0
            dept_total_volume = 0

            for idx, mode in enumerate(["自营", "X", "BPO"]):
                old_data = st.session_state[dept][mode]
                new_data = adjustments[dept][mode]

                if old_data["人力"] > 0:
                    per_capita_cost = old_data["成本"] / old_data["人力"]
                else:
                    per_capita_cost = 0

                old_cost = old_data["成本"]
                new_cost = new_data["人力"] * per_capita_cost

                old_volume = old_data["量级"]
                new_volume = new_data["量级"]

                if old_volume > 0:
                    old_wancase = (old_cost / old_volume) * 10000
                else:
                    old_wancase = 0

                if new_volume > 0:
                    new_wancase = (new_cost / new_volume) * 10000
                else:
                    new_wancase = 0

                labor_diff = new_data["人力"] - old_data["人力"]
                if old_wancase > 0:
                    cost_change = ((new_wancase - old_wancase) / old_wancase) * 100
                else:
                    cost_change = 0

                dept_results[mode] = {
                    "旧人力": old_data["人力"],
                    "新人力": new_data["人力"],
                    "旧成本": old_cost,
                    "新成本": new_cost,
                    "旧量级": old_volume,
                    "新量级": new_volume,
                    "旧万Case成本": old_wancase,
                    "新万Case成本": new_wancase,
                    "人力变动": labor_diff,
                    "成本变动": cost_change
                }

                dept_total_cost += new_cost
                dept_total_volume += new_volume

            # 计算该部门汇总
            old_dept_cost = sum(st.session_state[dept][mode]["成本"] for mode in ["自营", "X", "BPO"])
            old_dept_volume = sum(st.session_state[dept][mode]["量级"] for mode in ["自营", "X", "BPO"])

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

            all_dept_results[dept] = {
                "mode_results": dept_results,
                "dept_total_cost": dept_total_cost,
                "dept_total_volume": dept_total_volume,
                "old_dept_cost": old_dept_cost,
                "old_dept_volume": old_dept_volume,
                "old_dept_wancase": old_dept_wancase,
                "new_dept_wancase": new_dept_wancase,
                "dept_cost_change": dept_cost_change
            }

            total_dept_cost += dept_total_cost
            total_dept_volume += dept_total_volume

        # 计算总的汇总
        old_total_cost = 0
        old_total_volume = 0
        for dept in departments[:3]:
            old_total_cost += sum(st.session_state[dept][mode]["成本"] for mode in ["自营", "X", "BPO"])
            old_total_volume += sum(st.session_state[dept][mode]["量级"] for mode in ["自营", "X", "BPO"])

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

        # 保存到session state
        st.session_state.all_dept_results = all_dept_results
        st.session_state.total_result = {
            "total_dept_cost": total_dept_cost,
            "total_dept_volume": total_dept_volume,
            "old_total_cost": old_total_cost,
            "old_total_volume": old_total_volume,
            "old_total_wancase": old_total_wancase,
            "new_total_wancase": new_total_wancase,
            "total_cost_change": total_cost_change
        }

    # 显示总的测算结果
    if 'all_dept_results' in st.session_state and 'total_result' in st.session_state:
        st.header("📈 测算结果")

        # 先显示每个部门的结果
        for dept in departments[:3]:
            dept_data = st.session_state.all_dept_results[dept]

            st.subheader(f"📊 {dept}")

            # 显示三种用工模式的结果
            col1, col2, col3 = st.columns(3)

            for idx, mode in enumerate(["自营", "X", "BPO"]):
                mode_data = dept_data["mode_results"][mode]
                with [col1, col2, col3][idx]:
                    st.markdown(f"**{mode}**")
                    st.metric("人力", f"{mode_data['新人力']} 人", f"{mode_data['人力变动']:+d}")
                    st.metric("万Case成本", f"{mode_data['新万Case成本']:,.0f} 元", f"{mode_data['成本变动']:+.1f}%")
                    st.write(f"成本: {mode_data['旧成本']:,.0f} → {mode_data['新成本']:,.0f} 万元")
                    st.write(f"量级: {mode_data['旧量级']:,} → {mode_data['新量级']:,}")

            # 显示该部门汇总
            st.markdown("---")
            st.markdown(f"**📌 {dept} 汇总**")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总成本", f"{dept_data['dept_total_cost']:,.0f} 万元", f"{dept_data['dept_total_cost'] - dept_data['old_dept_cost']:+,.0f}")
            with col2:
                st.metric("总量级", f"{dept_data['dept_total_volume']:,}", f"{dept_data['dept_total_volume'] - dept_data['old_dept_volume']:+,}")
            with col3:
                st.metric("万Case成本", f"{dept_data['new_dept_wancase']:,.0f} 元", f"{dept_data['dept_cost_change']:+.1f}%")

            st.markdown("---")

        # 显示总的汇总
        st.header("🎯 三级部门：开发者生态 汇总")

        total_data = st.session_state.total_result

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总成本", f"{total_data['total_dept_cost']:,.0f} 万元", f"{total_data['total_dept_cost'] - total_data['old_total_cost']:+,.0f}")
        with col2:
            st.metric("总量级", f"{total_data['total_dept_volume']:,}", f"{total_data['total_dept_volume'] - total_data['old_total_volume']:+,}")
        with col3:
            st.metric("万Case成本", f"{total_data['new_total_wancase']:,.0f} 元", f"{total_data['total_cost_change']:+.1f}%")

st.markdown("---")
st.caption("🦐 虾滑团团出品 | 万Case成本计算器 v7.0 | 单部门独立显示 + 保持其他部门不变 + 总的测算页面 + 保留原有功能")

