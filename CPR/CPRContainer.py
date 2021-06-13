from nameko.containers import ServiceContainer
from CPR.CPRService import CPRCalc

class CPRContain:
    name = "CPR Service"
    container = ServiceContainer(CPRCalc,config={'AMQP_URI': 'pyamqp://guest:guest@localhost'})
    service_extensions = list(container.extensions)

    container.start()

    container.stop()
