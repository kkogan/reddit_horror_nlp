(function() {
  var filters = {};

  $(".image_button").click(e => {
    const ref = $(e.target);
    const title = ref.attr("title");
    if (ref.hasClass("active")) {
      filters[title] = 0;
      ref.removeClass("active");
    } else {
      filters[title] = 1;
      ref.addClass("active");
    }
    button(ref);
  });
  function button(filter) {
    console.log(filter);
    console.log(filters);

    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/filter",
      dataType: "json",
      async: true,
      data: JSON.stringify({
        topics: Object.keys(filters).filter(k => filters[k])
      }),
      success: function(data) {
        //res = JSON.parse(data);
        res = data;
        res = res.map(row => {
          row.topic_score = row.topic_score.toFixed(1);
          return row;
        });
        hackerList.clear();
        hackerList.add(res);
      },
      error: function(err) {
        console.error(err);
      }
    });
  }

  // https://stackoverflow.com/questions/18205598/add-image-src-and-a-href-in-list-js
  var options = {
    valueNames: [
      "score",
      "topic_score",
      "title",
      { attr: "href", name: "full_link" }
    ],
    // This describes how items must look like in HTML
    item:
      '<li class="table-row"><div class="score" data-label="Score">42235</div><div class="topic_score" data-label="Topic Score"></div><a class="full_link"><h4 class="title"></h4></a></li>'
  };
  // These items will be added to the list on initialization.
  var values = [
    {
      score: "Jonas Arnklint",
      topic_score: 666,
      title: 1985,
      full_link: "https"
    }
  ];
  console.log("button");

  var hackerList = new List("hacker-list", options, values);
  button();

  // It's possible to add items after list been initiated
}.call(this));
