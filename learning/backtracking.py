def bit_str_gen(count, str):
    print "count = : ",count
    if count == 1:
        return str
    # data = [digit + bits for digit in bit_str_gen(1,str) for bits in bit_str_gen(count -
    #                                                                    1,str)]
    data1 = []
    for digit in bit_str_gen(1, str):
        for bits in bit_str_gen(count - 1, str):
            data1.append(digit+bits)


    # print data
    print "data1 : ",data1
    return data1


print bit_str_gen(4, 'xyz')