function start() {
    global let n = random(5, 15);
    if (n < 10) {
        print(factorial(n));
    } else {
        printSum();
    }
}

function factorial(x) {
    if (x == 0) {
        return 1;
    }
    return factorial(x - 1) * x;
}

function printSum() {
    let s = 0;
    for (let i = 1; i <= n; i = i + 1) {
        s = s + i;
    }
    print(s);
}
