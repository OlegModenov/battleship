class Test:
    var1 = 5

    def __init__(self, var):
        self.var = var


test = Test(6)

print(test.__dict__)
print(test.var)
print(test.var1)