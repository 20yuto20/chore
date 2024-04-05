ggplot(data = data_condo, aes(x = num_floor)) + 
  geom_histogram(colour = "black", fill = "dodgerblue4") +
  ggtitle("階数と物件数") +
  labs(x = "階数", y = "count") +
  geom_vline(xintercept = quantile(data_condo$num_floor, 0.95), color = "red", linetype = "dashed", 
             aes(label = as.character(quantile(data_condo$num_floor, 0.95)))) +
  theme_bw(base_family = "HiraKakuProN-W3")

# 必要なライブラリを読み込む
library(dplyr)
library(ggplot2)

# num_floorの値を1~2、3~4、5~6、7~8、9~10、11~12、13~14と二つ区切りで分ける
data_condo <- data_condo %>%
  mutate(floor_group = cut(num_floor, breaks = seq(1, 15, by = 2), labels = c("1-2", "3-4", "5-6", "7-8", "9-10", "11-12", "13-14")))

# 各区間ごとにprice_wo_commaの平均値とデータ数を計算
summary_data <- data_condo %>%
  group_by(floor_group) %>%
  summarize(mean_price = mean(price_wo_comma, na.rm = TRUE), data_count = n())

# 散布図を作成
ggplot(data = summary_data, aes(x = data_count, y = mean_price)) +
  geom_point(aes(size = data_count), color = "blue", alpha = 0.7) +
  geom_text(aes(label = floor_group), vjust = -0.5, hjust = 1, size = 3) +
  labs(title = "階数ごとの価格平均とデータ数", x = "データ数", y = "price_wo_commaの平均価格") +
  theme_bw(base_family = "HiraKakuProN-W3") +
  geom_hline(yintercept = 3065, color = "red") +
  geom_text(aes(label = "namamugi"), x = 500, y = 3065, color = "red", hjust = 0) +
  
  geom_hline(yintercept = 2994, color = "blue") +
  geom_text(aes(label = "miyamaedaira"), x = 500, y = 2994, color = "blue", hjust = 0) +
  
  geom_hline(yintercept = 3585, color = "green") +
  geom_text(aes(label = "odasakae"), x = 500, y = 3585, color = "green", hjust = 0) 
