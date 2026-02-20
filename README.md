# 📜 KidsScale Manager 2026

Sistema inteligente para geração automatizada da escala do Ministério Infantil. O algoritmo utiliza lógica elástica de priorização para garantir o preenchimento das salas respeitando restrições eclesiásticas, de gênero e de parentesco.

## 🚀 Objetivo

Gerar uma escala de voluntários para o período de **Março a Julho de 2026**, otimizando o descanso dos membros e garantindo a segurança e conformidade das salas.

## 🛠️ Regras de Negócio Implementadas

O motor de agendamento segue uma hierarquia rigorosa de regras para evitar conflitos:

1. **Bloqueio de Reforma:** As salas `JUNIORES` e `MONITORES` permanecem com status "FECHADO (REFORMA)" até 31/03/2026.
2. **Composição de Gênero:** Cada sala comporta no máximo **01 voluntário do sexo masculino** simultaneamente.
3. **Restrição de Parentesco (Antinepotismo):** Voluntários com o mesmo sobrenome não podem ser escalados na mesma sala, no mesmo dia.
4. **Lógica de Descanso Elástica:**
* O sistema busca sempre o voluntário com o **maior número de dias descansados** disponível.
* O intervalo ideal é de **14 dias** (2 domingos), mas em casos excepcionais (vagas abertas), o sistema aceita um intervalo mínimo de **7 dias**.


5. **Equilíbrio de Carga (Fairness):** Em caso de empate no tempo de descanso, o sistema escala quem possui o **menor número total de participações** no semestre.
6. **Prevenção de Duplicidade:** Um voluntário nunca será escalado para duas salas diferentes no mesmo domingo.

## 📊 Estrutura do Arquivo de Entrada

O script espera um arquivo `.csv` com as seguintes colunas:

* `NOME`: Nome completo do voluntário.
* `SALA ATRIBUÍDA`: Sala preferencial ou permitida.
* `Sexo`: Gênero (Feminino/Masculino).

## 💻 Como Utilizar no Google Colab

1. Faça o upload do notebook `.ipynb` no Colab.
2. Carregue o arquivo `Escala KIDS.xlsx - _NomesLista.csv` no diretório de arquivos do ambiente.
3. Execute todas as células.
4. O arquivo `escala_kids_2026_elastica.csv` será gerado automaticamente para download.

## 📈 Relatórios

Ao final da execução, o script imprime um relatório de frequência, permitindo à liderança identificar quais voluntários estão com baixa participação (abaixo da meta de **6 escalas**) para ações de engajamento.
