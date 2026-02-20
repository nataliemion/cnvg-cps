# -*- coding: utf-8 -*-
import pandas as pd
from datetime import date, timedelta
import random

# ----------------------------------------------------------------------
# 1. Configurações e Carregamento de Dados
# ----------------------------------------------------------------------

NOME_ARQUIVO_CSV = 'Escala KIDS.xlsx - _NomesLista.csv' 

try:
    df_voluntarios = pd.read_csv(NOME_ARQUIVO_CSV)
except FileNotFoundError:
    print(f"❌ Erro: Arquivo '{NOME_ARQUIVO_CSV}' não encontrado no Colab.")
    raise

# Limpeza e Normalização
df_voluntarios['NOME'] = df_voluntarios['NOME'].str.strip()
df_voluntarios['SALA ATRIBUÍDA'] = df_voluntarios['SALA ATRIBUÍDA'].str.strip().str.upper()
df_voluntarios['Sexo'] = df_voluntarios['Sexo'].str.strip()

# Configurações de Negócio
START_DATE = date(2026, 3, 1)
END_DATE = date(2026, 7, 31)
MIN_ESCALAS = 6 
LIMITE_MINIMO_EXCEPCIONAL = 7 # Nunca menos de 7 dias (trabalhar 2 domingos seguidos)

REFORMA_FIM = date(2026, 3, 31)
SALAS = ['MATERNAL', 'KINDER', 'JUNIORES (7-11)', 'MONITORES']

# ----------------------------------------------------------------------
# 2. Funções Auxiliares
# ----------------------------------------------------------------------

def get_sobrenome(nome):
    partes = nome.split()
    return partes[-1].lower() if partes else ""

def gerar_domingos(start_date, end_date):
    datas = []
    current_date = start_date
    while current_date.weekday() != 6: current_date += timedelta(days=1)
    while current_date <= end_date:
        datas.append(current_date)
        current_date += timedelta(days=7)
    return datas

# ----------------------------------------------------------------------
# 3. Preparação dos Dados
# ----------------------------------------------------------------------

datas_escala = gerar_domingos(START_DATE, END_DATE)
voluntarios_por_sala = {sala: {'Feminino': [], 'Masculino': []} for sala in SALAS}

for _, row in df_voluntarios.iterrows():
    sala, genero, nome = row['SALA ATRIBUÍDA'], row['Sexo'], row['NOME']
    if sala in voluntarios_por_sala:
        voluntarios_por_sala[sala][genero].append(nome)

todos_nomes_unicos = df_voluntarios['NOME'].unique()
ultimo_trabalho = {nome: date(1900, 1, 1) for nome in todos_nomes_unicos}
contagem_escala = {nome: 0 for nome in todos_nomes_unicos}
escala = {sala: {} for sala in SALAS}

# ----------------------------------------------------------------------
# 4. Função de Agendamento (Lógica de Maior Descanso)
# ----------------------------------------------------------------------

def agendar_sala(data, sala, escala_atual, ult_trab_restrito, ultimo_trabalho_global, contagem_escala_global):
    
    if sala in ['JUNIORES (7-11)', 'MONITORES'] and data <= REFORMA_FIM:
        escala_atual[sala][data] = ['FECHADO (REFORMA)', 'FECHADO (REFORMA)']
        return []

    # Busca todos os voluntários da sala que não estão ocupados hoje e respeitam o mínimo de 7 dias
    candidatos_base = []
    v_sala = voluntarios_por_sala.get(sala, {'Feminino': [], 'Masculino': []})
    
    for genero, lista_nomes in v_sala.items():
        for nome in lista_nomes:
            dias_descanso = (data - ultimo_trabalho_global[nome]).days
            # Filtro: Mínimo de 7 dias E não estar em outra sala no mesmo dia
            if dias_descanso >= LIMITE_MINIMO_EXCEPCIONAL:
                if (data - ult_trab_restrito[nome]).days > 0:
                    # Guardamos (Dias de Descanso, Contagem Total, Nome, Gênero)
                    candidatos_base.append({
                        'descanso': dias_descanso,
                        'contagem': contagem_escala_global[nome],
                        'nome': nome,
                        'genero': genero
                    })

    escalados_na_data = []

    for pos in ['P1', 'P2']:
        # Filtra quem ainda não foi escalado para P1 nesta sala hoje
        nomes_ja_escalados = [n for _, n, _ in escalados_na_data]
        candidatos_disp = [c for c in candidatos_base if c['nome'] not in nomes_ja_escalados]

        # Regras de P2 (Gênero e Sobrenome)
        if pos == 'P2' and escalados_na_data:
            p1_n, p1_g = escalados_na_data[0][1], escalados_na_data[0][2]
            p1_s = get_sobrenome(p1_n)
            
            if p1_g == 'Masculino':
                candidatos_disp = [c for c in candidatos_disp if c['genero'] == 'Feminino']
            candidatos_disp = [c for c in candidatos_disp if get_sobrenome(c['nome']) != p1_s]

        # ORDENAÇÃO ELÁSTICA: 
        # 1. Prioriza quem tem MAIOR descanso (descanso)
        # 2. Em caso de empate, quem tem MENOR número de escalas no total (contagem)
        # 3. Empate técnico, sorteio
        candidatos_disp = sorted(
            candidatos_disp, 
            key=lambda x: (-x['descanso'], x['contagem'], random.random())
        )

        if candidatos_disp:
            selecionado = candidatos_disp[0]
            escalados_na_data.append((selecionado['contagem'], selecionado['nome'], selecionado['genero']))
            
            if data not in escala_atual[sala]: escala_atual[sala][data] = [None, None]
            idx = 0 if pos == 'P1' else 1
            escala_atual[sala][data][idx] = selecionado['nome']
        else:
            break

    # Validação Final
    if data not in escala_atual[sala] or None in escala_atual[sala][data]:
        # Se a sala não está em reforma, marca a falha para você saber que nem com 7 dias deu certo
        if not (sala in ['JUNIORES (7-11)', 'MONITORES'] and data <= REFORMA_FIM):
            escala_atual[sala][data] = ['FALTA CRÍTICA', 'FALTA CRÍTICA']
        return []

    return [n for _, n, _ in escalados_na_data]

# ----------------------------------------------------------------------
# 5. Processamento e Saída
# ----------------------------------------------------------------------

for data in datas_escala:
    salas_hoje = list(SALAS)
    random.shuffle(salas_hoje)
    voluntarios_hoje = set()

    for sala in salas_hoje:
        res_temp = ultimo_trabalho.copy()
        for n in voluntarios_hoje: res_temp[n] = data
        
        nomes_sala = agendar_sala(data, sala, escala, res_temp, ultimo_trabalho, contagem_escala)
        for n in nomes_sala:
            voluntarios_hoje.add(n)
            ultimo_trabalho[n] = data
            contagem_escala[n] += 1

# Exportação CSV
df_final = []
for sala in SALAS:
    for i, f in enumerate(['P1', 'P2']):
        linha = {'SALA': sala, 'FUNÇÃO': f}
        for d in datas_escala:
            linha[d.strftime('%d/%m/%Y')] = escala[sala].get(d, ['N/A', 'N/A'])[i]
        df_final.append(linha)

df_escala = pd.DataFrame(df_final)
df_escala.to_csv('escala_kids_2026_elastica.csv', index=False)

print("✅ Escala 'Elástica' gerada. Prioridade: Maior descanso disponível (mín. 7 dias).")
