$(".test").on('hover', function(){
  console.log('hover working')
  test = $(".test")
  test.attr('style', 'color:red')
});
//
//
$(function(){
  console.log('function running')
  test2 = $(".test")
  test2.attr('style', 'color:green')
  // test2.bind('hover', function(){
  //   console.log(test2.attr('style'))
  //   if (test2.attr('style') == 'color:red'){
  //     test2.attr('style','color:green')
  //   } else {
  //     test2.attr('style','color:red')
  //   }
  // })
  test2.hover(function(){
    test2.attr('style','color:red')
  }, function(){
    test2.attr('style','color:blue')
  })
})

// console.log('Javascript is working externally')
//
// val = $("h1")
// console.log('Jquery is working')
// console.log('jquery object: ', val)
// console.log('objects style attribute: ', val.attr('style'))
// val.attr('style','color:red')
