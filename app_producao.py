import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Painel Gerdau", layout="wide")

# 2. CSS ULTRA-COMPACTO
def inject_custom_css():
    st.markdown("""
        <style>
        .section-title {
            font-size: 1.1rem;
            font-weight: bold;
            margin-top: 0.2rem;
            margin-bottom: 0.4rem;
            padding-bottom: 0.1rem;
            border-bottom: 2px solid #e0e0e0;
        }
        .section-title.tu { color: #4285f4; border-color: #4285f4; }
        .section-title.rb { color: #34a853; border-color: #34a853; }

        .card-grid {
            display: grid;
            /* Força a caber mais cards por linha (min 105px) */
            grid-template-columns: repeat(auto-fill, minmax(105px, 1fr));
            gap: 0.3rem;
            margin-bottom: 0.5rem;
        }

        .machine-card {
            background-color: #ffffff; 
            border-radius: 6px;
            padding: 0.3rem; /* Quase sem espaço sobrando */
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-left: 5px solid #ccc; 
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .status-rodando { border-left-color: #34a853; }      
        .status-manutencao { border-left-color: #ea4335; }  
        .status-troca { border-left-color: #fbbc05; }       
        .status-parada { border-left-color: #757575; }      

        .card-header {
            display: flex;
            align-items: center;
            gap: 4px;
            margin-bottom: 0.2rem;
        }
        
        .machine-name {
            font-size: 0.85rem; /* Fonte menor */
            font-weight: bold;
            color: #1f1f1f !important; 
        }
        .machine-icon { font-size: 0.9rem; }

        .bitola-container {
            background-color: #f0f2f6;
            border-radius: 4px;
            padding: 0.1rem;
            width: 100%;
        }
        .bitola-value {
            font-size: 1rem; /* Numero da bitola mais focado */
            font-weight: bold;
            color: #1a73e8 !important;
        }

        .rb-fonte {
            font-size: 0.65rem;
            color: #555555 !important;
            margin-top: 0.1rem;
        }
        
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def get_status_class(status):
    status_map = {"Rodando": "status-rodando", "Manutenção": "status-manutencao", "Troca de Bitola": "status-troca", "Parada": "status-parada"}
    return status_map.get(status, "")

# 3. CARREGAMENTO DE DADOS (SESSION STATE)
if 'tu_data' not in st.session_state:
    st.session_state.tu_data = pd.DataFrame({
        "Máquina": [f"TU {str(i).zfill(2)}" for i in range(1, 25)],
        "Bitola (mm)": [1.20] * 24,
        "Status": ["Desprogramada"] * 24
    })
    st.session_state.tu_data.loc[st.session_state.tu_data["Máquina"].isin(["TU 20", "TU 21", "TU 22", "TU 23", "TU 24", "TU 26", "TU 01", "TU 02", "TU 03"]), "Status"] = "Rodando"

if 'rb_barrica_data' not in st.session_state:
    equipamentos = [f"RB {str(i).zfill(2)}" for i in range(1, 19)] + ["Barrica 2", "Barrica 3", "Barrica 4"]
    st.session_state.rb_barrica_data = pd.DataFrame({
        "Equipamento": equipamentos,
        "Bitola (mm)": [1.20] * len(equipamentos),
        "Fonte (TU)": ["-"] * len(equipamentos),
        "Status": ["Desprogramada"] * len(equipamentos)
    })
    st.session_state.rb_barrica_data.loc[st.session_state.rb_barrica_data["Equipamento"].isin(["RB 01", "RB 02", "RB 03", "RB 04", "Barrica 2", "Barrica 3"]), "Status"] = "Rodando"

# 4. INÍCIO DA PÁGINA
inject_custom_css()

st.title("🏭 Painel de Produção Gerdau")

opcoes_status = ["Rodando", "Manutenção", "Troca de Bitola", "Parada", "Desprogramada"]
opcoes_bitola = [1.00, 1.20, 1.32, 1.60]
opcoes_fonte = ["-"] + [f"TU {str(i).zfill(2)}" for i in range(1, 25)]

# --- ÁREA DE EDIÇÃO ---
with st.expander("⚙️ ATUALIZAR DADOS (Teclado pode abrir no celular)", expanded=False):
    
    st.subheader("Trefilas Úmidas (TUs)")
    edited_tu = st.data_editor(
        st.session_state.tu_data, 
        hide_index=True, 
        use_container_width=True,
        column_config={
            "Máquina": st.column_config.TextColumn("Máquina", disabled=True),
            "Bitola (mm)": st.column_config.SelectboxColumn("Bitola (mm)", options=opcoes_bitola, required=True),
            "Status": st.column_config.SelectboxColumn("Status", options=opcoes_status, required=True)
        }
    )
    st.session_state.tu_data = edited_tu

    st.subheader("Rebobinadores & Barricas")
    edited_rb = st.data_editor(
        st.session_state.rb_barrica_data, 
        hide_index=True, 
        use_container_width=True,
        column_config={
            "Equipamento": st.column_config.TextColumn("Equipamento", disabled=True),
            "Bitola (mm)": st.column_config.SelectboxColumn("Bitola (mm)", options=opcoes_bitola, required=True),
            "Fonte (TU)": st.column_config.SelectboxColumn("Fonte (TU)", options=opcoes_fonte, required=True),
            "Status": st.column_config.SelectboxColumn("Status", options=opcoes_status, required=True)
        }
    )
    st.session_state.rb_barrica_data = edited_rb

# --- ÁREA DE PRINT ---
st.markdown("---")

df_tu_print = st.session_state.tu_data[st.session_state.tu_data["Status"] != "Desprogramada"].copy()
df_rb_print = st.session_state.rb_barrica_data[st.session_state.rb_barrica_data["Status"] != "Desprogramada"].copy()

# Renderização das TUs
st.markdown('<div class="section-title tu">🔵 Trefilas Úmidas</div>', unsafe_allow_html=True)
if df_tu_print.empty:
    st.info("Nenhuma Trefila Úmida ativa.")
else:
    cards_html = '<div class="card-grid">\n'
    for _, row in df_tu_print.iterrows():
        status_class = get_status_class(row["Status"])
        cards_html += f"""<div class="machine-card {status_class}">
<div class="card-header"><span class="machine-icon">⚙️</span><span class="machine-name">{row['Máquina']}</span></div>
<div class="bitola-container"><div class="bitola-value">{row['Bitola (mm)']:.2f} mm</div></div>
</div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

# Renderização das RBs
st.markdown('<div class="section-title rb">🟢 Rebobinadores & Barricas</div>', unsafe_allow_html=True)
if df_rb_print.empty:
    st.info("Nenhum Rebobinador ou Barrica ativa.")
else:
    cards_html = '<div class="card-grid">\n'
    for _, row in df_rb_print.iterrows():
        status_class = get_status_class(row["Status"])
        is_barrica = "Barrica" in row['Equipamento']
        icon = "🛢️" if is_barrica else "🔄"
        
        cards_html += f"""<div class="machine-card {status_class}">
<div class="card-header"><span class="machine-icon">{icon}</span><span class="machine-name">{row['Equipamento']}</span></div>
<div class="bitola-container"><div class="bitola-value">{row['Bitola (mm)']:.2f} mm</div></div>"""
        
        if not is_barrica and row['Fonte (TU)'] != "-":
            cards_html += f'<div class="rb-fonte">Fonte: {row["Fonte (TU)"]}</div>'
            
        cards_html += f"""</div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)