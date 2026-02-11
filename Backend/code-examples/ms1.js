function start(){
    global let [20][20] board;
    global let [8] xx, yy;
    global let bombs = 30;
    xx[0]=0;xx[1]=0;xx[2]=1;xx[3]= -1;xx[4]=1;xx[5]=1;xx[6]= -1;xx[7]= -1;
    yy[0]=1;yy[1]= -1;yy[2]=0;yy[3]=0;yy[4]=1;yy[5]= -1;yy[6]=1;yy[7]= -1;
    initBoard();
    generateBombs(bombs);
}
function initBoard(){
    for(let i=0;i<20;i=i+1){
        for(let j=0;j<20;j=j+1){
            board[i][j] = 0;
        }
    }
}
function generateBombs(nr){
    while(nr>0){
        let x=random(0,19);
        let y=random(0,19);
        if(board[x][y] == 0){
            board[x][y]= -1;
            nr=nr-1;
        }
    }
}
function insideBoard(x,y){
    if(x<0 or y<0 or x==20 or y==20){
        return 0;
    }
    return 1;
}
function getAdjacentBombsNr(x,y){
    let nr=0;
    for(let i=0;i<8;i=i+1){
        if(insideBoard(x+xx[i],y+yy[i]) == 1){
            if(board[x+xx[i]][y+yy[i]] == -1){
                nr = nr+1;
            }
        }
    }
    return nr;
}
function rightClickCell(i,j){
    setCell(i,j, -1);
}
function checkBombs(x,y){
    let [500] qx,qy;
    qx[0]=x;qy[0]=y;
    let p=0,u=1;
    while(p<u){
        x=qx[p];
        y=qy[p];
        let adjBombs = getAdjacentBombsNr(x,y);
        setCell(x,y,adjBombs);
        board[x][y] = -2;
        
        if(adjBombs == 0){
        for(let i=0;i<8;i=i+1){
            if(insideBoard(x+xx[i],y+yy[i]) == 1){
                if(board[x+xx[i]][y+yy[i]] == 0){
                    checkBombs(x+xx[i],y+yy[i]);
                }
            }
        }
    }
        p=p+1;
    }
}
function leftClickCell(i,j){
    checkBombs(i,j);
}