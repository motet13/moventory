// Output html depending on their package type & quantity
let level = function(qty, min_qty, max_qty) {
    let highLevel = `<i class="bi bi-emoji-smile-fill text-success fs-4"></i>`;
    let mediumLevel = `<i class="bi bi-emoji-neutral-fill text-warning fs-4"></i>`;
    let lowLevel = `<i class="bi bi-emoji-frown-fill text-danger fs-4"></i>`;
    let emptyLevel = `<i class="bi bi-emoji-dizzy text-muted fs-4"></i>`;
    
    if (qty == 0) {
      return emptyLevel
    } else if (qty <= min_qty) {
      return lowLevel
    } else if (qty < max_qty) {
      return mediumLevel
    } else {
      return highLevel;
    }
}