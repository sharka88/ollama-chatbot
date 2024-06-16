import streamlit as st
import ollama

def main():
    st.title("AI聊天室")


    model_list = ollama.list()['models']
    model_names = [model['model'] for model in model_list]

    #如果 session_state 中尚未設置模型，則設置預設模型
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = model_names[0]  # 預設選擇列表中的第一個模型

    #創建一個下拉選單，並使用 session_state 來記錄選擇
    selected_model = st.selectbox("選擇模型", model_names, index=model_names.index(st.session_state.selected_model))
    st.session_state.selected_model = selected_model  # 更新選擇的模型

    #設置用戶輸入框
    user_input = st.text_area("你好！有什麼我可以幫上忙的嗎？", "")

    #當使用者按下送出按鈕後的處理
    if st.button("提交"):
        if user_input:
            #使用選擇的模型進行推理
            response = ollama.chat(model=st.session_state.selected_model, messages=[{'role': 'user', 'content': user_input}])
            
            #顯示回答
            st.text("回答：")
            if 'message' in response:
                st.write(selected_model)
            else:
                st.error("推理錯誤，請檢查輸出")
        else:
            st.warning("請輸入問題！")

if __name__ == "__main__":
    main()
