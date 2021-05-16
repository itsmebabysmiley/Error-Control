#!/usr/bin/env python3

# itsmebabysmiley | May 16,2021.
'''
    use only final examination.

'''


# ---------------------------------------
#              Parity bit
# ---------------------------------------


def parity_gen(dataword, word_size, parity_type, array_size):
    if word_size < 5: return 'word size should more than 5.'
    if parity_type == 'one-dimensional-odd':
        return parity_gen_1D(dataword, word_size, array_size, 'odd')
    elif parity_type == 'one-dimensional-even':
        return parity_gen_1D(dataword, word_size, array_size, 'even')
    elif parity_type == 'two-dimensional-even':
        return parity_gen_2D(dataword, word_size, array_size, 'even')
    elif parity_type == 'two-dimensional-odd':
        return parity_gen_2D(dataword, word_size, array_size, 'odd')


def parity_gen_1D(dataword, word_size, array_size, method):
    x = ['1', '0'] if method == 'odd' else ['0', '1']
    new_dataword = ''  # dataword with extra bit.
    for i in range(array_size):
        # if data bit is less than wordsize, then append bit 0 untill equal wordsize
        dataword[i] = dataword[i] if len(
            dataword[i]) - word_size == 0 else dataword[i].ljust(word_size, '0')
        # if method is odd, then add extra bit 1 if count bit 1 is even else add bit 0 for odd
        count_bit1 = dataword[i].count('1')
        dataword[i] += x[0] if count_bit1 % 2 == 0 else x[1]
        new_dataword += dataword[i] + ' '
    return new_dataword[:-1]  # remove extra 0 in the end.


def parity_gen_2D(dataword, word_size, array_size, method):
    if(array_size < 2): return 'size of array must bigger than 1'
    x = ['1', '0'] if method == 'odd' else ['0', '1']
    dataword = combine_string(dataword, word_size);
    rows = dataword.split(' ')  # spilt frame of data into array
    # rows that will append extra bit
    rows_addbit = parity_gen_1D(rows, word_size, array_size, method)
    p_b = ''  # extra row for parity bit
    # jump step[wordsize + 1 space between + 1 extra bit from row]
    jump = word_size+2;
    # check bit 1 at every column if method is odd and count bit 1 is even add bit 1 else add bit 0
    for i in range(0, len(rows[0])+1):
        column = ''
        for j in range(i, len(rows_addbit), jump):
            column += rows_addbit[j]
        p_b += x[0] if column.count('1') % 2 == 0 else x[1]

    return rows_addbit+' '+p_b[:-1]


def parity_check(codeword, parity_type, array_size):
    if parity_type == 'one-dimensional-odd':
        return parity_check_1D(codeword, 'odd')
    elif parity_type == 'one-dimensional-even':
        return parity_check_1D(codeword, 'even')
    elif parity_type == 'two-dimensional-even':
        return parity_check_2D(codeword, array_size, 'even')
    elif parity_type == 'two-dimensional-odd':
        return parity_check_2D(codeword, array_size, 'odd')


def parity_check_1D(codeword, method):
    x = 1 if method == 'odd' else 0
    for i in codeword:
        if i.count('1') % 2 != x:
#             print(f'codeword {i} error: true')
            return 0
    return 1


def parity_check_2D(codeword, array_size, method):
    x = 1 if method == 'odd' else 0
    word_size = len(codeword[0])
    rows_addbit = combine_string(codeword, word_size)
    # check row error without parity bit row
    if parity_check_1D(codeword[:-1], method) == 0:
        return 0
    # check column error
    jump = word_size + 1
    for i in range(len(codeword[0])):
        column = ''
        for j in range(i, len(rows_addbit), jump):
            column += rows_addbit[j]
        if column.count('1') % 2 != x:
            return 0

    return 1


def combine_string(codeword, word_size):
    new_codeword = ''
    for i in codeword:
        if len(i) - word_size == 0:
            new_codeword += i + ' '
        else:
            new_codeword += i.ljust(word_size, '0') + ' '
    return new_codeword[:-1]

# ---------------------------------------
#              Check sum
# ---------------------------------------


def checksum_gen(dataword, word_size, num_blocks):
    if word_size <= 4: return 'word size should more than 4'
    # if dataword is not equal to word size, then add 0 at first.
    dataword = [i.zfill(word_size) for i in dataword]
    copy_dataword = ' '.join(dataword)  # keep original for return
    # convert binary to decimal
    dataword = [int(dataword[i], 2) for i in range(num_blocks)]
    # find summation of dataword and covert back to binary
    summation = bin(sum(dataword))[2:]
    # find the extra bit
    size_extra_bit = len(summation) - word_size  # find the number of extra bit
    extra_bit = summation[:size_extra_bit].zfill(
        word_size)  # fill 0 until same length w/ word size
    summation = summation[size_extra_bit:]
#     print(summation+'\n'+extra_bit)
    # calculate checksum by summation+extra bit.(list of binary(charecter))
    checksum = list(
        str(bin(int(summation, 2)+int(extra_bit, 2))[2:]).zfill(word_size))
    # 1's complement
    checksum = [str(int(not int(i))) for i in checksum]

    return copy_dataword + ' '+''.join(checksum)


def checksum_check(codeword, word_size, num_blocks):
    # convert binary to decimal
    codeword = [int(codeword[i], 2) for i in range(num_blocks)]
    # find summation of codeword and covert back to binary
    summation = bin(sum(codeword))[2:]
    # find the extra bit
    size_extra_bit = len(summation) - word_size  # find the number of extra bit
    extra_bit = summation[:size_extra_bit].zfill(
        word_size)  # fill 0 until same length w/ word size
    summation = summation[size_extra_bit:]
#     print(summation+'\n'+extra_bit)
    # calculate checksum by summation+extra bit.(list of binary(charecter))
    checksum = list(
        str(bin(int(summation, 2)+int(extra_bit, 2))[2:]).zfill(word_size))
    # 1's complement
    checksum = [str(int(not int(i))) for i in checksum]
    # if there is no bit in checksum, then no error.
    return 1 if '1' not in checksum else 0


# ---------------------------------------
#                   CRC
# ---------------------------------------

def CRC_gen(dataword, wordsize, crc_type):
    if wordsize <= 4:
        return 'wordsize should more than 5'
    # if len(dataword) < len(crc_type):
    #     return 'length of dataword should more than crc-type'
    # if length dataword is less than wordsize.
    dataword = dataword.zfill(wordsize)
    n = len(crc_type)-1  # degree of G(x)
    # convert dataword to list and add extra bit by degree of gx
    message = list(dataword + ('0'*n))
    # generate crc from start of dataword until wordsize or no bit 1 in the dataword left.
    while '1' in message[:wordsize]:
        find_one = message.index('1')
#         if(find_one >= wordsize):
#             break
        # XOR between dataword and divisor
        for i in range(len(crc_type)):
            message[find_one +
                i] = str(int(message[find_one+i]) ^ int(crc_type[i]))

    # only {wordsize} bits are crc
    crc = ''.join(message[wordsize:])
#     print(f'dataword: {dataword} G(x): {crc_type}\ncodeword:',end=' ')
    return dataword+crc


def CRC_check(codeword, wordsize, crc_type):
    if wordsize < 5:
        return 'wordsize should more than 5'
    # if len(codeword) < len(crc_type):
    #     return 'length of mx should more than gx'
    n = len(crc_type)-1  # degree of G(x)

    # convert condword to list because string does not support item assignment.
    message = list(codeword)
    # size of real dataword(not includ crc bit)
    size_of_dataword = len(message) - n
    # generate crc from start of dataword until wordsize or no bit 1 in the dataword left.
    while '1' in message[:size_of_dataword]:
        find_one = message.index('1')
        # XOR between dataword and divisor
        for i in range(len(crc_type)):
            message[find_one +
                i] = str(int(message[find_one+i]) ^ int(crc_type[i]))
    # if remainder is 0, no error
    remainder = ''.join(message[size_of_dataword:])
#     print(f'codeword: {codeword} G(x): {crc_type}\nremainder:{remainder}',end=' ')
    return 1 if remainder.count('1') == 0 else 0
#     return remainder


# ---------------------------------------
#             Hamming code
# ---------------------------------------

def hamming_gen(dataword):
    size_dataword = len(dataword)
    dataword = list(dataword)
    dataword.reverse()
    # Calculate number of parity bit 2**p > size(dataword) + p + 1
    p = 0
    while 2**p < size_dataword + p + 1:
        dataword.insert(2**p-1, 'P')
        p += 1
#     print(dataword)
    # Calcuate parity bit and insert into Parity position.
    p_postion = 0
    for i in range(len(dataword)):
        # temporary string to store the parity for each parity bit.
        str_check_bit_1 = []
        # in every Parity position
        if dataword[i] == 'P':
            # start คือ bit เริ่มต้น
            # stop คือ bit สิ้นสุด
            start = (2**p_postion-1)
            stop = start + 2 ** p_postion
#             print('R',i+1,end=' ')
            while start < len(dataword):
#                 print(f'x[{start},{stop}]',end=' ')
                # extend datword with length of Parity bit Ex. P1: 1,3,5,7 P2:2,3,6,7,9,10
                str_check_bit_1.extend(dataword[start:stop])
                # Calculate new start stop position
                start += 2 ** p_postion + i + 1
                stop = start + 2**p_postion
#             print('\n')
            # Add Pairity bit in position.
            dataword[i] = '0' if str_check_bit_1.count('1') % 2 == 0 else '1'
            p_postion += 1  # move to next parity bit position.
        else:
            pass  # Baby style.
    dataword.reverse()
    return ''.join(dataword)


def hamming_check(codeword):
    from colored import fg, bg, attr
    size_codeword = len(codeword)
    codeword = list(codeword)
    codeword.reverse()
    p_position = []
    p = 0
    # Find postion of Parity bit
    while 2**p < size_codeword + p:
        p_position.append(2**p - 1)
        p += 1
    # print(codeword)
    p_postion = 0
    error_bit = ''
    for i in p_position:
        str_check_bit_1 = []
        start = (2**p_postion-1)
        stop = start + 2 ** p_postion
#         print('R',i+1,end=' ')
        while start < len(codeword):
#             print(f'x[{start},{stop}]',end=' ')
            str_check_bit_1.extend(codeword[start:stop])
            start += 2 ** p_postion + i + 1
            stop = start + 2**p_postion
#         print('\n')
        # print(str_check_bit_1)
        error_bit += '0' if str_check_bit_1.count('1') % 2 == 0 else '1'
        p_postion += 1
    error_dec = int(error_bit[::-1], 2)
    error_message = 'its me baby'
    if error_dec == 0:
        error_message = '%s%sError bit at position: None%s' % (
            fg("green"), attr("bold"), attr("reset"))
    else:
        color_bit = list(codeword)
        color_bit.reverse()
        before = ''.join(color_bit[:error_dec*-1])
        after = ''.join(color_bit[(error_dec*-1):])
        error_color = '%s%s%s%s%s%s%s' % (fg('green'), before, fg(
            'red'), after[0], fg("green"), after[1:], attr("reset"))
        error_message = '%s%sFound an error:        %s %s [position:%d]' % (
            fg('green'), attr("bold"), error_color, attr("bold"), error_dec)
        color_bit = list(codeword)
        color_bit.reverse()
        before = ''.join(color_bit[:error_dec*-1])
        after = ''.join(color_bit[(error_dec*-1):])
        curr = '1' if after[0] == '0' else '1'
        error_color = '%s%s%s%s%s%s%s' % (fg('green'), before, fg(
            'red'), curr, fg("green"), after[1:], attr("reset"))
        error_message += '\n%sLet me fix it:         %s%s%s' % (
            fg("green"), attr("bold"), error_color, attr("reset"))
    pfor = "%s[Output] : %s %s %s" % (
        fg("green"), fg("yellow"), error_message, attr("reset"))

    return print(pfor)


# ---------------------------------------
#         Unreliable tranmission
# ---------------------------------------

def unreliable_transmission(frame, prob, n):
    import random
    from colored import fg, bg, attr
    original_frame = frame
    count_error_bit = 0
    
    print('%s%sOriginal frame %s%s'%(fg("green"),attr("bold"),original_frame,attr("reset")))
    for i in range(n):
        frame = list(original_frame)
        for j in range(len(frame)):
            p = random.uniform(0, 1)
            
            # p more then prob then no bit error
            if p > prob:
                frame[j] = '%s%s%s'%(fg("red"),frame[j],attr("reset"))
                pass
            else:
                if frame[j] == '1':
                    frame[j] = '%s0%s'%(fg("red"),attr("reset"))
                else:
                    frame[j] = '%s1%s'%(fg("green"),attr("reset"))
                count_error_bit += 1

        print('%sSending bit.. ' %(fg("green")), ''.join(frame));
    print("** NOTE bit %s%sred%s is change bit"%(fg('red'),attr("bold"),attr("reset")))
    print("Total error bit occur: %s%d%s" %(fg("green"),count_error_bit,attr("reset")))
    print('Do not trust this method(seed kinda suck)')


def checkstring(dataword):
    from colored import fg, bg, attr
    import re
    for i in dataword:
        for j in i:
            if j != '0' and j != '1':
                return True
    return False


def main():

    import time
    from colored import fg, bg, attr
    type_func = {
        1: ("%s%sParity bit" % (fg("green"), attr("bold"))) + (" %s(Generator)" % (fg("red"))),
        2: ("%s%sParity bit" % (fg("green"), attr("bold"))) + (" %s(Checker)" % (fg("yellow"))),
        3: ("%s%sChecksum" % (fg("green"), attr("bold"))) + (" %s(Generator)" % (fg("red"))),
        4: ("%s%sChecksum" % (fg("green"), attr("bold"))) + (" %s(Checker)" % (fg("yellow"))),
        5: ("%s%sCRC" % (fg("green"), attr("bold"))) + (" %s(Generator)" % (fg("red"))),
        6: ("%s%sCRC" % (fg("green"), attr("bold"))) + (" %s(Checker)" % (fg("yellow"))),
        7: ("%s%sHamming code" % (fg("green"), attr("bold"))) + (" %s(Generator)" % (fg("red"))),
        8: ("%s%sHamming code" % (fg("green"), attr("bold"))) + (" %s(Checker)" % (fg("yellow"))),
        9: ("%s%sUnreliable transmission" % (fg("green"), attr("bold")))
    }
    welcome_message = " ______                        _____            _             _\n" +\
                      "|  ____|                      / ____|          | |           | |\n" +\
                      "| |__   _ __ _ __ ___  _ __  | |     ___  _ __ | |_ _ __ ___ | |\n" +\
                      "|  __| | '__| '__/ _ \| '__| | |    / _ \| '_ \| __| '__/ _ \| |\n" +\
                      "| |____| |  | | | (_) | |    | |___| (_) | | | | |_| | | (_) | |\n" +\
                      "|______|_|  |_|  \___/|_|     \_____\___/|_| |_|\__|_|  \___/|_|\n" +\
                      "\n                Created by John Doe :3 (v.0.1)                 "

    print("%s%s%s%s" % (fg("yellow"), attr("bold"), welcome_message, attr("reset")))
    print("%s----------------------------------------------------------------" %(fg('green')))
    time.sleep(1)
    print("%s%s        ctrl+c to exit       %s" %(fg("white"), bg("red"), attr("reset")))
    print("%s%sAvailable Function:" % (fg("green"), attr("bold")));
    for i in type_func:
        print('%s[%d] : %s' % (fg("green"), i, type_func[i]));
    print("%s%s        ctrl+c to exit       %s" %(fg("white"), bg("red"), attr("reset")))
    select_fun = int(input("%sSelect function: " % (fg("yellow"))))
    if select_fun not in type_func:
        print("%s%sInvalid input!%s" %(fg("red"), attr("bold"), attr("reset")))
    else:
        print('%s------- %s %s %s------- %s' % (fg("green"), attr("bold"),type_func[select_fun], fg("green"), attr("reset")))
        if select_fun in [1, 2]:
            print("%s%s[1] : 1D %s(Even) " %(fg("green"), attr("bold"), fg("red")));
            print("%s[2] : 1D %s(Odd)  " % (fg("green"), fg("yellow")));
            print("%s[3] : 2D %s(Even) " % (fg("green"), fg("red")));
            print("%s[4] : 2D %s(Odd)  " % (fg("green"), fg("yellow")));
            select_option = int(input("%sSelect type: " % (fg('yellow'))))
            parity_option = {
                1: "one-dimensional-even",
                2: "one-dimensional-odd",
                3: "two-dimensional-even",
                4: "two-dimensional-odd",
            }

            if select_option not in [1, 2, 3, 4]:
                print("%s%sInvalid input!%s" %(fg("red"), attr("bold"), attr("reset")))
            else:
                if select_fun == 1: size_dataword = int(input("%sInput size of dataword(>= 5): " % (fg("yellow"))))
                dataword = str(input("%sInput frame seperate by space( ): " % (fg("yellow"))))
                try:
                    dataword = dataword.split(' ')
                    if checkstring(dataword) == True:
                        return print("%s%sInvalid input!%s" % (fg("red"), attr("bold"), attr("reset")))

                    print("%s%s[Input]  : %s %s" % (fg("green"), attr("bold"), fg("yellow"), ' '.join(dataword)))
                    if select_fun == 1:
                        codeword = parity_gen(dataword, size_dataword, parity_option[select_option], len(dataword))
                        codeword = '%s%s' % (fg("yellow"), codeword)
                    else:
                        codeword = parity_check(dataword, parity_option[select_option], len(dataword))
                        codeword = '%sNo damage%s' % (fg("yellow"), attr("bold")) if codeword == 1 else '%sDamaged!%s' % (fg("yellow"), attr("bold"))
                    print("%s%s[Output] : %s %s %s" % (fg("green"), attr("bold"), fg("yellow"), codeword, attr("reset")))

                except:
                    return print("%s%sError !%s" % (fg("red"), attr("bold"), attr("reset")))
        elif select_fun in [3, 4]:
            size_dataword = int(input("%sInput size of dataword(>= 5): " % (fg("yellow"))))
            dataword = str(input("%sInput frame seperate by space( ): " % (fg("yellow"))))
            try:
                dataword = dataword.split(' ')
                if checkstring(dataword) == True:
                    return print("%s%sInvalid input!%s" % (fg("red"), attr("bold"), attr("reset")))

                print("%s%s[Input]  : %s %s" % (fg("green"), attr("bold"), fg("yellow"), ' '.join(dataword)))
                if select_fun == 3:
                    codeword = checksum_gen(dataword, size_dataword, len(dataword))
                    codeword = '%s%s' % (fg("yellow"), codeword)
                else:
                    codeword = checksum_check(dataword, size_dataword, len(dataword))
                    codeword = '%sNo damage%s' % (fg("yellow"), attr("bold")) if codeword == 1 else '%sDamaged!%s' % (fg("yellow"), attr("bold"))
                print("%s%s[Output] : %s %s %s" % (fg("green"), attr("bold"), fg("yellow"), codeword, attr("reset")))
            except:
                return print("%s%sError !%s" % (fg("red"), attr("bold"), attr("reset")))
        elif select_fun in [5, 6]:
            crc_dict = {
                "crc-32": "100000100110000010001110110110111",
                "crc-24": "1100000000101000100000001",
                "crc-16": "11000000000000101",
                "rcrc-16": "10100000000000011",
                "crc-8": "111010101",
                "crc-4": "11111"
            }
            size_dataword = int(input(("%sInput size of dataword(>= 5): " % (fg("yellow")))))
            dataword = str(input("%sInput data: " % (fg("yellow"))))

            try:
                if checkstring(dataword) == True:
                    return print("%s%sInvalid input!%s" % (fg("red"), attr("bold"), attr("reset")))
                count = 1;
                for i in crc_dict:
                    print('%s%s[%s] : (%s) %s' % (fg("green"),attr("bold"), count, i, crc_dict[i]))
                    count += 1
                
                print("%s[%s] : %sManually(Insert by yourself)" %(fg("green"), count, attr("bold")))
                select_crc = int(input("%sSelect divisor: %s" %(fg("yellow"), attr("reset"))))
                if select_crc not in [0, 1, 2, 3, 4, 5, 6, 7]: 
                    print("%s%sInvalid input!%s" % (fg("red"), attr("bold"), attr("reset")))
                if select_crc == 7:
                    crc = str(input("%sInput divisor: " %(fg("yellow"))))
                else:
                    crc_values=list(crc_dict.values())
                    crc=crc_values[select_crc-1]
                print("%s%s[Input]   : %s %s" %(fg("green"), attr("bold"), fg("yellow"), dataword))
                print("%s[Divisor] : %s %s" % (fg("green"), fg("yellow"), crc))
                if select_fun == 5:
                    codeword=CRC_gen(dataword, size_dataword, crc)
                    codeword='%s%s size[%d]' % (fg("yellow"), codeword, len(codeword))
                else:
                    codeword=CRC_check(dataword, size_dataword, crc)
                    codeword='%sNo damage%s' % (fg("yellow"), attr("bold")) if codeword == 1 else '%sDamaged!%s' % (fg("yellow"), attr("bold"))
                print("%s[Output]  : %s %s %s" %(fg("green"), fg("yellow"), codeword, attr("reset")))
            except :
                return print("%s%sError !%s" % (fg("red"), attr("bold"), attr("reset")))


        elif select_fun in [7, 8]:
            dataword=str(input("%sInput data: "%(fg("yellow"))))
            try:
                if checkstring(dataword) == True:
                    return print("%s%sInvalid input!%s" % (fg("red"), attr("bold"), attr("reset")))
                print("%s%s[Input]  : %s %s" %(fg("green"), attr("bold"), fg("yellow"), dataword))
                if select_fun == 7:
                    codeword=hamming_gen(dataword)
                    codeword='%s%s' % (fg("yellow"), codeword)
                    print("%s[Output] : %s %s %s" %(fg("green"), fg("yellow"), codeword, attr("reset")))
                else:
                    hamming_check(dataword)
            except:
                return print("%s%sError !%s" % (fg("red"), attr("bold"), attr("reset")))
        elif select_fun == 9:
            dataword=str(input("%sInput data: "%(fg("yellow"))))
            n = int(input("%sHow many time?: "%(fg("yellow"))))
            try:
                if checkstring(dataword) == True:
                    return print("%s%sInvalid input!%s" % (fg("red"), attr("bold"), attr("reset")))
                prob=float(input("%sInput probability(0.0-1.0):"%(fg("yellow"))))
                unreliable_transmission(dataword, prob, n)
            except:
                return print("%s%sError !%s" % (fg("red"), attr("bold"), attr("reset")))

# Driver code
if __name__ == '__main__':
	# install colored...
    try:
        from termcolor import colored
    except ImportError:
        import pip
        failed=pip.main(["install", 'colored'])
    from colored import fg, bg, attr
    while True:
        main()
        if str(input("%s%sContinue press [Enter] Exit press [q]: %s" %(fg("white"),bg("grey_46"),attr("reset")))) == ('q' or 'Q'):
            exit()
        
