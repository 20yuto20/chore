-- テーブル1: 取引先
CREATE TABLE `取引先` (
  `取引先ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '取引先ID',
  `取引先名` VARCHAR(100) NOT NULL COMMENT '取引先名',
  PRIMARY KEY (`取引先ID`)
) COMMENT='取引先情報を格納するテーブル';

-- テーブル2: 銀行
CREATE TABLE `銀行` (
  `銀行ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '銀行ID',
  `銀行名` VARCHAR(50) NOT NULL COMMENT '銀行名', 
  `支店名` VARCHAR(50) COMMENT '支店名',
  `口座番号` VARCHAR(20) COMMENT '口座番号',
  PRIMARY KEY (`銀行ID`)
) COMMENT='銀行情報を格納するテーブル';

-- テーブル3: 支払い方法 
CREATE TABLE `支払い方法` (
  `支払い方法ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '支払い方法ID',
  `名前` VARCHAR(50) NOT NULL COMMENT '支払い方法名',
  `カテゴリ` VARCHAR(50) COMMENT '支払い方法カテゴリ',
  `銀行ID` INT UNSIGNED COMMENT '銀行ID',
  PRIMARY KEY (`支払い方法ID`),
  FOREIGN KEY (`銀行ID`) REFERENCES `銀行`(`銀行ID`)
) COMMENT='支払い方法の情報を格納するテーブル';

-- テーブル4: 支払い
CREATE TABLE `支払い` (
  `支払いID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '支払いID',
  `取引先ID` INT UNSIGNED NOT NULL COMMENT '取引先ID',
  `支払い方法ID` INT UNSIGNED NOT NULL COMMENT '支払い方法ID',
  `支払い金額` DECIMAL(15,2) NOT NULL COMMENT '支払い金額',
  `支払い期限` DATE NOT NULL COMMENT '支払い期限',
  `振込先口座番号ID` INT UNSIGNED COMMENT '振込先口座番号ID',
  PRIMARY KEY (`支払いID`),
  FOREIGN KEY (`取引先ID`) REFERENCES `取引先`(`取引先ID`),
  FOREIGN KEY (`支払い方法ID`) REFERENCES `支払い方法`(`支払い方法ID`),
  FOREIGN KEY (`振込先口座番号ID`) REFERENCES `銀行`(`銀行ID`)
) COMMENT='支払い情報を格納するテーブル';

-- テーブル5: 仕訳
CREATE TABLE `仕訳` (
  `仕訳ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '仕訳ID',
  `支払いID` INT UNSIGNED NOT NULL COMMENT '支払いID',
  `仕訳メモ` VARCHAR(200) COMMENT '仕訳メモ',
  `計上日` DATE NOT NULL COMMENT '計上日',
  `摘要` VARCHAR(200) COMMENT '摘要',
  PRIMARY KEY (`仕訳ID`),
  FOREIGN KEY (`支払いID`) REFERENCES `支払い`(`支払いID`)
) COMMENT='仕訳情報を格納するテーブル';

-- テーブル6: 勘定科目
CREATE TABLE `勘定科目` (
  `勘定科目ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '勘定科目ID',
  `勘定科目名` VARCHAR(100) NOT NULL COMMENT '勘定科目名',
  PRIMARY KEY (`勘定科目ID`)
) COMMENT='勘定科目情報を格納するテーブル';

-- テーブル7: 補助科目
CREATE TABLE `補助科目` (
  `補助科目ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '補助科目ID',
  `補助科目名` VARCHAR(100) NOT NULL COMMENT '補助科目名',
  PRIMARY KEY (`補助科目ID`)
) COMMENT='補助科目情報を格納するテーブル';

-- テーブル8: 部門
CREATE TABLE `部門` (
  `部門ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '部門ID',
  `部門名` VARCHAR(100) NOT NULL COMMENT '部門名',
  PRIMARY KEY (`部門ID`)
) COMMENT='部門情報を格納するテーブル';

-- テーブル9: 税区分
CREATE TABLE `税区分` (
  `税区分ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '税区分ID',
  `税区分名` VARCHAR(50) NOT NULL COMMENT '税区分名',
  PRIMARY KEY (`税区分ID`)
) COMMENT='税区分情報を格納するテーブル';

-- テーブル10: 仕訳明細借方
CREATE TABLE `仕訳明細借方` (
  `明細ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '明細ID',
  `仕訳ID` INT UNSIGNED NOT NULL COMMENT '仕訳ID',
  `勘定科目ID` INT UNSIGNED NOT NULL COMMENT '勘定科目ID',
  `金額` DECIMAL(15,2) NOT NULL COMMENT '金額',
  `補助科目ID` INT UNSIGNED COMMENT '補助科目ID',
  `部門ID` INT UNSIGNED COMMENT '部門ID',
  `税区分ID` INT UNSIGNED COMMENT '税区分ID',
  PRIMARY KEY (`明細ID`),
  FOREIGN KEY (`仕訳ID`) REFERENCES `仕訳`(`仕訳ID`),
  FOREIGN KEY (`勘定科目ID`) REFERENCES `勘定科目`(`勘定科目ID`),
  FOREIGN KEY (`補助科目ID`) REFERENCES `補助科目`(`補助科目ID`),
  FOREIGN KEY (`部門ID`) REFERENCES `部門`(`部門ID`),
  FOREIGN KEY (`税区分ID`) REFERENCES `税区分`(`税区分ID`)
) COMMENT='仕訳の借方明細を格納するテーブル';

-- テーブル11: 仕訳明細貸方
CREATE TABLE `仕訳明細貸方` (
  `明細ID` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '明細ID',
  `仕訳ID` INT UNSIGNED NOT NULL COMMENT '仕訳ID',
  `勘定科目ID` INT UNSIGNED NOT NULL COMMENT '勘定科目ID',
  `金額` DECIMAL(15,2) NOT NULL COMMENT '金額',
  `補助科目ID` INT UNSIGNED COMMENT '補助科目ID',
  `部門ID` INT UNSIGNED COMMENT '部門ID',
  `税区分ID` INT UNSIGNED COMMENT '税区分ID',
  PRIMARY KEY (`明細ID`),
  FOREIGN KEY (`仕訳ID`) REFERENCES `仕訳`(`仕訳ID`),
  FOREIGN KEY (`勘定科目ID`) REFERENCES `勘定科目`(`勘定科目ID`),
  FOREIGN KEY (`補助科目ID`) REFERENCES `補助科目`(`補助科目ID`),
  FOREIGN KEY (`部門ID`) REFERENCES `部門`(`部門ID`),
  FOREIGN KEY (`税区分ID`) REFERENCES `税区分`(`税区分ID`)
) COMMENT='仕訳の貸方明細を格納するテーブル';