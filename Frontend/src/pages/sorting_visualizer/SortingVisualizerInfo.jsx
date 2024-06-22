import "../modal.css";
function SortingVisualizerInfo({ modal, setModal }) {
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
            <h2>Tic-Tac-Toe</h2>
            <p>
              Your goal in this level is to implement the logic of the popular game Tic-Tac-Toe. 
              You can either make it singleplayer, playing against an AI designed by you or multyplayer.&nbsp;
              <b>The freedom is yours.</b>
            </p>
            <p>
              Here are the functions and variables that you need to interact with the game:
            </p>
            <p>
              <b>setScoreX(value)</b>: used to set the score for X based on <b>value</b>
            </p>
            <p>
              <b>scoreX</b>: variable that keeps the score for X
            </p>
            <p>
              <b>setScoreO(value)</b>: used to set the score for O based on <b>value</b>
            </p>
            <p>
              <b>scoreO</b>: variable that keeps the score for O
            </p>
            <p>
              <b>setCell(i,value)</b>: used to set the content of the cell with index <b>i</b> with <b>value</b>
            </p>
            <p>
              <b>board[i]</b>: array that holds the content of the cell at index <b>i</b>
            </p>
            <p>
              <b>clickCell(i)</b>: you need to implement this function, it will be called whenever the player clicks on a cell. 
              The index of the clicked cell will be passed inside the variable <b>i</b>
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

export default SortingVisualizerInfo;
