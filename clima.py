from shiny import App, ui, render
import requests

API_KEY = '1b2c05abfdeec9b4468b1480cb30c9a6'

app_ui = ui.page_fluid(
    ui.input_text("cidade", "Digite o nome da cidade (ou várias, separadas por vírgula):", placeholder="Ex: São Paulo, Rio de Janeiro"),
    ui.output_text("resultado")
)

def server(input, output, session):
    @output
    @render.text
    def resultado():
        texto = input.cidade().strip()
        if not texto:
            return "Por favor, insira pelo menos uma cidade."

        cidades = [c.strip() for c in texto.split(",")]

        resultados = []
        for cidade in cidades:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dados = resposta.json()
                temperatura = dados['main']['temp']
                descricao = dados['weather'][0]['description']
                resultados.append(f"{cidade.title()}: {temperatura}°C, {descricao}.")
            else:
                resultados.append(f"{cidade.title()}: Cidade não encontrada ou erro na requisição.")

        return "\n".join(resultados)

app = App(app_ui, server)