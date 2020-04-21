from utils.decorators import timeit
import time
class Test:

    @timeit
    def test(self,var):
        time.sleep(2)
        return var*2

x =Test()
y = x.test(2)
print(y)