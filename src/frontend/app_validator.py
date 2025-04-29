import streamlit as st
import pandas as pd
from src.backend.data_validator import validate_csv_data, convert_validated_to_dataframe

def main():
    st.title("Validador de Dados de Campanhas")
    st.write("Faça o upload de um arquivo CSV para validação contra o contrato de dados.")
    
    # Componente de upload de arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        try:
            # Preview dos dados
            st.write("Preview dos dados:")
            df_preview = pd.read_csv(uploaded_file)
            st.dataframe(df_preview.head())
            
            # Botão para validar os dados
            if st.button("Validar Dados"):
                with st.spinner("Validando dados..."):
                    # Chama a função de validação do backend
                    dados_validados, erros = validate_csv_data(uploaded_file)
                    
                    if erros:
                        st.error("Foram encontrados erros na validação:")
                        for erro in erros:
                            st.write(erro)
                    else:
                        st.success("Todos os dados foram validados com sucesso!")
                        
                        # Mostra quantidade de registros validados
                        st.write(f"Total de registros validados: {len(dados_validados)}")
                        
                        # Opção para download dos dados validados
                        df_validado = convert_validated_to_dataframe(dados_validados)
                        st.download_button(
                            label="Download dos dados validados",
                            data=df_validado.to_csv(index=False).encode('utf-8'),
                            file_name="dados_validados.csv",
                            mime="text/csv"
                        )
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")

if __name__ == "__main__":
    main()