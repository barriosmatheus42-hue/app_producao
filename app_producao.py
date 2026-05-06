import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da página
st.set_page_config(page_title="Painel Gerdau", layout="wide")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. CSS (O mesmo visual compacto que você gostou)
def inject_custom_css():
    st.markdown("""
        <style>
        .section-title { font-size: 1.1rem; font-weight: bold; margin-top: 0.2rem; margin-bottom: 0.4rem; border-bottom: 2px solid #e0e0e0; }
        .section-title.tu { color: #4285f4; border-color: #4285f4; }
        .section-title.rb { color: #34a853; border-color: #34a853; }
        .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(105px, 1fr)); gap: 0.3rem; margin-bottom: 0.5rem; }
        .machine-card { background-color: #ffffff; border-radius: 6px; padding: 0.3rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #ccc; display: flex; flex-direction: column; align-items: center; text-align: center; }
        .status-rodando { border-left-color: #34a853; }      
        .status-manutencao { border-left-color: #ea4335; }  
        .status-troca { border-left-color: #fbbc05; }       
        .status-parada { border-left-color: #757575; }      
        .machine-name { font-size: 0.85rem; font-weight: bold; color: #1f1f1f !important; }
        .bitola-value { font-size: 1rem; font-weight: bold; color: #1a73e8 !important; }
        .rb-fonte { font-size: 0.65rem; color: #555555 !important; }
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# 3. CARREGAMENTO DOS DADOS (Vindo da Planilha ou Padrão)
# Aqui ele tenta ler a planilha. Se não existir, ele usa o padrão que definimos.
def load_data():
    try:
        # Tenta ler as abas 'TUs' e 'RBs' da sua planilha
        df_tu = conn.read(worksheet="TUs")
        df_rb = conn.read(worksheet="RBs")
        return df_tu, df_rb
    except:
        # Caso seja a primeira vez ou dê erro, cria os dados padrão
        tu_init = pd.DataFrame({
            "Máquina": [f"TU {str(i).zfill(2)}" for i in range(1, 25)],
            "Bitola (mm)": [1.20] * 24,
            "Status": ["Desprogramada"] * 24
        })
        rb_init = pd.DataFrame({
            "Equipamento": [f"RB {str(i).zfill(2)}" for i in range(1, 19)] + ["Barrica 2", "Barrica 3", "Barrica 4"],
            "Bitola (mm)": [1.20] * 21,
            "Fonte (TU)": ["-"] * 21,
            "Status": ["Desprogramada"] * 21
        })
        return tu_init, rb_init

df_tu, df_rb = load_data()

# 4. INÍCIO DA PÁGINA
inject_custom_css()
st.title("🏭 Painel de Produção Gerdau")

# --- ÁREA DE EDIÇÃO ---
with st.expander("⚙️ CONFIGURAR TURNO (Alterações fixas)", expanded=False):
    st.info("As alterações feitas aqui só serão salvas permanentemente ao clicar no botão 'SALVAR CONFIGURAÇÃO' abaixo.")
    
    opcoes_status = ["Rodando", "Manutenção", "Troca de Bitola", "Parada", "Desprogramada"]
    opcoes_bitola = [1.00, 1.20, 1.32, 1.60]
    opcoes_fonte = ["-"] + [f"TU {str(i).zfill(2)}" for i in range(1, 25)]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Trefilas Úmidas")
        new_tu = st.data_editor(df_tu, hide_index=True, use_container_width=True, key="tu_ed",
                                column_config={"Máquina": st.column_config.TextColumn(disabled=True),
                                              "Bitola (mm)": st.column_config.SelectboxColumn(options=opcoes_bitola),
                                              "Status": st.column_config.SelectboxColumn(options=opcoes_status)})
    with col2:
        st.subheader("Rebobinadores & Barricas")
        new_rb = st.data_editor(df_rb, hide_index=True, use_container_width=True, key="rb_ed",
                                column_config={"Equipamento": st.column_config.TextColumn(disabled=True),
                                              "Bitola (mm)": st.column_config.SelectboxColumn(options=opcoes_bitola),
                                              "Fonte (TU)": st.column_config.SelectboxColumn(options=opcoes_fonte),
                                              "Status": st.column_config.SelectboxColumn(options=opcoes_status)})

    if st.button("💾 SALVAR CONFIGURAÇÃO ATUAL"):
        # Salva os novos dados de volta na planilha do Google
        conn.update(worksheet="TUs", data=new_tu)
        conn.update(worksheet="RBs", data=new_rb)
        st.success("Configuração salva com sucesso! Agora ela aparecerá fixamente.")
        st.rerun()

# --- ÁREA DE VISUALIZAÇÃO ---
st.markdown("---")
# (O código de renderização dos cards continua o mesmo daqui para baixo, usando new_tu e new_rb)
# ... [Código de renderização dos cards que você já tem] ...
