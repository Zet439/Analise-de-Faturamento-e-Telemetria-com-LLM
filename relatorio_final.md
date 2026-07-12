# RELATÓRIO DE INTELIGÊNCIA DE NEGÓCIOS – OPERAÇÕES DE PEDÁGIO
**Data:** 24 de Maio de 202X | **Período Analisado:** Últimos 30 Dias | **Classificação:** Confidencial Operacional

---

### ### 1. Resumo Executivo

O faturamento bruto reportado para o período atingiu **R$ 25,4 mil**, com um volume de transações (N) de 1.025 e ticket médio estabilizado em R$ 24,79. Embora a operação apresente consistência no fluxo diário médio (~R$ 846/dia), o desempenho financeiro é impactado por distorções significativas nos dados brutos capturados pelos terminais de leitura (Sem Parar/Conquest).

A saúde da operação está comprometida pela presença de *outliers* sistêmicos e inconsistências contábeis que, se não corrigidas imediatamente, resultam em:
1.  **Superestimação artificial do faturamento** devido a valores placeholder (`999`).
2.  **Vazamentos financeiros potenciais** através de lançamentos negativos sem contrapartida adequada no ledger principal.

É imperativo realizar uma limpeza de dados (ETL) e auditoria forense antes da consolidação mensal para garantir conformidade com as normas do ANTT/ANP sobre integridade tarifária.

---

### ### 2. Alertas de Anomalias e Fraudes

A análise via Pandas identificou três categorias críticas que demandam intervenção imediata:

#### A. Outliers de Valor (Risco Financeiro Falso)
*   **Dado:** 5 transações com valor `999,0` (ex: PRACA_RJ_02).
*   **Análise Técnica:** O valor R$ 999 não corresponde a nenhuma tarifa vigente no sistema. Trata-se de um *placeholder* ou erro de integração do leitor eletrônico que enviou código de erro como transação monetária.
*   **Risco de Negócio:** Inflação indevida da receita bruta reportada ao faturamento e aos acionistas. Se creditado, representa fraude contábil passiva (falsificação de entrada).

#### B. Valores Negativos Não Autorizados (Vazamento)
*   **Dado:** 5 transações com valores negativos (-R$ 31 a -R$ 32), ex: ABC0049, ABC0007.
*   **Análise Técnica:** Lançamentos de crédito ou estorno processados diretamente no fluxo principal sem registro em nota fiscal de devolução (NFD) associada à transação original.
*   **Risco de Negócio:** Indica falha na sincronização entre o sistema de leitura e a plataforma financeira. Se não revertidos, representam perda direta de receita líquida estimada em ~R$ 150 neste período apenas por bugs operacionais.

#### C. Frequência Anormal de Placas (Clonagem/Reutilização)
*   **Dado:** 49 placas com >10 passagens no mês, ex: ABC0001 (24 vezes).
*   **Análise Técnica:** Em um cenário normal de mobilidade urbana, a frequência média é proporcional ao tráfego. Concentração excessiva em poucas identificadoras sugere que uma única placa física está sendo usada para validar múltiplas passagens distintas ou há falha no banco de dados de bloqueio (tagging).
*   **Risco de Negócio:** Alto risco de clonagem de placas (fraude ativa) onde um usuário utiliza a mesma credencial em diferentes praças sem pagar as taxas correspondentes, explorando brechas na validação geográfica.

---

### ### 3. Tendências e Insights de Negócio

*   **Desempenho Regional:** As três praças líderes (**PRACA_RJ_02**, **PRACA_MG_03** e **PRACA_SP_01**) concentram mais da metade do faturamento total (R$ 8.5k + R$ 6.2k + R$ 5.5k). Isso indica que a operação é robusta nos corredores principais, mas também concentra o risco operacional nessas mesmas localidades.
*   **Estabilidade Tarifária:** O ticket médio de R$ 24,79 demonstra consistência nas tarifas aplicadas (Sem Parar), sem flutuações bruscas sugerindo erros de cálculo dinâmico ou aplicação incorreta de alíquotas promocionais.
*   **Eficiência Operacional vs. Qualidade dos Dados:** O volume de transações é saudável para a escala atual, mas a qualidade do dado está degradada (aproximadamente 10% das linhas afetadas por anomalias). Isso sugere que o hardware ou software intermediário precisa de manutenção preventiva antes da degradação total impactar a confiança no sistema.

---

### ### 4. Recomendações Estratégicas (Plano de Ação)

Para mitigação dos riscos identificados e otimização do faturamento, as seguintes ações devem ser executadas nas próximas 24 horas:

1.  **Limpeza Imediata da Base (Data Governance):**
    *   Instruir a equipe de TI para aplicar filtros no ETL que rejeitem automaticamente transações com valor > R$ 50 ou < -R$ 1 até validação manual. Isso corrigirá o faturamento bruto e evitará contabilidade incorreta nos próximos fechamentos diários.

2.  **Auditoria Forense de Placas (Fraud Detection):**
    *   Cruzar os dados das 49 placas com alta frequência (>10 passagens) contra logs geográficos do sistema telemático. Se a placa não estiver fisicamente presente em múltiplos pontos simultâneos ou consecutivos sem intervalo lógico, bloqueie o acesso e solicite verificação de clonagem física junto à frota contratante (ex: logística).

3.  **Patching da Integração Financeira:**
    *   Investigar a origem dos valores negativos (-R$ 30) nos logs do servidor de leitura. Implementar regra de negócio que exija aprovação manual para qualquer estorno superior a R$ 5, garantindo que o crédito não seja aplicado sem registro na nota fiscal original da cobrança.

4.  **Monitoramento em Tempo Real (Real-time Monitoring):**
    *   Configurar alertas no painel BI para disparo imediato quando uma placa exceder N passagens por hora ou dia fora do padrão histórico, permitindo intervenção operacional antes que o dano financeiro se acumule.