# ライブラリを読み込む
library(ggplot2)

# 回帰モデルの残差を計算
residuals_yokohama <- resid(reg_yokohama)

#横浜市
# 残差プロットを作成
residual_plot_yokohama <- ggplot(data = data.frame(Residuals = residuals_yokohama), aes(x = seq_along(Residuals), y = Residuals)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE, color = "blue") +
  labs(x = "観測値", y = "残差") +
  ggtitle("残差プロット（横浜市）") +
  theme_bw(base_family = "HiraKakuProN-W3")

# 残差プロットを表示
print(residual_plot_yokohama)

# Q-Qプロットを作成
qq_plot_yokohama <- ggplot(data = data.frame(Standardized_Residuals = rstandard(reg_yokohama)), 
                  aes(sample = Standardized_Residuals)) +
  geom_qq() +
  geom_qq_line() +
  labs(title = "Q-Qプロット（横浜市）") +
  theme_bw(base_family = "HiraKakuProN-W3")

# Q-Qプロットを表示
print(qq_plot_yokohama)


#川崎市
# 残差プロットを作成
residuals_kawasaki <- resid(reg_kawasaki)
residual_plot_kawasaki <- ggplot(data = data.frame(Residuals = residuals_yokohama), aes(x = seq_along(Residuals), y = Residuals)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE, color = "blue") +
  labs(x = "観測値", y = "残差") +
  ggtitle("残差プロット（川崎市）") +
  theme_bw(base_family = "HiraKakuProN-W3")

# 残差プロットを表示
print(residual_plot_kawasaki)

# Q-Qプロットを作成
qq_plot_kawasaki <- ggplot(data = data.frame(Standardized_Residuals = rstandard(reg_kawasaki)), 
                           aes(sample = Standardized_Residuals)) +
  geom_qq() +
  geom_qq_line() +
  labs(title = "Q-Qプロット（川崎市）") +
  theme_bw(base_family = "HiraKakuProN-W3")

# Q-Qプロットを表示
print(qq_plot_kawasaki)


#その他の市
# 残差プロットを作成
residuals_other <- resid(reg_other_new)
residual_plot_other <- ggplot(data = data.frame(Residuals = residuals_other), aes(x = seq_along(Residuals), y = Residuals)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE, color = "blue") +
  labs(x = "観測値", y = "残差") +
  ggtitle("残差プロット（その他の市）") +
  theme_bw(base_family = "HiraKakuProN-W3")

# 残差プロットを表示
print(residual_plot_other)

# Q-Qプロットを作成
# Q-Qプロットを作成
qq_plot_other <- ggplot(data = data.frame(Standardized_Residuals = rstandard(reg_other_new)), 
                           aes(sample = Standardized_Residuals)) +
  geom_qq() +
  geom_qq_line() +
  labs(title = "Q-Qプロット（その他の市）") +
  theme_bw(base_family = "HiraKakuProN-W3")

# Q-Qプロットを表示
print(qq_plot_other)

