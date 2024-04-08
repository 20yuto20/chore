function deleteScriptProperty() {
    var scriptProperties = PropertiesService.getScriptProperties();
    scriptProperties.deleteProperty('lastProcessedRow');
  }