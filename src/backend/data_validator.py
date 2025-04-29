import pandas as pd
from src.config.csv_contract import PlanilhaVendas
from pydantic import ValidationError
from io import StringIO, BytesIO

def validate_csv_data(csv_data, encoding='utf-8'):
    """
    Valida os dados de um arquivo CSV contra o contrato de dados definido.
    
    Args:
        csv_data: Pode ser um caminho de arquivo (str), um objeto BytesIO (Streamlit uploaded_file)
                  ou um DataFrame já carregado.
        encoding (str): Codificação do arquivo CSV, padrão UTF-8.
    
    Returns:
        tuple: (dados_validados, erros)
            - dados_validados: Lista de objetos Pydantic validados.
            - erros: Lista de mensagens de erro para linhas inválidas.
    """
    try:
        # Verifica se csv_data é um caminho de arquivo, BytesIO ou DataFrame
        if isinstance(csv_data, str):
            df = pd.read_csv(csv_data, encoding=encoding)
        elif isinstance(csv_data, (BytesIO, StringIO)):
            df = pd.read_csv(csv_data, encoding=encoding)
        elif isinstance(csv_data, pd.DataFrame):
            df = csv_data
        else:
            raise ValueError("Tipo de dado CSV não suportado.")
    except Exception as e:
        return [], [f"Erro ao carregar o arquivo CSV: {str(e)}"]
    
    erros = []
    dados_validados = []
    
    for index, row in df.iterrows():
        try:
            # Converte a linha do DataFrame para dicionário
            dados = row.to_dict()
            # Valida os dados usando o modelo PlanilhaVendas
            usuario_validado = PlanilhaVendas(**dados)
            dados_validados.append(usuario_validado)
        except ValidationError as e:
            erros.append(f"Erro na linha {index + 2}: {str(e)}")
    
    return dados_validados, erros

def convert_validated_to_dataframe(dados_validados):
    """
    Converte uma lista de objetos Pydantic validados para um DataFrame.
    
    Args:
        dados_validados (list): Lista de objetos Pydantic validados.
    
    Returns:
        pd.DataFrame: DataFrame contendo os dados validados.
    """
    if not dados_validados:
        return pd.DataFrame()
    return pd.DataFrame([dados.dict() for dados in dados_validados])