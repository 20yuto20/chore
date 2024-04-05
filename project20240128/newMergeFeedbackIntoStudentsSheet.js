function newMergeFeedbackIntoStudentsSheet() {
    var scriptProperties = PropertiesService.getScriptProperties();
    var lastProcessedRow = scriptProperties.getProperty('lastProcessedRow');
    var startRow = lastProcessedRow ? parseInt(lastProcessedRow, 10) : 2;
  
    var ss = SpreadsheetApp.openById('');
    var mergedSheet = ss.getSheetByName('2023年度卒');
    var lastRowMerged = mergedSheet.getLastRow();
    var lastColumnMerged = mergedSheet.getLastColumn();
    var headerRowMerged = mergedSheet.getRange(1, 1, 1, lastColumnMerged).getValues()[0];
  
    var columns = [

    ];
  
    var columnIndexes = {};
    columns.forEach(function(columnName) {
      var columnIndex = headerRowMerged.indexOf(columnName) + 1;
      if (columnIndex > 0) {
        columnIndexes[columnName] = columnIndex;
      }
    });
  
    var jobTitleIndex = headerRowMerged.indexOf("企業名") + 1;
  
    for (var i = startRow; i <= lastRowMerged;) {
      var studentSurname = mergedSheet.getRange(i, headerRowMerged.indexOf("姓") + 1).getValue();
      var studentName = mergedSheet.getRange(i, headerRowMerged.indexOf("名") + 1).getValue();
      var studentJobTitle = mergedSheet.getRange(i, jobTitleIndex).getValue();
      var fullName = studentSurname + studentName;
  
      var feedbackSheetName = fullName + '_feedback';
      var feedbackSheet = ss.getSheetByName(feedbackSheetName);
  
      if (feedbackSheet) {
        var feedbackHeaderRow = feedbackSheet.getRange(1, 1, 1, feedbackSheet.getLastColumn()).getValues()[0];
        var jobTitleIndexFeedback = feedbackHeaderRow.indexOf("企業名") + 1; 
  
        var feedbackJobTitle = feedbackSheet.getRange(2, jobTitleIndexFeedback).getValue(); 
  
        if (studentJobTitle.includes(feedbackJobTitle)) {
          var feedbackLastRow = feedbackSheet.getLastRow();
          var feedbackData = feedbackSheet.getRange(2, 1, feedbackLastRow - 1, columns.length).getValues();
  
          for (var j = 0; j < feedbackData.length; j++) {
            if (j > 0) {
              mergedSheet.insertRowAfter(i + j - 1);
              lastRowMerged++;
            }
  
            feedbackData[j].forEach(function(value, index) {
              var columnName = columns[index];
              var columnIndexMerged = columnIndexes[columnName];
              if (columnIndexMerged) {
                mergedSheet.getRange(i + j, columnIndexMerged).setValue(value);
              }
            });
          }
  
          // feedbackData.length分だけ挿入されたので、もとの行はクリアしない
          // mergedSheet.getRange(i, 1, feedbackData.length, mergedSheet.getLastColumn()).clearContent();
  
          i += feedbackData.length;
        } else {
          Logger.log(fullName + " を削除しました");
          // i行目のデータをクリア
          mergedSheet.getRange(i, 1, 1, mergedSheet.getLastColumn()).clearContent();
          i++;
        }
      } else {
        Logger.log("Feedback sheet not found for: " + fullName);
        i++;
      }
  
      // スクリプトプロパティをループ内で更新
      scriptProperties.setProperty('lastProcessedRow', i.toString());
  
      // ログにスクリプトプロパティの値を出力
      Logger.log('lastProcessedRowの値: ' + scriptProperties.getProperty('lastProcessedRow'));
    }
  }
  