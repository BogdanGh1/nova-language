function start() {
    print(factorial(10));
}
function factorial(x) {
    if (x == 0) {
        return 1;
    }
    return factorial(x - 1) * x;
}