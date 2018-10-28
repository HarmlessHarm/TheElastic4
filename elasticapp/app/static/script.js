
// Timeline
$(document).ready(function() {
	var container = document.getElementById('timeline')
	// var data = $(container).attr('data-timeline')
	data_set = []
	for (i in timeline_data) {
		date = timeline_data[i]
		content = date
		data_item = {id: i, content: content, start: date}
		data_set.push(data_item)
	}

	var items = new vis.DataSet(data_set);

  	var options = {
  		stack: true,
  		maxHeight: 300
  	};

  	var timeline = new vis.Timeline(container, items, options);
})

// Wordcloud
$(document).ready(function(){
  $('.stat-link').click(function(){
    var text = $(this).attr('href')
    var qId = text.replace('#statistics-', '')
    var wordcloud_text = wordcloud_data
    var wordcloud_div_id = $(this).parents('.card').find(text).find(".wordcloud-data").attr("data-id")
    console.log(wordcloud_div_id)
    if (!document.getElementById(wordcloud_div_id.slice(1)).hasChildNodes()) {
      drawWordCloud(wordcloud_text[qId].join(' '), wordcloud_div_id)
    }
  })
})

function drawWordCloud(text_string,location){
  var common = "\\";
  var word_count = {};
  var words = text_string.split(/[ '\-\(\)\*":;\[\]|{},.!?]+/);
  if (words.length == 1){
    word_count[words[0]] = 1;
  } else {
    words.forEach(function(word){
      var word = word.toLowerCase();
      if (word != "" && common.indexOf(word)==-1 && word.length>1){
        if (word_count[word]){
          word_count[word]++;
        } else {
          word_count[word] = 1;
        }
      }
    })
  }
  var svg_location = location;
  var width = 500;
  var height = width;

  var fill = d3.scale.category20();

  var word_entries = d3.entries(word_count);

  var xScale = d3.scale.linear()
  .domain([0, d3.max(word_entries, function(d) {
    return d.value;
  })
  ])
  .range([10,100]);

  d3.layout.cloud().size([width, height])
  .timeInterval(20)
  .words(word_entries)
  .fontSize(function(d) { return xScale(+d.value); })
  .text(function(d) { return d.key; })
  .rotate(function() { return ~~(Math.random() * 2) * 90; })
  .font("Impact")
  .on("end", draw)
  .start();

  function draw(words) {
    d3.select(svg_location).append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
    .selectAll("text")
    .data(words)
    .enter().append("text")
    .style("font-size", function(d) { return xScale(d.value) + "px"; })
    .style("font-family", "Impact")
    .style("fill", function(d, i) { return fill(i); })
    .attr("text-anchor", "middle")
    .attr("transform", function(d) {
      return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    })
    .text(function(d) { return d.key; });
  }

  d3.layout.cloud().stop();
}
