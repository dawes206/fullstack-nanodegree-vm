restaurant = $(".restaurant")
restaurantParent = restaurant.parent()
restaurant.hover(function(event) {
  console.log(event.target)
  changeRest = $(event.target)
  changeRest.attr('style','background-color:76DFFF')},
function(event) {
  changeRest.attr('style', 'background-color:none')})
