function init() {
    setScoreX(0);
    setScoreO(0);
    global let player;
    player = "X";
}

function clickCell(i) {
    setCell(i, player);
    if (player == "X") {
        player = "O";
    }
    if (player == "O") {
        player = "X";
    }
}
function checkWinner() {
    if (board[0] == board[1] && board[1] == board[2]) {
        if (board[0] == "X") {
            setScoreX(scoreX + 1);
            reset();
        }
        if (board[0] == "O") {
            setScoreO(scoreO + 1);
            reset();
        }
    }
}
function reset() {
    let i = 0;
    while (i < 9) {
        setCell(i, "");
        i = i + 1;
    }
}