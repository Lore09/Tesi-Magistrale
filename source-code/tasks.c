@Task
@LibDeps("stdio.h","stdlib.h")
float get_average_rand(float values[]){
    return 5;
}

@ModuleName("Tattitto")
@TaskCloud
@LibDeps("math.h")
int is_even(int number){
    if(number%2==0)return 1;
    else return 0;
}

@LibDeps("stdio.h","string.h")
@TaskDevice
void printaaaa(String text){
    printf("aaaa %s\n",text);
}