import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from fareader import FAReader


class FACollector(object):
    callsCount=0
    failsCount=0
    startTime = 0
    def __init__(self):
        self.startTime = time.time()
        pass

    def collect(self):
        try:
            values = FAReader.read()
            
            self.callsCount+=1
            
            ccalls = CounterMetricFamily("Calls", 'Numero de Chamadas', labels=['status'])
            ccalls.add_metric(['success'],self.callsCount)
            ccalls.add_metric(['fail'],self.failsCount)

            yield ccalls

            ctime = CounterMetricFamily("Runtime", 'Runtime', labels=['id'])
            ctime.add_metric(['default'],time.time()-self.startTime)

            yield ctime

            gcand = GaugeMetricFamily("Candidaturas", 'Numero de Candidaturas', labels=['state'])
            gcand.add_metric(['total'],values.candidaturas)
            gcand.add_metric(['validadas'],values.validadas)
            gcand.add_metric(['por_validar'],values.por_avaliar)
            gcand.add_metric(['pagas'],values.pagas)
            gcand.add_metric(['nao_elegiveis'],values.nao_elegiveis)
            gcand.add_metric(['canceladas'],values.canceladas)

            gcand.add_metric(['dentro_plafond'],values.cand_plafond)
            gcand.add_metric(['minha'],25503)

            
            
            yield gcand
            
            gval = GaugeMetricFamily("Valores", 'Valores', labels=['state'])
            gval.add_metric(['total'],values.vlr_total)
            gval.add_metric(['pago'],values.valor_pago)
            gval.add_metric(['remanescente'],values.valor_remanescente)
            gval.add_metric(['valor_por_candidatura'],values.vlr_per_cand)

            gval.add_metric(['probab_sucesso'],values.probabilidade_sucesso)
            
            
            yield gval
        except Exception as e:
            print("Something went wrong:", e)
            self.failsCount+=1
        
if __name__ == '__main__':
    start_http_server(9011)
    REGISTRY.register(FACollector())
    
    while True:
        time.sleep(1)
