var Delete_ID;
var Url_Address

function bindBtnDeleteEvent() {
    $(".deleteBtn").click(function () {
        $("#deleteModal").modal('show');
        Delete_ID = $(this).attr("did");
    })
}

function bindDoDelete() {
    $("#confirmDelete").click(function () {
        Url_Address = $(this).attr("durl");
        $.ajax({
            url: Url_Address,
            type: "GET",
            data: {
                id: Delete_ID,
            },
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    alert("删除成功");
                    // 刷新页面
                    location.reload();
                } else {
                    alert(res.error)
                }
            }
        })
    })
}