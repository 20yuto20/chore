function paintingRows() {
    var scriptProperties = PropertiesService.getScriptProperties();
    var lastProcessedRow = scriptProperties.getProperty('lastProcessedRow');
    var startRow = lastProcessedRow ? parseInt(lastProcessedRow, 10) : 2;
  
    var sheetId = '';
    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName('2024年度卒');
  
    var lastRow = sheet.getLastRow();
    var range = sheet.getRange(2, 1, lastRow - 1, 1);
    var values = range.getValues();
  
    var lightGreen_1 = '#c0f9d2';  
    var lightGreen_2 = '#d6fada';   
  
    var currentColor = lightGreen_1;
  
    for (var i = startRow; i <= lastRow; i++) {
      var currentCell = values[i - 2][0];
      var nextCell = (i < lastRow) ? values[i - 1][0] : null;
  
      if (currentCell !== '' && currentCell !== nextCell) {
        var endRow = (i < lastRow) ? i : lastRow;
        if (endRow > startRow) {
          sheet.getRange(startRow, 1, endRow - startRow + 1, sheet.getLastColumn()).setBackground(currentColor);
        }
        currentColor = (currentColor === lightGreen_1) ? lightGreen_2 : lightGreen_1;
        startRow = i;
      }
    }
  
    // スクリプトプロパティをループ内で更新
    scriptProperties.setProperty('lastProcessedRow', i.toString());
  
    // ログにスクリプトプロパティの値を出力
    Logger.log('lastProcessedRowの値: ' + scriptProperties.getProperty('lastProcessedRow'));
  }
  