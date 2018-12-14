var wrapper = document.getElementById("main");
var recButton = wrapper.querySelector("[data-action=recog]");
var clearButton = wrapper.querySelector("[data-action=clear]");
var canvas = wrapper.querySelector("canvas");

var signaturePad = new SignaturePad(canvas, {
  backgroundColor: 'rgb(255, 255, 255)', //背影必须设置为不透明才能转jpg
  minWidth: 7.0, //加粗笔画便于识别
  maxWidth: 7.0
});

// Adjust canvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
// This also causes canvas to be cleared.
function resizeCanvas() {
  // When zoomed out to less than 100%, for some very strange reason,
  // some browsers report devicePixelRatio as less than 1
  // and only part of the canvas is cleared then.
  var ratio = Math.max(window.devicePixelRatio || 1, 1);

  // This part causes the canvas to be cleared
  canvas.width = canvas.offsetWidth * ratio;
  canvas.height = canvas.offsetHeight * ratio;
  canvas.getContext("2d").scale(ratio, ratio);

  // This library does not listen for canvas changes, so after the canvas is automatically
  // cleared by the browser, SignaturePad#isEmpty might still return false, even though the
  // canvas looks empty, because the internal data of this library wasn't cleared. To make sure
  // that the state of this library is consistent with visual state of the canvas, you
  // have to clear it manually.
  signaturePad.clear();
}

// On mobile devices it might make more sense to listen to orientation change,
// rather than window resize events.
window.onresize = resizeCanvas;
resizeCanvas();

clearButton.addEventListener("click", function () {
  signaturePad.clear();
});

recButton.addEventListener("click", function () {
  if (signaturePad.isEmpty()) {
    alert("先写个数呗~");
  } else {
    const dataURL = signaturePad.toDataURL("image/jpeg");
    post('/handwriting/result', 'recog', dataURL);
  }
});


function post(url, opt, data) {  // 以虚拟表单形式发送post
  var temp = document.createElement("form");
  temp.action = url;
  temp.method = "post";
  temp.style.display = "none";

  var option = document.createElement("textarea");
  option.name = "actOpt";
  option.value = opt;
  temp.appendChild(option);
  
  var content = document.createElement("textarea");
  content.name = "postContent";
  content.value = data;
  temp.appendChild(content);

  document.body.appendChild(temp);
  temp.submit();
  return temp;
}