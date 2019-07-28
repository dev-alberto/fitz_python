import zerorpc


class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name

    def type_check(self, tt):
        print(type(tt))
        print(tt)
        return tt

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()