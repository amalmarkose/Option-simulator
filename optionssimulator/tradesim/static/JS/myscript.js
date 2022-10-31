//global variable
let POSITION_UPDATED = true;
let BUILDER_UPDATED = true;
let CHAIN_UPDATED = true;
let CHAIN_FOCUS = true;
let STRATEGY = "";
let CREATED_ON = "";
let EXPIRY = "";
let B = "B";
let S = "S";
let add = "add";
let remove = "remove";
let substract = "substract";
let squareoff = "squareoff";
let stoploss = "stoploss";
let plus = "plus";
let minus = "minus";

//builder
function buildermodify(token, bs, action) {
  $.ajax({
    type: "GET",
    url:
      "http://127.0.0.1:8000/tradesim/buildermodify/" +
      token +
      "/" +
      bs +
      "/" +
      action,
    success: function (response) {
      if (response.messages == "true") {
        BUILDER_UPDATED = true;
      }
    },
    error: function (response) {
      //alert("error occured - buildermodify");
    },
  });
}
function increment(token, bs, action, i) {
  document.getElementById("lotInput" + i).stepUp();
  buildermodify(token, bs, action);
}
function decrement(token, bs, action, i) {
  document.getElementById("lotInput" + i).stepDown();
  buildermodify(token, bs, action);
}
function addtoposition() {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/tradesim/addtoposition",
    success: function (response) {
      if (response.messages == "true") {
        BUILDER_UPDATED = true;
        POSITION_UPDATED = true;
      }
    },
    error: function (response) {
      alert("error occured - buildermodify");
    },
  });
}

//position
function positionmodify(token, action) {
  if (action == "stoploss") {
    var value = $("#stoploss" + token).val();
  } else if (action == "squareoff") {
    var value = $("#lotremove" + token).val();
  } else if (action == "squareoffall") {
    var value = 10;
  }

  $.ajax({
    type: "GET",
    url:
      "http://127.0.0.1:8000/tradesim/positionmodify/" +
      token +
      "/" +
      action +
      "/" +
      value,
    success: function (response) {
      if (response.messages == "true") {
        POSITION_UPDATED = true;
      }
    },
    error: function (response) {
      alert(url);
      alert("error occured - positionmodify");
    },
  });
}
//inviewdata
$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/tradesim/inviewpush",
    success: function (response) {
      console.log(response);
      for (var key in response.messages) {
        STRATEGY = response.messages[key].strategy;
        CREATED_ON = response.messages[key].createdon;
        EXPIRY = response.messages[key].expiry;
      }
    },
    error: function (response) {
      //alert("error occured - inview details");
    },
  });
});
//field updates
//dashboard
$(document).ready(function () {
  setInterval(function () {
    $.ajax({
      type: "GET",
      url:
        "http://127.0.0.1:8000/tradesim/dashboardpush/" +
        STRATEGY +
        "/" +
        CREATED_ON,
      success: function (response) {
        console.log(response);
        $("#detailsfetch").empty();
        for (var key in response.messages) {
          var temp =
            '<div class="col-lg-4 col-md-12"><p>Max profit <span style="float: right">' +
            response.messages[key].maxprofit +
            '</span></p><p>Max loss <span style="float: right">' +
            response.messages[key].maxloss +
            '</span></p><p>Risk / Reward <span style="float: right">' +
            response.messages[key].rrr +
            '</span></p></div><div class="col-lg-4 col-md-12"><p>Breakeven 1 <span style="float: right">' +
            response.messages[key].breakeven1 +
            '</span></p><p>Breakeven 2 <span style="float: right">' +
            response.messages[key].breakeven2 +
            "</span></p></div></>";
          $("#detailsfetch").append(temp);
        }
      },
      error: function (response) {
        //alert("error occured - dashboard details");
      },
    });
  }, 1200);
});
//display
$(document).ready(function () {
  setInterval(function () {
    $.ajax({
      type: "GET",
      url: "http://127.0.0.1:8000/tradesim/displaydatapush",
      success: function (response) {
        console.log(response);
        $("#displaydatafetch").empty();
        for (var key in response.messages) {
          if (response.messages[key].percentagechange > 0) {
            label = "label label-success";
          } else {
            label = "label label-danger";
          }
          var temp =
            '<div class="col-lg-3 col-md-6"><div class="headitem"><p>' +
            response.messages[key].name +
            " " +
            +response.messages[key].value +
            ' <span class="' +
            label +
            '">' +
            response.messages[key].percentagechange +
            "%</span></p></div></div>";
          $("#displaydatafetch").append(temp);
        }
      },
      error: function (response) {
        //alert("error occured - display");
      },
    });
  }, 1000);
});
//position

$(document).ready(function () {
  setInterval(function () {
    $.ajax({
      type: "GET",
      url:
        "http://127.0.0.1:8000/tradesim/positionspush/" +
        STRATEGY +
        "/" +
        CREATED_ON,
      success: function (response) {
        console.log(response);
        if (POSITION_UPDATED == true || response.POSITION_UPDATED == true) {
          $("#positionsfetch").empty();
          let i = 1;
          for (var key in response.messages) {
            if (response.messages[key].bs == "B") {
              color = "#6ab762";
            } else {
              color = "#ed603d";
            }
            var temp =
              '<div class="row" style="background-color: ' +
              color +
              '; color: azure;"><div class="col-xs-1"><p id="bs' +
              i +
              '" style="font-weight: bold">' +
              response.messages[key].bs +
              '</p></div><div class="col-xs-1"><p style="font-size: 13px" id="expiry' +
              i +
              '">' +
              response.messages[key].expiry +
              '</p></div><div class="col-xs-1"><p id="strike' +
              i +
              '">' +
              response.messages[key].strike +
              '</p></div><div class="col-xs-1"><p id="cepe' +
              i +
              '" font-weight: bold">' +
              response.messages[key].cepe +
              '</p></div><div class="col-xs-1"><p id="lots' +
              i +
              '">' +
              response.messages[key].lots +
              '</p></div><div class="col-xs-1"><p id="entry' +
              i +
              '">' +
              response.messages[key].entry +
              '</p></div><div class="col-xs-2"><p><input style="color: black;" class="stoploss" id="stoploss' +
              response.messages[key].token +
              '" type="number" value="' +
              response.messages[key].stoploss +
              '" min="0"/><button onclick="positionmodify(' +
              response.messages[key].token +
              "," +
              stoploss +
              ')"><span style="color: black;" class="glyphicon glyphicon-floppy-disk"></span></button></p></div><div class="col-xs-1"><p id="price' +
              i +
              '">' +
              response.messages[key].price +
              '</p></div><div class="col-xs-1"><p id="pnl' +
              i +
              '">' +
              response.messages[key].pnl +
              '</p></div><div class="col-xs-2"><p><input style="color: black;" class="lotremove" id="lotremove' +
              response.messages[key].token +
              '" type="number" value="1" min="1" max="' +
              response.messages[key].lots +
              '"/>' +
              '<button onclick="positionmodify(' +
              response.messages[key].token +
              "," +
              squareoff +
              ')"><span style="color: black;" class="glyphicon glyphicon-remove"></span></button></p></div></div>';
            $("#positionsfetch").append(temp);
            i++;
          }
          for (var key in response.notactive) {
            if (response.notactive[key].bs == "B") {
              color = "#30c630";
            } else {
              color = "#ed603d";
            }
            var temp =
              '<div class="row"><div class="col-xs-1"><p id="bs' +
              i +
              '" style="color: ' +
              color +
              '; font-weight: bold">' +
              response.notactive[key].bs +
              '</p></div><div class="col-xs-1"><p style="font-size: 13px" id="expiry' +
              i +
              '">' +
              response.notactive[key].expiry +
              '</p></div><div class="col-xs-1"><p id="strike' +
              i +
              '">' +
              response.notactive[key].strike +
              '</p></div><div class="col-xs-1"><p id="cepe' +
              i +
              '" font-weight: bold">' +
              response.notactive[key].cepe +
              '</p></div><div class="col-xs-1"><p id="lots' +
              i +
              '">' +
              response.notactive[key].lots +
              '</p></div><div class="col-xs-1"><p id="entry' +
              i +
              '">' +
              response.notactive[key].entry +
              '</p></div><div class="col-xs-2"><p>' +
              response.notactive[key].stoploss +
              '</p></div><div class="col-xs-1"><p id="price' +
              i +
              '">' +
              response.notactive[key].price +
              '</p></div><div class="col-xs-1"><p id="pnl' +
              i +
              '">' +
              response.notactive[key].pnl +
              '</p></div><div class="col-xs-2"></div></div>';
            $("#positionsfetch").append(temp);
          }
          $("#totalpnl").empty();
          $("#totallots").empty();
          $("#totalpnl").append(response.totalpnl.pnl__sum);
          $("#totallots").append(response.totallots.lots__sum);
          POSITION_UPDATED = false;
        } else {
          let i = 1;
          for (var keys in response.messages) {
            $("#price" + i).empty();
            $("#pnl" + i).empty();

            $("#price" + i).append(response.messages[keys].price);
            $("#pnl" + i).append(response.messages[keys].pnl);
            i++;
          }
          $("#totalpnl").empty();
          $("#totallots").empty();
          $("#totalpnl").append(response.totalpnl.pnl__sum);
          $("#totallots").append(response.totallots.lots__sum);
        }
      },
      error: function (response) {
        //alert("error occured - positions");
      },
    });
  }, 300);
});
//option chain
$(document).ready(function () {
  $("#chain").mouseenter(function () {
    CHAIN_FOCUS = true;
    CHAIN_UPDATED = true;
  });
  $("#chain").mouseleave(function () {
    CHAIN_FOCUS = false;
    $.ajax({
      type: "GET",
      url:
        "http://127.0.0.1:8000/tradesim/optionchainpush/" + EXPIRY + "/false",
    });
  });
  setInterval(function () {
    if (CHAIN_FOCUS == true) {
      $.ajax({
        type: "GET",
        url:
          "http://127.0.0.1:8000/tradesim/optionchainpush/" + EXPIRY + "/true",
        success: function (response) {
          console.log(response);
          if (CHAIN_UPDATED == true) {
            $("#chainfetch").empty();
            let i = 0;
            for (var key in response.messages) {
              let bg = ``;
              if (response.messages[key].strike == response.spotstrike) {
                bg = `style="background-color: #eaeab5;"`;
              }
              var temp =
                "<tr " +
                bg +
                ' ><td id="coi' +
                i +
                '">' +
                response.messages[key].coi +
                '</td><td> <button onclick="buildermodify(' +
                response.messages[key].ctoken +
                "," +
                B +
                "," +
                add +
                ');" type="button" class="btn btn-success">B</button> <button onclick="buildermodify(' +
                response.messages[key].ctoken +
                "," +
                S +
                "," +
                add +
                ');" type="button" class="btn btn-danger">S</button> </td> <td id="cltp' +
                i +
                '">' +
                response.messages[key].cltp +
                "</td><td>" +
                response.messages[key].strike +
                '</td><td id="pltp' +
                i +
                '">' +
                response.messages[key].pltp +
                '</td><td><button onclick="buildermodify(' +
                response.messages[key].ptoken +
                "," +
                B +
                "," +
                add +
                ');" type="button" class="btn btn-success">B</button> <button onclick="buildermodify(' +
                response.messages[key].ptoken +
                "," +
                S +
                "," +
                add +
                ');" type="button" class="btn btn-danger">S </button> </td><td id="poi' +
                i +
                '">' +
                response.messages[key].poi +
                "</td></tr>";
              $("#chainfetch").append(temp);
              i++;
            }
            CHAIN_UPDATED = false;
          } else {
            i = 0;
            for (var keys in response.messages) {
              $("#coi" + i).empty();
              $("#cltp" + i).empty();
              $("#pltp" + i).empty();
              $("#poi" + i).empty();

              $("#coi" + i).append(response.messages[keys].coi);
              $("#cltp" + i).append(response.messages[keys].cltp);
              $("#pltp" + i).append(response.messages[keys].pltp);
              $("#poi" + i).append(response.messages[keys].poi);
              i++;
            }
          }
        },
        error: function () {
          //alert("error occured - option chain mouse in");
        },
      });
    }
  }, 700);
});
//builder
$(document).ready(function () {
  setInterval(function () {
    $.ajax({
      type: "GET",
      url:
        "http://127.0.0.1:8000/tradesim/builderpush/" +
        STRATEGY +
        "/" +
        CREATED_ON,
      success: function (response) {
        console.log(response);
        if (BUILDER_UPDATED == true) {
          $("#builderfetch").empty();
          let i = 1;
          for (var key in response.messages) {
            if (response.messages[key].bs == "B") {
              color = "#30c630";
            } else {
              color = "#ed603d";
            }
            var temp =
              '<div class="row"><div class="col-xs-1"><p style="color: ' +
              color +
              '">' +
              response.messages[key].bs +
              '</p></div><div class="col-xs-1" style="padding: 0px" ><p id="builderexpiry' +
              i +
              '">' +
              response.messages[key].expiry +
              '</p></div><div class="col-xs-3"> <p> <button onclick="buildermodify(' +
              response.messages[key].token +
              "," +
              response.messages[key].bs +
              "," +
              plus +
              ')"><span class="glyphicon glyphicon-plus" style="color: #30c630"></span> </button> <span style="font-weight: bold" id="builderstrike' +
              i +
              '">' +
              response.messages[key].strike +
              ' </span><button style="margin-left: 5px" onclick="buildermodify(' +
              response.messages[key].token +
              "," +
              response.messages[key].bs +
              "," +
              minus +
              ')"><span class="glyphicon glyphicon-minus" style="color: #ed603d"></span> </button></p></div><div class="col-xs-1"><p id="buildercepe' +
              i +
              '">' +
              response.messages[key].cepe +
              '</p> </div><div class="col-xs-3 builderlots"> <p> <input id="lotInput' +
              i +
              '"  type="number" value="' +
              response.messages[key].lots +
              '" min="1" max="110" /> <button onclick="increment(' +
              response.messages[key].token +
              "," +
              response.messages[key].bs +
              "," +
              add +
              "," +
              i +
              ')"><span class="glyphicon glyphicon-plus" style="color: #30c630"></span> </button><button onclick="decrement(' +
              response.messages[key].token +
              "," +
              response.messages[key].bs +
              "," +
              substract +
              "," +
              i +
              ')"><span class="glyphicon glyphicon-minus"style="color: #ed603d"></span></button></p></div><div class="col-xs-1"><p id="builderprice' +
              i +
              '">' +
              response.messages[key].price +
              '</p></div><div class="col-xs-2"><p><button type="button" class="btn btn-default" onclick="buildermodify(' +
              response.messages[key].token +
              "," +
              response.messages[key].bs +
              "," +
              remove +
              ')"><span class="glyphicon glyphicon-trash"></span></button></p></div></div>';
            $("#builderfetch").append(temp);
            i++;
          }
          BUILDER_UPDATED = false;
        } else {
          let i = 1;
          for (var key in response.messages) {
            $("#builderprice" + i).empty();
            $("#builderexpiry" + i).empty();
            $("#builderstrike" + i).empty();
            $("#buildercepe" + i).empty();
            $("#builderprice" + i).append(response.messages[key].price);
            $("#builderexpiry" + i).append(response.messages[key].expiry);
            $("#builderstrike" + i).append(response.messages[key].strike);
            $("#buildercepe" + i).append(response.messages[key].cepe);
            i++;
          }
        }
      },
      error: function (response) {
        //alert("error occured - builder");
      },
    });
  }, 330);
});
//chart
function chartgenerator(data, spot) {
  var dataPoints = [];
  var y = 0;

  var lowlimit = spot - 1000;
  var highlimit = spot + 1000;
  var maxprofit = 0;
  var maxloss = 0;
  const breakeven = [];
  let t = 0;
  for (var i = lowlimit; i < highlimit; i++) {
    pnl = 0;
    for (var key in data) {
      if (data[key].cepe == "CE") {
        if (data[key].bs == "B") {
          pnl +=
            (Math.max(i - data[key].strike, 0) - data[key].premium) *
            data[key].lots *
            50;
        } else if (data[key].bs == "S") {
          pnl +=
            (Math.min(data[key].strike - i, 0) + data[key].premium) *
            data[key].lots *
            50;
        }
      } else if (data[key].cepe == "PE") {
        if (data[key].bs == "B") {
          pnl +=
            (Math.max(data[key].strike - i, 0) - data[key].premium) *
            data[key].lots *
            50;
        } else if (data[key].bs == "S") {
          pnl +=
            (Math.min(i - data[key].strike, 0) + data[key].premium) *
            data[key].lots *
            50;
        }
      }
    }
    if (pnl > maxprofit) {
      maxprofit = pnl;
    }
    if (pnl < maxloss) {
      maxloss = pnl;
    }
    if (Math.sign(pnl) + Math.sign(t) == 0 || Math.sign(pnl) == 0) {
      breakeven.push(i);
    }
    t = pnl;
    dataPoints.push({ x: i, y: pnl });
  }
  $.ajax({
    url:
      "http://127.0.0.1:8000/tradesim/dashboardmodify/" +
      maxprofit +
      "/" +
      maxloss +
      "/" +
      breakeven[0] +
      "/" +
      breakeven[1],
  });

  var options = {
    animationEnabled: false,
    zoomEnabled: true,
    title: {
      text: "Pay-off chart",
    },
    data: [
      {
        type: "line",
        dataPoints: dataPoints,
      },
    ],
  };

  $("#chartContainer").CanvasJSChart(options);
}
//chartpopulate
$(document).ready(function () {
  var g = 0;
  setInterval(function () {
    if (POSITION_UPDATED == true || BUILDER_UPDATED == true || g == 20) {
      g = 0;
      $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/tradesim/chartpush",
        success: function (response) {
          console.log(response);
          chartgenerator(response.data, response.spot);
        },
        error: function (response) {
          //alert("An error - chart");
        },
      });
    }
    g++;
  }, 100);
});
//new trade
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
