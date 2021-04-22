var retrievedObject = localStorage.getItem('token')
var room_id = localStorage.getItem("game_room_id");
var SUCCESS = "SUCCESS";
var FAILURE = "FAILURE";
var DRAW = "DRAW";
var popupShown = false;
function closeModal() {
  const modal = document.getElementById("myModal");
  const modalIcon = document.getElementById("modal-icon")
  const modalText = document.getElementById("modal-text")
  modal.style.display = "none";
  modalIcon.classList.remove( "fa-jedi-order", "fa-galactic-senate","fa-galactic-republic","fa-jedi","fa-journal-whills","fa-frown-open")
  modalText.innerHTML = ''
}
window.onclick = function(event) {
  const modal = document.getElementById("myModal");
  const modalIcon = document.getElementById("modal-icon")
  const modalText = document.getElementById("modal-text")
  if (event.target == modal) {
    modal.style.display = "none";
    modalIcon.classList.remove( "fa-jedi-order", "fa-galactic-senate","fa-galactic-republic","fa-jedi","fa-journal-whills","fa-frown-open")
    modalText.innerHTML = ''
  }
}
function onPlay(value) {
    var payload = {'cell': value};
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            render(this.responseText);
        }
    };
    xmlhttp.open("POST","/games/"+room_id+"/play", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.setRequestHeader('Authorization',"Bearer "+ localStorage.getItem("token"+room_id));
    xmlhttp.send(JSON.stringify(payload));
}

function onReset(value) {
  alert(value)
  popupShown = false
}

function onRelinquish(value) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            render(this.responseText);
            popupShown = false
        }
    };
    xmlhttp.open("POST","/games/"+room_id+"/relinquish-first-turn", true);
    xmlhttp.setRequestHeader('Authorization',"Bearer "+ localStorage.getItem("token"+room_id));
    xmlhttp.send();
}

function onReset(value) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            render(this.responseText);
            popupShown = false
        }
    };
    xmlhttp.open("POST","/games/"+room_id+"/reset", true);
    xmlhttp.setRequestHeader('Authorization',"Bearer "+ localStorage.getItem("token"+room_id));
    xmlhttp.send();
    const boardElement= document.getElementById("board");
    boardElement.classList.remove('disabled')
}

function onHome() {
    location.replace("/")
    popupShown = false
}

function convert(x, id ) {
    const cellElement = document.getElementById(id)
    if(x == '0' || x == 0){
        cellElement.innerHTML = ' '
        cellElement.classList.remove('disabled')
        return;
    }else {
        cellElement.innerHTML = x
        cellElement.classList.add('disabled')
        return;
    }
}

function render(response){
    var myObj = JSON.parse(response);
    convert(myObj.board[0][0],"a");
    convert(myObj.board[0][1],"b");
    convert(myObj.board[0][2],"c");
    convert(myObj.board[1][0],"d");
    convert(myObj.board[1][1],"e");
    convert(myObj.board[1][2],"f");
    convert(myObj.board[2][0],"g");
    convert(myObj.board[2][1],"h");
    convert(myObj.board[2][2],"i");
    var message = "";

    const boardElement= document.getElementById("board");
    if(myObj.is_draw){
        message = "The game is draw";
        boardElement.classList.add('disabled')
        generateGreetings(DRAW);
    }else if(myObj.who_won != null){
        message = myObj.who_won+" won the game";
        boardElement.classList.add('disabled')
        if(myObj.who_won == myObj.id){
            generateGreetings(SUCCESS);
        }else {
            generateGreetings(FAILURE);
        }
    }else{
        message = myObj.player_to_play + "'s turn to play";
        if(myObj.player_to_play != myObj.id){
            boardElement.classList.add('disabled')
        }else {
            boardElement.classList.remove('disabled')
        }
    }

    document.getElementById("message").innerHTML = message;
    document.getElementById("id").innerHTML = "You are "+myObj.id;

}


function refresh() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            render(this.responseText);
            popupShown = false
        }
    };
    xmlhttp.open("GET","/games/"+room_id, true);
    xmlhttp.setRequestHeader('Authorization',"Bearer "+ localStorage.getItem("token"+room_id));
    xmlhttp.send();
}

function onLoad() {
    refresh();
    setInterval(function(){ refresh(); }, 1500);
}

function generateGreetings(popupType){
 if(!popupShown){
    if(popupType == SUCCESS){
            showSuccessPopup();
        }else if (popupType == FAILURE){
            showFailurePopup();
        }else{
            showDrawPopup();
        }
    popupShown = true
 }
}

function showSuccessPopup(){

  const modal = document.getElementById("myModal");
  const modalIcon = document.getElementById("modal-icon")
  const modalText = document.getElementById("modal-text")
    const badgeIcons = ["fa-thumbs-up","fa-galactic-senate","fa-jedi"]
    const greetText = ["May The force be with you!","You are a gifted battlefield tactician, Stazi!","There is no such thing as luck, Jedi!"]

    const randomIndex = Math.floor(Math.random() * 3)
    modalIcon.classList.add(badgeIcons[randomIndex])
    modalText.innerHTML = greetText[randomIndex]
    modal.style.display = "block";
}

function showFailurePopup(){

  const modal = document.getElementById("myModal");
  const modalIcon = document.getElementById("modal-icon")
  const modalText = document.getElementById("modal-text")
    const badgeIcons = ["fa-sad-tear"]
    const greetText = ["Sorry! You Lost!"]
    modalIcon.classList.add(badgeIcons[0])
    modalText.innerHTML = greetText[0]
    modal.style.display = "block";
}

function showDrawPopup(){
  const modal = document.getElementById("myModal");
  const modalIcon = document.getElementById("modal-icon")
  const modalText = document.getElementById("modal-text")
    const badgeIcons = ["fa-journal-whills"]
    const greetText = ["Draw! Note to not repeat it!"]
    modalIcon.classList.add(badgeIcons[0])
    modalText.innerHTML = greetText[0]
    modal.style.display = "block";
}