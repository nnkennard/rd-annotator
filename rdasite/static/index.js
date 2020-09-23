switchTab(-1, 1, 1); // Display the first tab
document.getElementById("submitBtn").disabled = "true";
window.annotation_map = {}
window.error_map = {
    "review_errors": Array(),
    "rebuttal_errors": Array()
}

function hello(review_length, rebuttal_length) {
    for (const rebuttal_idx of Array(rebuttal_length).keys()) {
        window.annotation_map[rebuttal_idx] = {}
        for (const review_idx of Array(review_length).keys()) {
            window.annotation_map[rebuttal_idx][review_idx] = null;
        }
    }
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

function handleClick(rebuttal_idx, review_idx, value) {
    chunk_id = rebuttal_idx + "-" + review_idx;
    relevant_row = document.getElementById("reviewrow_" + chunk_id)

    if (value == 1) {
        relevant_row.className = "table-success";
        window.annotation_map[rebuttal_idx][review_idx] = true;

    } else {
        relevant_row.className = "table-secondary";
        window.annotation_map[rebuttal_idx][review_idx] = false;

    }
    document.getElementById("submitBtn").disabled = "true";
}

function updateError(rebuttal_chunk, rebuttal_or_review, add_or_remove) {
    console.log(rebuttal_or_review)
    if (rebuttal_or_review == "0") {
            console.log("Adding", rebuttal_chunk, "to rebuttal errors")
        relevant_map = window.error_map["rebuttal_errors"]
    } else {
            console.log("Adding", rebuttal_chunk, "to review errors")
        relevant_map = window.error_map["review_errors"]
    }

    if (add_or_remove == "0") {
        relevant_map.push(rebuttal_chunk)
    } else {
        new_map = relevant_map.filter(function(x) {
            return x !== rebuttal_chunk;
        });
        if (rebuttal_or_review == "0") {
            console.log("Deleting", rebuttal_chunk, "from rebuttal errors")
            window.error_map["rebuttal_errors"] = new_map
        } else {
            console.log("Deleting", rebuttal_chunk, "from review errors")
            window.error_map["review_errors"] = new_map

        }
    }
    document.getElementById("submitBtn").disabled = "true";
}

function cleanAnnotations(){
  
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
            "alignments": window.annotation_map,
            "errors": window.error_map
        }
        console.log(result)
        document.getElementById("annotation").value = JSON.stringify(result)
        alert("Good to go! Please review then submit")
    }

}

function doSubmit() {
    alert("Submitted");
}