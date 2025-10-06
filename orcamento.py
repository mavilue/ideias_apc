import streamlit as st
import pandas as pd
from datetime import datetime

# --- Título e Configuração Inicial ---
st.set_page_config(layout="wide")
st.title("Meu Controle de Orçamento Pessoal 💸")

# --- Inicialização do Estado da Sessão ---
# Adicionamos 'editing' e 'edit_index' para controlar o modo de edição
if 'transacoes' not in st.session_state:
    st.session_state.transacoes = []
if 'editing' not in st.session_state:
    st.session_state.editing = False
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# --- Funções Auxiliares ---
def adicionar_transacao(tipo, descricao, categoria, valor, data):
    """Função para adicionar uma nova transação."""
    valor_final = -valor if tipo == "Despesa" else valor
    nova_transacao = {
        "Data": data.strftime("%d/%m/%Y"), "Tipo": tipo, "Descrição": descricao,
        "Categoria": categoria, "Valor": valor_final
    }
    st.session_state.transacoes.append(nova_transacao)

def atualizar_transacao(index, tipo, descricao, categoria, valor, data):
    """Função para atualizar uma transação existente."""
    valor_final = -valor if tipo == "Despesa" else valor
    st.session_state.transacoes[index] = {
        "Data": data.strftime("%d/%m/%Y"), "Tipo": tipo, "Descrição": descricao,
        "Categoria": categoria, "Valor": valor_final
    }

# --- Barra Lateral (Sidebar) ---
# A sidebar agora tem dois modos: "Adicionar" ou "Editar"
# Verificamos o st.session_state para decidir qual modo exibir

# MODO DE EDIÇÃO
if st.session_state.get('editing', False):
    st.sidebar.header("✏️ Editar Transação")
    
    # Pega o índice e os dados da transação que está sendo editada
    index = st.session_state.edit_index
    transacao = st.session_state.transacoes[index]

    # Preenche o formulário com os dados existentes
    tipo_edit = st.sidebar.selectbox("Tipo", ["Receita", "Despesa"], index=["Receita", "Despesa"].index(transacao['Tipo']))
    data_edit = st.sidebar.date_input("Data", datetime.strptime(transacao['Data'], "%d/%m/%Y"))
    descricao_edit = st.sidebar.text_input("Descrição", value=transacao['Descrição'])
    
    categorias = ("Salário", "Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação", "Outros")
    categoria_edit = st.sidebar.selectbox("Categoria", categorias, index=categorias.index(transacao['Categoria']))
    
    valor_edit = st.sidebar.number_input("Valor", min_value=0.01, format="%.2f", value=abs(transacao['Valor']))

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Salvar Alterações"):
            atualizar_transacao(index, tipo_edit, descricao_edit, categoria_edit, valor_edit, data_edit)
            st.session_state.editing = False # Sai do modo de edição
            st.session_state.edit_index = None
            st.success("Transação atualizada com sucesso!")
            st.rerun()
    with col2:
        if st.button("Cancelar Edição"):
            st.session_state.editing = False # Sai do modo de edição
            st.session_state.edit_index = None
            st.rerun()

# MODO PADRÃO (ADICIONAR)
else:
    st.sidebar.header("➕ Adicionar Nova Transação")
    tipos_transacao = ("Receita", "Despesa")
    tipo = st.sidebar.selectbox("Tipo", tipos_transacao)
    data = st.sidebar.date_input("Data", datetime.now())
    descricao = st.sidebar.text_input("Descrição", key="desc_add")
    categorias = ("Salário", "Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação", "Outros")
    categoria = st.sidebar.selectbox("Categoria", categorias)
    valor = st.sidebar.number_input("Valor", min_value=0.01, format="%.2f", key="valor_add")

    if st.sidebar.button("Adicionar"):
        if not descricao or valor <= 0:
            st.sidebar.error("Por favor, preencha a descrição e um valor válido.")
        else:
            adicionar_transacao(tipo, descricao, categoria, valor, data)
            st.sidebar.success("Transação adicionada com sucesso!")
            st.rerun()

# --- Área Principal ---
st.header("Resumo Financeiro")
if st.session_state.transacoes:
    df = pd.DataFrame(st.session_state.transacoes)
    total_receitas = df[df['Valor'] > 0]['Valor'].sum()
    total_despesas = df[df['Valor'] < 0]['Valor'].sum()
    saldo = total_receitas + total_despesas
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Receitas Totais", f"R$ {total_receitas:,.2f}")
    c2.metric("Despesas Totais", f"R$ {total_despesas:,.2f}")
    c3.metric("Saldo Final", f"R$ {saldo:,.2f}")
else:
    st.info("Nenhuma transação adicionada ainda para exibir o resumo.")

# --- Seção para Gerenciar (Deletar e Editar) ---
st.header("Gerenciar Transações")
if st.session_state.transacoes:
    opcoes_para_gerenciar = []
    for i, t in enumerate(st.session_state.transacoes):
        opcoes_para_gerenciar.append(f"{i}: {t['Data']} - {t['Descrição']} (R$ {t['Valor']:.2f})")

    transacao_selecionada_str = st.selectbox("Selecione uma transação para gerenciar", options=opcoes_para_gerenciar)

    col_del, col_edit = st.columns(2)
    with col_del:
        if st.button("Deletar Transação Selecionada"):
            if transacao_selecionada_str:
                indice_para_deletar = int(transacao_selecionada_str.split(':')[0])
                st.session_state.transacoes.pop(indice_para_deletar)
                st.success("Transação deletada com sucesso!")
                st.rerun()
    with col_edit:
        # BOTÃO DE EDITAR: ativa o modo de edição
        if st.button("Editar Transação Selecionada"):
            if transacao_selecionada_str:
                st.session_state.edit_index = int(transacao_selecionada_str.split(':')[0])
                st.session_state.editing = True
                st.rerun()
else:
    st.write("Nenhuma transação para gerenciar.")

# --- Visualizações e Histórico ---
st.header("Análise de Despesas")
if st.session_state.transacoes:
    df = pd.DataFrame(st.session_state.transacoes)
    despesas_df = df[df['Valor'] < 0].copy()
    if not despesas_df.empty:
        despesas_df['ValorAbs'] = despesas_df['Valor'].abs()
        gastos_por_categoria = despesas_df.groupby('Categoria')['ValorAbs'].sum()
        st.bar_chart(gastos_por_categoria)
    else:
        st.write("Nenhuma despesa registrada para análise.")

st.header("Histórico Completo")
if st.session_state.transacoes:
    st.dataframe(pd.DataFrame(st.session_state.transacoes), use_container_width=True)
else:
    st.info("Nenhuma transação registrada no histórico.")