var v = $('#card1 option:contains("' + cardName + '")').val();

$('#card1').select2('val', v);
$('#card1').trigger('select2-close');
$('#card1').trigger('change');