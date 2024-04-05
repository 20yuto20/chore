function addHashesToSheets() {
    var ssId = '';
    var ss = SpreadsheetApp.openById(ssId);
    var sheets = ss.getSheets();
  
    for (var i = 0; i < sheets.length; i++) {
      var sheet = sheets[i];
      var sheetName = sheet.getName();
  
      // '年度卒'で終わるワークシートの条件
      if (sheetName.endsWith('年度卒')) {
        var lastRow = sheet.getLastRow();
        var nextBlankRow = lastRow + 1;
  
        // 最終行の次の空白の行に'####'を記載
        sheet.getRange(nextBlankRow, 1, 1, sheet.getLastColumn()).setValue('####');
      }
    }
  }
  