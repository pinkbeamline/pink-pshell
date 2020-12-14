try:
    for i in range(10):
        print(i)
        sleep(1)
except BaseException, errormsg:
    print("[Err]: " + str(errormsg) )

print("ok")