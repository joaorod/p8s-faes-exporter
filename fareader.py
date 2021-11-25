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
    nao_elegiveis:int
    canceladas:int
    probabilidade_sucesso:float
    vlr_per_cand:float
    vlr_total:float
    cand_plafond : int
               



class FAReader:

    def read() -> FAValues:

        def text_from_cell(cell):
            return cell.text.replace("\n","").replace("\r","").strip()
            
        def value_from_cell(cell):
            return float(text_from_cell(cell))

        url = 'https://www.fundoambiental.pt/paes-ii/ponto-de-situacao-das-candidaturas-em-tempo-real.aspx'

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.findAll("table", {"class": "TabelaGeral"})[0]
        
        cells = soup.findAll("td", {"class": "Celula"})
        
        for i in range(len(cells)):
            print(i, ":'", text_from_cell(cells[i]),"'", sep='')
                
        # candidaturas:int            -> 1 OK
        # validadas:int = Submetidas - Em Analise
        # por_avaliar:int             -> 14
        # pagas:int                   -> 5:elegiveis, 17: pagas
        # valor_pago:float            -> 6 : valor elegivel, 18: valor pago
        # valor_remanescente:float    -> 3
        # nao_elegiveis:int           -> 8
        # canceladas:int              -> 11
        # probabilidade_sucesso:float 
        # vlr_per_cand:float          
        # vlr_total:float
        # cand_plafond : int
        values = FAValues(
            int(value_from_cell(cells[1]))
            ,0
            ,int(value_from_cell(cells[14]))
            ,int(value_from_cell(cells[5]))
            ,value_from_cell(cells[6]) 
            ,value_from_cell(cells[3])
            ,int(value_from_cell(cells[8]))
            ,int(value_from_cell(cells[11]))
            ,0,0,0,0
            )



        values.validadas = values.candidaturas - values.por_avaliar;

        # Prever o no de candidaturas dentro do plafond
        values.probabilidade_sucesso = float(values.pagas)/(float(values.validadas)-float(values.canceladas))
        values.vlr_per_cand = values.valor_pago/values.pagas
        values.vlr_total = values.valor_pago+values.valor_remanescente
        values.cand_plafond = int(values.vlr_total/values.vlr_per_cand/values.probabilidade_sucesso)


        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), " candidaturas:",values.candidaturas,"validadas:",values.validadas,"por_avaliar:",values.por_avaliar,"pagas/elegiveis:",values.pagas,"valor pago:",values.valor_pago, "valor remanescente:",values.valor_remanescente, "nao elegiveis:", values.nao_elegiveis, "canceladas:",values.canceladas, "prob_suc:",values.probabilidade_sucesso, "vlr_per_cand:",values.vlr_per_cand,"vlr_total:",values.vlr_total,"candidaturas no plafond:", values.cand_plafond)

        return values

    def read_old() -> FAValues:

        def value_from_cell(cell):
            return float(cell.text.replace("\n","").replace("\r","").replace(" ",""))

        url = 'https://www.fundoambiental.pt/apoios-prr/paes-2021.aspx'

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.findAll("table", {"class": "TabelaGeral"})[0]
        
        cells = soup.findAll("td", {"class": "Celula"})

        values = FAValues(int(value_from_cell(cells[1])),0,int(value_from_cell(cells[15])),int(value_from_cell(cells[6])),value_from_cell(cells[7]),value_from_cell(cells[3]),int(value_from_cell(cells[9])),int(value_from_cell(cells[12])),0,0,0,0)



        values.validadas = values.candidaturas - values.por_avaliar;

        # Prever o no de candidaturas dentro do plafond
        values.probabilidade_sucesso = float(values.pagas)/(float(values.validadas)-float(values.canceladas))
        values.vlr_per_cand = values.valor_pago/values.pagas
        values.vlr_total = values.valor_pago+values.valor_remanescente
        values.cand_plafond = int(values.vlr_total/values.vlr_per_cand/values.probabilidade_sucesso)


        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), " candidaturas:",values.candidaturas,"validadas:",values.validadas,"por_avaliar:",values.por_avaliar,"pagas/elegiveis:",values.pagas,"valor pago:",values.valor_pago, "valor remanescente:",values.valor_remanescente, "nao elegiveis:", values.nao_elegiveis, "canceladas:",values.canceladas, "prob_suc:",values.probabilidade_sucesso, "vlr_per_cand:",values.vlr_per_cand,"vlr_total:",values.vlr_total,"candidaturas no plafond:", values.cand_plafond)

        return values
