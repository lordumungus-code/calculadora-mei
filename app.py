import os
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'mei_simulator_secret_key_2026'

# Simulando banco de dados para contatos
contatos = []

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
            
            # Tabela de alíquotas MEI 2026
            # Anexo I - Comércio, Indústria
            # Anexo II - Serviços
            # Anexo III - Serviços (maior valor)
            
            if anexo == 'I':
                aliquota = 0.047  # 4,7%
                nome_anexo = "Comércio e Indústria"
                descricao = "Anexo I: comércio, indústria, transporte de carga"
            elif anexo == 'II':
                aliquota = 0.047  # 4,7%
                nome_anexo = "Serviços (padrão)"
                descricao = "Anexo II: serviços em geral"
            else:  # Anexo III
                aliquota = 0.055  # 5,5%
                nome_anexo = "Serviços (maior valor)"
                descricao = "Anexo III: serviços como advocacia, medicina, engenharia"
            
            # Valor fixo do DAS MEI 2026 (R$ 71,60 para comércio, R$ 72,60 para serviços)
            das_fixo = 71.60 if anexo == 'I' else 72.60
            
            # Cálculo do DAS baseado no faturamento
            das_proporcional = faturamento_mensal * aliquota
            das_pagar = max(das_fixo, das_proporcional)  # Paga o maior
            
            # Cálculo anual
            faturamento_anual = faturamento_mensal * 12
            limite_anual = 81000.00  # Limite MEI 2026
            percentual_limite = (faturamento_anual / limite_anual) * 100
            
            # Verificar se está próximo do limite
            if faturamento_anual >= limite_anual:
                alerta = "ATENÇÃO: Seu faturamento anual ultrapassa o limite do MEI! Consulte um contador."
                classe_alerta = "danger"
            elif faturamento_anual >= limite_anual * 0.9:
                alerta = f"Cuidado: Você está a {limite_anual - faturamento_anual:.2f} de atingir o limite do MEI."
                classe_alerta = "warning"
            else:
                alerta = None
                classe_alerta = ""
            
            resultado = {
                'faturamento_mensal': faturamento_mensal,
                'faturamento_anual': round(faturamento_anual, 2),
                'limite_anual': limite_anual,
                'percentual_limite': round(percentual_limite, 1),
                'aliquota': round(aliquota * 100, 1),
                'nome_anexo': nome_anexo,
                'descricao_anexo': descricao,
                'das_fixo': das_fixo,
                'das_proporcional': round(das_proporcional, 2),
                'das_pagar': round(das_pagar, 2),
                'alerta': alerta,
                'classe_alerta': classe_alerta
            }
            
        except ValueError:
            flash('Por favor, insira valores numéricos válidos', 'error')
        except Exception as e:
            flash(f'Erro no cálculo: {str(e)}', 'error')
    
    return render_template('simulador_mei.html', resultado=resultado)

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

# Artigos
@app.route('/artigos/como-abrir-mei')
def artigo_abrir_mei():
    return render_template('artigos/como_abrir_mei.html')

@app.route('/artigos/obrigacoes-mei')
def artigo_obrigacoes():
    return render_template('artigos/obrigacoes_mei.html')

@app.route('/artigos/teto-faturamento')
def artigo_teto():
    return render_template('artigos/teto_faturamento.html')

@app.route('/artigos/guia-impostos-mei')
def artigo_impostos():
    return render_template('artigos/guia_impostos_mei.html')

@app.route('/artigos/mei-ou-me')
def artigo_mei_me():
    return render_template('artigos/mei_ou_me.html')

@app.route('/ads.txt')
def ads_txt():
    # Substitua pelo código exato que o Google forneceu
    return "google.com, pub-2580999860510639, DIRECT, f08c47fec0942fa0"    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)