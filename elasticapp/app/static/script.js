
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