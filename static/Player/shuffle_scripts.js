
// _____Array Shuffler_____
function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;
  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;
    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue; }
  return array; }


// _____Load 1 Random Video (from specified dir)_____
function oneRanFrom(dir) {
  let rf = dirs[dir].contents[Math.floor(Math.random() * dirs[dir].size)]
  // Make sure it is a video not an image file
  i = 1
  while ( vidTypes.includes(rf.substring(rf.length-3)) == false && vidTypes.includes(rf.substring(rf.length-4)) == false ) {
    rf = dirs[dir].contents[Math.floor(Math.random() * dirs[dir].size)]
    i++
    // Roll a new directory if can't find video file in specified directory
    if ( i % 599 == 0 ) { dir = Object.keys(dirs)[Math.floor(Math.random() * Object.keys(dirs).length)] }
    if ( i == 19999 ) { break }
  }
  videoList[selectedVid].src = dirs[dir].path + rf
  currDirPer[selectedVid] = dir
  // Declare an empty list for autoplay queue of selected frame (will be caught in autoplay functions)
  autoplayIndexPos[selectedVid] = []
}


// _____Load 1 Random Video (from any dir)_____
function load1Ran() {
  // Random directory
  let rd = Object.keys(dirs)[Math.floor(Math.random() * Object.keys(dirs).length)]
  // Random file from that directory
  let rf = dirs[rd].contents[Math.floor(Math.random() * dirs[rd].size)]
  // Make sure it is a video not an image file
  i = 1
  while ( vidTypes.includes(rf.substring(rf.length-3)) == false && vidTypes.includes(rf.substring(rf.length-4)) == false ) {
    rf = dirs[rd].contents[Math.floor(Math.random() * dirs[rd].size)]
    i++
    // Roll a new directory if can't find video file in current roll (every 7 tries)
    if ( i % 7 == 0 ) { rd = Object.keys(dirs)[Math.floor(Math.random() * Object.keys(dirs).length)] }
    if ( i == 9999 ) { break }
  }
  videoList[selectedVid].src = dirs[rd].path + rf
  currDirPer[selectedVid] = rd
  // Declare an empty list for autoplay queue of selected frame (will be caught in autoplay functions)
  autoplayIndexPos[selectedVid] = []
}


// _____Load 3 Random Videos (from specified dir)_____
function load3RanFrom(dir) {
  let temp = selectedVid
  for (q=0; q < videoList.length; q++) {
    selectedVid = q
    oneRanFrom(dir)
  }
  selectedVid = temp
}


// _____Load 3 Random Videos (from random folders)_____
function load3Ran() {
  let temp = selectedVid
  for (q=0; q < videoList.length; q++) {
    selectedVid = q
    load1Ran()
  }
  selectedVid = temp
}


// _____Populate Playlist Column Randomly_____
function ranPlaylist() {
  a = 1; allLengths = {};
  preserverOrder = false

  // If not enough files -> Prioritize showing all files over true random order
  if ( Object.keys(dirs).length == 1 ) { preserverOrder = true }
  
  else {
    totalContents = 0;
    for ( const obj of Objects.keys(dirs) ) {
        totalContents += dirs[obj].contents.length;
        allLengths[(dirs[obj].contents.length)] = [dirs[obj].name];
    }

    if ( totalContents > playlistSlots + 50 ) {
      if ( Object.keys(dirs).length < 4 ) {
        preserverOrder = true
      }
    }
    else if ( totalContents > playlistSlots + 110 ) {
      if ( Object.keys(dirs).length < 6 ) {
        preserverOrder = true
      }
    }
  }
  

  // If there is one folder with way more contents and a bunch of small folders,
  // avoid random shuffling favoring smaller folders
  onlyOne = false
  if ( Math.max( Object.keys(allLengths) / totalContents > .88 ) ) {
    onlyOne = allLengths[ Math.max( Object.keys(allLengths) ) ]
  }

  else if ( Math.max( Object.keys(allLengths) / totalContents > .65 && Objects.keys(dirs)).length > 5 ) {
    onlyOne = allLengths[ Math.max( Object.keys(allLengths) ) ]
  }

  else if ( Math.max( Object.keys(allLengths) / totalContents > .55 && Objects.keys(dirs)).length > 8 ) {
    onlyOne = allLengths[ Math.max( Object.keys(allLengths) ) ]
  }

  else if ( Math.max( Object.keys(allLengths) / totalContents > .50 && Objects.keys(dirs)).length > 14 ) {
    onlyOne = allLengths[ Math.max( Object.keys(allLengths) ) ]
  }


    // ---------------------------------------


  
    alert(preserverOrder)
    alert(onlyOne)
    if ( !!onlyOne || !!preserverOrder  ) {
      if ( !!onlyOne  ) { start = dirs[onlyOne] }
      else              { start = (Object.keys(dirs))[0] }

      while ( a < playlistSlots ) {
      shuffled = shuffle( dirs[start].contents )
      index = 0 
      for ( const pic of shuffled ) {
        if (( imgTypes.includes(pic.substring(pic.length-3)) == false && imgTypes.includes(pic.substring(pic.length-4)) == false )) {
            document.getElementById(a).src = dirs[start].path + pic
            document.getElementById(a).setAttribute( "onClick", "eHyperLink(this)" )
            document.getElementById(a).style.position = "absolute"
            let p = document.createElement("div");
            p.innerHTML = start + " / " + pic.substring(0,pic.length-4)
            p.classList.add("overlay")
            document.getElementById(a).parentElement.appendChild(p)
            a++
            console.log(index.toString() + ":" + pic)
            index++
        }
      }

      if ( a < playlistSlots ) {
        let rd = Object.keys(dirs)[Math.floor(Math.random() * Object.keys(dirs).length)]
        // Random file from that directory
        let rf = dirs[rd].contents[Math.floor(Math.random() * dirs[rd].size)]
        // Make sure it is an image file
        i = 1
        while ( imgTypes.includes(rf.substring(rf.length-3)) == false && imgTypes.includes(rf.substring(rf.length-4)) == false ) {
          rf = dirs[rd].contents[Math.floor(Math.random() * dirs[rd].size)]
          i++
          // Roll a new directory if can't find img in this directory (every 7 tries)
          if ( i % 7 == 0 ) { rd = Object.keys(dirs)[Math.floor(Math.random() * Object.keys(dirs).length)] }
          if ( i == 9999 ) { break }
          }
        document.getElementById(a).src = dirs[rd].path + rf
        document.getElementById(a).setAttribute( "onClick", "eHyperLink(this)" )
        document.getElementById(a).style.position = "absolute"
        let p = document.createElement("div");
        p.innerHTML = rd + " / " + rf.substring(0,rf.length-4)
        p.classList.add("overlay")
        document.getElementById(a).parentElement.appendChild(p)
        a++
        }
      }
    }

    else {
      while ( a < playlistSlots ) {
      // Random directory
      let rd = Object.keys(dirs)[Math.floor(Math.random() * Object.keys(dirs).length)]
      // Random file from that directory
      let rf = dirs[rd].contents[Math.floor(Math.random() * dirs[rd].size)]
      // Make sure it is an image file
      i = 1
      while ( imgTypes.includes(rf.substring(rf.length-3)) == false && imgTypes.includes(rf.substring(rf.length-4)) == false ) {
        rf = dirs[rd].contents[Math.floor(Math.random() * dirs[rd].size)]
        i++
        // Roll a new directory if can't find img in this directory (every 7 tries)
        if ( i % 7 == 0 ) { rd = Object.keys(dirs)[Math.floor(Math.random() * Object.keys(dirs).length)] }
        if ( i == 9999 ) { break }
        }
      document.getElementById(a).src = dirs[rd].path + rf
      document.getElementById(a).setAttribute( "onClick", "eHyperLink(this)" )
      document.getElementById(a).style.position = "absolute"
      let p = document.createElement("div");
      p.innerHTML = rd + " / " + rf.substring(0,rf.length-4)
      p.classList.add("overlay")
      document.getElementById(a).parentElement.appendChild(p)
      a++
    }
  }
}