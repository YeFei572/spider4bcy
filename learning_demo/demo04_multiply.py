i = 1
while i < 100:
    j = 1
    while j <= i:
        content = f"{j} x {i} = {i*j}"
        j += 1
        print(content, end="\t")
    print()
    i += 1
