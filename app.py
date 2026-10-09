import os
from flask import Flask, render_template, request, flash, redirect, url_for, Response

app = Flask(__name__)
app.secret_key = 'mei_simulator_secret_key_2026'

ARTIGOS = {
    # ============ 5 ARTIGOS ORIGINAIS ============
    "como-abrir-mei": {
        "titulo": "Como Abrir MEI em 2026: Guia Grátis em 5 Passos (Atualizado)",
        "descricao": "Aprenda a abrir MEI gratuitamente em 2026 em 5 passos. Documentos, custos e o que fazer depois. Guia atualizado pela Receita Federal.",
        "data": "2026-01-10",
        "categoria": "Primeiros Passos",
        "template": "artigos/como_abrir_mei.html"
    },
    "obrigacoes-mei": {
        "titulo": "Obrigações do MEI em 2026: Lista Completa Para Não Pagar Multa",
        "descricao": "Todas as obrigações mensais e anuais do MEI em 2026. DAS, nota fiscal, DASN-SIMEI e mais. Evite multas e mantenha o CNPJ regular.",
        "data": "2026-01-12",
        "categoria": "Obrigações",
        "template": "artigos/obrigacoes_mei.html"
    },
    "teto-faturamento": {
        "titulo": "Teto do MEI 2026: Limite de R$ 81.000 e o Que Fazer se Ultrapassar",
        "descricao": "Entenda o limite de R$ 81.000 do MEI em 2026, o que acontece se ultrapassar e como regularizar. Excesso até 20% tem regra especial.",
        "data": "2026-01-14",
        "categoria": "Regras",
        "template": "artigos/teto_faturamento.html"
    },
    "guia-impostos-mei": {
        "titulo": "Guia MEI 2026: Todos os Impostos que Você Paga (DAS, ICMS, ISS, INSS)",
        "descricao": "Guia completo dos impostos do MEI em 2026: DAS, INSS, ICMS e ISS. Veja os valores exatos por atividade e como calcular o seu.",
        "data": "2026-01-16",
        "categoria": "Impostos",
        "template": "artigos/guia_impostos_mei.html"
    },
    "mei-ou-me": {
        "titulo": "MEI ou ME em 2026? Compare Limites, Impostos e Quando Migrar",
        "descricao": "MEI ou ME? Compare limites, impostos, funcionários e obrigações. Descubra qual é melhor para o seu negócio em 2026.",
        "data": "2026-01-18",
        "categoria": "Comparativos",
        "template": "artigos/mei_ou_me.html"
    },

    # ============ 10 ARTIGOS TEMÁTICOS ============
    "como-pagar-das-mei": {
        "titulo": "Como Pagar o DAS do MEI em 2026: Guia Passo a Passo (App, Site, Banco)",
        "descricao": "Aprenda a gerar e pagar o DAS do MEI em 2026 pelo app, site ou banco. Valores, prazo (dia 20) e o que fazer se atrasar.",
        "data": "2026-02-01",
        "categoria": "Impostos",
        "template": "artigos/como_pagar_das_mei.html"
    },
    "declaracao-anual-mei-dasn-simei": {
        "titulo": "Declaração Anual MEI (DASN-SIMEI) 2026: Como Fazer em 7 Passos",
        "descricao": "Passo a passo da Declaração Anual do MEI (DASN-SIMEI) 2026. Prazo até 31 de maio, multa de R$ 50 se não entregar. Guia completo.",
        "data": "2026-02-03",
        "categoria": "Obrigações",
        "template": "artigos/declaracao_anual_mei_dasn_simei.html"
    },
    "mei-pode-ter-funcionario": {
        "titulo": "MEI Pode Ter Funcionário em 2026? Regras, Custos e Como Contratar",
        "descricao": "Sim, o MEI pode ter 1 funcionário. Veja regras CLT, custo real (~30% acima do salário) e como registrar no eSocial em 2026.",
        "data": "2026-02-05",
        "categoria": "Regras",
        "template": "artigos/mei_pode_ter_funcionario.html"
    },
    "como-emitir-nota-fiscal-mei": {
        "titulo": "Como Emitir Nota Fiscal MEI em 2026: Guia Simples (NFS-e, NF-e, NFC-e)",
        "descricao": "Aprenda a emitir nota fiscal como MEI em 2026. Quando é obrigatório, tipos de nota (NFS-e, NF-e, NFC-e) e o que acontece se não emitir.",
        "data": "2026-02-07",
        "categoria": "Obrigações",
        "template": "artigos/como_emitir_nota_fiscal_mei.html"
    },
    "o-que-acontece-se-ultrapassar-limite-mei": {
        "titulo": "MEI Ultrapassou o Limite de R$ 81.000? Veja o Que Acontece em 2026",
        "descricao": "Descubra o que acontece se o MEI ultrapassar o limite de R$ 81.000 em 2026. Excesso até 20%, desenquadramento e como regularizar.",
        "data": "2026-02-09",
        "categoria": "Regras",
        "template": "artigos/o_que_acontece_se_ultrapassar_limite_mei.html"
    },
    "mei-inss-beneficios-aposentadoria": {
        "titulo": "Aposentadoria MEI 2026: Como Funciona e Quais Benefícios Você Tem",
        "descricao": "Descubra como funciona a aposentadoria do MEI em 2026. Idade mínima, carência, benefícios (auxílio-doença, salário-maternidade) e como complementar.",
        "data": "2026-02-11",
        "categoria": "Benefícios",
        "template": "artigos/mei_inss_beneficios_aposentadoria.html"
    },
    "como-fechar-mei": {
        "titulo": "Como Fechar o MEI em 2026: Passo a Passo Grátis em 5 Minutos",
        "descricao": "Aprenda a fechar o MEI em 2026 gratuitamente em 5 minutos. O que precisa estar em dia, documentos e o que fazer depois da baixa.",
        "data": "2026-02-13",
        "categoria": "Primeiros Passos",
        "template": "artigos/como_fechar_mei.html"
    },
    "mei-pode-ser-mei-e-clt": {
        "titulo": "Posso Ser MEI e CLT ao Mesmo Tempo em 2026? Entenda as Regras",
        "descricao": "Sim, é permitido ser MEI e CLT em 2026. Veja regras, como declarar as duas rendas e em quais casos pode dar problema.",
        "data": "2026-02-15",
        "categoria": "Regras",
        "template": "artigos/mei_pode_ser_mei_e_clt.html"
    },
    "melhores-atividades-para-mei": {
        "titulo": "30 Melhores Atividades Para Ser MEI em 2026 (Lista Atualizada e Lucrativa)",
        "descricao": "Lista atualizada das 30 melhores atividades para MEI em 2026. Veja as mais lucrativas, com menor concorrência e como escolher a sua.",
        "data": "2026-02-17",
        "categoria": "Primeiros Passos",
        "template": "artigos/melhores_atividades_para_mei.html"
    },
    "mei-nao-pagou-das-o-que-acontece": {
        "titulo": "MEI Não Pagou o DAS? Veja as Consequências e Como Regularizar",
        "descricao": "Não pagou o DAS do MEI? Veja multas, juros, perda de benefícios do INSS e como regularizar 100% online. Guia atualizado 2026.",
        "data": "2026-02-19",
        "categoria": "Impostos",
        "template": "artigos/mei_nao_pagou_das_o_que_acontece.html"
    },

    # ============ 5 ARTIGOS POR ATIVIDADE PROFISSIONAL ============
    "mei-eletricista": {
        "titulo": "MEI Eletricista 2026: CNAE, DAS R$ 82,05, CBO e Como Se Formalizar",
        "descricao": "Guia completo para eletricista ser MEI em 2026: CNAE 4321-5/00, DAS de R$ 82,05, CBO 7156-05 e dicas de precificação.",
        "data": "2026-03-01",
        "categoria": "Atividades",
        "template": "artigos/mei_eletricista.html"
    },
    "mei-manicure": {
        "titulo": "MEI Manicure 2026: CNAE, DAS R$ 86,05, CBO e Como Se Formalizar",
        "descricao": "Guia para manicure e pedicure ser MEI em 2026: CNAE 9602-5/01, DAS de R$ 86,05, CBO 5161-20 e dicas de precificação.",
        "data": "2026-03-03",
        "categoria": "Atividades",
        "template": "artigos/mei_manicure.html"
    },
    "mei-confeiteiro": {
        "titulo": "MEI Confeiteiro 2026: CNAE, DAS R$ 82,05, CBO e Como Se Formalizar",
        "descricao": "Guia para confeiteiro ser MEI em 2026: CNAE 1091-1/02, DAS de R$ 82,05, CBO 8483-10 e dicas de precificação.",
        "data": "2026-03-05",
        "categoria": "Atividades",
        "template": "artigos/mei_confeiteiro.html"
    },
    "mei-designer-grafico": {
        "titulo": "Designer Gráfico Pode Ser MEI? Entenda a Regra em 2026",
        "descricao": "Designer Gráfico não pode ser MEI. Entenda o motivo, qual CNAE usar (7410-2/99) e como se formalizar como ME em 2026.",
        "data": "2026-03-07",
        "categoria": "Atividades",
        "template": "artigos/mei_designer_grafico.html"
    },
    "mei-motorista-app": {
        "titulo": "MEI Motorista de App 2026: CNAE Correto, DAS R$ 82,05 e Regras",
        "descricao": "Motorista de app pode ser MEI em 2026. Veja o CNAE correto (4923-0/01), DAS de R$ 82,05, CBO 5191-10 e dicas de precificação.",
        "data": "2026-03-09",
        "categoria": "Atividades",
        "template": "artigos/mei_motorista_app.html"
    },
}

# Simulando banco de dados para contatos
contatos = []


# ============================================================
# ROTAS PRINCIPAIS
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/simulador-mei', methods=['GET', 'POST'])
def simulador_mei():
    resultado = None
    if request.method == 'POST':
        try:
            faturamento_mensal = float(request.form['faturamento_mensal'])
            anexo = request.form['anexo']

            # ============================================================
            # VALORES OFICIAIS DO DAS 2026
            # Base: salário mínimo R$ 1.621,00
            # ============================================================
            salario_minimo = 1621.00

            # MEI geral: 5% do salário mínimo
            inss_geral = round(salario_minimo * 0.05, 2)  # R$ 81,05

            # MEI caminhoneiro: 12% do salário mínimo
            inss_caminhoneiro = round(salario_minimo * 0.12, 2)  # R$ 194,52

            icms = 1.00  # comércio/indústria
            iss = 5.00   # serviços

            if anexo == 'I':  # Comércio / Indústria
                das_fixo = inss_geral + icms                # R$ 82,05
                nome_anexo = "Comércio e Indústria"
                descricao = "INSS + ICMS"
            elif anexo == 'II':  # Serviços
                das_fixo = inss_geral + iss                 # R$ 86,05
                nome_anexo = "Serviços"
                descricao = "INSS + ISS"
            elif anexo == 'III':  # Comércio + Serviços
                das_fixo = inss_geral + icms + iss          # R$ 87,05
                nome_anexo = "Comércio e Serviços"
                descricao = "INSS + ICMS + ISS"
            elif anexo == 'CAMINHONEIRO':  # MEI Caminhoneiro
                das_fixo = inss_caminhoneiro + icms         # R$ 195,52
                nome_anexo = "MEI Caminhoneiro"
                descricao = "INSS 12% + ICMS"
            else:
                das_fixo = inss_geral + icms
                nome_anexo = "Comércio e Indústria"
                descricao = "INSS + ICMS"

            faturamento_anual = faturamento_mensal * 12
            limite_anual = 81000.00
            percentual_limite = (faturamento_anual / limite_anual) * 100

            if faturamento_anual > limite_anual:
                alerta = "ATENÇÃO: Seu faturamento anual ultrapassa o limite do MEI! Consulte um contador."
                classe_alerta = "danger"
            elif faturamento_anual >= limite_anual * 0.9:
                alerta = f"Cuidado: você está a R$ {limite_anual - faturamento_anual:.2f} de atingir o limite do MEI."
                classe_alerta = "warning"
            else:
                alerta = None
                classe_alerta = ""

            resultado = {
                'faturamento_mensal': faturamento_mensal,
                'faturamento_anual': round(faturamento_anual, 2),
                'limite_anual': limite_anual,
                'percentual_limite': round(percentual_limite, 1),
                'nome_anexo': nome_anexo,
                'descricao_anexo': descricao,
                'das_pagar': round(das_fixo, 2),
                'inss': inss_caminhoneiro if anexo == 'CAMINHONEIRO' else inss_geral,
                'icms': icms if anexo in ('I', 'III', 'CAMINHONEIRO') else 0,
                'iss': iss if anexo in ('II', 'III') else 0,
                'alerta': alerta,
                'classe_alerta': classe_alerta,
            }
        except ValueError:
            flash('Por favor, insira valores numéricos válidos', 'error')
        except Exception as e:
            flash(f'Erro no cálculo: {str(e)}', 'error')

    return render_template('simulador_mei.html', resultado=resultado)


# ============================================================
# PÁGINAS INSTITUCIONAIS
# ============================================================
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            email = request.form['email']
            mensagem = request.form['mensagem']

            if not nome or not email or not mensagem:
                flash('Todos os campos são obrigatórios', 'error')
                return render_template('contato.html')

            contatos.append({
                'nome': nome,
                'email': email,
                'mensagem': mensagem
            })

            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
        except KeyError:
            flash('Erro ao processar o formulário', 'error')

        return redirect(url_for('contato'))

    return render_template('contato.html')


@app.route('/politica-de-privacidade')
def politica_privacidade():
    return render_template('politica_privacidade.html')


# ============================================================
# ARTIGOS
# ============================================================
@app.route('/artigos')
def lista_artigos():
    artigos_ordenados = sorted(
        ARTIGOS.items(),
        key=lambda x: x[1]['data'],
        reverse=True
    )
    return render_template('artigos/lista.html', artigos=artigos_ordenados)


@app.route('/artigos/<slug>')
def artigo(slug):
    artigo_data = ARTIGOS.get(slug)
    if not artigo_data:
        return render_template('404.html'), 404
    return render_template(artigo_data['template'], meta=artigo_data, slug=slug)


# ============================================================
# SEO TÉCNICO: ads.txt, robots.txt, sitemap.xml
# ============================================================
@app.route('/ads.txt')
def ads_txt():
    conteudo = "google.com, pub-2580999860510639, DIRECT, f08c47fec0942fa0\n"
    return Response(conteudo, mimetype='text/plain')


@app.route('/robots.txt')
def robots():
    conteudo = """User-agent: *
Allow: /
Disallow: /static/

Sitemap: https://www.calculadora-mei.net.br/sitemap.xml
"""
    return Response(conteudo, mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap():
    urls = [
        ('/', '1.0', 'weekly'),
        ('/simulador-mei', '0.9', 'monthly'),
        ('/artigos', '0.8', 'weekly'),
        ('/sobre', '0.5', 'monthly'),
        ('/contato', '0.5', 'monthly'),
        ('/politica-de-privacidade', '0.3', 'yearly'),
    ]
    for slug in ARTIGOS.keys():
        urls.append((f'/artigos/{slug}', '0.7', 'monthly'))

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, prio, freq in urls:
        xml.append('  <url>')
        xml.append(f'    <loc>https://www.calculadora-mei.net.br{url}</loc>')
        xml.append(f'    <priority>{prio}</priority>')
        xml.append(f'    <changefreq>{freq}</changefreq>')
        xml.append('  </url>')
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')


# ============================================================
# ERRO 404
# ============================================================
@app.errorhandler(404)
def nao_encontrado(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)