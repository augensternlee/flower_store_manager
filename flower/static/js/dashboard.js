$(document).ready(function() {
  $.ajax({
    url: 'http://your_metabase_server/api/dashboard/{dashboard_id}/cards',
    type: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Metabase-Session': 'your_api_key'
    },
    data: {
      parameters: [
        {
          type: 'date/all-options',
          id: 'date'
        }
      ]
    },
    success: function(data) {
      // 将 JSON 数据传递给另一个函数以呈现仪表板数据
      renderDashboard(data);
    },
    error: function(xhr, status, error) {
      console.log('An error occurred:', error);
    }
  });
  function renderDashboard(data) {
    // 根据您的需要解析 JSON 数据并呈现到模板中
    // 这里的代码只是一个示例，您可以根据实际情况自行更改
    var html = '';
    data.forEach(function(card) {
      html += '<div>';
      html += '<h3>' + card.name + '</h3>';
      html += '<img src="' + card.visualization_settings['image-data'] + '" />';
      html += '</div>';
    });
    $('#dashboard').html(html);
  }
});