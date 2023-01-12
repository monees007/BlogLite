function hide_all_comments() {
    let comms = document.querySelectorAll("#commentx");
    comms.forEach(function (d, i) {
        d.style.display = "none";
    });
}

async function delete_comment(cid, pid) {
    let req = await fetch("/api/comment?cid=" + cid, {method: 'DELETE'})
    if (req.status === 200) {
        location.reload()
        toastEl = `<div class="toast align-items-center" role="alert" aria-live="assertive" aria-atomic="true">
  <div class="d-flex">
    <div class="toast-body">
    Hello, world! This is a toast message.
   </div>
    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
  </div>
</div>`
        const toast = new bootstrap.Toast(toastEl)
        toast.show()
        await hide_all_comments()
    }
}


async function comments_hider(el, pid) {
    hide_all_comments()
    let count = 1;
    let comment_elements = el.parentNode.parentNode.parentNode.querySelector('#commentx')
    const current_user = document.getElementById('current_user').textContent


    // #get comments
    let loaded_comments = "";
    let delete_btn = ''
    let comment_list = await fetch('http://127.0.0.1:5000/api/comment?pid=' + pid, {
        method: 'GET',
        credentials: 'include'
    }).then((response) => response.json()).then((data) => data)
    for (c in comment_list) {
        // to show delete comment button
        if (comment_list[c]['email'] === current_user) {
            delete_btn = `<button onclick="delete_comment(${comment_list[c]['cid']},${pid})"
                                    class=" btn btn-sm d-flex align-items-center me-1">
                                <span class="material-symbols-outlined me-2">delete</span>
                            </button>`
        } else {
            delete_btn = ""
        }
        loaded_comments += `<div class="card-footer py-3 border-0" style="background-color: #f8f9fa;">
                        <div class="d-flex flex-start w-100">
                            <img class="rounded-circle shadow-1-strong me-3"
                                 src="${comment_list[c]['profile_pic']}" alt="avatar"
                                 width="40"
                                 height="40"/>
                            <div class="d-flex flex-start flex-column form-outline w-100">
                                <small class="text-primary">${comment_list[c]['username']}</small>
                                <small class="text-secondary">${comment_list[c]['timestamp']}</small>
                                <small>${comment_list[c]['content']}</small>

                            </div>` + delete_btn + `</div>
                    </div>`
    }
    comment_elements.innerHTML = loaded_comments;
    comment_elements.innerHTML += `<div class="card-footer py-3 border-0" style="background-color: #f8f9fa;">

                            <div id="cl1" class="d-flex flex-start w-100">
<!--                                    <img class="rounded-circle shadow-1-strong me-3"-->
<!--                                         src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(19).webp" alt="avatar"-->
<!--                                         width="40"-->
<!--                                         height="40"/>-->
                                <div id="cl2" class="form-outline w-100">
            <input class="form-control NewComment" id="NewComment" type="text" 
                      style="background: #fff;word-break: break-word;"></input>
                                </div>
                            </div>
                            <div class="float-end mt-2 pt-1">
                                <button type="button" onclick="post_comment(this,'${pid}')" class="btn btn-primary btn-sm">Post comment</button>
                                <button type="button" onclick="hide_all_comments()" class="btn btn-outline-primary btn-sm">Cancel</button>
                            </div>
                        </div>`
    // #show comments section
    if (comment_elements.style.display === 'none') {
        comment_elements.style.display = 'block'
    } else {
        comment_elements.style.display = 'none';
    }

}

async function post_comment(inx, pid) {
    inx.disabled = true;
    content = inx.parentElement.parentElement.querySelector('#NewComment').value;
    response = await fetch('http://127.0.0.1:5000/api/comment?pid=' + pid + '&content=' + content, {
        method: 'POST', credentials: 'include'
    }).then((res) => {
        if (res.ok) {
            inx.disabled = false
        }
    })
    comments_hider(inx.closest('section'), pid)
}
