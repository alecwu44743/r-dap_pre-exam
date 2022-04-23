#include <stdio.h>
#include <stdlib.h>

#define QUANT_MASK 0xf
#define SEG_SHIFT  4

static int seg_aend[8] = {
                            0x1F, 0x3F, 0x7F, 0xFF,
                            0x1FF, 0x3FF, 0x7FF, 0xFFF
                         };

int find_aend(int data, int *table, int n){
    int i;
    for(i = 0; i < n; i++){
        if(data <= *table++){
            return i;
        }
    }
    return n;
}

int linear_to_alaw(int val){
    int mask;
    int seg;
    int aval;

    val = val >> 3;

    if(val >= 0){
        mask = 0xD5;
    }
    else{
        mask = 0x55;
        val = -val - 1;
    }

    seg = find_aend(val, seg_aend, 8);

    if(seg >= 8){
        return (0x7F ^ mask);
    }
    else{
        aval = seg << SEG_SHIFT;

        if(seg < 2){
            aval |= (val >> 1) & QUANT_MASK;
        }
        else{
            aval |= (val >> seg) & QUANT_MASK;
        }
        return (aval ^ mask);
    }
}

int main(){
    int test;

    while(scanf("%d", &test) != EOF){
        printf("%d\n", linear_to_alaw(test));
    }
}