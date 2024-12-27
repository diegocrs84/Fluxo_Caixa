import sqlite3
from datetime import datetime

def obter_transacoes_reais():
    try:
        # Conectar ao banco de dados SQLite3
        conectar_banco = sqlite3.connect('transacoes.db') ####ALTERAR O CAMINHO PARA O LOCAL DESEJADO.
        cursor = conectar_banco.cursor()

        # Data atual para filtro das transações
        data_inicio = datetime(2024, 6, 1).strftime('%Y-%m-%d')
        data_fim = datetime(2024, 6, 30).strftime('%Y-%m-%d')

        query = 'select id, data, tipo, valor from transacoes where data between ? and ? order by data;'

        cursor.execute(query, (data_inicio, data_fim))

        # Extrai os dados para um formato de lista de dicionários
        transacoes_reais = [
            {'id': row[0], 'data': row[1], 'tipo': row[2], 'valor': row[3]}
            for row in cursor.fetchall()
        ]

        cursor.close()
        conectar_banco.close()

        return transacoes_reais

    except sqlite3.DatabaseError as e:
        print(f"Erro na consulta ao banco de dados: {e}")
        return []

def verificar_discrepancias(transacoes_reais, transacoes_previstas):
    discrepancias = []

    # Comparar transações previstas com as reais
    for transacao_prevista in transacoes_previstas:
        transacao_real = next((t for t in transacoes_reais if t['id'] == transacao_prevista['id']), None)

        if not transacao_real:
            discrepancias.append({
                'tipo': 'Ausente',
                'id': transacao_prevista['id'],
                'data': transacao_prevista['data'],
                'tipo transacao': transacao_prevista['tipo'],
                'valor previsto': transacao_prevista['valor'],
                'erro': 'Transação prevista ausente nas transações reais'
            })
        elif transacao_real['valor'] != transacao_prevista['valor']:
            discrepancias.append({
                'tipo': 'Valor Inconsistente',
                'id': transacao_prevista['id'],
                'data': transacao_prevista['data'],
                'tipo transacao': transacao_prevista['tipo'],
                'valor previsto': transacao_prevista['valor'],
                'valor eal': transacao_real['valor'],
                'erro': 'Valor inconsistente entre transações previstas e reais'
            })

    # Verificar transações reais não previstas
    for transacao_real in transacoes_reais:
        transacao_prevista = next((t for t in transacoes_previstas if t['id'] == transacao_real['id']), None)

        if not transacao_prevista:
            discrepancias.append({
                'tipo': 'Transação Real Não Prevista',
                'id': transacao_real['id'],
                'data': transacao_real['data'],
                'tipo transacao': transacao_real['tipo'],
                'valor real': transacao_real['valor'],
                'erro': 'Transação real não prevista no relatório de previsão'
            })

    return discrepancias

def prever_fluxo_caixa(transacoes):
   
    previsao = sum(
        transacao['valor'] if transacao['tipo'] == 'Receita' else -transacao['valor']
        for transacao in transacoes
    )
    return previsao

def gerar_relatorio_previsao():
    transacoes = obter_transacoes_do_mes()
    previsao = prever_fluxo_caixa(transacoes)

    relatorio = {
        'previsao': previsao,
        'detalhes': transacoes
    }
    return relatorio

def processo_verificacao():
    # Obter transações reais e previstas
    transacoes_reais = obter_transacoes_reais()
    relatorio_previsao = gerar_relatorio_previsao()
    transacoes_previstas = relatorio_previsao['detalhes']

    # Identificar discrepâncias
    discrepancias = verificar_discrepancias(transacoes_reais, transacoes_previstas)

    if discrepancias:
        print("Discrepâncias encontradas:")
        for discrepancia in discrepancias:
            print(discrepancia)
    else:
        print("Não há discrepâncias. As transações estão consistentes.")

    # Gerar e exibir relatório de previsão
    print("\nRelatório de Previsão do Fluxo de Caixa:")
    print(f"Previsão total: {relatorio_previsao['previsao']}")
    for transacao in relatorio_previsao['detalhes']:
        print(transacao)    

def obter_transacoes_do_mes():
    # Simulação de transações previstas para o exemplo
    transacoes_mes = [
        {'id': 1, 'data': '2024-06-01', 'tipo': 'Receita', 'valor': 5000},
        {'id': 2, 'data': '2024-06-05', 'tipo': 'Despesa', 'valor': 2000},
        {'id': 3, 'data': '2024-06-10', 'tipo': 'Receita', 'valor': 7000},
        {'id': 4, 'data': '2024-06-15', 'tipo': 'Receita', 'valor': 1000},
    ]
    return transacoes_mes

def executar_comparacao():
    processo_verificacao()

executar_comparacao()

