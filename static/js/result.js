var wrapper = document.getElementById("main");
var trainButton0 = wrapper.querySelector("[data-action=train0]");
var trainButton1 = wrapper.querySelector("[data-action=train1]");
var trainButton2 = wrapper.querySelector("[data-action=train2]");
var trainButton3 = wrapper.querySelector("[data-action=train3]");
var trainButton4 = wrapper.querySelector("[data-action=train4]");
var trainButton5 = wrapper.querySelector("[data-action=train5]");
var trainButton6 = wrapper.querySelector("[data-action=train6]");
var trainButton7 = wrapper.querySelector("[data-action=train7]");
var trainButton8 = wrapper.querySelector("[data-action=train8]");
var trainButton9 = wrapper.querySelector("[data-action=train9]");

trainButton0.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton0.value)
});
trainButton1.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton1.value)
});
trainButton2.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton2.value)
});
trainButton3.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton3.value)
});
trainButton4.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton4.value)
});
trainButton5.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton5.value)
});
trainButton6.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton6.value)
});
trainButton7.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton7.value)
});
trainButton8.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton8.value)
});
trainButton9.addEventListener("click", function () {
  post('/handwriting', 'train', trainButton9.value)
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