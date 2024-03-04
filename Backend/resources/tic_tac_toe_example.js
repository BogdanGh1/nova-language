function start() {
    setScoreX(0);
    setScoreO(0);
    global let player = "X";
    global let [8][3] winComb;
    winComb[0][0] = 0; winComb[0][1] = 1; winComb[0][2] = 2;
    winComb[1][0] = 3; winComb[1][1] = 4; winComb[1][2] = 5;
    winComb[2][0] = 6; winComb[2][1] = 7; winComb[2][2] = 8;
    winComb[3][0] = 0; winComb[3][1] = 3; winComb[3][2] = 6;
    winComb[4][0] = 1; winComb[4][1] = 4; winComb[4][2] = 7;
    winComb[5][0] = 2; winComb[5][1] = 5; winComb[5][2] = 8;
    winComb[6][0] = 0; winComb[6][1] = 4; winComb[6][2] = 8;
    winComb[7][0] = 2; winComb[7][1] = 4; winComb[7][2] = 6;
}

function clickCell(i) {
    setCell(i, player);
    checkWinner();
    if (player == "X") {
        player = "O";
        return;
    }
    if (player == "O") {
        player = "X";
        return;
    }
}
function checkWinner() {
    print("check");
    for (let i = 0; i < 8; i = i + 1) {
        if (board[winComb[i][0]] == board[winComb[i][1]] and board[winComb[i][1]] == board[winComb[i][2]]) {
            if (board[winComb[i][0]] == "X") {
                setScoreX(scoreX + 1);
                reset();
                return;
            }
            if (board[winComb[i][0]] == "O") {
                setScoreO(scoreO + 1);
                reset();
                return;
            }
        }
    }
    let nr = 0;
    for (let i = 0; i < 9; i = i + 1) {
        if (board[i] == "X" or board[i] == "O") {
            nr = nr + 1;
        }
    }
    if (nr == 9) {
        reset();
    }
}
function reset() {
    for (let i = 0; i < 9; i = i + 1) {
        setCell(i, "");
    }
    player = "X";
}