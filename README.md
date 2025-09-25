# 🎭 Analisador de Sentimentos com IA

Um projeto simples e eficaz para análise de emoções em textos usando Python e interface gráfica.

## 📋 Funcionalidades

- **Análise de 7 emoções**: Alegria, Tristeza, Raiva, Medo, Amor, Nojo, Surpresa
- **Interface gráfica** intuitiva com Tkinter
- **Sistema de pontuação** por intensidade emocional
- **Histórico** das últimas 10 análises
- **Dicas personalizadas** para cada emoção detectada
- **Análise em tempo real** com feedback visual

## 🚀 Como usar

### Pré-requisitos
- Python 3.6 ou superior
- pip (gerenciador de pacotes do Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/KarolNutty/Analise_de_Sentimentos.git
cd Analise_de_Sentimentos
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python analisador_emocoes.py
```

## 🎯 Exemplo de uso

1. Digite um texto na área de entrada
2. Clique em "🔍 Analisar Emoções"
3. Veja o resultado com:
   - Emoções detectadas
   - Intensidade (sistema de pontos)
   - Emoção predominante
   - Dica personalizada

### Textos de exemplo para testar:
- **Alegria**: "Estou muito feliz hoje! Que dia maravilhoso!"
- **Tristeza**: "Me sinto vazio e com muita saudade..."
- **Raiva**: "Que situação irritante e injusta!"

## 🛠️ Tecnologias utilizadas

- **Python 3.x**
- **Tkinter** - Interface gráfica
- **Requests** - Requisições HTTP (futuras implementações)
- **JSON** - Manipulação de dados

## 📊 Como funciona

O sistema utiliza análise baseada em palavras-chave, onde:
- Cada emoção possui um dicionário de palavras associadas
- O texto é analisado procurando por essas palavras
- A pontuação é calculada pela quantidade de indicadores encontrados
- A emoção com maior pontuação é considerada predominante

## 🔮 Próximas implementações

- [ ] Integração com APIs de IA para análise mais avançada
- [ ] Suporte a análise de arquivos de texto
- [ ] Gráficos de tendências emocionais
- [ ] Exportação de resultados (CSV, PDF)
- [ ] Análise de múltiplos idiomas

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**KarolNutty** - [GitHub](https://github.com/KarolNutty)

---

⭐ Se este projeto te ajudou, deixe uma estrela no repositório!