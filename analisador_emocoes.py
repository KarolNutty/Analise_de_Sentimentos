
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
from datetime import datetime
import threading

class AnalisadorEmocoes:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 Analisador de Emoções com IA")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        self.criar_interface()
        self.historico = []
        
    def criar_interface(self):
        # Título principal
        titulo = tk.Label(
            self.root, 
            text="🎭 Analisador de Emoções", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        titulo.pack(pady=15)
        
        # Frame para entrada de texto
        frame_entrada = ttk.LabelFrame(self.root, text="Digite seu texto:", padding=10)
        frame_entrada.pack(padx=20, pady=10, fill="x")
        
        self.texto_entrada = scrolledtext.ScrolledText(
            frame_entrada, 
            height=4, 
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.texto_entrada.pack(fill="x")
        
        # Botão de análise
        btn_analisar = ttk.Button(
            self.root, 
            text="🔍 Analisar Emoções", 
            command=self.analisar_emocoes
        )
        btn_analisar.pack(pady=10)
        
        # Frame para resultados
        frame_resultado = ttk.LabelFrame(self.root, text="Resultado da Análise:", padding=10)
        frame_resultado.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Área de resultado
        self.resultado_texto = scrolledtext.ScrolledText(
            frame_resultado, 
            height=8, 
            wrap=tk.WORD,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.resultado_texto.pack(fill="both", expand=True)
        
        # Frame para botões inferiores
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="📋 Limpar", command=self.limpar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="📊 Histórico", command=self.mostrar_historico).pack(side=tk.LEFT, padx=5)
        
    def analisar_emocoes_local(self, texto):
        """Análise simples de emoções usando palavras-chave"""
        
        # Dicionários de palavras associadas a emoções (expandido)
        emocoes = {
            "😊 Alegria": ["feliz", "alegre", "contente", "animado", "eufórico", "radiante", "satisfeito", "otimista", 
                          "bem", "bom", "ótimo", "maravilhoso", "incrível", "fantástico", "perfeito", "sorrindo"],
            
            "😢 Tristeza": ["triste", "deprimido", "melancólico", "abatido", "desanimado", "desolado", "lamentável",
                           "vazio", "solidão", "saudade", "saudades", "lágrimas", "chorar", "perdido", "sozinho",
                           "silenciosa", "silêncio", "cinzento", "peso", "pesar", "dor", "sofrimento", "mal"],
            
            "😠 Raiva": ["raiva", "irritado", "furioso", "bravo", "zangado", "indignado", "revoltado", "ódio",
                        "raivoso", "nervoso", "estressado", "chateado", "aborrecido", "injusto", "revolta"],
            
            "😨 Medo": ["medo", "assustado", "aterrorizado", "nervoso", "ansioso", "apreensivo", "preocupado",
                       "receio", "temor", "inseguro", "aflito", "angustiado", "tenso", "pânico"],
            
            "😍 Amor": ["amor", "paixão", "carinho", "afeto", "adorar", "amar", "querido", "coração",
                       "amado", "beijar", "abraçar", "casal", "romance", "apaixonado", "paixonite"],
            
            "😤 Nojo": ["nojo", "repugnante", "asqueroso", "detesto", "horrível", "repulsivo",
                       "disgusto", "enjoado", "terrível", "péssimo", "ruim", "odiar"],
            
            "😮 Surpresa": ["surpreso", "chocado", "espantado", "impressionado", "inesperado", "surpreendente",
                           "nossa", "uau", "inacreditável", "choque", "pasmo", "boquiaberto"]
        }
        
        texto_lower = texto.lower()
        resultados = {}
        
        for emocao, palavras in emocoes.items():
            pontuacao = sum(1 for palavra in palavras if palavra in texto_lower)
            if pontuacao > 0:
                resultados[emocao] = pontuacao
        
        return resultados
    
    def analisar_emocoes_api(self, texto):
        """Análise usando API externa (TextBlob via API pública)"""
        try:
            # Usando uma API pública para análise de sentimentos
            url = "https://api.meaningcloud.com/sentiment-2.1"
            
            # Parâmetros para a API (você pode usar sua própria chave)
            payload = {
                'key': 'demo',  # Chave demo - limitada
                'txt': texto,
                'lang': 'pt',  # português
                'model': 'general'
            }
            
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                resultado = json.loads(response.text)
                
                # Mapear resultados da API para nossas emoções
                score_tag = resultado.get('score_tag', 'NEU')
                confidence = resultado.get('confidence', 0)
                
                mapeamento = {
                    'P+': '😊 Alegria',
                    'P': '😊 Alegria',
                    'NEU': '😐 Neutro',
                    'N': '😢 Tristeza',
                    'N+': '😢 Tristeza',
                    'NONE': '🤔 Indefinido'
                }
                
                emocao_detectada = mapeamento.get(score_tag, '🤔 Indefinido')
                
                return {
                    'emocao_principal': emocao_detectada,
                    'confianca': confidence,
                    'detalhes': resultado,
                    'metodo': 'API'
                }
            else:
                return None
                
        except Exception as e:
            print(f"Erro na API: {e}")
            return None
    
    def analisar_emocoes(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning("Aviso", "Por favor, digite um texto para analisar!")
            return
        
        # Desabilitar botão durante análise
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete("1.0", tk.END)
        self.resultado_texto.insert("1.0", "🔄 Analisando... Por favor aguarde!")
        self.resultado_texto.config(state=tk.DISABLED)
        
        # Executar análise em thread separada para não travar a interface
        thread = threading.Thread(target=self.processar_analise, args=(texto,))
        thread.daemon = True
        thread.start()
    
    def processar_analise(self, texto):
        try:
            # Primeiro tentar análise via API
            resultado_api = self.analisar_emocoes_api(texto)
            
            # Sempre fazer análise local também
            emocoes_detectadas = self.analisar_emocoes_local(texto)
            
            # Preparar resultado
            resultado = f"📝 Texto analisado: \"{texto[:50]}{'...' if len(texto) > 50 else ''}\"\n"
            resultado += f"⏰ Análise feita em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n\n"
            
            if emocoes_detectadas:
                resultado += "🎯 Emoções detectadas:\n"
                # Ordenar por pontuação
                emocoes_ordenadas = sorted(emocoes_detectadas.items(), key=lambda x: x[1], reverse=True)
                
                for emocao, pontuacao in emocoes_ordenadas:
                    intensidade = "●" * min(pontuacao, 5)  # Máximo 5 pontos
                    resultado += f"   {emocao}: {intensidade} ({pontuacao} indicadores)\n"
                
                # Emoção dominante
                emocao_principal = emocoes_ordenadas[0][0]
                resultado += f"\n🏆 Emoção predominante: {emocao_principal}"
                
                # Dicas baseadas na emoção principal
                dicas = {
                    "😊 Alegria": "Continue cultivando pensamentos positivos! 🌟",
                    "😢 Tristeza": "Lembre-se: sentimentos passam. Procure apoio se necessário. 🤗",
                    "😠 Raiva": "Respire fundo e tente encontrar soluções construtivas. 🧘‍♀️",
                    "😨 Medo": "Encare os medos como oportunidades de crescimento. 💪",
                    "😍 Amor": "O amor é uma das forças mais poderosas! Compartilhe-o. ❤️",
                    "😤 Nojo": "Identifique o que incomoda e busque alternativas. ✨",
                    "😮 Surpresa": "A surpresa mantém a vida interessante! 🎉"
                }
                
                resultado += f"\n💡 Dica: {dicas.get(emocao_principal, 'Mantenha-se consciente de suas emoções!')}"
                
            else:
                resultado += "🤔 Nenhuma emoção específica foi detectada no texto.\n"
                resultado += "💭 O texto parece neutro ou contém linguagem técnica."
            
            # Salvar no histórico
            self.historico.append({
                'texto': texto,
                'emocoes': emocoes_detectadas,
                'data': datetime.now()
            })
            
            # Mostrar resultado
            self.resultado_texto.config(state=tk.NORMAL)
            self.resultado_texto.delete("1.0", tk.END)
            self.resultado_texto.insert("1.0", resultado)
            self.resultado_texto.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na análise: {str(e)}")
    
    def limpar(self):
        self.texto_entrada.delete("1.0", tk.END)
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete("1.0", tk.END)
        self.resultado_texto.config(state=tk.DISABLED)
    
    def mostrar_historico(self):
        if not self.historico:
            messagebox.showinfo("Histórico", "Nenhuma análise foi feita ainda!")
            return
        
        # Criar janela do histórico
        janela_historico = tk.Toplevel(self.root)
        janela_historico.title("📊 Histórico de Análises")
        janela_historico.geometry("500x400")
        
        historico_texto = scrolledtext.ScrolledText(janela_historico, wrap=tk.WORD)
        historico_texto.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mostrar histórico
        conteudo = "📊 HISTÓRICO DE ANÁLISES\n" + "="*50 + "\n\n"
        
        for i, item in enumerate(reversed(self.historico[-10:]), 1):  # Últimas 10 análises
            conteudo += f"{i}. {item['data'].strftime('%d/%m/%Y %H:%M:%S')}\n"
            conteudo += f"   Texto: \"{item['texto'][:40]}{'...' if len(item['texto']) > 40 else ''}\"\n"
            
            if item['emocoes']:
                emocao_principal = max(item['emocoes'].items(), key=lambda x: x[1])
                conteudo += f"   Emoção principal: {emocao_principal[0]}\n"
            else:
                conteudo += f"   Emoção: Neutro\n"
            
            conteudo += "\n" + "-"*30 + "\n\n"
        
        historico_texto.insert("1.0", conteudo)
        historico_texto.config(state=tk.DISABLED)
    
    def executar(self):
        self.root.mainloop()

# Executar o aplicativo
if __name__ == "__main__":
    print("🚀 Iniciando Analisador de Emoções...")
    app = AnalisadorEmocoes()
    
    # Exemplo de uso no console
    print("\n📋 Você também pode usar via código:")
    print("app = AnalisadorEmocoes()")
    print("resultado = app.analisar_emocoes_local('Estou muito feliz hoje!')")
    print("print(resultado)")
    
    app.executar()