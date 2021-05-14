/*
  // Backup Img for playlist thumb on error
  $('img').on("error", function() {
    eName = $(this).attr("id")
    index = parseInt(eName)
    var a = $(this).parent()[0]
    eName = eName.toString()
    if ( folderSizes.indexOf(currDir) == 0 ) { currFolder = 0 }
    else { currFolder = (folderSizes.indexOf(currDir) + 1)/3 }
    eName = eName + files[currFolder][index]
    a.innerHTML = eName
    a.style.fontSize = "2em"
    // hyperLinkSrc = "eHyperLink('" + dirName + "%" + r2 + "')"
    // $(this).attr( "onClick",hyperLinkSrc )
  });
*/
/*
// Backup Vid on Err
$('video').on("error", function() {
  eName = $(this).attr("id")
  index = pareseInt(eName)
  var a = $(this).parent()[0]
  eName = eName.toString()
  if ( folderSizes.indexOf(currDir) == 0 ) { currFolder = 0 }
  else { currFolder = (folderSizes.indexOf(currDir) + 1)/3 }
  eName = eName + files[currFolder][index]
  msg = "failed to load: " + eName
  a.innerHTML =  msg
  a.style.fontSize = "3em"
});
*/