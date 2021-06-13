from nameko.runners import ServiceRunner
from nameko.testing.utils import get_container
from CPR.CPRService import CPRCalc
from Patterns.NarrowRangeService import NarrowRangeService
from Patterns.PricePatternService import PricePattern

runner = ServiceRunner(config={'AMQP_URI': 'pyamqp://guest:guest@localhost'})
runner.add_service(CPRCalc)
runner.add_service(NarrowRangeService)
runner.add_service(PricePattern)

runner.start()
runner.stop()



