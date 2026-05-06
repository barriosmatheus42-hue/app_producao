import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Painel Gerdau", layout="wide")

# 2. CSS ULTRA-COMPACTO
st.markdown("""
    <style>
    .section-title { font-size: 1.1rem; font-weight: bold; margin-top: 0.2rem; border-bottom: 2px solid #e0e0e0; }
    .section-title.tu { color: #4285f4; border-color: #4285f4; }
    .section-title.rb { color: #34a853; border-color: #34a853; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(105px, 1fr)); gap: 0.3rem; }
    .machine-card { background-color: #ffffff; border-radius: 6px; padding: 0.3rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #ccc; display: flex; flex-direction: column; align-items: center; text-align: center; }
    .status-rodando { border-left-color: #34a853; }      
    .status-manutencao { border-left-color: #ea4335; }  
    .status-troca { border-left-color: #fbbc05; }       
    .status-parada { border-left-color: #757575; }      
    .machine-name { font-size: 0.85rem; font-weight: bold; color: #1f1f1f !important; }
    .bitola-value { font-size: 1rem; font-weight: bold; color: #1a73e8 !important; }
    .rb-fonte { font-size: 0.65rem; color: #555555 !important; }
    #MainMenu, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 3. DEFINIÇÃO DO ESTADO NATURAL (DEFAULT)
tus_rodando = ["TU 01", "TU 02", "TU 04", "TU 05", "TU 06", "TU 20", "TU 21", "TU 22", "TU 23", "TU 24"]
rbs_rodando = ["RB 12", "RB 13", "RB 14", "Barrica 2", "Barrica 3", "Barrica 4"]

if 'tu_data' not in st.session_state:
    df_tu = pd.DataFrame({
        "Máquina": [f"TU {str(i).zfill(2)}" for i in range(1, 25)],
        "Bitola (mm)": [1.20] * 24,
        "Status": ["Desprogramada"] * 24
    })
    # Aplica o estado "Rodando" para as TUs selecionadas
    df_tu.loc[df_tu["Máquina"].isin(tus_rodando), "Status"] = "Rodando"
    st.session_state.tu_data = df_tu

if 'rb_data' not in st.session_state:
    equipamentos = [f"RB {str(i).zfill(2)}" for i in range(1, 19)] + ["Barrica 2", "Barrica 3", "Barrica 4"]
    df_rb = pd.DataFrame({
        "Equipamento": equipamentos,
        "Bitola (mm)": [1.20] * len(equipamentos),
        "Fonte (TU)": ["-"] * len(equipamentos),
        "Status": ["Desprogramada"] * len(equipamentos)
    })
    # Aplica o estado "Rodando" para as RBs e Barricas selecionadas
    df_rb.loc[df_rb["Equipamento"].isin(rbs_rodando), "Status"] = "Rodando"
    st.session_state.rb_data = df_rb

# --- INTERFACE ---
st.title("🏭 Painel de Produção")

with st.expander("⚙️ ATUALIZAR DADOS", expanded=False):
    opcoes_status = ["Rodando", "Manutenção", "Troca de Bitola", "Parada", "Desprogramada"]
    opcoes_bitola = [1.00, 1.20, 1.32, 1.60]
    opcoes_fonte = ["-"] + [f"TU {str(i).zfill(2)}" for i in range(1, 25)]

    st.session_state.tu_data = st.data_editor(st.session_state.tu_data, hide_index=True, use_container_width=True,
        column_config={"Máquina": st.column_config.TextColumn(disabled=True),
                      "Bitola (mm)": st.column_config.SelectboxColumn(options=opcoes_bitola),
                      "Status": st.column_config.SelectboxColumn(options=opcoes_status)})

    st.session_state.rb_data = st.data_editor(st.session_state.rb_data, hide_index=True, use_container_width=True,
        column_config={"Equipamento": st.column_config.TextColumn(disabled=True),
                      "Bitola (mm)": st.column_config.SelectboxColumn(options=opcoes_bitola),
                      "Fonte (TU)": st.column_config.SelectboxColumn(options=opcoes_fonte),
                      "Status": st.column_config.SelectboxColumn(options=opcoes_status)})

# --- CARDS VISUAIS ---
def get_status_class(status):
    return {"Rodando": "status-rodando", "Manutenção": "status-manutencao", "Troca de Bitola": "status-troca", "Parada": "status-parada"}.get(status, "")

# TUs
st.markdown('<div class="section-title tu">🔵 Trefilas Úmidas</div>', unsafe_allow_html=True)
df_tu_p = st.session_state.tu_data[st.session_state.tu_data["Status"] != "Desprogramada"]
cards_tu = '<div class="card-grid">'
for _, r in df_tu_p.iterrows():
    cards_tu += f'<div class="machine-card {get_status_class(r["Status"])}"><div class="machine-name">⚙️ {r["Máquina"]}</div><div class="bitola-value">{r["Bitola (mm)"]:.2f} mm</div></div>'
st.markdown(cards_tu + '</div>', unsafe_allow_html=True)

# RBs
st.markdown('<div class="section-title rb">🟢 Rebobinadores & Barricas</div>', unsafe_allow_html=True)
df_rb_p = st.session_state.rb_data[st.session_state.rb_data["Status"] != "Desprogramada"]
cards_rb = '<div class="card-grid">'
for _, r in df_rb_p.iterrows():
    icon = "🛢️" if "Barrica" in r['Equipamento'] else "🔄"
    cards_rb += f'<div class="machine-card {get_status_class(r["Status"])}"><div class="machine-name">{icon} {r["Equipamento"]}</div><div class="bitola-value">{r["Bitola (mm)"]:.2f} mm</div>'
    if r['Fonte (TU)'] != "-": cards_rb += f'<div class="rb-fonte">F: {r["Fonte (TU)"]}</div>'
    cards_rb += '</div>'
st.markdown(cards_rb + '</div>', unsafe_allow_html=True)
