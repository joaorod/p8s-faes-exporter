import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FAValues:
    candidaturas:int
    validadas:int
    por_avaliar:int
    pagas:int
    valor_pago:float
    valor_remanescente:float

class FAReader:

    def read() -> FAValues:

        def value_from_cell(cell):
            return float(cell.text.replace("\n","").replace("\r",""))

        url = 'https://www.fundoambiental.pt/avisos-2020/mitigacao-das-alteracoes-climaticas/programa-de-apoio-a-edificios-mais-sustentaveis/quadro-edificios-2020.aspx'

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        cells = soup.findAll("td", {"class": "Celula"})

        values = FAValues(int(value_from_cell(cells[0])),int(value_from_cell(cells[1])),int(value_from_cell(cells[2])),int(value_from_cell(cells[3])),value_from_cell(cells[4]),value_from_cell(cells[5]))

        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), " candidaturas:",values.candidaturas,"validadas:",values.validadas,"por_avaliar:",values.por_avaliar,"pagas:",values.pagas,"valor pago:",values.valor_pago, "valor remanescente:",values.valor_remanescente)

        return values