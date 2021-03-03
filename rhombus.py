def rhombus_1(l):
    " 적당한 마름모 "

    i=0
    while i < l:
        print(" "*(l-i-1)+"*"+" "*(i*2-1)+(i!=0)*"*")
        i = i + 1
    
    i = i - 2
    
    while i >= 0:
        print(" "*(l-i-1)+"*"+" "*(i*2-1)+(i!=0)*"*")
        i = i - 1

def rhombus_2(l):
    " 숏코딩한 마름모 "

    d=[" "*(l-x-1)+"*"+" "*(x*2-1)+"*"*(x!=0) for x in range(l)]
    print("\n".join(d));d.reverse();print("\n".join(d[1:]))


if __name__ == "__main__":
    print("일반 :")
    rhombus_1(6)

    print("숏코딩 한거 :")
    rhombus_2(6)

    ''' 대충 이런 모양
         *
        * *
       *   *
      *     *
     *       *
    *         *
     *       *
      *     *
       *   *
        * *
         *
    '''
