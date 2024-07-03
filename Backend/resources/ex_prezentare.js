function start() {
    global let n = random(4,10);
    if(n%2 == 0){
        print(factorial(15));
    }
    else{
        printSum();
    }
}
function factorial(x) {
    if (x == 0) {
        return 1;
    }
    return factorial(x - 1) * x;
}
function suma(){
    let s=0;
    for(let i=1;i<=n;i=i+1){
        s=s+i;
    }
    print(s);
}