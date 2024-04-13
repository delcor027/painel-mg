from PIL import Image
import streamlit as st
from fpdf import FPDF
import base64
from budget import Budget, BudgetItem

budget = Budget()

icon = Image.open('favicon.ico')
st.set_page_config(page_title='MG Marmoraria', page_icon=icon, layout="centered")

menu = st.sidebar.selectbox('Menu', ['Home', 'Orçamento'])

if menu == 'Home':
    st.title('Painel MG Marmoraria')
    st.write('Bem-vindo à MG Marmoraria!')

elif menu == 'Orçamento':
    st.title('Orçamento')
    client_name = st.text_input('Nome do Cliente')
    client_location = st.selectbox('Localização do Cliente', budget.get_cities_list())

    service_type = st.selectbox('Tipo de Serviço', ['Selecione', 'Bancadas', 'Pias', 'Peças Retas'])

    if service_type in ['Bancadas', 'Pias']:
        length_cm = st.number_input('Comprimento (cm)', min_value=0.0, format="%.0f")
        width_cm = st.number_input('Largura (cm)', min_value=0.0, format="%.0f")
        price_per_meter = st.number_input('Preço por metro quadrado (R$)', min_value=0.0, format="%.2f")
        
        if service_type == 'Bancadas':
            saia_length_cm = st.number_input('Saia Comprimento (cm)', min_value=0.0, format="%.0f")
            saia_width_cm = st.number_input('Saia Largura (cm)', min_value=0.0, format="%.0f")
            budget.add_item(BudgetItem(saia_length_cm, saia_width_cm, price_per_meter))
        
        rodabanca_length_cm = st.number_input('Rodabanca Comprimento (cm)', min_value=0.0, format="%.0f")
        rodabanca_width_cm = st.number_input('Rodabanca Largura (cm)', min_value=0.0, format="%.0f")
        budget.add_item(BudgetItem(rodabanca_length_cm, rodabanca_width_cm, price_per_meter))

        tipo_acabamento = st.selectbox('Tipo de Acabamento', budget.get_acabamento_types())
        acabamento_cm = st.number_input('Acabamento (cm)', min_value=0.0, format="%.0f")

        include_sink = st.checkbox('Incluir Cuba')
        sink_price = 0
        if include_sink:
            sink_price = st.number_input('Valor da Cuba (R$)', min_value=0.0, format="%.2f")

        if st.button('Calcular Preço'):
            main_item = BudgetItem(length_cm, width_cm, price_per_meter)
            budget.add_item(main_item)
            total_price = budget.calculate_total_price(tipo_acabamento, acabamento_cm, sink_price)
            st.success(f'O preço estimado é R${total_price:.2f}')

            # Gerar arquivo PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt=f"Cliente: {client_name}", ln=True)
            pdf.cell(200, 10, txt=f"Localização do Cliente: {client_location}", ln=True)
            pdf.cell(200, 10, txt=f"Tipo de Serviço: {service_type}", ln=True)

            # Adicione mais informações específicas para cada tipo de serviço (bancadas, pias, peças retas, etc.)

            pdf.cell(200, 10, txt=f"Preço Total: R${total_price:.2f}", ln=True)

            # Salvar o PDF em um arquivo temporário
            pdf_output = "temp_orcamento.pdf"
            pdf.output(pdf_output)

            # Carregar o arquivo PDF como base64 para permitir o download
            with open(pdf_output, "rb") as pdf_file:
                pdf_base64 = base64.b64encode(pdf_file.read()).decode()

            # Exibir o link de download
            st.markdown(f'<a href="data:application/octet-stream;base64,{pdf_base64}" download="orcamento.pdf">Baixar Orçamento</a>', unsafe_allow_html=True)
    
    elif service_type == 'Peças Retas':
        # Lógica específica para 'Peças Retas'
        pass
