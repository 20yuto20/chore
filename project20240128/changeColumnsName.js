function changeColumnsName() {
    var ss = SpreadsheetApp.openById('');
    var sheets = ss.getSheets();
  
    var headers = [
      
    ];
  
    for (var i = 0; i < sheets.length; i++) {
      var sheet = sheets[i];
      var sheetName = sheet.getName();
  
      // ワークシート名が '_feedback' で終わる場合のみ処理を実行
      if (sheetName.endsWith('_feedback')) {
        var headerRow = sheet.getRange(1, 1, 1, headers.length);
        headerRow.setValues([headers]);
      }
    }
  }
  