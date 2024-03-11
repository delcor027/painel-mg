from PIL import Image
import streamlit as st
from calculator import calculate_price
import json

# Carregando sa listas dos arquivos JSON
with open('data_utils.json', encoding='utf-8') as data_file:
    data = json.load(data_file)
    cities_list = data['cities']
    acabamentos_list = data['acabamentos']

icon = Image.open('favicon.ico')
st.set_page_config(
    page_title='MG Marmoraria', page_icon=icon,
    layout="centered")

# Menu na barra lateral
menu = st.sidebar.selectbox('Menu', ['Home', 'Orçamento'])

if menu == 'Home':
    st.title('Painel MG Marmoraria')
    st.write('Bem-vindo à MG Marmoraria!')

elif menu == 'Orçamento':
    st.title('Orçamento')
    # Entradas para nome do cliente e localização
    client_name = st.text_input('Nome do Cliente')
    client_location = st.selectbox('Localização do Cliente', cities_list)
    
    # Valor fixo por metro de acabamento (em centímetros)
    fixed_acabamento_price_per_cm = 1.0
    
    # Entrada de dimensões em centímetros
    length_cm = st.number_input('Comprimento (cm)', min_value=0.0, format="%.0f")
    width_cm = st.number_input('Largura (cm)', min_value=0.0, format="%.0f")
    
    # Seleção do tipo de acabamento
    tipo_acabamento_options = [acabamento['tipo'] for acabamento in acabamentos_list]
    tipo_acabamento = st.selectbox('Tipo de Acabamento', tipo_acabamento_options)
    
    # Entrada para a quantidade de centímetros de acabamento
    acabamento_cm = st.number_input('Acabamento (cm)', min_value=0.0, format="%.0f")

    # Conversão de centímetros para metros para as dimensões
    length_m = length_cm / 100
    width_m = width_cm / 100
    acabamento_m = acabamento_cm / 100

    # Entrada de preço por metro quadrado pelo usuário
    price_per_meter = st.number_input('Preço por metro quadrado (R$)', min_value=0.0, format="%.2f")

    # Botão para cálculo do preço
    if st.button('Calcular Preço'):
        # Calculando o preço base da área
        price_area = calculate_price(length_m, width_m, price_per_meter)
        
        # Encontrar o preço por centímetro do acabamento selecionado
        acabamento_info = next((item for item in acabamentos_list if item['tipo'] == tipo_acabamento), None)
        if acabamento_info is not None:
            # Cálculo do custo de acabamento baseado na quantidade em centímetros
            acabamento_cost = acabamento_m * acabamento_info['preco']
        else:
            # Caso não encontre o acabamento, defina o custo como 0
            acabamento_cost = 0
        
        # Calculando o preço total incluindo o custo de acabamento
        total_price = price_area + acabamento_cost
        st.success(f'O preço estimado é R${total_price:.2f}')
