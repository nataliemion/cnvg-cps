📅 Gerador de Escala Kids (Janeiro a Julho 2026)
Este projeto contém um script Python otimizado para gerar a escala de voluntários do Ministério Infantil (Kids) para o primeiro semestre de 2026, respeitando um conjunto rigoroso de restrições lógicas e de carga de trabalho.

🎯 Objetivo
O objetivo principal do script é automatizar a criação da escala de domingo (Janeiro a Julho de 2026) para as salas MATERNAL, KINDER, Kids 1 e Kids 2, garantindo a conformidade com as regras de logística, tempo de descanso e distribuição de gênero.

⚙️ Regras de Consistência Implementadas
O algoritmo de agendamento garante o cumprimento das seguintes regras:

Período da Escala: Todos os Domingos de Janeiro/2026 à Julho/2026.

Reforma de Salas: As salas Kids 1 e Kids 2 estão marcadas como FECHADO (REFORMA) durante todo o mês de Janeiro de 2026.

Intervalo Mínimo: Cada voluntário deve ter um intervalo mínimo de 2 domingos (14 dias) de folga entre as escalas.

Impedimento Consecutivo: Uma pessoa não pode trabalhar em dois domingos consecutivos.

Dupla Atribuição: Uma pessoa não pode ser escalada em duas salas diferentes no mesmo domingo.

Equipe por Sala: Cada sala deve ter exatamente 2 professores (P1 e P2) por domingo.

Restrição de Gênero: Não é permitido ter 2 professores do sexo Masculino trabalhando na mesma sala.

Sala de Referência: O script prioriza voluntários em suas salas de referência, mas permite flexibilidade se a regra de intervalo for mantida.

Carga Mínima (NOVO): Cada voluntário deve aparecer na escala ao menos 6 vezes durante o período (7 meses). O script utiliza uma lógica de priorização para garantir que os voluntários com menor contagem sejam escalados primeiro, ajudando a atingir esse mínimo.

🚀 Como Utilizar (Google Colab)
O script foi desenvolvido para ser executado de forma simples e rápida no Google Colab.

1. Preparação
Acesse o Google Colab e crie um novo notebook Python.

Certifique-se de ter seu arquivo de lista de voluntários (Escala KIDS_NomesLista.csv) pronto.

2. Upload do Arquivo de Dados
No painel lateral esquerdo do Colab (ícone de pastas/Arquivos), clique em "Fazer upload para o armazenamento da sessão".

Faça o upload do seu arquivo de entrada, renomeado para Escala KIDS_NomesLista.csv.

3. Execução do Script
Copie e cole todo o código Python fornecido no seu notebook do Colab.

Execute a célula de código.

4. Resultado
Após a execução, o script irá:

Imprimir um "Relatório de Frequência de Escala" no console, mostrando a contagem exata de escalas por voluntário e se o mínimo de 6 escalas foi atingido.

Gerar o arquivo escala_kids_2026.csv no ambiente do Colab, pronto para download.
