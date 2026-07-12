import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def gerar_dados():
    np.random.seed(12)
    random.seed(12)
    
    placas = [f"ABC{str(i).zfill(4)}" for i in range(1, 50)] #cria placas aleatoriamente
    pracas = ["PRACA_SP_01", "PRACA_RJ_02", "PRACA_MG_03", "PRACA_ES_04"]
    tipos_veiculo = ["Carro", "Moto", "Caminhao", "Onibus"]
    valores_base = {"Carro": 15.50, "Moto": 8.00, "Caminhao": 32.00, "Onibus": 25.00}
    
    dados = []
    data_base = datetime.now() - timedelta(days=30)
    
    #Gera 1000 transações normais
    for _ in range(1000):
        placa = random.choice(placas)
        tipo = random.choice(tipos_veiculo)
        dados.append({
            "data_hora": data_base + timedelta(minutes=random.randint(1, 43200)),
            "placa": placa,
            "praca": random.choice(pracas),
            "tipo_veiculo": tipo,
            "valor": valores_base[tipo] + random.uniform(-2, 2),
            "status": "OK"
        })
        
    #Injeta nomalias
    #Placa clonada/fraude (muitas passagens em pouco tempo)
    for _ in range(15):
        placa = random.choice(placas)
        tipo = random.choice(tipos_veiculo)
        dados.append({
            "data_hora": data_base + timedelta(hours=2, minutes=random.randint(1, 10)),
            "placa": placa,
            "praca": random.choice(pracas),
            "tipo_veiculo": tipo,
            "valor": valores_base[tipo] + random.uniform(-2, 2), #-2 e 2 são arredondamentos ou descontos
            "status": "OK"
        })
        
    #Valor absurdo (Erro de sistema ou fraude)
    for _ in range(5):
        placa = random.choice(placas)
        tipo = random.choice(tipos_veiculo)
        dados.append({
            "data_hora": data_base + timedelta(hours=2, minutes=random.randint(1, 10)),
            "placa": placa,
            "praca": random.choice(pracas),
            "tipo_veiculo": tipo,
            "valor": 999.00,
            "status": "OK"
        })

    #Valor negativo (Estorno não processado ou bug)
    for _ in range(5):
        placa = random.choice(placas)
        tipo = random.choice(tipos_veiculo)
        dados.append({
            "data_hora": data_base + timedelta(hours=2, minutes=random.randint(1, 10)),
            "placa": placa,
            "praca": random.choice(pracas),
            "tipo_veiculo": tipo,
            "valor": (valores_base[tipo] + random.uniform(-2, 2)) * -1,
            "status": "OK"
        })

    df = pd.DataFrame(dados)
    df = df.sort_values(by="data_hora").reset_index(drop=True) #Evitar bagunça de índice
    df.to_csv("dados_faturamento.csv", index=False, float_format="%.2f")
    print("CSV 'dados_faturamento.csv' gerado com sucesso!")

if __name__ == "__main__":
    gerar_dados()