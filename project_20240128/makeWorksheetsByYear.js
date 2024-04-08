function makeWorksheetsByYear() {
    var ssId = "";
    var ssName = "";
    
    var spreadSheet = SpreadsheetApp.openById(ssId);
    var sheet = spreadSheet.getSheetByName(ssName); // sheetは学生の合格者情報
  
    var lastRow = sheet.getLastRow();
    var lastColumn = sheet.getLastColumn();
  
    // ヘッダー行を取得
    var headerRow = sheet.getRange(1, 1, 1, lastColumn).getValues()[0];
  
    // '卒業予定' カラムのインデックスを取得
    var graduationIndex = headerRow.indexOf('卒業予定') + 1;
  
    // ワークシートを年度ごとに作成
    for (var i = 2; i <= lastRow; i++) { // データが2行目から始まると仮定
      var graduationDate = sheet.getRange(i, graduationIndex).getValue();
      
      if (graduationDate instanceof Date) {
        var year = graduationDate.getFullYear();
        var formattedYear = year + '年度卒';
        
        // ワークシートが存在しなければ新規作成
        var yearSheet = spreadSheet.getSheetByName(formattedYear);
        if (!yearSheet) {
          yearSheet = spreadSheet.insertSheet(formattedYear);
          yearSheet.appendRow(headerRow); // ヘッダー行を追加
        }
  
        // データをコピー
        yearSheet.appendRow(sheet.getRange(i, 1, 1, lastColumn).getValues()[0]);
      }
    }
  }
  