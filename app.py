import streamlit as st
import random
import streamlit.components.v1 as components 

# --- 設定網頁標題 ---
st.set_page_config(page_title="2048", page_icon="🎮")

# --- 1. 遊戲核心邏輯 ---
def start_game():
    mat = []
    for i in range(4):
        mat.append([0] * 4)
    add_new_2(mat)
    add_new_2(mat)
    return mat

def add_new_2(mat):
    empty_cells = []
    for r in range(4):
        for c in range(4):
            if mat[r][c] == 0:
                empty_cells.append((r, c))
    if empty_cells:
        r, c = random.choice(empty_cells)
        mat[r][c] = 2

def compress(mat):
    changed = False
    new_mat = []
    for i in range(4):
        new_mat.append([0] * 4)
    for i in range(4):
        pos = 0
        for j in range(4):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1
    return new_mat, changed

def merge(mat):
    changed = False
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0
                changed = True
    return mat, changed

def reverse(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][3 - j])
    return new_mat

def transpose(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    return new_mat

def move_left(grid):
    new_grid, changed1 = compress(grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    return new_grid, changed

def move_right(grid):
    new_grid = reverse(grid)
    new_grid, changed = move_left(new_grid)
    new_grid = reverse(new_grid)
    return new_grid, changed

def move_up(grid):
    new_grid = transpose(grid)
    new_grid, changed = move_left(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed

def move_down(grid):
    new_grid = transpose(grid)
    new_grid, changed = move_right(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed

def check_status(mat):
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 2048:
                return 'WON'
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 0:
                return 'GAME NOT OVER'
    for i in range(3):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] or mat[i][j] == mat[i + 1][j]:
                return 'GAME NOT OVER'
    for j in range(3):
        if mat[3][j] == mat[3][j + 1]: return 'GAME NOT OVER'
    for i in range(3):
        if mat[i][3] == mat[i + 1][3]: return 'GAME NOT OVER'
    return 'LOST'

# --- 2. 網頁介面邏輯 ---

if 'board' not in st.session_state:
    st.session_state.board = start_game()
    st.session_state.status = 'GAME NOT OVER'

def get_color(num):
    colors = {0:"#cdc1b4", 2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", 32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", 512:"#edc850", 1024:"#edc53f", 2048:"#edc22e"}
    return colors.get(num, "#3c3a32")

def get_text_color(num):
    return "#776e65" if num < 8 else "#f9f6f2"

def display_board(board):
    html_board = '<div style="background-color:#bbada0; padding:10px; border-radius:6px; width:330px; height:330px;">'
    for row in board:
        html_board += '<div style="display:flex; justify-content:space-between; margin-bottom:10px;">'
        for num in row:
            display_num = str(num) if num != 0 else ""
            bg_color = get_color(num)
            txt_color = get_text_color(num)
            html_board += f'<div style="width:70px; height:70px; background-color:{bg_color}; color:{txt_color}; font-size:24px; font-weight:bold; display:flex; justify-content:center; align-items:center; border-radius:3px;">{display_num}</div>'
        html_board += '</div>'
    html_board += '</div>'
    st.markdown(html_board, unsafe_allow_html=True)

def handle_move(direction):
    if st.session_state.status != 'GAME NOT OVER': return
    changed = False
    if direction == 'UP': st.session_state.board, changed = move_up(st.session_state.board)
    elif direction == 'DOWN': st.session_state.board, changed = move_down(st.session_state.board)
    elif direction == 'LEFT': st.session_state.board, changed = move_left(st.session_state.board)
    elif direction == 'RIGHT': st.session_state.board, changed = move_right(st.session_state.board)
    
    if changed:
        add_new_2(st.session_state.board)
        st.session_state.status = check_status(st.session_state.board)

# --- 版面配置 ---
st.title("🎮 Python 2048")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    display_board(st.session_state.board)
    st.write("") 
    
    # --- 修改重點：按鈕佈局改為倒T型 ---
    
    # 第一排：中間是「上」
    m1, m2, m3 = st.columns([1, 1, 1])
    with m2:
        if st.button("⬆️ 上", key="btn_up"):
            handle_move('UP')
            st.rerun()
            
    # 第二排：左、下、右
    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        if st.button("⬅️ 左", key="btn_left"):
            handle_move('LEFT')
            st.rerun()
    with b2:
        if st.button("⬇️ 下", key="btn_down"):
            handle_move('DOWN')
            st.rerun()
    with b3:
        if st.button("➡️ 右", key="btn_right"):
            handle_move('RIGHT')
            st.rerun()
    # --------------------------------

    if st.session_state.status == 'WON':
        st.success("🎉 贏了！")
        if st.button("再玩一次"):
            st.session_state.board = start_game()
            st.session_state.status = 'GAME NOT OVER'
            st.rerun()
    elif st.session_state.status == 'LOST':
        st.error("💀 輸了...")
        if st.button("重試"):
            st.session_state.board = start_game()
            st.session_state.status = 'GAME NOT OVER'
            st.rerun()

# --- 3. 鍵盤控制 (JavaScript 加強版) ---
components.html("""
<script>
const doc = window.parent.document;
const keyMap = {
    'w': '⬆️ 上', 'a': '⬅️ 左', 's': '⬇️ 下', 'd': '➡️ 右',
    'arrowup': '⬆️ 上', 'arrowleft': '⬅️ 左', 'arrowdown': '⬇️ 下', 'arrowright': '➡️ 右'
};

doc.addEventListener('keydown', function(e) {
    const key = e.key.toLowerCase();
    if (key in keyMap) {
        const targetText = keyMap[key];
        const buttons = Array.from(doc.querySelectorAll('button'));
        const targetButton = buttons.find(b => b.innerText.includes(targetText));
        
        if (targetButton) {
            targetButton.click();
        }
    }
});
</script>
""", height=0)
