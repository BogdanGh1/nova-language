function start() {
    let a = 100, b = 20;
    while (a > b or a < b) {
        if (a > b) {
            a = a - b;
        } else {
            b = b - a;
        }
    }
    print(a);
}