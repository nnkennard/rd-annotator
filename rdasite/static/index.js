switchTab(-1, 1, 1); // Display the first tab
document.getElementById("submitBtn").disabled="true";
window.annotation_map = {}

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
    document.getElementById("submitBtn").disabled="true";
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
}

function generateJson(review_length, rebuttal_length) {
    console.log("Trying to finalize")
    missing_annotations = Array();
    for (const rebuttal_idx of Array(rebuttal_length).keys()) {
        for (const review_idx of Array(review_length).keys()) {
            if (window.annotation_map[rebuttal_idx][review_idx] == null) {
              console.log(rebuttal_idx)
                missing_annotations.push(Array(rebuttal_idx, review_idx))
            }
        }
    }
    if (missing_annotations.length == 0){
      submitButton = document.getElementById("submitBtn");
      submitButton.removeAttribute("disabled");
      document.getElementById("jsonBox").innerHTML = JSON.stringify(window.annotation_map)
      alert("Good to go! Please review then submit")
    } else {
      console.log("Missing some judgments")
      alert_string = "Missing judgments for:"
      for(const indices of missing_annotations){
        alert_string += "\nRebuttal chunk " + indices[0] + " and review chunk " + indices[1]
      }
      alert(alert_string)
    }

}

function doSubmit(){
  alert("Submitted");
}