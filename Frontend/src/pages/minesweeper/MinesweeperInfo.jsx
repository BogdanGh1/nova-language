import "../modal.css";
function MinesweeperInfo({ modal, setModal }) {
  const toggleModal = () => {
    setModal(!modal);
  };

  if (modal) {
    document.body.classList.add("active-modal");
  } else {
    document.body.classList.remove("active-modal");
  }

  return (
    <>
      {modal && (
        <div className="modal">
          <div onClick={toggleModal} className="overlay"></div>
          <div className="modal-content">
            <h2>Minesweeper</h2>
            <p>
              Your goal in this level is to implement the logic of the popular game Minesweeper. 
            </p>
            <p>
              <b>setCell(i,j,value)</b>: used to set the content of the cell with indexes <b>i</b> and <b>j</b> with <b>value</b>
            </p>
            <p>
              <b>board[i][j]</b>: matrix that holds the content of the cell at index <b>i</b>  and <b>j</b>
            </p>
            <p>
              <b>rightClickCell(i,j)</b>: you need to implement this function, it will be called whenever the player right-clicks on a cell. 
              The indexes of the clicked cell will be passed inside the variables <b>i</b> and <b>j</b>
            </p>
            <p>
              <b>leftClickCell(i,j)</b>: you need to implement this function, it will be called whenever the player left-clicks on a cell. 
              The indexes of the clicked cell will be passed inside the variables <b>i</b> and <b>j</b>
            </p>

            <button className="close-modal" onClick={toggleModal}>
              CLOSE
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default MinesweeperInfo;
