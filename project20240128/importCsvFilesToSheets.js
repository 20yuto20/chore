function importCsvFilesToSheets() {
    var folderId = ''; // Google Drive上のフォルダID
    var folder = DriveApp.getFolderById(folderId);
    var files = folder.getFilesByType(MimeType.CSV);
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    
    while (files.hasNext()) {
      var file = files.next();
      var fileName = file.getName();
      var csvData = Utilities.parseCsv(file.getBlob().getDataAsString());
      var sheetName = fileName.replace('.csv', '');
      
      var sheet = spreadsheet.getSheetByName(sheetName);
      if (sheet != null) {
        // 既に同じ名前のシートが存在する場合は、そのシートを削除
        spreadsheet.deleteSheet(sheet);
      }
      // 新しいシートを作成
      sheet = spreadsheet.insertSheet(sheetName);
      
      // CSVデータをシートにセット
      sheet.getRange(1, 1, csvData.length, csvData[0].length).setValues(csvData);
    }
  }
  