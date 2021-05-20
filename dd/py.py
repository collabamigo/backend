lis = [['B20064', '5'], ['B20121', '5']]
for k in range(len(lis)):
    print(lis[k][0])
    km = {
        'fn':'heemank',
        'ln':'verma'
    }
    l = dict(km)
    lis[k][0] = km
    print(lis[k][0])