from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS para permitir requisições do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://front-girls.vercel.app",
    "http://localhost:5173",
    ],  # Altere para o domínio do seu frontend se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define o modelo de dados recebido
class Answer(BaseModel):
    questionIndex: int
    selectedOption: int
    isCorrect: bool

gabarito = {
    1: "C",
    2: "A",
    3: "A",
    4: "B",
    5: "D",
    6: "C",
    7: "C",
    8: "B",
    9: "D"
}


topicos = {
    1: 'conceito',
    2: 'primeiros socorros',
    3: 'prevenção',
    4: 'riscos',
    5: 'primeiros socorros',
    6: 'riscos',
    7: 'primeiros socorros',
    8: 'Segurança em situações de emergência',
    9: 'Segurança em situações de emergência'
}



def option_to_letter(option: int) -> str:
    """Converte número da opção em letra."""
    return chr(65 + option)  # 0

def filterIncorrect(value):    
    valueL = list()
    for i in value:
        if not i.isCorrect: 
            valueL.append(i)
    return valueL

def filterCorrect(value):    
    valueL = list()
    for i in value:
        if i.isCorrect: 
            valueL.append(i)
    return valueL


@app.post("/api/score")
async def sugerVideo(listValue: List[Answer]):    
    asnswerValues = dict()
    errosSave = defaultdict(int)
   
    #sujestão de video
    for item in listValue:        
        numberQuestion = item.questionIndex + 1
        letterAnswer = option_to_letter(item.selectedOption)
        asnswerValues[numberQuestion] = letterAnswer
    for i, valor in asnswerValues.items():
        if valor != gabarito[i]:
            topico = topicos[i]
            errosSave[topico]+=1
    if len(errosSave)!=0:
        frequenciaErro = max(errosSave, key=errosSave.get)    
        return [frequenciaErro]
    else:
        return["0 Erros"]
