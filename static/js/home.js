function onCreate() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
     var data = JSON.parse(this.responseText);
     var token = data.token
     var room_id = data.room_id
     localStorage.setItem("token"+room_id,token);
     localStorage.setItem("game_room_id",room_id);
     window.location.href = "/ui/games/" + data.room_id
     }
  };
  xhttp.open("POST", "/games", true);
  xhttp.send();
}

function OnJoin() {
    var textcontrol = document.getElementById("txtname");
    var room_id = textcontrol.value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {

        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            var token = data.token
            var room_id = data.room_id
            localStorage.setItem("token"+room_id,token);
            localStorage.setItem("game_room_id",room_id);
            window.location.href = "/ui/games/" + room_id
        }else if (this.readyState == 4 && this.status == 404) {
            textcontrol.value = ' ';
            document.getElementById("demo").innerHTML = "No such room exists";
        }
    };
    xhttp.open("POST", "/games/"+room_id+"/join", true);
    xhttp.send();
}
