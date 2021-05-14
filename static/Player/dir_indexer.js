


//
// _____Load a Directory to Playlist_____
//

function getFolder(dName) {
  pli = 1
  for ( const file of dirs[dName].contents ) {
    // Pictures Only
    if ( !imgTypes.includes(file.substring(file.length-4)) && !imgTypes.includes(file.substring(file.length-3)) ) {
      continue
    }
    document.getElementById(pli).src = dirs[dName].path + file;
    document.getElementById(pli).style.position = "absolute";
    document.getElementById(pli).style.opacity = .86;
    document.getElementById(pli).setAttribute( "onClick", "eHyperLink(this)" );
    // Caption
    document.getElementById(pli).parentElement.childNodes[2].innerHTML = file.substring(file.length-3)
    pli++
    // Don't load playlist items past max available slots
    if ( pli == playlistSlots ) { break }
} }


//
// _____Load Video_____
//

imgTypes = ["jpg", "png", "tif", "raw", "eps", "gif", "psd","xcf", "ai", "cdr", "bmp", "jpeg", "cr2", "nef", "orf", "sr2","jpe", "jif", "jfif", "jfi", "webp", "k25", "nrw", "arw", "dib", "heif", "heic", "ind", "indd", "indt", "jp2", "j2k", "jpf", "jpx", "jpm", "mj2", "svg", "svgz", "ini"]
vidTypes = ["webm", "mpg", "mp2", "mpeg", "mpe", "mpv", "ogg", "mp4", "m4p", "m4v", "avi", "wmv", "mov", ".qt", "flv", "swf", "vchd"]

var eHyperLink = function(caller) {
  pngSrc = caller.src
  toArray = pngSrc.split("/")
  namewCode = toArray[toArray.length - 1]
  directoryName = toArray[toArray.length - 2]
  nameParts = namewCode.split(".")
  nameParts.pop()
  name1 = nameParts.join().replace("%20", " ")

  dirsObject = dirs[directoryName]
  i = 0
  while ( dirsObject.contents[i].includes(name1) == false || imgTypes.includes(dirsObject.contents[i].substring(dirsObject.contents[i].length - 3)) || imgTypes.includes(dirsObject.contents[i].substring(dirsObject.contents[i].length - 4)) ) {
    // Catch if the thumbnail img file doesn't have an associated video file
    if ( i == dirsObject.size - 1 ) {
      oneRanFrom(directoryName);
      break
    }
    // TO DO: iterate through all directories to see if the associated video is
    // somehow in another folder away from its thumbnail
    i++
  }
  videoList[selectedVid].src = dirsObject.path + dirsObject.contents[i];
  videoList[selectedVid].play();
  currDirPer[selectedVid] = directoryName
  // Declare an empty list for autoplay queue of selected frame (will be caught in autoplay functions)
  autoplayIndexPos[selectedVid] = []

  /*
  if ( imgTypes.includes(currFileCode) == true ) {
  // Set to hidden div so you can get dimensions -- do before re-assigning 'newVid'
  document.getElementById("loadingZone").src = newVid
  newWidth = loadingWidth(); newHeight = loadingHeight();
  positioned = "no-repeat left " + gifPosLeft + "px top " + gifPosTop + "px/auto auto "
  var preLoad = ''
  if ( document.body.style.background != "") {
    preLoad = "," +  document.body.style.background; }
  newContrast();
  newVid = positioned + "url('" + newVid + "')" + preLoad
  document.body.style.background = newVid
  // Update Position Variables for Next Img
  counter = counter + 1;
  bound = document.body.clientWidth; upBound = document.body.clientHeight;
  heightArray.push(newHeight)
  gifPosLeft += newWidth
  if ( gifPosLeft >= bound && counter != 0 ) {
    gifPosTop += Math.max.apply(null, heightArray) - 10
    if ( gifPosTop >= upBound ) {
      document.body.style.minHeight = "20000px" }
    heightArray = []; gifPosLeft = 0 } }
  else {

  } */ }


//
// _____Image Mode_____
//

var counter = 0;
var heightArray=[];
gifPosTop = 0; gifPosLeft = 0; gifPosRight = 0; gifPosBot = 0;
function loadingWidth(){ var realWidth = document.getElementById("loadingZone").naturalWidth; return realWidth }
function loadingHeight(){ var realHeight = document.getElementById("loadingZone").naturalHeight; return realHeight }