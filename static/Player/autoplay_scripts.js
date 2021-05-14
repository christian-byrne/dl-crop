
var autoplayMode = "on";
var orderedAutoplayMode = "off";

// var currDirPer = ['AAANEW', 'AAANEW', 'AAANEW']
var autoplayIndexPos = [[], [], [], []]


function newAutoplay(callerNum) {
  frame = parseInt(callerNum)

  if ( autoplayMode == "on" ) {
    // Create a random order (index list) of videos if it doesnt exist already
    if ( !!autoplayIndexPos[frame] ) {
      autoplayIndexPos[frame] = shuffle(Array.from(Array(dirs[currDirPer[frame]].size).keys()))
      }
    v = dirs[currDirPer[frame]].contents[autoplayIndexPos[frame][0]]
    // Make sure it is a video not an image file
    while ( vidTypes.includes(v.substring(v.length-3)) == false && vidTypes.includes(v.substring(v.length-4)) == false ) {
      autoplayIndexPos[frame].shift()
      // Start from beginning of playlist if at end
      if ( !!autoplayIndexPos[frame] ) {
        autoplayIndexPos[frame] = shuffle(Array.from(Array(dirs[currDirPer[frame]].size).keys()))
        }
      v = dirs[currDirPer[frame]].contents[autoplayIndexPos[frame][0]]
      }
    newVid = dirs[currDirPer[frame]].path + v
    videoList[frame].src = newVid
    videoList[frame].play();
    autoplayIndexPos[frame].shift()
    }

  else if ( orderedAutoplayMode == "on" ) {
    vp = document.getElementsByTagName("video")[frame].src.split("/");
    cDir = vp[vp.length -2];
    cName = vp[vp.length - 1].replace("%20", " ");
    cPos = dirs[cDir].contents.indexOf(cName) + 1;
    // Start from beginning of playlist if at end
    if ( cPos == dirs[cDir].contents.length ) { cPos = 0}
    v = dirs[cDir].contents[cPos];
    // Make sure it is a video not an image file
    while ( vidTypes.includes(v.substring(v.length-3)) == false && vidTypes.includes(v.substring(v.length-4)) == false ) {
      cPos++
      v = dirs[cDir].contents[cPos]
    }
    newVid = dirs[cDir].path + v
    videoList[frame].src = newVid
    videoList[frame].play();
  }

  else {
    videoList[frame].currentTime = 0.1
    videoList[frame].play();
}}