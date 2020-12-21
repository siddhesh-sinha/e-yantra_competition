/* global webots, sendBenchmarkRecord, showBenchmarkRecord, showBenchmarkError */
$('#infotabs').tabs();


webots.window('task_1').receive = function(message, robot) {
  // updates the metric
  if (message.startsWith('update_time:')) {
    var segmentIndex = 12;
    $("#time_remaining").html("<strong>"+message.substring(segmentIndex,18)+"</strong>");

  } else if (message.startsWith('update_waypoints:')) {
    var segmentIndex = 17;
    $("#waypoints_reached").html("<strong>"+message.substring(segmentIndex)+"</strong>");

    }
  else if (message == "stop") {
   $("#submission_status").html("ZIP file successfully saved to the parent folder");
   $("#waypoints_reached").css('color','green');
   $("#time_remaining").css('color','green'); 
  }
  else if (message == "time_up") {
   $("#submission_status").html("Time is up. The ZIP file has been successfully saved to the parent folder");
   $("#waypoints_reached").css('color','green');
   $("#time_remaining").css('color','red'); 
  } else
    console.log("Received unknown message for robot '" + robot + "': '" + message + "'");


};
