const popup = (id) => {
    var writable = localStorage.getItem("writable")
    const data = JSON.parse(localStorage.getItem(id))
    $('#contentmodaltitle').text(data.title + " - 错误代码：" + data.errcode);
    var html = "";
    if(writable=='W')
    {
        html = `<a class='btn btn-primary text-white' href='/record/${data.id}/edit/'>修改</a><hr>`;
    }
    html += "<h5>问题详细描述</h5>";
    html += data.detail;
    html += "<hr><h5>问题解决方案</h5>";
    html += data.solution;
    html += "<hr><h5>附件</h5>"
    for(var i=0;i<data.attachments.length;++i)
    {
        if(data.attachments[i].endsWith(".png")||data.attachments[i].endsWith(".jpg")||data.attachments[i].endsWith(".jpeg")||data.attachments[i].endsWith(".gif")||data.attachments[i].endsWith(".svg"))
        {
            html += `<img class='w-100' src="${data.attachments[i]}"/>`
        }
        else
        {
            html += `<a href="${data.attachments[i]}" download>${data.attachments[i]}</a><br>`
        }
    }
    $('#contentmodalbody').html(html);
    $('#contentmodal').modal({
        backdrop: 'static',
        keyboard: false
    })
    return false;
}
