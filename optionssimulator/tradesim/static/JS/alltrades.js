function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}
function newtrade() {
  var strategy = $("#newstrategy").val();
  var expiry = $("#newexpiry").val();
  $.ajax({
    type: "GET",
    url:
      "http://127.0.0.1:8000/tradesim/inviewupdate/" + strategy + "/" + expiry,
    success: function (response) {
      if (response.messages == "true") {
        window.location.href = "http://127.0.0.1:8000/tradesim/";
      }
    },
    error: function (response) {
      alert("error occured - inview update");
    },
  });
}
function modifytrade(id, strategy, expiry, action) {
  $.ajax({
    type: "GET",
    url:
      "http://127.0.0.1:8000/tradesim/trademodify/" +
      id +
      "/" +
      strategy +
      "/" +
      expiry +
      "/" +
      action,
    success: function (response) {
      if (response.messages == "true") {
        window.location.href = "http://127.0.0.1:8000/tradesim/alltrades";
      }
    },
    error: function (response) {
      alert("error occured - inview update");
    },
  });
}
