function init() {
    let s = 0;
    for (let i = 1; i <= 10; i = i + 1) {
        for (let j = 1; j <= 10; j = j + 1) {
            s = s + 100;
        }
    }
    print(s);
}