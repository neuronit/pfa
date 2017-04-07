
function modif(val) {
  var ava = document.getElementById("avancement");
  if((ava.value+val)<=ava.max && (ava.value+val)>0) {
     ava.value += val;
  }
  avancement();
}


