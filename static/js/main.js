function commentReplyToggle(parent_id) {
    const comment = document.getElementById(parent_id);
    if (comment.classList.contains('d-none')) {
        comment.classList.remove('d-none');
    } else {
        comment.classList.add('d-none');
    }
}