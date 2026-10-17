"""Regras de cálculo das calculadoras do site.

Todas as funções recebem valores já convertidos e levantam ValueError com uma
mensagem amigável quando a entrada é inválida.
"""
from datetime import date, timedelta

# Salário mínimo por ano (base do INSS do DAS)
SALARIO_MINIMO = {
    2024: 1412.00,
    2025: 1518.00,
    2026: 1621.00,
}
ANO_ATUAL_REGRAS = max(SALARIO_MINIMO)

ICMS = 1.00
ISS = 5.00

LIMITE_MEI = 81000.00
LIMITE_CAMINHONEIRO = 251600.00

ATIVIDADES_DAS = {
    'I': 'Comércio / Indústria',
    'II': 'Serviços',
    'III': 'Comércio + Serviços',
    'CAMINHONEIRO': 'MEI Caminhoneiro',
}


def composicao_das(anexo, ano=ANO_ATUAL_REGRAS):
    """Valores de INSS, ICMS e ISS do DAS para a atividade e o ano informados."""
    if ano not in SALARIO_MINIMO:
        raise ValueError(f'Temos os valores do DAS de {min(SALARIO_MINIMO)} a {max(SALARIO_MINIMO)}.')
    if anexo not in ATIVIDADES_DAS:
        raise ValueError('Escolha uma atividade válida.')

    salario = SALARIO_MINIMO[ano]
    caminhoneiro = anexo == 'CAMINHONEIRO'
    inss = round(salario * (0.12 if caminhoneiro else 0.05), 2)
    icms = ICMS if anexo in ('I', 'III', 'CAMINHONEIRO') else 0
    iss = ISS if anexo in ('II', 'III') else 0
    return {
        'inss': inss,
        'icms': icms,
        'iss': iss,
        'total': round(inss + icms + iss, 2),
        'caminhoneiro': caminhoneiro,
        'nome': ATIVIDADES_DAS[anexo],
    }


# ============================================================
# DAS EM ATRASO
# ============================================================
def vencimento_das(ano, mes):
    """Dia 20 do mês seguinte à competência; fim de semana passa para segunda."""
    if mes == 12:
        venc = date(ano + 1, 1, 20)
    else:
        venc = date(ano, mes + 1, 20)
    if venc.weekday() == 5:
        venc += timedelta(days=2)
    elif venc.weekday() == 6:
        venc += timedelta(days=1)
    return venc


def das_atrasado(competencia, anexo, data_pagamento, selic_mensal):
    """
    competencia: 'AAAA-MM'. selic_mensal em % (ex.: 1.0).
    Multa de mora: 0,33% por dia de atraso, limitada a 20%.
    Juros: Selic acumulada dos meses seguintes ao vencimento até o mês anterior
    ao pagamento, mais 1% no mês do pagamento.
    """
    try:
        ano, mes = (int(p) for p in competencia.split('-'))
        date(ano, mes, 1)
    except (ValueError, AttributeError):
        raise ValueError('Informe o mês de referência do DAS.')
    if selic_mensal < 0 or selic_mensal > 5:
        raise ValueError('Informe uma taxa Selic mensal entre 0% e 5%.')

    das = composicao_das(anexo, ano)
    valor = das['total']
    venc = vencimento_das(ano, mes)
    dias = (data_pagamento - venc).days

    if dias <= 0:
        multa_pct = juros_pct = 0.0
        meses = 0
    else:
        multa_pct = min(0.0033 * dias, 0.20)
        meses = (data_pagamento.year * 12 + data_pagamento.month) - (venc.year * 12 + venc.month)
        juros_pct = 0.0 if meses <= 0 else (selic_mensal / 100) * (meses - 1) + 0.01

    multa = round(valor * multa_pct, 2)
    juros = round(valor * juros_pct, 2)
    return {
        'competencia': f'{mes:02d}/{ano}',
        'atividade': das['nome'],
        'valor_original': valor,
        'vencimento': venc,
        'pagamento': data_pagamento,
        'dias_atraso': max(dias, 0),
        'em_dia': dias <= 0,
        'multa_pct': round(multa_pct * 100, 2),
        'multa': multa,
        'multa_no_teto': multa_pct >= 0.20,
        'juros_pct': round(juros_pct * 100, 2),
        'juros': juros,
        'total': round(valor + multa + juros, 2),
    }


# ============================================================
# LIMITE PROPORCIONAL
# ============================================================
def limite_proporcional(abertura, ano_analise, faturamento, caminhoneiro=False):
    """
    abertura: 'AAAA-MM'. No ano de abertura o limite é proporcional aos meses
    de atividade (contando o mês de abertura).
    """
    try:
        ano_ab, mes_ab = (int(p) for p in abertura.split('-'))
        date(ano_ab, mes_ab, 1)
    except (ValueError, AttributeError):
        raise ValueError('Informe o mês de abertura do MEI.')
    if (ano_ab, mes_ab) > (ano_analise, 12):
        raise ValueError('A data de abertura não pode ser depois do ano analisado.')
    if faturamento < 0:
        raise ValueError('O faturamento não pode ser negativo.')

    limite_anual = LIMITE_CAMINHONEIRO if caminhoneiro else LIMITE_MEI
    limite_mensal = limite_anual / 12
    primeiro_ano = ano_ab == ano_analise
    meses = 13 - mes_ab if primeiro_ano else 12
    limite = round(limite_mensal * meses, 2)
    tolerancia = round(limite * 1.2, 2)

    if faturamento <= limite:
        situacao = 'dentro'
    elif faturamento <= tolerancia:
        situacao = 'excesso_ate_20'
    else:
        situacao = 'excesso_acima_20'

    excesso = max(round(faturamento - limite, 2), 0)
    return {
        'ano': ano_analise,
        'primeiro_ano': primeiro_ano,
        'meses': meses,
        'limite_mensal': round(limite_mensal, 2),
        'limite': limite,
        'tolerancia': tolerancia,
        'faturamento': faturamento,
        'restante': max(round(limite - faturamento, 2), 0),
        'excesso': excesso,
        # Excesso de até 20% é tributado pelas alíquotas do Simples (4% comércio, 6% serviços)
        'imposto_excesso_min': round(excesso * 0.04, 2),
        'imposto_excesso_max': round(excesso * 0.06, 2),
        'percentual': round(faturamento / limite * 100, 1) if limite else 0,
        'situacao': situacao,
        'caminhoneiro': caminhoneiro,
    }


# ============================================================
# MEI OU ME (SIMPLES NACIONAL)
# ============================================================
# (limite da faixa, alíquota nominal, parcela a deduzir)
ANEXO_I = [
    (180000, 0.04, 0),
    (360000, 0.073, 5940),
    (720000, 0.095, 13860),
    (1800000, 0.107, 22500),
    (3600000, 0.143, 87300),
    (4800000, 0.19, 378000),
]
ANEXO_III = [
    (180000, 0.06, 0),
    (360000, 0.112, 9360),
    (720000, 0.135, 17640),
    (1800000, 0.16, 35640),
    (3600000, 0.21, 125640),
    (4800000, 0.33, 648000),
]
ANEXOS_SIMPLES = {
    'comercio': ('Comércio / Indústria (Anexo I)', ANEXO_I, 'I'),
    'servicos': ('Serviços (Anexo III)', ANEXO_III, 'II'),
}


def aliquota_efetiva(rbt12, tabela):
    for teto, aliquota, deducao in tabela:
        if rbt12 <= teto:
            return (rbt12 * aliquota - deducao) / rbt12 if rbt12 else aliquota
    raise ValueError('O Simples Nacional vai até R$ 4,8 milhões por ano.')


def mei_ou_me(faturamento_mensal, atividade, contador_mensal):
    if faturamento_mensal <= 0:
        raise ValueError('Informe um faturamento mensal maior que zero.')
    if contador_mensal < 0:
        raise ValueError('O custo do contador não pode ser negativo.')
    if atividade not in ANEXOS_SIMPLES:
        raise ValueError('Escolha uma atividade válida.')

    nome, tabela, anexo_mei = ANEXOS_SIMPLES[atividade]
    anual = faturamento_mensal * 12
    efetiva = aliquota_efetiva(anual, tabela)

    pode_mei = anual <= LIMITE_MEI
    das_mei_anual = round(composicao_das(anexo_mei)['total'] * 12, 2)
    imposto_me = round(anual * efetiva, 2)
    contador_anual = round(contador_mensal * 12, 2)
    total_me = round(imposto_me + contador_anual, 2)

    return {
        'atividade': nome,
        'faturamento_anual': round(anual, 2),
        'pode_mei': pode_mei,
        'das_mei_anual': das_mei_anual,
        'das_mei_mensal': round(das_mei_anual / 12, 2),
        'aliquota_efetiva': round(efetiva * 100, 2),
        'imposto_me_anual': imposto_me,
        'imposto_me_mensal': round(imposto_me / 12, 2),
        'contador_anual': contador_anual,
        'total_me_anual': total_me,
        'economia_mei': round(total_me - das_mei_anual, 2),
    }


# ============================================================
# IMPOSTO DE RENDA DO MEI (PESSOA FÍSICA)
# ============================================================
PRESUNCAO_IR = {
    'comercio': ('Comércio, indústria ou transporte de cargas', 0.08),
    'passageiros': ('Transporte de passageiros', 0.16),
    'servicos': ('Serviços em geral', 0.32),
}


def imposto_renda_mei(receita, despesas, atividade):
    if receita <= 0:
        raise ValueError('Informe a receita bruta anual.')
    if despesas < 0:
        raise ValueError('As despesas não podem ser negativas.')
    if atividade not in PRESUNCAO_IR:
        raise ValueError('Escolha uma atividade válida.')

    nome, pct = PRESUNCAO_IR[atividade]
    lucro = round(receita - despesas, 2)
    limite_isento = round(receita * pct, 2)

    if lucro <= 0:
        isento, tributavel = 0.0, 0.0
    elif lucro <= limite_isento:
        isento, tributavel = lucro, 0.0
    else:
        isento, tributavel = limite_isento, round(lucro - limite_isento, 2)

    return {
        'atividade': nome,
        'percentual': int(pct * 100),
        'receita': receita,
        'despesas': despesas,
        'lucro': lucro,
        'limite_isento': limite_isento,
        'isento': isento,
        'tributavel': tributavel,
    }


# ============================================================
# CUSTO DE FUNCIONÁRIO DO MEI
# ============================================================
FGTS = 0.08
CPP_MEI = 0.03  # contribuição patronal do MEI com empregado


def custo_funcionario(salario, vale_transporte=0.0, ano=ANO_ATUAL_REGRAS):
    minimo = SALARIO_MINIMO[ano]
    if salario < minimo:
        minimo_br = f'{minimo:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        raise ValueError(f'O salário não pode ser menor que o salário mínimo (R$ {minimo_br}).')
    if vale_transporte < 0:
        raise ValueError('O vale-transporte não pode ser negativo.')

    decimo = salario / 12
    ferias = salario / 12 * 4 / 3
    base_encargos = salario + decimo + ferias
    fgts = base_encargos * FGTS
    cpp = base_encargos * CPP_MEI
    # Empregador pode descontar até 6% do salário no vale-transporte
    vt_empresa = max(vale_transporte - salario * 0.06, 0)

    total = salario + decimo + ferias + fgts + cpp + vt_empresa
    return {
        'salario': salario,
        'decimo': round(decimo, 2),
        'ferias': round(ferias, 2),
        'fgts': round(fgts, 2),
        'cpp': round(cpp, 2),
        'vale_transporte': round(vt_empresa, 2),
        'total_mensal': round(total, 2),
        'total_anual': round(total * 12, 2),
        'acrescimo_pct': round((total / salario - 1) * 100, 1),
        'acima_minimo': salario > minimo,
    }
