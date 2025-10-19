import streamlit as st
import pandas as pd

# dicionario = {"categoria_select": [], "tipo_movimentacao": [], "descricao_f": [], "data_inscrita": []} - nesse caso o session state ja funciona como um dicionario

if 'dicionario' not in st.session_state: # memoria temporaria, salva o estado de sessao atual
    st.session_state['dicionario'] = {"categoria_select": [], "tipo_movimentacao": [],"valor_insert":[], "descricao_f": [], "data_inscrita": []}

def rendimentoTotal(dicionario):
    valor_total = 0
    for i in range(len(dicionario["tipo_movimentacao"])): # usei a msm estrutura de resoluçao das quest do the huxley
        tipo = dicionario["tipo_movimentacao"][i]
        x = dicionario["valor_insert"][i]

        if tipo == "Receita":
            valor_total+=x
        elif tipo == "Despesa":
            valor_total-=x
    return valor_total


st.title("CONTROLE DE GASTOS")
categoria = st.selectbox("CATEGORIA", ["Selecione", "Alimentação","Transporte","Moradia","Saúde","Educação","Salário","Renda extra", "Investimento", "Serviços digitais", "Lazer", "Cuidados pessoais", "Outros"])
tipo_mov = st.radio("TIPO DE MOVIMENTAÇÃO", ["Receita", "Despesa"])
valor = st.number_input("Insira o valor")
descricao = st.text_area("Descrição")
data = st.date_input("Data")
data_format = data.strftime("%d/%m/%Y") # so formatei pra deixar a data em ordem, o streamlit n faz essa formataçao 
if data_format:
    st.info(f"Data selecionada: {data_format}")


if st.button("Adicionar"):
    st.session_state['dicionario']["categoria_select"].append(categoria)
    st.session_state['dicionario']["tipo_movimentacao"].append(tipo_mov)
    st.session_state['dicionario']["valor_insert"].append(valor)
    st.session_state['dicionario']["descricao_f"].append(descricao)
    st.session_state['dicionario']["data_inscrita"].append(data_format)

    exibicao_saldo = rendimentoTotal(st.session_state['dicionario'])
    st.header(f"Saldo atual: R$ {exibicao_saldo:.2f}")
    
    # apresentar os dados coletados em forma de tabela
    df = pd.DataFrame(st.session_state['dicionario'])
    st.dataframe(df)