function addColumnsToSheet() {

    var spreadSheetId ='';
    var sheetName = '';
  
    var spreadSheet = SpreadsheetApp.openById(spreadSheetId);
    var sheet = spreadSheet.getSheetByName(sheetName);
  
    var columns = [

    ];
  
    // 現在のワークシートの最終列を取得
    var lastColumn = sheet.getLastColumn();
  
    for (var i = 0; i < columns.length; i++) {
      var columnPosition = lastColumn + i +1;
      sheet.getRange(1, columnPosition).setValue(columns[i]);
    }
    
  }
  