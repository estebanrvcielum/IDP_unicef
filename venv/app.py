import PyPDF2
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def process():
    key = request.form.get("api_key")
    pathPDF = request.form.get("pdf_file")
    question = request.form.get("question")

    print(key)
    print(pathPDF)
    print(question)


    # openai.api_key = "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"
    openai.api_key = key

    pdf_path = pathPDF

    # Abrir el archivo PDF
    with open(pdf_path, "rb") as pdf_file:
        # Crear un objeto de lectura de PDF
        reader = PyPDF2.PdfReader(pdf_file)

        # Obtener el número de páginas del PDF
        num_pages = len(reader.pages)

        # Recorrer cada página del PDF
        for page_num in range(num_pages):
            # Obtener el objeto de página actual
            page_obj = reader.pages[page_num]

            # Extraer el texto de la página y mostrarlo
            contentBot = page_obj.extract_text()
           # print(contentBot)
    #while True:
        # Inicializar la conversación con OpenAI
        messages = [{"role": "system", "content": contentBot}]

        # Pedir la entrada del usuario y agregarla a la lista de mensajes
        #content = input("Haz una pregunta: ")
        content = question;
        #if content == "exit":
         #   break
        messages.append({"role": "user", "content": content})

        # Obtener la respuesta de OpenAI
        response = openai.ChatCompletion.create(
            #engine="text-davinci-002",
            model="gpt-3.5-turbo-0301",
            messages=messages,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            stop=None,
            timeout=10,
        )

        # Imprimir la respuesta de OpenAI
        print(response.choices[0].message.content)
        response = response.choices[0].message.content

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run()
