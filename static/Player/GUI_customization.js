
// Onload CSS changes to override external stylesheets
function CSSoverrides() {
  document.documentElement.style.backgroundColor = "#121212"
}


// Fullscreen Mode
var tempSelected;
var tempBgSrc;
function fullScreenVid() {
  // case 1: if already in fullscreen mode
  if ( videoList[0].style.display == "none" && videoList[1].style.display == "none" && videoList[2].style.display == "none" ) {
    videoList[3].src = tempBgSrc
    selectedVid = tempSelected
  }
  // case 2: enter fullscreen mode, set temp values to return to original state later
  else {
  tempBgSrc = videoList[3].src;
  tempSelected = selectedVid;
  videoList[3].src = videoList[selectedVid].src;
  selectedVid = 3;
  for (q=0;q<3;q++) {
    if ( videoList[q].paused != true ) {
      videoList[q].pause()
    } }
  }
  toggleBgVid();
  hideAll();
}


// Toggle display of background video
function toggleBgVid() {
  if ( document.getElementsByClassName("bgVid")[0].style.display == "block" ) {
    document.getElementsByClassName("bgVid")[0].style.display = "none";
    document.getElementsByClassName("bgVid")[1].style.display = "none"
    }
  else {
    document.getElementsByClassName("bgVid")[0].style.display = "block";
    document.getElementsByClassName("bgVid")[1].style.display = "block"
    }
}


function changeToggle() {
  if ( toggle == "on" ) { document.getElementById('togTxt').innerHTML = "All" }
  if ( toggle == "off" ) {
    v = (selectedVid + 1).toString()
    document.getElementById('togTxt').innerHTML = v }
}


function newContrast () {
  document.getElementById("dirList").style.color = "#de1243"
  document.getElementById("dirList").style.backgroundColor = "#eaffca"
  document.getElementById("dirList").style.opacity = ".6" }


function showCaptions() {
  captions = document.getElementsByClassName("overlay")
  for ( const e of captions ) {
    e.style.display = "block"
  }
}


function backToOG () {
  document.getElementById("dirList").style.color = "#FFFFFF"
  document.getElementById("dirList").style.backgroundColor = "#181818"
  document.getElementById("dirList").style.opacity = "1"
  document.body.style.background = "unset"
  document.body.style.backgroundColor = "#121212"
  document.body.style.minHeight = "unset"
  gifPosRight = 0; gifPosBot = 0; gifPosTop = 0; gifPosLeft = 0; }


function hideAll() {
  if ($('#directory').css('display') == "none") {
    $('#directory').css('display','block') }
  else { $('#directory').css('display','none') }
  if ($('#togTxt').css('display') == "none") {
    $('#togTxt').css('display','block') }
  else { $('#togTxt').css('display','none') }
  if ($('#mainVid1').css('display') == "none") {
    $('#mainVid1').css('display','block') }
  else { $('#mainVid1').css('display','none') }
  if ($('#sideBar').css('display') == "none") {
    $('#sideBar').css('display','block') }
  else { $('#sideBar').css('display','none') }
  if ($('#rowvid1').css('display') == "none") {
    $('#rowvid1').css('display','block')
    $('#rowvid2').css('display','block') }
  else { $('#rowvid1').css('display','none');
  $('#rowvid2').css('display','none') }
  if ($('#btn1').css('display') == "none") {
    $('#btn1').css('display','block') }
  else { $('#btn1').css('display','none') }
  if ($('#btn2').css('display') == "none") {
    $('#btn2').css('display','block') }
  else { $('#btn2').css('display','none') }
  if ($('#btn3').css('display') == "none") {
    $('#btn3').css('display','block') }
  else { $('#btn3').css('display','none') }
  if ($('#btn4').css('display') == "none") {
    $('#btn4').css('display','block') }
  else { $('#btn4').css('display','none') }
}


function directoryBtn(element) {
  element.classList.toggle('open');
  if ($('#directory').css('display') == "none") {
    $('#directory').css('display','block') }
  else { $('#directory').css('display','none') }
  if ($('#togTxt').css('display') == "none") {
    $('#togTxt').css('display','block') }
  else { $('#togTxt').css('display','none') }
  if ($('#toggleBtn').css('display') == "none") {
    $('#toggleBtn').css('display','block') }
  else { $('#toggleBtn').css('display','none') }
};


function directoryBtn1(element) {
  element.classList.toggle('open');
  if ($('#mainVid1').css('display') == "none") {
    $('#mainVid1').css('display','block') }
  else { $('#mainVid1').css('display','none') }
  if ($('#togTxt').css('display') == "none") {
    $('#togTxt').css('display','block') }
  else { $('#togTxt').css('display','none') }
  if ($('#toggleBtn').css('display') == "none") {
    $('#toggleBtn').css('display','block') }
  else { $('#toggleBtn').css('display','none') }
};


function directoryBtn3(element) {
  element.classList.toggle('open');
  if ($('#sideBar').css('display') == "none") {
    $('#sideBar').css('display','block') }
  else { $('#sideBar').css('display','none') }
};


function directoryBtn4(element) {
  element.classList.toggle('open');
  if ($('#rowvid1').css('display') == "none") {
    $('#rowvid1').css('display','block')
    $('#rowvid2').css('display','block') }
  else { $('#rowvid1').css('display','none');
  $('#rowvid2').css('display','none') }
};