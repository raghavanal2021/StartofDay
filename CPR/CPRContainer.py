from nameko.containers import ServiceContainer
from CPRService import CPRCalc


container = ServiceContainer(CPRCalc,config={'AMQP_URI': 'pyamqp://guest:guest@localhost'})
service_extensions = list(container.extensions)

container.start()

container.stop()
