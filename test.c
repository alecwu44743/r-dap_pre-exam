#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(){
    char input_code[100] = "";
    char compressed_code[8][4] = {
        "000", "001", "010", "011", "100", "101", "110", "111"
    };
    //    7      6      5      4      3      2      1      0    -->  length
    //    0      1      2      3      4      5      6      7    -->  index

    while(scanf("%s", input_code) != EOF){
        char s;
        char out[12] = "";
        int length = 0;

        s = (char)(1 ^ (input_code[0] - '0') + '0');
        for(int i=1; i<8; i++){
            if(input_code[i]-'0' == 0){
                length++;
                continue;
            }

            break;
        }
        // printf("%d\n", length);

        strncat(out, &s, 1);
        strcat(out, compressed_code[7-length]);
        strncat(out, input_code+1+length+1, 4);

        printf("%s\n", out);

        int flag = 1;
        for(int i=strlen(out)-1; i>0; i--){
            if(flag){
                out[i] = (char)(1 ^ (out[i] - '0') + '0');
                flag = 0;
                continue;
            }
            flag = 1;
        }

        printf("%s\n", out);
        
    }    
}

// test : 0 0001 10010001010     0000110010001010
// out  : 1 001 1100
//        1 101 1100