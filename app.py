import streamlit as st
from backend import *
from datetime import datetime

with open("./main.css",encoding="utf-8") as f:
    style_file_content = f.read()
st.set_page_config(
    page_title="Thesis",  # Custom title shown in browser tab
    page_icon="🎓",         # Custom favicon (emoji or URL)
    layout="wide"             # "wide" for full-screen layout
)

def format_timedelta(start, end, level):
    delta = end - start
    minutes, seconds = divmod(delta.total_seconds(), 60)
    return f"{level} completed:\n{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')} - {int(minutes)} mins {int(seconds)}s"

def main():
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None
    if 'timed_result' not in st.session_state:
        st.session_state.timed_result = ""
    sidebar = st.sidebar
    st.title('IUFlowGen App :mortar_board:')
    st.write('This is a system to turn documents into comprehensible flowcharts')
    st.sidebar.title(':gear: Menu Settings')
    # selection a level
    level = sidebar.selectbox(
        'Select flowchart detail level:',
        ['None','Level 1', 'Level 2', 'Level 3', 'Level 4']
    )
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        view_chart = col1.toggle("Show chart", value=True)
        rankdir_option=col1.selectbox("Choose flow direction", options=["LR", "TB"], index=0) 
       
    with col2:
        view_doc = col2.toggle("Show doc", value=True)
        chart_mode = col2.radio("Choose view mode", options=["overview", "detailed"], index=0)
        
    if level == 'Level 1':
        st.sidebar.write('You selected Level 1')
        with open ('level1.txt', 'r') as f:
                level1 = f.read()
        dot_code = clean_dot_code(level1)   
        st.session_state.dot_code = dot_code
        if view_chart and "dot_code" in st.session_state:
            dot= convert_clusters_to_nodes(st.session_state.dot_code)
            full_code = st.session_state.dot_code
            if chart_mode == "detailed":
                full_code = beatify_dot_code(full_code)
                dot_code_modified = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", full_code)
                render_dot_to_streamlit(dot_code_modified)
            else:
                dot = beatify_dot_code(dot)
                dot = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", dot)
                render_dot_to_streamlit(dot)
    elif level == 'Level 2':
        st.sidebar.write('You selected Level 2')
        with open ('level2.txt', 'r') as f:
                level2 = f.read()
        dot_code = clean_dot_code(level2)   
        st.session_state.dot_code = dot_code
        if view_chart and "dot_code" in st.session_state:
            dot= convert_clusters_to_nodes(st.session_state.dot_code)
            full_code = st.session_state.dot_code
            if chart_mode == "detailed":
                full_code = beatify_dot_code(full_code)
                dot_code_modified = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", full_code)
                render_dot_to_streamlit(dot_code_modified)
            else:
                dot = beatify_dot_code(dot)
                dot = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", dot)
                render_dot_to_streamlit(dot)
    elif level == 'Level 3':
        st.sidebar.write('You selected Level 3')
        with open ('level3.txt', 'r') as f:
                level3 = f.read()
        dot_code = clean_dot_code(level3)   
        st.session_state.dot_code = dot_code
        if view_chart and "dot_code" in st.session_state:
            dot= convert_clusters_to_nodes(st.session_state.dot_code)
            full_code = st.session_state.dot_code
            if chart_mode == "detailed":
                full_code = beatify_dot_code(full_code)
                dot_code_modified = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", full_code)
                render_dot_to_streamlit(dot_code_modified)
            else:
                dot = beatify_dot_code(dot)
                dot = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", dot)
                render_dot_to_streamlit(dot)
    elif level == 'Level 4':
        st.sidebar.write('You selected Level 4')
        with open ('level4.txt', 'r') as f:
                level4 = f.read()
        dot_code = clean_dot_code(level4)   
        st.session_state.dot_code = dot_code
        if view_chart and "dot_code" in st.session_state:
            dot= convert_clusters_to_nodes(st.session_state.dot_code)
            full_code = st.session_state.dot_code
            if chart_mode == "detailed":
                full_code = beatify_dot_code(full_code)
                dot_code_modified = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", full_code)
                render_dot_to_streamlit(dot_code_modified)
            else:
                dot = beatify_dot_code(dot)
                dot = re.sub(r"rankdir=\s*\w+;", f"rankdir={rankdir_option};", dot)
                render_dot_to_streamlit(dot)
    if st.sidebar.button("Mark Time"):
        now = datetime.now()
        if st.session_state.start_time is None:
            st.session_state.start_time = now
            st.sidebar.success(f"Start time recorded: {now.strftime('%H:%M:%S')}")
        else:
            st.session_state.end_time = now
            st.session_state.timed_result = format_timedelta(st.session_state.start_time, st.session_state.end_time, level)
            st.session_state.start_time = None  # Reset for next round

    # Display result
    if st.session_state.timed_result:
        st.sidebar.info(st.session_state.timed_result)
if __name__ == "__main__":
    main()

