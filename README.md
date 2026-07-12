# Analise-de-Faturamento-e-Telemetria-com-LLM

## Sobre o Projeto
O sistema processa dados para identificação de anomalias, fraudes ou problemas do sistema, utilizando LLMs para a geração de análises e insights sobre o projeto.

# Arquitetura
Processamento: O pandas realiza o cálculo de estatísticas para detecção das métricas desejadas e outros valores para facilitar a interpretação da LLM

Engenharia de Prompt: O prompt foi feito de maneira que a LLM tenha um custo reduzido de tokens pois ela não realiza cálculos e diminuir alucinações recebendo um resumo detalhado dos dados obtidos.

# Tecnologias utilizadas
Linguagem: python 3.13

Manipulação de dados: Numpy, Pandas

Integração com IA: OpenAI SDK
