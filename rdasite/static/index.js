switchTab(-1, 1, 1); // Display the first tab

function switchTab(current_tab, total_tabs, direction) {
  new_tab = (current_tab + direction + total_tabs) % total_tabs;
  var tabs = document.getElementsByClassName("tab");
  if(current_tab > -1) {
    tabs.item(current_tab).style.display = "none";
  }
  tabs.item(new_tab).style.display = "block";
  //currentTab = newTab;
}

function handleClick(rebuttal_idx, review_idx, value){
  chunk_id = rebuttal_idx + "-" + review_idx;
  console.log(chunk_id)
  relevant_row = document.getElementById("reviewrow_" + chunk_id)

  if(value == 1){
    relevant_row.className="table-success";
  } else {
    relevant_row.className="table-secondary";
  }
}
