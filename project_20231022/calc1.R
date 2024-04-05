ggplot(data = data_condo, aes(x = housing_age)) + 
  geom_histogram(colour = "black", fill = "dodgerblue4") +
  ggtitle("築年数と物件数") +
  labs(x = "築年数", y = "count") +
  geom_vline(xintercept = quantile(data_condo$housing_age, 0.95), color = "red", linetype = "dashed") +
  theme_bw(base_family = "HiraKakuProN-W3")

# ライブラリを読み込む
library(dplyr)
library(ggplot2)

# housing_ageの範囲を設定
age_ranges <- seq(1, 50, by = 5)

# 各範囲でのprice_wo_commaの平均値を計算
summary_data <- data_condo %>%
  mutate(age_range = cut(housing_age, breaks = age_ranges)) %>%
  group_by(age_range) %>%
  summarise(
    avg_price = mean(price_wo_comma),
    data_count = n()
  )

# 散布図を作成
ggplot(summary_data, aes(x = data_count, y = avg_price)) +
  geom_point() +
  geom_text(aes(label = age_range), vjust = -0.5, hjust = -0.5) +
  labs(
    x = "物件数",
    y = "価格の平均値",
    title = "築年数別の価格の平均値とデータ量"
  ) +
  theme_minimal() +
  theme_bw(base_family = "HiraKakuProN-W3") +
  # 平均価格を示す線を追加
  geom_hline(yintercept = 3065, color = "red") +
  geom_text(aes(label = "namamugi"), x = 500, y = 3065, color = "red", hjust = 0) +
  
  geom_hline(yintercept = 2994, color = "blue") +
  geom_text(aes(label = "miyamaedaira"), x = 500, y = 2994, color = "blue", hjust = 0) +
  
  geom_hline(yintercept = 3585, color = "green") +
  geom_text(aes(label = "odasakae"), x = 500, y = 3585, color = "green", hjust = 0) 
 
