function mergeColumns() {
    var sheetId = '';
    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName('2029年度卒');
  
    var lastRow = sheet.getLastRow();
    var range = sheet.getRange(2, 1, lastRow - 1, 1);
    var values = range.getValues();
  
    var columnsToMerge = [
    ];
  
    var startRow = 2;
  
    // ヘッダー行がある場合、ヘッダー行を取得
    var headerValues = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    
    for (var i = 2; i <= lastRow; i++) {
      var currentCell = values[i - 2][0];
      var nextCell = (i < lastRow) ? values[i - 1][0] : null;
  
      if (currentCell !== '' && currentCell !== nextCell) {
        var endRow = (i < lastRow) ? i - 1 : lastRow - 1;
  
        // カラムごとに結合
        columnsToMerge.forEach(function(column) {
          var columnIndex = headerValues.indexOf(column) + 1;
          if (columnIndex > 0) {
            var numRows = endRow - startRow + 1;
            if (numRows > 0) {
              sheet.getRange(startRow, columnIndex, numRows, 1).merge();
            }
          }
        });
  
        startRow = i;
      }
    }
  }
  