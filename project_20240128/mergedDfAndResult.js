function mergedDfAndResult() {
    var ssId = "";
    var ssName_1 = "revised_merged_only_accepted_students_df";
    var ssName_2 = "result";
  
    var spreadSheet = SpreadsheetApp.openById(ssId);
    var sheet_1 = spreadSheet.getSheetByName(ssName_1); // sheet_1は学生の合格者情報
    var sheet_2 = spreadSheet.getSheetByName(ssName_2); // sheet_2はスクレイピングの結果のデータ
  
    var lastRow_1 = sheet_1.getLastRow();
    var lastRow_2 = sheet_2.getLastRow();
    
    for (var i = 2; i <= lastRow_1; i++) { // 行のデータが2行目から始まると仮定
      var companyName = sheet_1.getRange(i, 15).getValue();
      
      // sheet_2のnameカラムと企業名が一致するか検索
      var nameMatchedRow = null;
      for (var j = 2; j <= lastRow_2; j++) { // 行のデータが2行目から始まると仮定
        var name = sheet_2.getRange(j, 1).getValue();
        if (name === companyName) {
          nameMatchedRow = j;
          break;
        }
      }
      
      if (nameMatchedRow !== null) {
        // 企業名が一致する場合
        var category1 = sheet_2.getRange(nameMatchedRow, 7).getValue();
        var category2 = sheet_2.getRange(nameMatchedRow, 8).getValue();
        
        // 該当の行に情報をコピー
        sheet_1.getRange(i, 27).setValue(category1);
        sheet_1.getRange(i, 28).setValue(category2);
      } else {
        // 企業名が一致しない場合
        sheet_1.getRange(i, 27).setValue("N/A");
        sheet_1.getRange(i, 28).setValue("N/A");
        
        // コンソールに出力
        Logger.log("企業名が一致しない行：" + i + " - 企業名：" + companyName);
      }
    }
  }
  