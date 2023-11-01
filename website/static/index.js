function deleteNote(noteId){
    fetch('/delete-note',{
        method: "POST",
        body: JSON.stringify({noteId: noteId})
    }).then(_res=>{
        window.location.href="/";
    });
}

function deleteRequest(requestId) {
    fetch("/delete-request", {
        method: "POST",
        body: JSON.stringify({ requestId: requestId }),
    }).then((_res) => {
        window.location.href = "/resident-request";
    });
}