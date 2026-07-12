import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key="ollama" # SDK exige API
)
MODELO_IA = "qwen3.5"

def carregar_dados():
    #Aplicar a um banco de dados real posteriormente


    #diz que a coluna data_hora é uma date para cálculos temporais
    return pd.read_csv("dados_faturamento.csv", parse_dates=["data_hora"])

def analisar_dados_com_pandas(df: pd.DataFrame) -> str:
    #Cálculos pré-feitos para economizar tokens
    
    #Métricas Gerais
    faturamento_total = df["valor"].sum()
    ticket_medio = df["valor"].mean()
    total_transacoes = len(df)
    
    #Anomalias Estatísticas (Outliers)
    q1 = df["valor"].quantile(0.25)
    q3 = df["valor"].quantile(0.75)
    iqr = q3 - q1
    limite_superior = q3 + 1.5 * iqr
    outliers_valor = df[df["valor"] > limite_superior]
    valores_negativos = df[df["valor"] < 0]
    
    #Comportamento Suspeito (Frequência de placas)
    contagem_placas = df.groupby("placa").size().reset_index(name="qtd_passagens")
    placas_suspeitas = contagem_placas[contagem_placas["qtd_passagens"] > 10]
    
    #Tendências por Local
    faturamento_por_praca = df.groupby("praca")["valor"].sum().sort_values(ascending=False)

    #Montagem do texto resumo para a IA
    resumo = f"""
    DADOS ESTATÍSTICOS DO PERÍODO (Últimos 30 dias):
    - Faturamento Total: R$ {faturamento_total:,.2f}
    - Ticket Médio: R$ {ticket_medio:,.2f}
    - Total de Transações: {total_transacoes}
    
    ANOMALIAS DETECTADAS (Pandas):
    - Outliers de Valor (> R$ {limite_superior:,.2f}): {len(outliers_valor)} transações. Exemplos: {outliers_valor[['placa', 'valor', 'praca']].head(3).to_string(index=False)}
    - Valores Negativos: {len(valores_negativos)} transações. Exemplos: {valores_negativos[['placa', 'valor']].head(3).to_string(index=False)}
    - Placas com Frequência Anormal (>10 passagens): {len(placas_suspeitas)} placas. Ex: {placas_suspeitas.head(3).to_string(index=False)}
    
    TOP 3 PRAÇAS POR FATURAMENTO:
    {faturamento_por_praca.head(3).to_string()}
    """
    return resumo

def gerar_relatorio_com_llm(resumo_pandas: str) -> str:
    #Chama a IA para interpretar o relatório
    
    prompt_sistema = """
    Você é um Diretor de Inteligência de Negócios (BI) especializado em mobilidade urbana, 
    telemetria e sistemas de pedágio (ex: Sem Parar, Conquest, Veloe). 
    Seu tom deve ser executivo, analítico e focado em tomada de decisão.
    """
    
    prompt_usuario = f"""
    Abaixo estão os resumos estatísticos e anomalias extraídas de nossa base de faturamento de pedágio.
    
    {resumo_pandas}
    
    Com base nesses dados, gere um RELATÓRIO EXECUTIVO em Markdown estruturado exatamente com as seguintes seções:
    
    ### 1. Resumo Executivo
    (Visão geral do faturamento e saúde da operação)
    
    ### 2. Alertas de Anomalias e Fraudes
    (Analise as anomalias detectadas. Explique o risco de negócio de cada uma, ex: clonagem de placas, bugs de integração, erros de cadastro. Seja específico com os dados fornecidos).
    
    ### 3. Tendências e Insights de Negócio
    (O que os dados das praças e ticket médio dizem sobre o comportamento do usuário?)
    
    ### 4. Recomendações Estratégicas (Plano de Ação)
    (Forneça 3 a 4 ações práticas e imediatas que a equipe de operações/tecnologia deve tomar com base nas anomalias e tendências).
    """

    response = client.chat.completions.create(
        model="qwen3.5",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content #Apenas a resposta da IA

def main():
    print("Carregando base de dados")
    df = carregar_dados()
    
    print("Processando dados e extraindo anomalias com Pandas")
    resumo_pandas = analisar_dados_com_pandas(df)
    
    print("Consultando LLM")
    relatorio = gerar_relatorio_com_llm(resumo_pandas)
    
    # Salva o relatório
    with open("relatorio_final.md", "w", encoding="utf-8") as f:
        f.write(relatorio)
        
    print("\n" + "="*50)
    print(" RELATÓRIO GERADO COM SUCESSO! Salvo em 'relatorio_final.md'")
    print("="*50 + "\n")
    print(relatorio)

if __name__ == "__main__":
    main()