import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def get_Url(url):
    News = requests.get(url)  # Fazendo uma solicitação GET para a URL fornecida

    if News.status_code == 200:  # Verificando se a solicitação retornou com sucesso
        Page_content = News.text

        # Parseando o conteúdo HTML
        Parser = BeautifulSoup(Page_content, 'html.parser')

        # Extraindo os parágrafos da página
        extract = Parser.find_all('p')

        # Concatenando todo o texto dos parágrafos
        Text_News = " ".join([paragraph.get_text() for paragraph in extract])
        return Text_News
    else:
        print("Unable to access the page. Try again!")
        return None

def summarize_text(text):
    # Inicializando o pipeline de sumarização
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Verificando o comprimento do texto, pois há um limite de 1024 tokens
    if len(text) > 1024:
        # Se o texto for muito longo, pode ser necessário dividir em partes
        summarized_parts = summarizer(text[:1024], max_length=130, min_length=30, do_sample=False)
        summarized_text = summarized_parts[0]['summary_text']
    else:
        # Resumindo diretamente se o texto for curto o suficiente
        summarized_text = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

    # Exibindo o resumo
    print("\nNews Summary:\n", summarized_text)

if __name__ == "__main__":
    url = input("Enter the URL of the news you want to summarize:\n")
    
    # Extraindo o texto da notícia
    News_text = get_Url(url)

    # Se o texto foi extraído corretamente, faz o resumo
    if News_text:
        summarize_text(News_text)
