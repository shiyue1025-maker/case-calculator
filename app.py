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

#### 基准数据（1月）- 按用工模式拆分
<br>
#### 结构: base_data[部门][模式] = {人力, 成本, 量级, 人均成本}
base_data = {
    "抖音开放平台生态运营": {
        "自营": {"人力": 100, "成本": 54281, "量级": 35125, "人均成本": 542.81},
        "X": {"人力": 100, "成本": 54281, "量级": 35125, "人均成本": 542.81},
        "BPO": {"人力": 106, "成本": 57537, "量级": 35125, "人均成本": 542.81}
    },
    "短剧生态运营": {
        "自营": {"人力": 19, "成本": 8337, "量级": 8132, "人均成本": 438.81},
        "X": {"人力": 19, "成本": 8337, "量级": 8132, "人均成本": 438.81},
        "BPO": {"人力": 19, "成本": 8338, "量级": 8131, "人均成本": 438.81}
    },
    "游戏与社交生态运营": {
        "自营": {"人力": 158, "成本": 73626, "量级": 60120, "人均成本": 465.99},
        "X": {"人力": 158, "成本": 73626, "量级": 60120, "人均成本": 465.99},
        "BPO": {"人力": 158, "成本": 73627, "量级": 60121, "人均成本": 465.99}
    }
}

st.title("🦐 万Case成本计算器 🦐")
st.markdown("---")

#### 侧边栏 - 用工模式说明
st.sidebar.header("用工模式设置")
st.sidebar.info("💡 支持同时调整自营/X/BPO三种用工模式")
st.sidebar.markdown("---")
st.sidebar.markdown("### 说明")
st.sidebar.markdown("""
- 调整各子部门不同用工模式的人力和量级
- 点击「开始测算」查看结果
- 支持实时更新测算
- 显示三级部门（开发者生态）汇总数据
""")

#### 主界面 - 输入区域
st.header("📊 调整参数")

#### 存储调整后的数据
adjustments = {}

#### 遍历每个子部门
for dept in base_data.keys():
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
                value=base_data[dept]["自营"]["人力"],
                key=f"{dept}_自营_人力"
            ),
            "量级": st.number_input(
                "自营量级", 
                min_value=0, 
                value=base_data[dept]["自营"]["量级"],
                key=f"{dept}_自营_量级"
            )
        }
    
    with col2:
        st.markdown("**X**")
        adjustments[dept]["X"] = {
            "人力": st.number_input(
                "X人力", 
                min_value=0, 
                value=base_data[dept]["X"]["人力"],
                key=f"{dept}_X_人力"
            ),
            "量级": st.number_input(
                "X量级", 
                min_value=0, 
                value=base_data[dept]["X"]["量级"],
                key=f"{dept}_X_量级"
            )
        }
    
    with col3:
        st.markdown("**BPO**")
        adjustments[dept]["BPO"] = {
            "人力": st.number_input(
                "BPO人力", 
                min_value=0, 
                value=base_data[dept]["BPO"]["人力"],
                key=f"{dept}_BPO_人力"
            ),
            "量级": st.number_input(
                "BPO量级", 
                min_value=0, 
                value=base_data[dept]["BPO"]["量级"],
                key=f"{dept}_BPO_量级"
            )
        }
    
    st.markdown("---")

#### 测算按钮
st.markdown("---")
if st.button("🧮 开始测算", type="primary"):
    st.header("📈 测算结果")

    # 存储结果
    results = {}
    total_dept_cost = 0
    total_dept_volume = 0
    
    # 遍历每个子部门
    for dept in base_data.keys():
        st.subheader(f"📊 {dept}")
        
        dept_results = {}
        dept_total_cost = 0
        dept_total_volume = 0
        
        # 显示三种用工模式的结果
        col1, col2, col3 = st.columns(3)
        
        for idx, mode in enumerate(["自营", "X", "BPO"]):
            # 计算该模式的成本
            old_data = base_data[dept][mode]
            new_data = adjustments[dept][mode]
            
            old_cost = old_data["成本"]
            new_cost = new_data["人力"] * old_data["人均成本"]
            
            old_volume = old_data["量级"]
            new_volume = new_data["量级"]
            
            # 计算万Case成本
            if old_volume > 0:
                old_wancase = (old_cost / old_volume) * 10000
            else:
                old_wancase = 0
