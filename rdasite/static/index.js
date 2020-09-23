switchTab(-1, 1, 1); // Display the first tab
document.getElementById("submitBtn").disabled = "true";
window.error_map = {
    "review_errors": Array(),
    "rebuttal_errors": Array()
}


function switchTab(current_tab, total_tabs, direction) {
    new_tab = (current_tab + direction + total_tabs) % total_tabs;
    var tabs = document.getElementsByClassName("tab");
    if (current_tab > -1) {
        tabs.item(current_tab).style.display = "none";
    }
    tabs.item(new_tab).style.display = "block";
    paint(new_tab)
}


function paint(current_tab){
    var num_review_chunks = document.getElementById("reviewtablebody_"+current_tab).childElementCount
    for (var i of Array(num_review_chunks).keys()){
        chunk_id = current_tab + "-" + i
        if (document.getElementById("radios-"+ chunk_id + "-Yes").checked){
            document.getElementById("reviewrow_"+chunk_id).className = "table-success"
        } else {
            document.getElementById("reviewrow_"+chunk_id).className = "table-secondary"
        }
    }
}


function handleClick(rebuttal_idx) {
    paint(rebuttal_idx)
    document.getElementById("submitBtn").disabled = "true";
}


function updateError(rebuttal_chunk, rebuttal_or_review, add_or_remove) {
    if (rebuttal_or_review == "0") {
        relevant_map = window.error_map["rebuttal_errors"]
    } else {
        relevant_map = window.error_map["review_errors"]
    }

    if (add_or_remove == "0") {
        relevant_map.push(rebuttal_chunk)
    } else {
        new_map = relevant_map.filter(function(x) {
            return x !== rebuttal_chunk;
        });
        if (rebuttal_or_review == "0") {
            window.error_map["rebuttal_errors"] = new_map
        } else {
            window.error_map["review_errors"] = new_map

        }
    }
    document.getElementById("submitBtn").disabled = "true";
}


function buildAnnotationMap(){
  annotation_map = {}

    var num_rebuttal_chunks = document.getElementsByClassName("tab").length
    var num_review_chunks = document.getElementById("reviewtablebody_0").childElementCount

    for(var rebuttal_idx of Array(num_rebuttal_chunks).keys()){
        mapped_review_chunks = Array()
        for (var review_idx of Array(num_review_chunks).keys()){
            chunk_id = rebuttal_idx + "-" + review_idx
            if (document.getElementById("radios-"+ chunk_id + "-Yes").checked){
                mapped_review_chunks.push(review_idx)
            } 
         }
             if (mapped_review_chunks.length == 0){
        mapped_review_chunks.push(-1)
    }
    annotation_map[rebuttal_idx] = mapped_review_chunks
    }

  return annotation_map
}


function generateJson(review_length, rebuttal_length) {

    if (document.getElementById('initials').value === "") {
        alert("Please fill in your initials and run finalize again.")
    } else {
        submitButton = document.getElementById("submitBtn");
        submitButton.removeAttribute("disabled");
        result = {
            "review_supernote": document.getElementById("review_supernote").innerHTML,
            "rebuttal_supernote": document.getElementById("rebuttal_supernote").innerHTML,
            "annotator": document.getElementById('initials').value,
            "comments": document.getElementById('comments').value,
            "alignments": buildAnnotationMap(),
            "errors": window.error_map
        }
        document.getElementById("annotation").value = JSON.stringify(result)
        alert("Good to go! Please review then submit")
    }

}