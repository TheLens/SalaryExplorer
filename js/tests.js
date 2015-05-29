describe('DOM tests - Signup form', function() {
  var formElem = document.forms[0];
  var input_box = document.getElementById('input_box');
 
  it('input_box exists in the DOM', function() {
    expect(input_box).to.not.equal(null);
  });

});