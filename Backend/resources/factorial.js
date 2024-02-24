function init() {
    print(factorial(5));
}
function factorial(x) {
    if (x == 0) {
        return 1;
    }
    return factorial(x - 1) * x;
}